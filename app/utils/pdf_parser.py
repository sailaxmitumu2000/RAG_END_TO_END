from PyPDF2 import PdfReader
from typing import List

def extract_text_from_pdf(file_path: str) -> str:
    """
    Reads a PDF file and extracts all text as a single string.
    """
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""  # handle empty pages
    return text
