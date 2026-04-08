from app.ingestion.loader import load_documents
from app.ingestion.chunker import chunk_document
from app.retrieval.indexer import index_chunks
from app.retrieval.retriever import query_knowledge_base
from app.generation.answer_generator import generate_answer


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

    print("\nIndexing chunks...")
    index_chunks(all_chunks)

    query = "What are the requirements for certified datasets?"
    print(f"\nQuery: {query}")

    results = query_knowledge_base(query)

    retrieved_chunks = results["documents"][0]
    metadatas = results["metadatas"][0]

    print("\nRetrieved Context:\n")

    for doc, meta in zip(retrieved_chunks, metadatas):
        print("-----")
        print(meta)
        print(doc)
        print()

    print("\nGenerating Answer...\n")

    answer = generate_answer(query, retrieved_chunks)

    print("Final Answer:\n")
    print(answer)


if __name__ == "__main__":
    main()