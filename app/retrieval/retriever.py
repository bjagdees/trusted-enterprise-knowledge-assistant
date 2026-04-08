from chromadb.utils import embedding_functions

from app.retrieval.vector_store import get_chroma_client


def query_knowledge_base(query, top_k=3):
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