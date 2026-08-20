from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_home_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"mesaj": "Serverul functioneaza!"}


def test_ask_question_returns_answer_and_sources(mock_collection):
    response = client.get("/ask", params={"question": "Ce este RAG?"})
    assert response.status_code == 200
    body = response.json()
    assert body["question"] == "Ce este RAG?"
    assert body["answer"] == "Raspuns generat de test."
    assert body["sources"] == ["context relevant unu", "context relevant doi"]


def test_ask_question_requires_question_param():
    response = client.get("/ask")
    assert response.status_code == 422


def test_test_pdf_chunks_and_stores_embeddings(mock_collection, fake_pdf):
    response = client.post(
        "/test-pdf",
        files={"file": ("doc.pdf", b"%PDF-1.4 fake content", "application/pdf")},
    )
    assert response.status_code == 200
    chunks = response.json()

    assert len(chunks) > 0
    for chunk in chunks:
        assert set(chunk.keys()) == {"chunk_id", "text", "metadata"}

    assert len(mock_collection["add"]) == len(chunks)


def test_test_pdf_respects_length_and_overlap_params(mock_collection, fake_pdf):
    response = client.post(
        "/test-pdf",
        params={"length": 50, "overlap": 5},
        files={"file": ("doc.pdf", b"%PDF-1.4 fake content", "application/pdf")},
    )
    assert response.status_code == 200
    assert len(response.json()) > 0
