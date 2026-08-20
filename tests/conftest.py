import os
import sys
from unittest.mock import MagicMock

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault("GEMINI_API_KEY", "test-key-not-real")

import embedding
import generation
import ingestion
import retrieval


@pytest.fixture(autouse=True)
def mock_gemini(monkeypatch):
    def fake_embed_content(model, contents):
        fake_result = MagicMock()
        fake_result.embeddings = [MagicMock(values=[0.1, 0.2, 0.3])]
        return fake_result

    def fake_generate_content(model, contents):
        fake_response = MagicMock()
        fake_response.text = "Raspuns generat de test."
        return fake_response

    monkeypatch.setattr(embedding.client_gemini.models, "embed_content", fake_embed_content)
    monkeypatch.setattr(generation.client_gemini.models, "generate_content", fake_generate_content)


@pytest.fixture
def mock_collection(monkeypatch):
    calls = {"add": [], "query_result": {"documents": [["context relevant unu", "context relevant doi"]]}}

    def fake_add(**kwargs):
        calls["add"].append(kwargs)

    def fake_query(**kwargs):
        return calls["query_result"]

    monkeypatch.setattr(retrieval.collection, "add", fake_add)
    monkeypatch.setattr(retrieval.collection, "query", fake_query)
    return calls


class FakePage:
    def __init__(self, text):
        self._text = text

    def extract_text(self):
        return self._text


class FakePdfReader:
    def __init__(self, pages_text):
        self.pages = [FakePage(t) for t in pages_text]


@pytest.fixture
def fake_pdf(monkeypatch):
    pages_text = ["word " * 80]

    def fake_reader(file_obj):
        return FakePdfReader(pages_text)

    monkeypatch.setattr(ingestion.PyPDF2, "PdfReader", fake_reader)
    return pages_text
