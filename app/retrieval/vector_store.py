from chromadb import Client
from chromadb.config import Settings


def get_chroma_client():
    client = Client(Settings(persist_directory="data/vector_store"))
    return client