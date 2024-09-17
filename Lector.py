'''
Importamos python-docx
'''
from docx import Document
import os

def leer_documento(docx_path):
    # Cargar el documento
    doc = Document(docx_path)

    # Leer el contenido del documento
    for para in doc.paragraphs:
        print(para.text)

# Ubicación relativa del archivo desde el script
nombre_archivo = "1 - Contrato de Trabajo - Formato General.docx"
ruta_relativa = os.path.join("Rubrika-docx/Received", nombre_archivo)

# Imprimir la ruta absoluta para verificar si está apuntando correctamente al archivo
ruta_absoluta = os.path.abspath(ruta_relativa)
print(f"Intentando abrir el archivo en: {ruta_absoluta}")

# Llamada a la función para leer el documento
leer_documento(ruta_absoluta)
