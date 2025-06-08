import os
import fitz  # PyMuPDF
import pdfplumber
from pdf2docx import Converter
from pdf2image import convert_from_path

def pdf_to_text(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        return '\n'.join(page.extract_text() or "" for page in pdf.pages)

def pdf_to_docx(pdf_path, output_path):
    cv = Converter(pdf_path)
    cv.convert(output_path, start=0, end=None)
    cv.close()
    return output_path

def pdf_to_html(pdf_path, output_path):
    with pdfplumber.open(pdf_path) as pdf:
        html_content = ''.join(f"<p>{page.extract_text()}</p>" for page in pdf.pages)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"<html><body>{html_content}</body></html>")
    return output_path

def pdf_to_images(pdf_path, output_dir):
    images = convert_from_path(pdf_path)
    output_files = []
    for i, img in enumerate(images):
        img_path = os.path.join(output_dir, f"page_{i + 1}.png")
        img.save(img_path, "PNG")
        output_files.append(img_path)
    return output_files
