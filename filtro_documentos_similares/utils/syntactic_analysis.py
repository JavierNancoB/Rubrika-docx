import os
from config import RUTA_OUTPUT, UMBRAL_SIMILITUD_COSENO, UMBRAL_SIMILITUD_JACCARD, UMBRAL_SIMILITUD_DICE
from utils.file_manager import crear_carpetas
from utils.similarity_metrics import calcular_similitudes_sintacticas
import shutil

def analizar_sintactico():
    # Lista de documentos en output, filtrando solo archivos .txt
    documentos = [doc for doc in os.listdir(RUTA_OUTPUT) if os.path.isfile(os.path.join(RUTA_OUTPUT, doc)) and doc.endswith('.txt')]
    
    # Crear un conjunto para rastrear documentos ya agrupados
    documentos_agrupados = set()
    grupo_contador = 1
    
    for doc1 in documentos:
        # Si el documento ya está agrupado, se omite
        if doc1 in documentos_agrupados:
            continue
        
        # Crear una lista para almacenar documentos similares a doc1
        grupo_documentos = [doc1]
        
        # Buscar documentos similares a doc1
        for doc2 in documentos:
            if doc1 != doc2 and doc2 not in documentos_agrupados:
                # Leer contenido de doc1 y doc2
                with open(os.path.join(RUTA_OUTPUT, doc1), 'r', encoding='utf-8') as f1:
                    doc1_texto = f1.read()
                with open(os.path.join(RUTA_OUTPUT, doc2), 'r', encoding='utf-8') as f2:
                    doc2_texto = f2.read()
                
                # Calcular similitudes
                similitudes = calcular_similitudes_sintacticas(doc1_texto, doc2_texto)
                
                # Si el documento cumple los umbrales, agregarlo al grupo
                if (similitudes['coseno'] > UMBRAL_SIMILITUD_COSENO and
                    similitudes['jaccard'] > UMBRAL_SIMILITUD_JACCARD and
                    similitudes['dice'] > UMBRAL_SIMILITUD_DICE):
                    grupo_documentos.append(doc2)
                    documentos_agrupados.add(doc2)
        
        # Crear una carpeta para el grupo en output y mover los documentos agrupados
        grupo_nombre = f"grupo_{grupo_contador}"
        ruta_grupo = os.path.join(RUTA_OUTPUT, grupo_nombre)
        os.makedirs(ruta_grupo, exist_ok=True)
        
        for doc in grupo_documentos:
            shutil.move(os.path.join(RUTA_OUTPUT, doc), os.path.join(ruta_grupo, doc))
            documentos_agrupados.add(doc)
        
        # Incrementar el contador de grupos
        grupo_contador += 1
