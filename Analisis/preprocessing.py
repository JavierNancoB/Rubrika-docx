import re
import string
from unidecode import unidecode
from docx import Document
from nltk.tokenize import WhitespaceTokenizer
from nltk.corpus import stopwords

def read_docx(file_path):
    """Lee un archivo DOCX y devuelve el texto por párrafos."""
    doc = Document(file_path)
    return [para.text for para in doc.paragraphs if para.text.strip()]

def clean_text(text):
    """Limpia el texto eliminando caracteres innecesarios como guiones bajos, números y saltos de línea."""
    text = unidecode(text.lower())  # Convierte a minúsculas y elimina acentos
    text = re.sub(r'\d+', '', text)  # Elimina todos los números
    text = re.sub(r'\n', ' ', text)  # Elimina saltos de línea
    text = text.translate(str.maketrans('', '', string.punctuation))  # Elimina puntuación
    text = re.sub(r'\s+', ' ', text)  # Sustituye múltiples espacios consecutivos por un solo espacio
    return text.strip()  # Elimina espacios en blanco al inicio y final

def preprocess_paragraph(paragraph):
    """Preprocesa un párrafo eliminando stopwords, normalizando y tokenizando."""
    stop_words = set(stopwords.words('spanish'))
    paragraph = clean_text(paragraph)
    tokenizer = WhitespaceTokenizer()
    words = tokenizer.tokenize(paragraph)
    return [word for word in words if word not in stop_words]
