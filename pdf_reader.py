import pymupdf  # PyMuPDF

def extract_text(pdf_path):
    text = ""

    doc = pymupdf.open(pdf_path)

    for page in doc:
        text += page.get_text()

    doc.close()

    return text