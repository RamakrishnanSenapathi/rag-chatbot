import { useEffect, useRef, useState } from "react";
import Message from "./Message";
import ChatInput from "./ChatInput";
import { sendMessage } from "../services/api";

export default function ChatWindow() {
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content:
        "Hi! 👋 Ask me anything about the documents in the knowledge base.",
    },
  ]);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, loading]);

const handleSend = async (question) => {
  setError("");

  const userMessage = {
    role: "user",
    content: question,
  };

  setMessages((prev) => [...prev, userMessage]);
  setLoading(true);

  try {
    const data = await sendMessage(question);

    // Gemini response can be an array of content blocks
    let answer = "";

    if (typeof data.answer === "string") {
      answer = data.answer;
    } else if (Array.isArray(data.answer)) {
      answer = data.answer
        .filter((item) => item.type === "text")
        .map((item) => item.text)
        .join("\n");
    }

    const assistantMessage = {
      role: "assistant",
      content: answer || "I couldn't generate an answer.",
      sources: data.sources || [],
    };

    setMessages((prev) => [...prev, assistantMessage]);
  } catch (err) {
    setError(err.message);

    setMessages((prev) => [
      ...prev,
      {
        role: "assistant",
        content: "Sorry, I couldn't process your question.",
      },
    ]);
  } finally {
    setLoading(false);
  }
};

  return (
    <div className="flex h-full flex-col">
      {/* Chat messages */}
      <div className="flex-1 overflow-y-auto p-6">
        <div className="mx-auto max-w-4xl">
          {messages.map((message, index) => (
            <Message key={index} message={message} />
          ))}

          {loading && (
            <div className="mb-4 flex justify-start">
              <div className="rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm text-slate-500">
                Thinking...
              </div>
            </div>
          )}

          {error && (
            <div className="mb-4 rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-600">
              {error}
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input */}
      <div className="border-t bg-white p-4">
        <div className="mx-auto max-w-4xl">
          <ChatInput onSend={handleSend} loading={loading} />

          <p className="mt-2 text-center text-xs text-slate-400">
            Powered by Gemini + LangChain + Pinecone
          </p>
        </div>
      </div>
    </div>
  );
}