from chromadb.utils import embedding_functions
from typing import List, Dict, Any

from app.retrieval.vector_store import get_chroma_client


def query_knowledge_base_raw(query, top_k=3):
    """
    Original raw query (kept for debugging / inspection).
    Returns direct ChromaDB response.
    """
    client = get_chroma_client()

    embedding_function = embedding_functions.DefaultEmbeddingFunction()

    collection = client.get_collection(
        name="enterprise_knowledge",
        embedding_function=embedding_function
    )

    results = collection.query(
        query_texts=[query],
        n_results=top_k
    )

    return results


def query_knowledge_base(query, top_k=3) -> List[Dict[str, Any]]:
    """
    Normalized retrieval function.

    WHY THIS EXISTS:
    - Converts Chroma output into a clean, consistent structure
    - Enables citation-aware prompting ([Source 1], etc.)
    - Decouples retrieval layer from generation layer

    OUTPUT FORMAT:
    [
        {
            "text": "...chunk text...",
            "metadata": {
                "source": "...",
                "chunk_id": "..."
            }
        }
    ]
    """
    raw_results = query_knowledge_base_raw(query, top_k)

    documents = raw_results.get("documents", [[]])[0]
    metadatas = raw_results.get("metadatas", [[]])[0]

    normalized_results = []

    for idx, (doc, metadata) in enumerate(zip(documents, metadatas), start=1):
        metadata = metadata or {}

        normalized_results.append({
            "text": doc,
            "metadata": {
                "source": metadata.get("source", "unknown_document"),
                "chunk_id": metadata.get("chunk_id", f"chunk_{idx}")
            }
        })

    return normalized_results