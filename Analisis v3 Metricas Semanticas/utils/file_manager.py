# utils/file_manager.py
import os
from config import RUTA_DOCUMENTOS, RUTA_OUTPUT

def crear_carpetas():
    os.makedirs(RUTA_DOCUMENTOS, exist_ok=True)
    os.makedirs(RUTA_OUTPUT, exist_ok=True)

def obtener_documentos():
    # Lista solo los archivos .txt en Documentos_del_cliente
    documentos = [doc for doc in os.listdir(RUTA_DOCUMENTOS) if doc.endswith('.txt')]
    if len(documentos) < 2:
        raise ValueError("Debe haber al menos 2 documentos en la carpeta 'Documentos_del_cliente' para realizar el análisis.")
    return documentos[:2]  # Retorna solo los dos primeros documentos para la comparación
