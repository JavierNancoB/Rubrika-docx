# main.py
from utils.file_manager import crear_carpetas, organizar_archivos
from utils.syntactic_analysis import analizar_sintactico
from utils.semantic_analysis import analizar_semantico

def main():
    crear_carpetas()        # Paso 1: Crear estructura de carpetas
    organizar_archivos()    # Paso 2: Mover archivos desde text/ a output/
    analizar_sintactico()   # Paso 3: Análisis sintáctico y organización
    #analizar_semantico()    # Paso 4: Análisis semántico en archivos unificados

if __name__ == '__main__':
    main()
