from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from fastapi import HTTPException
from rag import create_vector_db, load_vector_db
from fastapi import UploadFile, File
from pathlib import Path
import shutil
from rag import create_vector_db, load_vector_db
from dotenv import load_dotenv
import os

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DOCUMENTS_DIR = BASE_DIR / "documents"
FAISS_DIR = BASE_DIR / "faiss_index"

DOCUMENTS_DIR.mkdir(exist_ok=True)

load_dotenv()


app = FastAPI(
    title="RAG Chatbot API"
)

vector_db = None

@app.on_event("startup")
def startup_event():
    global vector_db

    try:
        vector_db = load_vector_db()
        print("FAISS vector database loaded successfully")

    except Exception as e:
        print(f"FAISS database not loaded: {e}")



# React frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173",
                   "https://rag-chatbot-qc4xakmxj-rocking5.vercel.app",],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#llm definition
llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.3
)
# base model
class ChatRequest1(BaseModel):
    query: str
# base model for rag
class ChatRequest(BaseModel):
    question: str

#normal chat endpoint
@app.post("/chat1")
def chatch(request: ChatRequest1):
    response = llm.invoke(request.query)
    return {
        "query": request.query,
        "response": response.text
    }

#rag chat endpoint

@app.post("/chat")
def chat(request: ChatRequest):

    global vector_db

    if vector_db is None:
        raise HTTPException(
            status_code=503,
            detail="Vector database is not available"
        )

    try:
        docs = vector_db.similarity_search(
            request.question,
            k=3
        )

        context = "\n\n".join(
            doc.page_content
            for doc in docs
        )

        prompt = f"""
You are a helpful RAG assistant.

Answer the user's question using ONLY the
provided context.

If the answer is not available in the context,
say "I don't know based on the provided documents."

Context:
{context}

Question:
{request.question}

Answer:
"""

        response = llm.invoke(prompt)

        return {
            "question": request.question,
            "answer": response.content,
            "sources": [
                {
                    "page": doc.metadata.get("page"),
                    "source": doc.metadata.get("source")
                }
                for doc in docs
            ]
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"RAG processing failed: {str(e)}"
        )

#rag document retrieval endpoint
@app.post("/ingest")
def ingest_documents():

    global vector_db

    try:
        create_vector_db()

        vector_db = load_vector_db()

        return {
            "message": "Documents processed successfully"
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Ingestion failed: {str(e)}"
        )

# BASE_DIR = Path(__file__).resolve().parent

# DOCUMENTS_DIR = BASE_DIR / "documents"

# DOCUMENTS_DIR.mkdir(
#     exist_ok=True
# )

#upload PDF endpoint:
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    try:

        file_path = DOCUMENTS_DIR / file.filename

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        print(f"PDF saved: {file_path}")

        new_vector_db, chunk_count = create_vector_db(file_path)

        global vector_db
        vector_db = new_vector_db

        return {
            "message": f"{file.filename} uploaded successfully",
            "chunks": chunk_count
        }

    except Exception as e:

        print("UPLOAD ERROR:", repr(e))

        raise HTTPException(
            status_code=500,
            detail=f"Upload failed: {str(e)}"
        )

@app.get("/")
def home():
    return {
        "message": "RAG Chatbot API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }