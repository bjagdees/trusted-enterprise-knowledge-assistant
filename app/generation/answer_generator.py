import os
import requests
from openai import OpenAI
from dotenv import load_dotenv

from app.trust.trust_controls import build_trust_header

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

openai_client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None


def format_sources_for_prompt(retrieved_chunks):
    """
    Formats retrieved content into numbered source blocks.

    Supports BOTH:
    1. Old format: list[str]
    2. New format: list[{"text": ..., "metadata": {...}}]

    WHY THIS EXISTS:
    - creates clear evidence boundaries for the model
    - enables source-aware grounded answering
    - prepares the system for citation-friendly behavior
    """
    if not retrieved_chunks:
        return "No supporting sources were retrieved."

    formatted_blocks = []

    for idx, item in enumerate(retrieved_chunks, start=1):
        # Backward-compatible support for old list[str] format
        if isinstance(item, str):
            document_name = "unknown_document"
            chunk_id = f"chunk_{idx}"
            content = item.strip()

        # Future-ready support for structured retrieval format
        elif isinstance(item, dict):
            metadata = item.get("metadata", {}) or {}
            document_name = metadata.get("source", "unknown_document")
            chunk_id = metadata.get("chunk_id", f"chunk_{idx}")
            content = item.get("text", "").strip()

        else:
            document_name = "unknown_document"
            chunk_id = f"chunk_{idx}"
            content = str(item).strip()

        block = f"""
[Source {idx}]
Document: {document_name}
Chunk ID: {chunk_id}
Content:
{content}
""".strip()

        formatted_blocks.append(block)

    return "\n\n".join(formatted_blocks)


def build_prompt(query, retrieved_chunks):
    """
    Builds a grounded enterprise-safe prompt.

    DESIGN GOAL:
    Make the model answer only from retrieved enterprise evidence,
    not from general world knowledge.
    """
    sources_block = format_sources_for_prompt(retrieved_chunks)

    return f"""
You are a Trusted Enterprise Knowledge Assistant.

You answer enterprise questions using ONLY the retrieved enterprise knowledge sources below.

NON-NEGOTIABLE RULES:
- Use ONLY the provided sources.
- Do NOT invent policies, architecture decisions, controls, standards, or procedures.
- Do NOT use outside knowledge unless it is explicitly present in the retrieved sources.
- If the answer is not clearly supported, say:
  "I could not find sufficient information in the knowledge base."
- If evidence is partial, clearly state what is supported and what is unclear.
- Cite supporting evidence using [Source X].
- Be concise, factual, conservative, and trustworthy.

USER QUESTION:
{query}

RETRIEVED ENTERPRISE SOURCES:
{sources_block}

RESPONSE FORMAT:
Answer:
<grounded answer>

Citations:
- [Source X] <what it supports>
- [Source Y] <what it supports>

Confidence:
<High / Medium / Low>

Evidence Gaps:
<what is missing, unclear, or unsupported>
"""


def generate_answer_openai(prompt):
    if not openai_client:
        raise ValueError("OPENAI_API_KEY is not configured.")

    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    return response.choices[0].message.content


def generate_answer_ollama(prompt):
    response = requests.post(
        f"{OLLAMA_BASE_URL}/api/generate",
        json={
            "model": "phi3:mini",
            "prompt": prompt,
            "stream": False
        },
        timeout=120
    )

    response.raise_for_status()
    data = response.json()

    return data["response"]


def generate_answer(query, retrieved_chunks):
    """
    Main generation orchestration wrapper.

    FLOW:
    1. Build grounded prompt
    2. Try OpenAI
    3. Fall back to Ollama
    4. Attach trust summary
    """
    prompt = build_prompt(query, retrieved_chunks)
    trust_header = build_trust_header(retrieved_chunks)

    try:
        print("[Generation] Trying OpenAI first...")
        answer = generate_answer_openai(prompt)
        provider = "OpenAI"

    except Exception as openai_error:
        print(f"[Generation] OpenAI failed: {openai_error}")
        print("[Generation] Falling back to Ollama...")

        try:
            answer = generate_answer_ollama(prompt)
            provider = "Ollama"

        except Exception as ollama_error:
            return (
                "[Generation Failed]\n"
                f"OpenAI error: {openai_error}\n"
                f"Ollama error: {ollama_error}"
            )

    final_answer = f"""[Provider: {provider}]

{trust_header}

{answer}
"""
    return final_answer