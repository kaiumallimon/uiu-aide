# tools/pdf_reader.py
from PyPDF2 import PdfReader

def extract_pdf_text(pdf_path):
    reader = PdfReader(pdf_path)
    return " ".join(page.extract_text() or "" for page in reader.pages)
