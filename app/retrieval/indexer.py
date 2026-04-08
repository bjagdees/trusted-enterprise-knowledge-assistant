from chromadb.utils import embedding_functions

from app.retrieval.vector_store import get_chroma_client


def index_chunks(chunks):
    client = get_chroma_client()

    embedding_function = embedding_functions.DefaultEmbeddingFunction()

    collection = client.get_or_create_collection(
        name="enterprise_knowledge",
        embedding_function=embedding_function
    )

    documents = []
    metadatas = []
    ids = []

    for i, chunk in enumerate(chunks):
        documents.append(chunk["chunk"])
        metadatas.append(chunk["metadata"])
        ids.append(f"chunk_{i}")

    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )

    return collection