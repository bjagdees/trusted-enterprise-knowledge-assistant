from app.ingestion.loader import load_documents
from app.ingestion.chunker import chunk_document
from app.retrieval.indexer import index_chunks
from app.retrieval.retriever import query_knowledge_base


def main():
    docs = load_documents("data/raw_docs")

    all_chunks = []
    for doc in docs:
        chunks = chunk_document(doc["content"])

        for idx, chunk in enumerate(chunks):
            all_chunks.append({
                "chunk": chunk,
                "metadata": {
                    **doc["metadata"],
                    "chunk_id": idx
                }
            })

    print(f"Loaded {len(docs)} documents")
    print(f"Generated {len(all_chunks)} chunks")

    # Index into vector DB
    print("\nIndexing chunks...")
    index_chunks(all_chunks)

    # Test query
    query = "What are the requirements for certified datasets?"
    print(f"\nQuery: {query}")

    results = query_knowledge_base(query)

    print("\nTop Results:\n")

    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        print("-----")
        print(meta)
        print(doc)
        print()


if __name__ == "__main__":
    main()