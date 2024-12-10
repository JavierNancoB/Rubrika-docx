# config.py
import os

# Directorios principales
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RUTA_DOCUMENTOS = os.path.join(BASE_DIR, 'Documentos_del_cliente')
RUTA_OUTPUT = os.path.join(BASE_DIR, 'output')

# Parámetros del análisis semántico
UMBRAL_SIMILITUD_SEMANTICA = 0.85  # Ejemplo de umbral de similitud semántica
