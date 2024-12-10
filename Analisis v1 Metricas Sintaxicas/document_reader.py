from docx import Document

def read_docx(file_path):
    """Lee un archivo DOCX y devuelve el texto."""
    doc = Document(file_path)
    return " ".join([para.text for para in doc.paragraphs])
