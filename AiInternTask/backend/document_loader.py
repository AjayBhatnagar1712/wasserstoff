import os
from PyPDF2 import PdfReader
from PIL import Image
import pytesseract
import textwrap

# Load text from a document (PDF or image)
def load_document(file_path):
    ext = file_path.lower()

    if ext.endswith(".pdf"):
        return load_pdf(file_path)
    elif ext.endswith((".png", ".jpg", ".jpeg")):
        return load_image(file_path)
    else:
        raise ValueError("Unsupported file format. Please upload a PDF or image file.")

# Extract text from a PDF
def load_pdf(file_path):
    text = ""
    try:
        reader = PdfReader(file_path)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text.strip()

# Extract text from an image using Tesseract OCR
def load_image(file_path):
    try:
        image = Image.open(file_path)
        return pytesseract.image_to_string(image)
    except Exception as e:
        print(f"Error reading image: {e}")
        return ""

# Split text into chunks of ~300 tokens (or characters)
def chunk_text(text, max_length=300):
    return textwrap.wrap(text, width=max_length)
