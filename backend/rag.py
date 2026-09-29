import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

# --------------------------------------------------
# Paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

PDF_PATH = BASE_DIR / "documents" / "rag.pdf"
VECTOR_DB_PATH = BASE_DIR / "faiss_index"

# Make sure directories exist
PDF_PATH.parent.mkdir(exist_ok=True)
VECTOR_DB_PATH.mkdir(exist_ok=True)


# --------------------------------------------------
# Embeddings
# --------------------------------------------------

def get_embeddings():

    return GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )


# --------------------------------------------------
# Create / Update FAISS Vector DB
# --------------------------------------------------

def create_vector_db(pdf_path: str):

    pdf_path = Path(pdf_path)

    if not pdf_path.exists():
        raise FileNotFoundError(
            f"PDF not found: {pdf_path}"
        )

    print(f"Processing PDF: {pdf_path}")

    # --------------------------------------------------
    # Load PDF
    # --------------------------------------------------

    loader = PyPDFLoader(str(pdf_path))
    documents = loader.load()

    # --------------------------------------------------
    # Split documents
    # --------------------------------------------------

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = text_splitter.split_documents(documents)

    if not chunks:
        raise ValueError("No text found in PDF")

    print(f"Created {len(chunks)} chunks")

    # --------------------------------------------------
    # Embeddings
    # --------------------------------------------------

    embeddings = get_embeddings()

    # --------------------------------------------------
    # Check existing FAISS
    # --------------------------------------------------

    index_file = VECTOR_DB_PATH / "index.faiss"

    if index_file.exists():

        print("Existing FAISS found. Adding new document...")

        vector_db = FAISS.load_local(
            str(VECTOR_DB_PATH),
            embeddings,
            allow_dangerous_deserialization=True
        )

        vector_db.add_documents(chunks)

    else:

        print("Creating new FAISS vector database...")

        vector_db = FAISS.from_documents(
            chunks,
            embeddings
        )

    # --------------------------------------------------
    # Save FAISS
    # --------------------------------------------------

    vector_db.save_local(
        str(VECTOR_DB_PATH)
    )

    print("FAISS vector database updated successfully")

    return vector_db, len(chunks)


# --------------------------------------------------
# Load existing FAISS
# --------------------------------------------------

def load_vector_db():

    embeddings = get_embeddings()

    index_file = VECTOR_DB_PATH / "index.faiss"

    if not index_file.exists():

        print("FAISS database does not exist yet.")

        return None

    vector_db = FAISS.load_local(
        str(VECTOR_DB_PATH),
        embeddings,
        allow_dangerous_deserialization=True
    )

    print("FAISS vector database loaded")

    return vector_db