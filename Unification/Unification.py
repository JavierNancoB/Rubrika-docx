from docx import Document
import os
from fpdf import FPDF  # Este es el import correcto para fpdf2
import difflib

def load_docx_text(file_path):
    doc = Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

def compare_documents(text1, text2):
    d = difflib.Differ()
    diff = list(d.compare(text1.splitlines(), text2.splitlines()))
    result = []
    variable_count = 1
    for line in diff:
        if line.startswith('- ') or line.startswith('+ '):
            result.append(f"[$Variable{variable_count}$]")
            variable_count += 1
        elif line.startswith('  '):
            result.append(line[2:])
    return '\n'.join(result)

def save_to_pdf(text, filename="result.pdf"):
    directory = "Unification/Ejemplos"
    if not os.path.exists(directory):
        os.makedirs(directory)
    pdf = FPDF()
    pdf.add_page()
    # Asegúrate de que el archivo de fuente 'DejaVuSansCondensed.ttf' esté en el directorio correcto o usa una ruta absoluta aquí
    pdf.add_font('DejaVu', '', 'path/to/DejaVuSansCondensed.ttf')  # Cambia 'path/to/' con la ruta correcta
    pdf.set_font('DejaVu', '', 14)
    pdf.multi_cell(0, 10, text)
    pdf.output(os.path.join(directory, filename))

# Rutas a documentos
path1 = 'Unification/Ejemplos/Anexo Incentivo Bono de Gestión Asistente Comercial Solo Tienda Norte y Sur.docx'
path2 = 'Unification/Ejemplos/Anexo Incentivo Bono de Gestión Asistente Comercial Solo Tienda Stgo.docx'

text1 = load_docx_text(path1)
text2 = load_docx_text(path2)
result_text = compare_documents(text1, text2)
save_to_pdf(result_text, "output_result.pdf")
