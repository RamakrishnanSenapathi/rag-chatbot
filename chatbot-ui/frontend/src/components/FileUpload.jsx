import { useRef, useState } from "react";
import { uploadDocument } from "../services/api";

export default function FileUpload() {
  const fileInputRef = useRef(null);

  const [selectedFile, setSelectedFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState("");

  // Only select the file
  const handleFileChange = (event) => {
    const file = event.target.files[0];

    if (!file) return;

    if (file.type !== "application/pdf") {
      setMessage("Please select a PDF file.");
      setSelectedFile(null);
      return;
    }

    setSelectedFile(file);
    setMessage("");
  };

  // Endpoint is triggered ONLY here
  const handleUpload = async () => {
    if (!selectedFile) {
      setMessage("Please select a PDF first.");
      return;
    }

    setUploading(true);
    setMessage("");

    try {
      const data = await uploadDocument(selectedFile);

      setMessage(
        data.message || "PDF uploaded and processed successfully!"
      );

      setSelectedFile(null);

      // Reset file input
      if (fileInputRef.current) {
        fileInputRef.current.value = "";
      }
    } catch (error) {
      setMessage(error.message);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
      
      <div className="mb-4">
        <h2 className="font-semibold text-slate-800">
          Knowledge Base
        </h2>

        <p className="mt-1 text-sm text-slate-500">
          Select a PDF and upload it to the RAG knowledge base.
        </p>
      </div>

      {/* Hidden file input */}
      <input
        ref={fileInputRef}
        type="file"
        accept=".pdf,application/pdf"
        onChange={handleFileChange}
        className="hidden"
      />

      {/* Select PDF */}
      <button
        type="button"
        onClick={() => fileInputRef.current?.click()}
        disabled={uploading}
        className="w-full rounded-lg border border-slate-300 bg-white px-4 py-2.5 text-sm font-medium text-slate-700 hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-50"
      >
        📄 Select PDF
      </button>

      {/* Selected file */}
      {selectedFile && (
        <div className="mt-3 rounded-lg bg-slate-50 p-3">
          <p className="truncate text-sm font-medium text-slate-700">
            📄 {selectedFile.name}
          </p>

          <p className="mt-1 text-xs text-slate-400">
            {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
          </p>
        </div>
      )}

      {/* Upload button */}
      <button
        type="button"
        onClick={handleUpload}
        disabled={!selectedFile || uploading}
        className="mt-3 w-full rounded-lg bg-blue-600 px-4 py-2.5 text-sm font-medium text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-slate-300"
      >
        {uploading ? "Processing PDF..." : "Upload PDF"}
      </button>

      {/* Status */}
      {message && (
        <p className="mt-3 text-sm text-slate-600">
          {message}
        </p>
      )}
    </div>
  );
}