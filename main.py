from fastapi import FastAPI, UploadFile, File

from embedding import embed_text
from generation import generate_answer
from ingestion import chunk_pdf
from retrieval import query_similar, store_chunk

app = FastAPI()


@app.get("/")
def home():
    return {"mesaj": "Serverul functioneaza!"}


@app.post("/test-pdf")
async def test_pdf(file: UploadFile = File(...), length: int = 100, overlap: int = 10):
    content = await file.read()
    chunks = chunk_pdf(content, length, overlap)

    for chunk in chunks:
        if not chunk["text"].strip():
            continue  # sarim peste chunk-urile goale (Gemini respinge textul gol cu 400)
        vector = embed_text(chunk["text"])
        store_chunk(
            chunk_id=chunk["chunk_id"],
            text=chunk["text"],
            vector=vector,
            page=chunk["metadata"]["pageCount"],
        )

    return chunks


@app.get("/ask")
async def ask_question(question: str):
    question_vector = embed_text(question)
    relevant_chunks = query_similar(question_vector)
    answer = generate_answer(question, relevant_chunks)

    return {
        "question": question,
        "answer": answer,
        "sources": relevant_chunks,
    }
