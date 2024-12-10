import re
import string
from nltk.tokenize import WhitespaceTokenizer
from nltk.corpus import stopwords
from unidecode import unidecode
import nltk
nltk.download('stopwords')

'''
def clean_text(text):
    """Limpia el texto eliminando caracteres innecesarios y preservando los saltos de línea."""
    text = unidecode(text.lower())  # Convierte a minúsculas y elimina acentos
    #text = re.sub(r'\d+', '', text)  # Elimina todos los números
    text = re.sub(r'\n+', '\n', text)  # Preserva saltos de línea
    text = text.translate(str.maketrans('', '', string.punctuation))  # Elimina puntuación
    text = re.sub(r'\s+', ' ', text)  # Sustituye múltiples espacios por uno solo
    return text.strip()  # Elimina espacios al inicio y final
'''

def clean_text(text):
    """Limpia el texto eliminando caracteres innecesarios y preservando los saltos de línea."""
    # 1. Convertir a minúsculas y eliminar acentos
    text = unidecode(text.lower())
    
    # 2. Unificar saltos de línea: múltiples \n seguidos se convierten en uno solo
    text = re.sub(r'\n+', '\n', text)
    
    # 3. Unificar múltiples puntos consecutivos en un solo punto
    text = re.sub(r'\.{2,}', '.', text)
    
    # 4. Eliminar puntuación
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # 5. Reemplazar múltiples espacios por uno solo, sin eliminar saltos de línea
    #    Usamos [ \t]+ para no afectar los saltos de línea \n
    text = re.sub(r'[ \t]+', ' ', text)
    
    # 6. Eliminar espacios al inicio y final de cada línea
    lines = text.split('\n')
    lines = [line.strip() for line in lines]
    text = '\n'.join(lines)
    
    # 7. Quitar espacios en blanco innecesarios al inicio y final del texto completo (no afecta a los saltos de línea internos)
    return text.strip()

'''
ENCONTRAR MULTIPLES PUNTOS DEJAR UNO SOLO
PUNTOS
MINUSCULAS
ACENTOS
ESPACIOS ENTREMEDIO, ANTES Y AL INICIO
SALTOS DE LINEA
comillas
guiones largos
caracteres no deseados
'''


def preprocess(text):
    stop_words = set(stopwords.words('spanish'))
    text = clean_text(text)
    tokenizer = WhitespaceTokenizer()
    words = tokenizer.tokenize(text)
    return [word for word in words if word not in stop_words and word.strip()]

def generate_ngrams(text, n=2):
    return set(zip(*[text[i:] for i in range(n)]))
