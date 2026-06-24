from fastapi import FastAPI, UploadFile, File
from google import genai
import chromadb
import PyPDF2
import io,re

app = FastAPI()
client_gemini = genai.Client(api_key="API_KEY")
db_client = chromadb.PersistentClient(path="./vector_db")
collection = db_client.get_or_create_collection(name="pdf_knowledge_base")

def goDownTillaWordBegins(text,index):
    while text and text[index] != ' ':
        index-=1
    return index
def create_chunk_obj(chunk_id, text,indexStart,pageCount):
    return {
        "chunk_id": chunk_id,
        "text": text,
        "metadata": {
            "index_start": indexStart,
            "char_count": len(text),
            "pageCount":pageCount
        }
    }
def embedding(text):
    try:
        result = client_gemini.models.embed_content(
            model="models/gemini-embedding-001", 
            contents=text
        )
        vector = result.embeddings[0].values
    except Exception as e:
        print(f"Eroare: {e}")
    return vector

@app.get("/")
def home():
    return {"mesaj": "Serverul functioneaza!"}

@app.post("/test-pdf")
async def test_pdf(file: UploadFile = File(...),length:int=100,overlap:int=10):
    content = await file.read()
    pdf = PyPDF2.PdfReader(io.BytesIO(content))
    id=0
    chunks=[]

    pageCount,pageLen=0,len(pdf.pages)
    start_index=0
    while pageCount < pageLen:
        pagina=pdf.pages[pageCount]
        text_complet=pagina.extract_text()
        text_complet=re.sub(r'[^a-zA-Z0-9\s\.,!\?]', '', text_complet)
        if start_index:
            start_index=goDownTillaWordBegins(text_complet,start_index)
            text=text+text_complet[:start_index]
            id+=1
            chunks.append(create_chunk_obj(id,text,start_index,pageCount))
            start_index-=overlap


        while start_index+length<len(text_complet):
            start_index=goDownTillaWordBegins(text_complet,start_index)+1
            stop_index=goDownTillaWordBegins(text_complet,start_index+length)-1

            text=text_complet[start_index:stop_index+1]
            
            id+=1
            chunks.append(create_chunk_obj(id,text,start_index,pageCount))
            start_index=stop_index-overlap

        start_index=goDownTillaWordBegins(text_complet,start_index)
        text=text_complet[start_index:]
        start_index=len(text_complet)-start_index
        pageCount+=1
    
    id+=1
    chunks.append(create_chunk_obj(id,text,start_index,pageCount))
    for chunk in chunks:
        result = client_gemini.models.embed_content(
            model="models/gemini-embedding-001",
            contents=chunk["text"]
        )
        vector = result.embeddings[0].values

        # 2. Salvăm în ChromaDB
        collection.add(
            embeddings=[vector],         # Lista de numere (3072 dimensiuni)
            documents=[chunk["text"]],      # Textul brut (pentru a-l putea citi ulterior)
            ids=[f"id_{chunk['chunk_id']}_pg_{chunk['metadata']['pageCount']}"], # Un ID unic
            metadatas=[{"page": chunk["metadata"]["pageCount"]}] # Opțional: info extra despre pagină
        )
    
    return chunks


@app.get("/ask")
async def ask_question(question: str):
    # 1. Transformăm întrebarea utilizatorului în vector
    result = client_gemini.models.embed_content(
        model="models/gemini-embedding-001",
        contents=question
    )
    question_vector = result.embeddings[0].values

    # 2. Căutăm în ChromaDB cele mai relevante 3 fragmente
    # ChromaDB face automat calculul matematic de similitudine
    results = collection.query(
        query_embeddings=[question_vector],
        n_results=3  # Vrem cele mai bune 3 rezultate
    )

    # 3. Extragem textele găsite
    relevant_chunks = results['documents'][0]
    
    return {
        "question": question,
        "relevant_context": relevant_chunks
    }