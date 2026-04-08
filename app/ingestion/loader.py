import os


def load_documents(directory_path: str):
    documents = []

    for filename in os.listdir(directory_path):
        if filename.endswith(".md") or filename.endswith(".txt"):
            file_path = os.path.join(directory_path, filename)

            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

                documents.append({
                    "content": content,
                    "metadata": {
                        "source": filename,
                        "path": file_path
                    }
                })

    return documents