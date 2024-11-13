import os
import re
import numpy as np
from scipy import stats

def leer_datos_carpeta(carpeta):
    datos = {
        'documentos': [],
        'total_palabras': [],
        'palabras_comunes': [],
        'similitud_coseno': [],
        'similitud_jaccard': [],
        'similitud_dice': [],
        'distancia_levenshtein': []
    }
    
    for archivo in os.listdir(carpeta):
        if archivo.endswith(".txt"):
            ruta_archivo = os.path.join(carpeta, archivo)
            with open(ruta_archivo, 'r', encoding='latin-1') as file:
                contenido = file.read()

                total_palabras = re.search(r"Total de palabras \(sin stopwords\): (\d+)", contenido)
                palabras_comunes = re.search(r"Cantidad de palabras repetidas: (\d+)", contenido)
                similitud_coseno = re.search(r"Similitud del Coseno: ([\d.]+)", contenido)
                similitud_jaccard = re.search(r"Similitud de Jaccard basada en bigramas: ([\d.]+)", contenido)
                similitud_dice = re.search(r"Similitud de Dice basada en bigramas: ([\d.]+)", contenido)
                distancia_levenshtein = re.search(r"Similitud de Levenshtein a nivel de palabra: (\d+)", contenido)

                datos['documentos'].append(archivo)
                datos['total_palabras'].append(int(total_palabras.group(1)) if total_palabras else 0)
                datos['palabras_comunes'].append(int(palabras_comunes.group(1)) if palabras_comunes else 0)
                datos['similitud_coseno'].append(float(similitud_coseno.group(1)) if similitud_coseno else 0.0)
                datos['similitud_jaccard'].append(float(similitud_jaccard.group(1)) if similitud_jaccard else 0.0)
                datos['similitud_dice'].append(float(similitud_dice.group(1)) if similitud_dice else 0.0)
                datos['distancia_levenshtein'].append(int(distancia_levenshtein.group(1)) if distancia_levenshtein else 0)
    
    return datos

def calcular_estadisticas(datos):
    estadisticas = {
        'promedio': np.mean(datos),
        'minimo': np.min(datos),
        'maximo': np.max(datos),
        'moda': stats.mode(datos, keepdims=False).mode,
        'percentil_01': np.percentile(datos, 1)
    }
    return estadisticas

def escribir_resultados(datos, ruta_salida):
    with open(ruta_salida, 'w', encoding='utf-8') as archivo:
        archivo.write("Análisis de Documentos\n=================================\n")
        for key in datos:
            if key != 'documentos':  # Evitar procesar la lista de nombres de documentos
                archivo.write(f"{key.capitalize()}:\n")
                estadisticas = calcular_estadisticas(np.array(datos[key], dtype=float))
                for stat_key, value in estadisticas.items():
                    archivo.write(f"{stat_key.capitalize()}: {value:.2f}\n")
                archivo.write("\n")

# Configuración de rutas
carpeta_textos = os.path.join(os.getcwd(), 'Analisis V2/Estadisticas/text')
ruta_salida = os.path.join(os.getcwd(), 'resultados.txt')

# Ejecutar funciones
datos = leer_datos_carpeta(carpeta_textos)
escribir_resultados(datos, ruta_salida)
