import json

from app.ingestion.loader import load_documents
from app.ingestion.chunker import chunk_document


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
    print(f"Generated {len(all_chunks)} chunks\n")

    for c in all_chunks[:5]:
        print("-----")
        print(c["metadata"])
        print(c["chunk"])
        print()

    with open("data/processed_docs/chunks.json", "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2)

    print("Saved chunk output to data/processed_docs/chunks.json")


if __name__ == "__main__":
    main()