# config.py
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Rutas
RUTA_TEXTOS = os.path.join(BASE_DIR, 'text')
RUTA_OUTPUT = os.path.join(BASE_DIR, 'output')
RUTA_UNIFICADOS = os.path.join(RUTA_OUTPUT, 'unificados')
RUTA_SEMANTICAMENTE_EQUIVALENTES = os.path.join(RUTA_UNIFICADOS, 'semanticamente_equivalentes')
RUTA_RESULTADOS = os.path.join(BASE_DIR, 'results')

# Umbrales de similitud
UMBRAL_SIMILITUD_COSENO = 0.99
UMBRAL_SIMILITUD_JACCARD = 0.93
UMBRAL_SIMILITUD_DICE = 0.96
