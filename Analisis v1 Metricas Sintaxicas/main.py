# Autor: Javier Alonso Nanco Becerra
# Fecha: 2024/09/30

'''

Este script realiza el análisis de los documentos del cliente y guarda los resultados en un archivo de texto.

Tomando 2 archivos de texto, los limpia y los compara para encontrar similitudes y diferencias.

Guarda los resultados en un archivo de texto.

'''


import os
from datetime import datetime
from document_reader import read_docx
from text_cleaner import preprocess
from file_writer import write_all_results

# Configuración de rutas
current_dir = os.path.dirname(__file__)
docs_dir = os.path.join(current_dir, "Documentos del Cliente")
output_dir = os.path.join(current_dir, "resultados")
os.makedirs(output_dir, exist_ok=True)

# Cargar documentos como cadenas de texto
files = [f for f in os.listdir(docs_dir) if f.endswith('.docx')]
documents = [read_docx(os.path.join(docs_dir, file)) for file in files]

# Procesar los documentos
processed_docs = [preprocess(doc) for doc in documents]

# Generar timestamp y nombre de archivo de resultados
timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
result_file_path = os.path.join(output_dir, f"resultados_analisis_{timestamp}.txt")

# Escribir resultados en archivo
write_all_results(result_file_path, files, processed_docs, documents)  # Incluye documents como raw_docs
print(f"Análisis completado y guardado en '{result_file_path}'.")
