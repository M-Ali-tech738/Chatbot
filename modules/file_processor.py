import os
from PyPDF2 import PdfReader
from docx import Document
from pptx import Presentation
from PIL import Image
import pytesseract

def get_pdf_text(pdf, encoding='utf-8'):
    """Extracts and returns text from a PDF file."""
    text = ""
    pdf_reader = PdfReader(pdf)
    for page in pdf_reader.pages:
        text += page.extract_text().encode('latin1', 'replace').decode(encoding, 'replace')
    return text

def get_docx_text(docx_file):
    """Extracts and returns text from a DOCX file."""
    doc = Document(docx_file)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

def get_txt_text(uploaded_file):
    """Extracts and returns text from an uploaded TXT file."""
    text = ""
    # Reading directly from the UploadedFile object
    for line in uploaded_file:
        text += line.decode('utf-8')  # Decoding bytes to string if necessary
    return text


def get_pptx_text(pptx_file):
    """
    Extracts and returns text from a PPTX file.

    :param pptx_file: Path to the PPTX file or a file-like object
    :return: Extracted text as a string
    """
    text = ""  # Local variable to store the extracted text
    
    # Load the presentation
    presentation = Presentation(pptx_file)
    
    # Loop through each slide and each shape in the slide
    for slide in presentation.slides:
        for shape in slide.shapes:
            # Check if the shape has text
            if hasattr(shape, "text"):
                text += shape.text + "\n"
    
    return text

def extract_text_from_image(image_path):
    """
    Extracts and returns text from an image using OCR.

    :param image_path: Path to the image file
    :return: Extracted text as a string
    """
    # Open the image using PIL
    image = Image.open(image_path)
    
    # Use pytesseract to extract text from the image
    text = pytesseract.image_to_string(image)
    return text

def process_file(file):
    """Processes the file based on its type and returns the extracted text."""
    file_type = os.path.splitext(file.name)[1].lower()
    
    if file_type == ".pdf":
        return get_pdf_text(file)
    elif file_type == ".docx":
        return get_docx_text(file)
    elif file_type == ".txt":
        return get_txt_text(file)
    elif file_type == ".pptx":
        return get_pptx_text(file)
    elif (file_type == ".png" or file_type==".jpeg" or file_type==".jpg" ):
        return extract_text_from_image(file)
    else:
        raise ValueError("Unsupported file format")
