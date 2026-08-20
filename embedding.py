import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

client_gemini = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def embed_text(text: str) -> list[float]:
    result = client_gemini.models.embed_content(
        model="models/gemini-embedding-001",
        contents=text
    )
    return result.embeddings[0].values
