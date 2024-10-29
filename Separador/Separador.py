import os
import re
import shutil
from difflib import SequenceMatcher
from docx import Document

# Función para limpiar texto
def limpiar_texto(texto):
    texto = re.sub(r'[_\s]+', ' ', texto)  # Reemplaza guiones bajos y múltiples espacios por un solo espacio
    return texto.strip().lower()  # Elimina espacios al inicio/final y convierte todo a minúsculas

# Función para calcular la similitud sintáctica
def calcular_similitud(texto1, texto2):
    return SequenceMatcher(None, texto1, texto2).ratio() * 100  # Retorna porcentaje de similitud

# Función para leer el contenido de un archivo Word
def leer_archivo_word(ruta_archivo):
    doc = Document(ruta_archivo)
    contenido = "\n".join([p.text for p in doc.paragraphs])  # Extrae texto de cada párrafo
    return limpiar_texto(contenido)  # Limpia el texto

# Definir carpetas relativas
carpeta_original = os.path.join(os.path.dirname(__file__), 'Documentos del Cliente')  # Carpeta con documentos para analizar
carpeta_resultado = os.path.join(os.path.dirname(__file__), 'Documentos_Similares')  # Carpeta para guardar resultados

# Crear carpeta de resultados
if not os.path.exists(carpeta_resultado):
    os.makedirs(carpeta_resultado)

# Leer y procesar cada archivo en la carpeta inicial
archivos = [f for f in os.listdir(carpeta_original) if f.endswith('.docx')]
documentos = {archivo: leer_archivo_word(os.path.join(carpeta_original, archivo)) for archivo in archivos}

# Lista para guardar archivos ya agrupados
archivos_agrupados = set()

# Agrupar documentos similares en una sola carpeta por grupo
for archivo_base, contenido_base in documentos.items():
    if archivo_base in archivos_agrupados:
        continue  # Saltar si el archivo ya está agrupado

    grupo_similares = [archivo_base]  # Iniciar el grupo con el archivo base

    for archivo_comparado, contenido_comparado in documentos.items():
        if archivo_base != archivo_comparado and archivo_comparado not in archivos_agrupados:
            similitud = calcular_similitud(contenido_base, contenido_comparado)
            
            if similitud >= 97.5:  # Si la similitud es del 97% o más, añadir al grupo
                grupo_similares.append(archivo_comparado)
                archivos_agrupados.add(archivo_comparado)  # Marcar como agrupado

    # Crear una carpeta para el grupo si tiene más de un archivo
    if len(grupo_similares) > 1:
        nombre_grupo = f"Grupo_{archivo_base.split('.')[0]}"
        carpeta_grupo = os.path.join(carpeta_resultado, nombre_grupo)
        os.makedirs(carpeta_grupo, exist_ok=True)

        # Copiar archivos del grupo a la carpeta de grupo
        for archivo in grupo_similares:
            ruta_origen = os.path.join(carpeta_original, archivo)
            ruta_destino = os.path.join(carpeta_grupo, archivo)
            shutil.copy2(ruta_origen, ruta_destino)

        # Marcar archivo base como agrupado
        archivos_agrupados.add(archivo_base)

print("Comparación completada. Los documentos similares se han organizado en grupos en la carpeta:", carpeta_resultado)
