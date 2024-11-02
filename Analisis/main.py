import os
from datetime import datetime
from collections import Counter
from document_reader import read_docx
from text_cleaner import preprocess, generate_ngrams
from section_extractor import extract_sections
from similarity_calculator import calculate_similarity_matrix, find_optimal_matching
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
sectioned_docs = [extract_sections(doc) for doc in documents]

# Generar timestamp y nombre de archivo de resultados
timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
result_file_path = os.path.join(output_dir, f"resultados_analisis_{timestamp}.txt")

# Escribir resultados en archivo
write_all_results(result_file_path, files, processed_docs,)  # Asegúrate de pasar documents aquí
print(f"Análisis completado y guardado en '{result_file_path}'.")
