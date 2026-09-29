export default function Message({ message }) {
  const isUser = message.role === "user";

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"} mb-4`}>
      <div
        className={`max-w-[80%] rounded-2xl px-4 py-3 ${
          isUser
            ? "bg-blue-600 text-white"
            : "bg-white border border-slate-200 text-slate-800"
        }`}
      >
        <p className="whitespace-pre-wrap">{message.content}</p>

        {/* Sources from RAG */}
        {!isUser && message.sources?.length > 0 && (
          <div className="mt-4 border-t border-slate-200 pt-3">
            <p className="text-xs font-semibold text-slate-500 mb-2">
              Sources
            </p>

            <div className="space-y-2">
              {message.sources.map((source, index) => (
                <div
                  key={index}
                  className="rounded-lg bg-slate-50 border border-slate-200 p-2"
                >
                  <p className="text-xs text-slate-600">
                    {source.source || "Document"}
                  </p>

                  {source.page !== undefined && (
                    <p className="text-xs text-slate-400">
                      Page {source.page + 1}
                    </p>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}