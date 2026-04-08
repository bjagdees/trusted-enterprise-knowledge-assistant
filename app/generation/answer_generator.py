import os
import requests
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

openai_client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None


def build_prompt(query, retrieved_chunks):
    context = "\n\n".join(retrieved_chunks)

    return f"""
You are an enterprise AI assistant.

Answer the question ONLY using the provided context.

If the answer is not found in the context, say:
"I could not find sufficient information in the knowledge base."

Be concise, factual, and grounded.

Context:
{context}

Question:
{query}

Answer:
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

    return "[Provider: OpenAI]\n" + response.choices[0].message.content


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

    return "[Provider: Ollama]\n" + data["response"]


def generate_answer(query, retrieved_chunks):
    prompt = build_prompt(query, retrieved_chunks)

    try:
        print("[Generation] Trying OpenAI first...")
        return generate_answer_openai(prompt)

    except Exception as openai_error:
        print(f"[Generation] OpenAI failed: {openai_error}")
        print("[Generation] Falling back to Ollama...")

        try:
            return generate_answer_ollama(prompt)

        except Exception as ollama_error:
            return (
                "[Generation Failed]\n"
                f"OpenAI error: {openai_error}\n"
                f"Ollama error: {ollama_error}"
            )