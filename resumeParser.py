import os
import io
from dotenv import load_dotenv
from supabase import create_client
import PyPDF2

load_dotenv()

# Supabase client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")  # service key or anon key
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

BUCKET_NAME = "resumes"

def download_resume_bytes(file_name: str) -> bytes:
    """
    Download a file from Supabase Storage bucket as bytes.
    """
    try:
        data = supabase.storage.from_(BUCKET_NAME).download(file_name)
        return data
    except Exception as e:
        print(f"Error downloading file {file_name}: {e}")
        return None

def extract_pdf_text(pdf_bytes: bytes) -> str:
    """
    Extract text from a PDF file given as bytes.
    """
    if not pdf_bytes:
        return ""
    text = ""
    try:
        reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text

def get_resume_text(file_name: str) -> str:
    """
    Main function: downloads a PDF from Supabase and returns its text.
    """
    pdf_bytes = download_resume_bytes(file_name)
    return extract_pdf_text(pdf_bytes)

if __name__ == "__main__":
    # Example usage
    file_name = "aditya-sangwan-1757090476495.pdf"
    text = get_resume_text(file_name)
    print(text)
