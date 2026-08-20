import chromadb

db_client = chromadb.PersistentClient(path="./vector_db")
collection = db_client.get_or_create_collection(name="pdf_knowledge_base")


def store_chunk(chunk_id, text: str, vector: list[float], page: int) -> None:
    collection.add(
        embeddings=[vector],
        documents=[text],
        ids=[f"id_{chunk_id}_pg_{page}"],
        metadatas=[{"page": page}]
    )


def query_similar(question_vector: list[float], n_results: int = 3) -> list[str]:
    results = collection.query(
        query_embeddings=[question_vector],
        n_results=n_results
    )
    return results["documents"][0]
