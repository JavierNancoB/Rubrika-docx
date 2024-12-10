import re
import string
from nltk.tokenize import WhitespaceTokenizer
from nltk.corpus import stopwords
from unidecode import unidecode
import nltk
nltk.download('stopwords')

def clean_text(text):
    """Limpia el texto eliminando caracteres innecesarios y preservando los saltos de línea."""
    text = unidecode(text.lower())  # Convierte a minúsculas y elimina acentos
    #text = re.sub(r'\d+', '', text)  # Elimina todos los números
    text = re.sub(r'\n+', '\n', text)  # Preserva saltos de línea
    text = text.translate(str.maketrans('', '', string.punctuation))  # Elimina puntuación
    text = re.sub(r'\s+', ' ', text)  # Sustituye múltiples espacios por uno solo
    return text.strip()  # Elimina espacios al inicio y final

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
