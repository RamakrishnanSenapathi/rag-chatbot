import ChatWindow from "./components/ChatWindow";
import FileUpload from "./components/FileUpload";

function App() {
  return (
    <div className="flex min-h-screen flex-col bg-slate-100">
      
      {/* Header */}
      <header className="border-b bg-white">
        <div className="flex items-center justify-between px-6 py-4">
          <div>
            <h1 className="text-xl font-bold text-slate-900">
              RAG Chatbot
            </h1>

            <p className="text-sm text-slate-500">
              Chat with your documents using AI
            </p>
          </div>

          <div className="flex items-center gap-2">
            <span className="h-2 w-2 rounded-full bg-green-500"></span>

            <span className="text-sm text-slate-600">
              AI Online
            </span>
          </div>
        </div>
      </header>

      {/* Main */}
      <div className="flex flex-1 overflow-hidden">

        {/* Sidebar */}
        <aside className="hidden w-72 border-r bg-slate-50 p-4 md:block">
          <FileUpload />

          <div className="mt-6 rounded-xl border bg-white p-4">
            <h3 className="text-sm font-semibold text-slate-700">
              RAG Pipeline
            </h3>

            <div className="mt-3 space-y-2 text-xs text-slate-500">
              <p>📄 PDF</p>
              <p>↓</p>
              <p>✂️ Text Chunking</p>
              <p>↓</p>
              <p>🔢 Gemini Embeddings</p>
              <p>↓</p>
              <p>🗄️ FAISS</p>
              <p>↓</p>
              <p>🤖 Gemini LLM</p>
            </div>
          </div>
        </aside>

        {/* Chat */}
        <main className="flex-1 overflow-hidden">
          <ChatWindow />
        </main>

      </div>
    </div>
  );
}

export default App;