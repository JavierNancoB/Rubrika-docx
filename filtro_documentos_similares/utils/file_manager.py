import os
import shutil
from config import RUTA_TEXTOS, RUTA_OUTPUT, RUTA_UNIFICADOS, RUTA_RESULTADOS, RUTA_SEMANTICAMENTE_EQUIVALENTES
from docx import Document

# utils/file_manager.py

def crear_carpetas():
    os.makedirs(RUTA_TEXTOS, exist_ok=True)
    os.makedirs(RUTA_OUTPUT, exist_ok=True)
    os.makedirs(RUTA_UNIFICADOS, exist_ok=True)
    os.makedirs(RUTA_SEMANTICAMENTE_EQUIVALENTES, exist_ok=True)
    os.makedirs(RUTA_RESULTADOS, exist_ok=True)


'''
ESTANDARIZAR ARCHIVOS
'''


def extraer_texto_docx(ruta_archivo):
    # Extrae el texto de un archivo .docx y lo devuelve como una cadena de texto
    doc = Document(ruta_archivo)
    texto = "\n".join([p.text for p in doc.paragraphs])
    return texto

def organizar_archivos():
    # Convierte cada archivo .docx en .txt y lo guarda en la carpeta output/
    for archivo in os.listdir(RUTA_TEXTOS):
        ruta_origen = os.path.join(RUTA_TEXTOS, archivo)
        ruta_destino = os.path.join(RUTA_OUTPUT, archivo.replace('.docx', '.txt'))

        # Procesa solo archivos .docx
        if archivo.endswith(".docx"):
            # Extrae el texto y lo guarda en un archivo .txt en output
            texto = extraer_texto_docx(ruta_origen)
            with open(ruta_destino, 'w', encoding='utf-8') as f:
                f.write(texto)
        else:
            print(f"El archivo {archivo} no es un .docx y no será procesado.")

def mover_a_unificados(doc1, doc2):
    # Mueve los archivos .txt de output a la subcarpeta unificados
    shutil.move(os.path.join(RUTA_OUTPUT, doc1), os.path.join(RUTA_UNIFICADOS, doc1))
    shutil.move(os.path.join(RUTA_OUTPUT, doc2), os.path.join(RUTA_UNIFICADOS, doc2))
