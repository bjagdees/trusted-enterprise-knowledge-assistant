from typing import List, Dict, Any


def format_retrieved_sources(results: List[Dict[str, Any]]) -> str:
    """
    Formats retrieved RAG chunks into structured, numbered sources.

    WHY THIS EXISTS:
    - Establishes a clear boundary between retrieved evidence and model generation
    - Enables citation-aware prompting ([Source 1], [Source 2], ...)
    - Improves grounding and reduces hallucination risk

    IMPORTANT:
    The model should treat each block as an independent, auditable evidence unit,
    not as arbitrary text context.
    """
    if not results:
        return "No supporting sources were retrieved."

    formatted_blocks = []

    for idx, item in enumerate(results, start=1):
        metadata = item.get("metadata", {}) or {}
        document_name = metadata.get("source", "unknown_document")
        chunk_id = metadata.get("chunk_id", f"chunk_{idx}")
        content = item.get("text", "").strip()

        block = f"""
[Source {idx}]
Document: {document_name}
Chunk ID: {chunk_id}
Content:
{content}
""".strip()

        formatted_blocks.append(block)

    return "\n\n".join(formatted_blocks)