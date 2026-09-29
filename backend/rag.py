import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
DOCUMENTS_DIR = BASE_DIR / "documents"

PINECONE_INDEX_NAME = "ragbot"


def get_embeddings():
    return GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )


def create_vector_db(pdf_path: str):

    pdf_path = Path(pdf_path)

    if not pdf_path.exists():
        raise FileNotFoundError(
            f"PDF not found: {pdf_path}"
        )

    print(f"Processing PDF: {pdf_path}")

    # Load PDF
    loader = PyPDFLoader(str(pdf_path))
    documents = loader.load()

    # Split text
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = text_splitter.split_documents(documents)

    if not chunks:
        raise ValueError("No text found in PDF")

    print(f"Created {len(chunks)} chunks")

    # Gemini embeddings
    embeddings = get_embeddings()

    # Store vectors in Pinecone
    vector_db = PineconeVectorStore.from_documents(
        documents=chunks,
        embedding=embeddings,
        index_name=PINECONE_INDEX_NAME
    )

    print("Documents successfully added to Pinecone")

    return vector_db, len(chunks)


def load_vector_db():

    embeddings = get_embeddings()

    vector_db = PineconeVectorStore.from_existing_index(
        index_name=PINECONE_INDEX_NAME,
        embedding=embeddings
    )

    print("Pinecone vector database loaded")

    return vector_db