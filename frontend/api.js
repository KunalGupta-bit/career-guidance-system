const API_URL = "https://career-guidance-system-gwod.onrender.com";

export async function analyzeResume(file) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${API_URL}/analyze-resume`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error("Failed to analyze resume");
  }

  return response.json();
}
