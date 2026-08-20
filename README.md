# RAG

A complete Retrieval-Augmented Generation (RAG) pipeline: ingest PDFs, embed and store them, then retrieve and generate grounded answers to questions.

## Key Features

- **PDF Document Ingestion**: Upload and process PDF files with intelligent text chunking
- **Semantic Embeddings**: Convert text to high-dimensional vectors using Google's Gemini embedding model
- **Vector Storage**: Persist embeddings in ChromaDB for fast similarity search
- **Retrieval-Augmented Generation**: Retrieve relevant chunks and generate grounded answers with Gemini
- **REST API**: FastAPI-based endpoints for all RAG operations

## Tech Stack

- **Framework**: FastAPI (Python web framework)
- **Vector Database**: ChromaDB (persistent vector storage)
- **Embeddings**: Google Gemini API (`google-genai`)
- **PDF Processing**: PyPDF2
- **Server**: Uvicorn (ASGI server)
- **Dependencies**: Pydantic, Requests, NumPy

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/ioan-ung/RAG.git
   cd RAG
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up API credentials**
   - Obtain a Google Gemini API key from [Google AI Studio](https://ai.google.dev/)
   - Update the `API_KEY` in `ingestion.py`:
     ```python
     client_gemini = genai.Client(api_key="YOUR_API_KEY_HERE")
     ```

## Usage

### Start the server

```bash
uvicorn ingestion:app --reload
```

Server runs at `http://localhost:8000`

### API Endpoints

**Health check:**
```bash
GET /
```

**Upload and index a PDF:**
```bash
POST /test-pdf
```
Parameters:
- `file` (required): PDF file to upload
- `length` (optional, default=100): Chunk size in characters
- `overlap` (optional, default=10): Overlap between consecutive chunks

Example:
```bash
curl -X POST "http://localhost:8000/test-pdf" \
  -F "file=@document.pdf" \
  -F "length=100" \
  -F "overlap=10"
```

**Query the knowledge base:**
```bash
GET /ask?question=your_question_here
```

Example:
```bash
curl "http://localhost:8000/ask?question=What%20is%20the%20main%20topic%3F"
```

Response:
```json
{
  "question": "What is the main topic?",
  "answer": "Generated answer grounded in the retrieved context...",
  "sources": [
    "chunk 1 text...",
    "chunk 2 text...",
    "chunk 3 text..."
  ]
}
```

## How It Works

1. **Ingestion**: PDF files are parsed page-by-page, text is cleaned, and split into overlapping chunks
2. **Embedding**: Each chunk is converted to a 3072-dimensional vector using Gemini embeddings
3. **Storage**: Vectors and metadata are stored in ChromaDB with persistent SQLite backend
4. **Retrieval**: User queries are embedded and compared against stored vectors using cosine similarity, returning the top 3 most relevant chunks
5. **Augmentation**: The retrieved chunks are inserted into a prompt as grounding context
6. **Generation**: `gemini-2.5-flash` generates an answer constrained to that context

## Project Structure

```
RAG/
├── ingestion.py           # Main application: PDF processing, embedding, retrieval, generation
├── requirements.txt       # Python dependencies
├── embedding.py          # (Placeholder for embedding utilities)
├── vector_db/            # ChromaDB persistent storage (gitignored, generated locally)
├── venv/                 # Virtual environment (gitignored, generated locally)
└── README.md            # This file
```

## Notes

- API keys and credentials should be stored in environment variables (use `.env` file with `python-dotenv`)
- Text cleaning removes special characters, keeping only alphanumeric, spaces, and basic punctuation
- Chunk overlap prevents important context from being split across boundaries
- Vector database persists locally; no external database setup required

## License

Not specified. Add appropriate license if needed.
