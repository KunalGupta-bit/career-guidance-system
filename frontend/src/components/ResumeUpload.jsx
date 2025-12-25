import { useState } from "react";
import { UploadCloud, FileText, Loader2 } from "lucide-react";
import { analyzeResume } from "./api";

export default function ResumeUpload({ onResult }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async () => {
  if (!file) return alert("Upload a PDF");

  try {
    const data = await analyzeResume(file);
    onResult(data);
  } catch (err) {
    console.error(err);
    alert("Error analyzing resume");
  }
};

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);
    setError("");

    try {
      const response = await fetch("http://127.0.0.1:8000/analyze-resume", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Something went wrong");
      }

      onResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mt-8 max-w-full sm:max-w-md mx-auto bg-white/80 backdrop-blur-xl p-6 sm:p-8 rounded-2xl shadow-2xl border border-gray-200">
      {/* Header */}
      <div className="text-center mb-6">
        <h2 className="text-xl sm:text-2xl font-bold text-gray-800">
          AI Resume Analyzer
        </h2>
        <p className="text-xs sm:text-sm text-gray-500 mt-1">
          Upload your resume & discover your skill gaps
        </p>
      </div>

      {/* Upload Box */}
      <label className="flex flex-col items-center justify-center border-2 border-dashed border-gray-300 rounded-xl p-4 sm:p-6 cursor-pointer hover:border-blue-500 transition w-full">
        <UploadCloud className="w-8 h-8 sm:w-10 sm:h-10 text-blue-500 mb-2 sm:mb-3" />
        <p className="text-xs sm:text-sm text-gray-600 text-center break-words">
          {file ? (
            <span className="flex items-center gap-1 sm:gap-2 text-green-600 font-medium">
              <FileText className="w-3 h-3 sm:w-4 sm:h-4" />
              {file.name}
            </span>
          ) : (
            "Click to upload your resume (PDF)"
          )}
        </p>

        <input
          type="file"
          accept=".pdf"
          className="hidden"
          onChange={(e) => setFile(e.target.files[0])}
        />
      </label>

      {/* Button */}
      <button
        onClick={handleSubmit}
        disabled={loading}
        className="mt-4 sm:mt-6 w-full flex items-center justify-center gap-2 bg-gradient-to-r from-blue-600 to-indigo-600 text-white py-2.5 sm:py-3 rounded-xl font-semibold hover:opacity-90 transition disabled:opacity-60 text-sm sm:text-base"
      >
        {loading ? (
          <>
            <Loader2 className="animate-spin w-4 h-4 sm:w-5 sm:h-5" />
            Analyzing Resume...
          </>
        ) : (
          "Analyze Resume"
        )}
      </button>

      {/* Error */}
      {error && (
        <p className="text-red-600 text-xs sm:text-sm mt-3 sm:mt-4 text-center break-words">
          {error}
        </p>
      )}
    </div>
  );
}
