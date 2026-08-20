# RAG-core

Build the foundational basis of Retrieval-Augmented Generation (RAG) algorithms.

## Key Features

- **PDF Document Ingestion**: Upload and process PDF files with intelligent text chunking
- **Semantic Embeddings**: Convert text to high-dimensional vectors using Google's Gemini embedding model
- **Vector Storage**: Persist embeddings in ChromaDB for fast similarity search
- **Question-Answering**: Query the knowledge base to retrieve relevant document chunks
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
   git clone https://github.com/ioan-ung/RAG-core.git
   cd RAG-core
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
   - Create a `.env` file in the project root with:
     ```
     GEMINI_API_KEY=YOUR_API_KEY_HERE
     ```

## Usage

### Start the server

```bash
uvicorn main:app --reload
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
  "relevant_context": [
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
4. **Retrieval**: User queries are embedded and compared against stored vectors using cosine similarity
5. **Response**: Top 3 most relevant chunks are returned as context

## Project Structure

```
RAG-core/
├── main.py                # FastAPI app + endpoints (/test-pdf, /ask)
├── ingestion.py           # PDF reading + chunking
├── embedding.py           # Gemini embedding calls
├── retrieval.py           # ChromaDB storage + query
├── generation.py          # LLM step that writes the answer
├── requirements.txt       # Python dependencies
├── tests/                 # Automated test suite (pytest)
├── vector_db/             # ChromaDB persistent storage
│   ├── chroma.sqlite3     # Vector database file
│   └── [collection-id]/   # Collection metadata
├── venv/                  # Virtual environment
└── README.md              # This file
```

## Notes

- API keys and credentials should be stored in environment variables (use `.env` file with `python-dotenv`)
- Text cleaning removes special characters, keeping only alphanumeric, spaces, and basic punctuation
- Chunk overlap prevents important context from being split across boundaries
- Vector database persists locally; no external database setup required

## License

Not specified. Add appropriate license if needed.
