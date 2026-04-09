from app.ingestion.loader import load_documents
from app.ingestion.chunker import chunk_document
from app.retrieval.indexer import index_chunks
from app.retrieval.retriever import query_knowledge_base
from app.generation.answer_generator import generate_answer


def main():
    print("=== Trusted Enterprise Knowledge Assistant ===\n")

    # Phase 1: Load documents
    docs = load_documents("data/raw_docs")

    # Phase 1: Chunk documents with metadata
    all_chunks = []
    for doc in docs:
        chunks = chunk_document(doc["content"])

        for idx, chunk in enumerate(chunks):
            all_chunks.append({
                "chunk": chunk,
                "metadata": {
                    **doc["metadata"],
                    "chunk_id": f"{doc['metadata'].get('source', 'doc')}_chunk_{idx}"
                }
            })

    print(f"[Ingestion] Loaded {len(docs)} documents")
    print(f"[Chunking] Generated {len(all_chunks)} chunks")

    # Phase 2: Index chunks
    print("\n[Indexing] Indexing chunks...")
    index_chunks(all_chunks)

    # User query
    query = input("\nAsk a question: ").strip()
    print(f"\n[Query] {query}")

    # Phase 2: Retrieve relevant chunks
    retrieved_docs = query_knowledge_base(query)

    print("\n=== Retrieved Evidence ===\n")

    if not retrieved_docs:
        print("No relevant evidence retrieved.\n")
    else:
        for i, item in enumerate(retrieved_docs, start=1):
            text = item.get("text", "")
            metadata = item.get("metadata", {})

            print("-----")
            print(f"[Source {i}]")
            print(f"Document: {metadata.get('source', 'unknown_document')}")
            print(f"Chunk ID: {metadata.get('chunk_id', 'unknown_chunk')}")
            print(text)
            print()

    # Phase 3 + 4: Generate grounded answer
    print("\n[Generation] Generating grounded answer...\n")
    answer = generate_answer(query, retrieved_docs)

    print("=== Final Answer ===\n")
    print(answer)


if __name__ == "__main__":
    main()