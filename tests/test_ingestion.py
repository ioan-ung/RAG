import ingestion
from ingestion import chunk_pdf, create_chunk_obj, goDownTillaWordBegins


def test_go_down_till_a_word_begins_finds_preceding_space():
    text = "hello world foo"
    assert goDownTillaWordBegins(text, 8) == 5


def test_go_down_till_a_word_begins_stops_at_start_when_no_space_before():
    text = "NoSpaceBeforeThisPoint"
    assert goDownTillaWordBegins(text, 5) == 0


def test_chunk_pdf_handles_page_shorter_than_length(monkeypatch):
    class OnePage:
        def extract_text(self):
            return "Scurt."

    class ShortPdfReader:
        def __init__(self, _file_obj):
            self.pages = [OnePage()]

    monkeypatch.setattr(ingestion.PyPDF2, "PdfReader", ShortPdfReader)

    chunks = chunk_pdf(b"irrelevant, PdfReader is mocked", length=100, overlap=10)

    assert len(chunks) == 1
    assert chunks[0]["text"] == "Scurt."


def test_create_chunk_obj_shape():
    chunk = create_chunk_obj(1, "some text", 0, 2)
    assert chunk == {
        "chunk_id": 1,
        "text": "some text",
        "metadata": {
            "index_start": 0,
            "char_count": 9,
            "pageCount": 2,
        },
    }


def test_chunk_pdf_returns_well_formed_chunks(fake_pdf):
    chunks = chunk_pdf(b"%PDF-1.4 fake content", length=50, overlap=5)

    assert len(chunks) > 0
    for chunk in chunks:
        assert set(chunk.keys()) == {"chunk_id", "text", "metadata"}
        assert set(chunk["metadata"].keys()) == {"index_start", "char_count", "pageCount"}
