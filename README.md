# 🤖 RAG Chatbot

A full-stack **Retrieval-Augmented Generation (RAG) chatbot** that allows users to upload PDF documents and ask questions based on their content.

The application uses **Python FastAPI** for the backend, **React.js** for the frontend, **LangChain** for the RAG pipeline, **Gemini** for embeddings and LLM responses, and **FAISS** for vector similarity search.

## 🚀 Features

* 📄 Upload PDF documents
* ✂️ Automatic document text chunking
* 🔢 Gemini-based text embeddings
* 🗄️ FAISS vector database
* 🔍 Semantic similarity search
* 🤖 Gemini LLM-powered responses
* 📚 Answers grounded in uploaded documents
* 📌 Source/page information for retrieved documents
* ⚡ FastAPI REST APIs
* 🎨 React.js + Tailwind CSS UI
* 🔄 Multiple PDF document support
* 🌐 CORS-enabled frontend/backend communication

## 🏗️ Architecture

```text
                    User
                     │
                     ▼
              React.js Frontend
                     │
                     │ HTTP
                     ▼
              FastAPI Backend
                     │
              ┌──────┴──────┐
              │             │
          PDF Upload      Question
              │             │
              ▼             ▼
         PDF Loader     Query Embedding
              │             │
              ▼             ▼
         Text Chunking   FAISS Search
              │             │
              ▼             ▼
       Gemini Embeddings  Relevant Chunks
                            │
                            ▼
                       RAG Prompt
                            │
                            ▼
                       Gemini LLM
                            │
                            ▼
                       Final Answer
```

## 🛠️ Tech Stack

### Frontend

* React.js
* Vite
* Tailwind CSS
* JavaScript

### Backend

* Python
* FastAPI
* LangChain

### Generative AI

* Google Gemini
* Gemini Embeddings
* Retrieval-Augmented Generation (RAG)

### Vector Database

* FAISS

### Document Processing

* PyPDFLoader
* RecursiveCharacterTextSplitter

## 📁 Project Structure

```text
RAG-learning/
│
├── backend/
│   ├── documents/
│   ├── faiss_index/
│   ├── main.py
│   ├── rag.py
│   ├── requirements.txt
│   └── .gitignore
│
├── chatbot-ui/
│   └── frontend/
│       ├── src/
│       │   ├── components/
│       │   │   ├── ChatWindow.jsx
│       │   │   ├── ChatInput.jsx
│       │   │   ├── FileUpload.jsx
│       │   │   └── Message.jsx
│       │   ├── services/
│       │   │   └── api.js
│       │   ├── App.jsx
│       │   └── main.jsx
│       ├── public/
│       ├── package.json
│       └── vite.config.js
│
└── README.md
```

## 🔄 RAG Pipeline

The application follows these steps:

```text
PDF
 ↓
Document Loading
 ↓
Text Chunking
 ↓
Gemini Embeddings
 ↓
FAISS Vector Store
 ↓
User Question
 ↓
Similarity Search
 ↓
Relevant Context
 ↓
Prompt + Context + Question
 ↓
Gemini LLM
 ↓
Answer + Sources
```

## ⚙️ Backend Setup

Navigate to the backend:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
GOOGLE_API_KEY=your_google_api_key
```

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

Backend will run at:

```text
http://127.0.0.1:8000
```

## 🎨 Frontend Setup

Navigate to the frontend:

```bash
cd chatbot-ui/frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The frontend will run at:

```text
http://localhost:5173
```

## 🔐 Environment Variables

Never commit API keys or secrets to GitHub.

Example:

```env
GOOGLE_API_KEY=your_google_api_key
```

The `.env` file is excluded using `.gitignore`.

## 📡 API Endpoints

### Chat

```http
POST /chat
```

Example request:

```json
{
  "question": "What is mentioned in the document?"
}
```

### Upload PDF

```http
POST /upload
```

Uploads a PDF and adds its content to the RAG knowledge base.

### Health Check

```http
GET /
```

## 🧠 Key RAG Concepts Demonstrated

This project demonstrates practical implementation of:

* Retrieval-Augmented Generation
* Semantic Search
* Vector Embeddings
* Vector Databases
* Document Chunking
* Context Retrieval
* Prompt Engineering
* LLM Integration
* Source Attribution
* REST API Development
* React + FastAPI Integration

## 🚧 Future Improvements

* [ ] Deploy frontend and backend to the cloud
* [ ] Replace local FAISS with a cloud vector database such as Pinecone
* [ ] Add authentication and authorization
* [ ] Add document management and deletion
* [ ] Add conversation history
* [ ] Add streaming LLM responses
* [ ] Add reranking for improved retrieval
* [ ] Add production monitoring and logging

## 🎯 Purpose

This project was built as a hands-on implementation of a production-style **Generative AI and RAG application**, covering the complete flow from document ingestion and vectorization to retrieval, LLM generation, and a web-based chat interface.

## 👨‍💻 Author

**Ramakrishnan Senapathi**

Generative AI | RAG | Python | LangChain | FastAPI | React.js
