import { useState } from "react";
import ResumeUpload from "./components/ResumeUpload";
import ResultCard from "./components/ResultCard";
import './App.css';
import { analyzeResume } from "../api";

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);

  const handleSubmit = async () => {
    if (!file) return;

    const data = await analyzeResume(file);
    setResult(data);
  };

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <h1 className="text-3xl font-bold text-center mb-6">
        AI Career Guidance System
      </h1>

      <div className="max-w-xl mx-auto">
        <ResumeUpload onResult={setResult} />
        <ResultCard result={result} />
      </div>
    </div>
  );
}

export default App;
