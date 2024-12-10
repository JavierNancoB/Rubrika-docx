    # main.py
from config import RUTA_DOCUMENTOS, RUTA_OUTPUT, UMBRAL_SIMILITUD_SEMANTICA
from utils.file_manager import crear_carpetas, obtener_documentos
from utils.semantic_analysis import analizar_documentos
import os

def main():
    # Crear las carpetas necesarias
    crear_carpetas()
    
    # Obtener los dos documentos a comparar
    doc_files = obtener_documentos()
    doc1_path = os.path.join(RUTA_DOCUMENTOS, doc_files[0])
    doc2_path = os.path.join(RUTA_DOCUMENTOS, doc_files[1])
    
    # Leer el contenido de los documentos
    with open(doc1_path, 'r', encoding='utf-8') as f1:
        doc1_texto = f1.read()
    with open(doc2_path, 'r', encoding='utf-8') as f2:
        doc2_texto = f2.read()
    
    # Realizar análisis semántico
    similitud_semantica = analizar_documentos(doc1_texto, doc2_texto)
    
    # Crear un nombre único para el archivo de resultados
    nombre_resultado = f"similitud_{doc_files[0].replace('.txt', '')}_y_{doc_files[1].replace('.txt', '')}.txt"
    resultado_path = os.path.join(RUTA_OUTPUT, nombre_resultado)
    
    # Guardar resultados en el archivo con el formato solicitado
    with open(resultado_path, 'w', encoding='utf-8') as resultado:
        resultado.write(f"nombre doc 1: {doc_files[0]}\n")
        resultado.write(f"nombre doc 2: {doc_files[1]}\n\n")
        resultado.write("Métricas de similitud:\n")
        resultado.write(f"Similitud Semántica (Coseno): {similitud_semantica:.4f}\n")
        
        # Indicar si cumplen con el umbral de similitud semántica
        if similitud_semantica >= UMBRAL_SIMILITUD_SEMANTICA:
            resultado.write("Resultado: Los documentos son semánticamente similares.\n")
        else:
            resultado.write("Resultado: Los documentos NO son semánticamente similares.\n")

if __name__ == '__main__':
    main()
