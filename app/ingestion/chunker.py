def chunk_document(text, chunk_size=60, overlap=20):
    words = text.split()
    chunks = []

    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk_words = words[start:end]
        chunk_text = " ".join(chunk_words)

        chunks.append(chunk_text)

        start += (chunk_size - overlap)

    return chunks