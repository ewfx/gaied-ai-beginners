import os
from docx import Document
import pdfplumber
from io import BytesIO
import pytesseract
from PIL import Image

# Specify the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Update this path as needed
def read_document(file_bytes, file_extension):
    """
    Reads the content of a document (.docx, .pdf) from a bytearray and returns the text.
    :param file_bytes: The bytearray of the document.
    :param file_extension: The file extension (e.g., .docx, .pdf).
    :return: Extracted text from the document.
    """
    file_extension = file_extension.lower().replace("\x00", "").strip()

    if file_extension == ".docx":
        return read_docx(file_bytes)
    elif file_extension == ".pdf":
        return read_pdf_with_pdfplumber(file_bytes)  # Using pdfplumber
    else:
        raise ValueError("Unsupported file format. Please provide a .docx or .pdf file.")

# Helper functions
def read_docx(file_bytes):
    """
    Reads the content of a .docx file from a bytearray and returns the text.
    """
    doc = Document(BytesIO(file_bytes))  # Load the document from the bytearray
    content = []
    for paragraph in doc.paragraphs:
        content.append(paragraph.text)
    return "\n".join(content)

def read_pdf_with_pdfplumber(file_bytes):
    """
    Reads the content of a PDF file from a bytearray using pdfplumber and pytesseract for OCR.
    Returns the extracted text.
    """
    content = []
    with pdfplumber.open(BytesIO(file_bytes)) as pdf:  # Load the PDF from the bytearray
        for page in pdf.pages:
            # Extract text from the page
            text = page.extract_text()
            if text:
                content.append(text)

            # Extract images and perform OCR
            for image in page.images:
                # Extract the image from the page
                x0, y0, x1, y1 = image["x0"], image["y0"], image["x1"], image["y1"]
                cropped_image = page.within_bbox((x0, y0, x1, y1)).to_image()
                pil_image = cropped_image.original

                # Perform OCR on the image
                ocr_text = pytesseract.image_to_string(pil_image)
                if ocr_text.strip():  # Add OCR text if it's not empty
                    content.append(ocr_text)

            # Extract tables (if any)
            tables = page.extract_tables()
            for table in tables:
                table_content = "\n".join(["\t".join(row) for row in table])
                content.append(table_content)

    return "\n".join(content)