import pdfplumber
import warnings

warnings.filterwarnings("ignore", message=".*FontBBox.*")

def extract_text_from_pdf(path):
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text.lower()

if __name__ == "__main__":
    # Test with your resume file
    result = extract_text_from_pdf("resume_k.pdf")
    print(result)