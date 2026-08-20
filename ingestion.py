import io
import re

import PyPDF2


def goDownTillaWordBegins(text, index):
    while index > 0 and text[index] != ' ':
        index -= 1
    return index


def create_chunk_obj(chunk_id, text, indexStart, pageCount):
    return {
        "chunk_id": chunk_id,
        "text": text,
        "metadata": {
            "index_start": indexStart,
            "char_count": len(text),
            "pageCount": pageCount
        }
    }


def chunk_pdf(content: bytes, length: int = 100, overlap: int = 10) -> list[dict]:
    pdf = PyPDF2.PdfReader(io.BytesIO(content))
    id = 0
    chunks = []

    pageCount, pageLen = 0, len(pdf.pages)
    start_index = 0
    while pageCount < pageLen:
        pagina = pdf.pages[pageCount]
        text_complet = pagina.extract_text()
        text_complet = re.sub(r'[^a-zA-Z0-9\s\.,!\?]', '', text_complet)
        if start_index:
            start_index = goDownTillaWordBegins(text_complet, start_index)
            text = text + text_complet[:start_index]
            id += 1
            chunks.append(create_chunk_obj(id, text, start_index, pageCount))
            start_index -= overlap

        while start_index + length < len(text_complet):
            start_index = goDownTillaWordBegins(text_complet, start_index) + 1
            stop_index = goDownTillaWordBegins(text_complet, start_index + length) - 1

            text = text_complet[start_index:stop_index + 1]

            id += 1
            chunks.append(create_chunk_obj(id, text, start_index, pageCount))
            start_index = stop_index - overlap

        start_index = goDownTillaWordBegins(text_complet, start_index)
        text = text_complet[start_index:]
        start_index = len(text_complet) - start_index
        pageCount += 1

    id += 1
    chunks.append(create_chunk_obj(id, text, start_index, pageCount))
    return chunks
