import os  # Para interactuar con el sistema operativo
from docx import Document  # Para leer archivos DOCX
from sklearn.feature_extraction.text import TfidfVectorizer  # Para vectorización TF-IDF
from sklearn.metrics.pairwise import cosine_similarity  # Para calcular similitud del coseno
from nltk.tokenize import WhitespaceTokenizer  # Tokenizador que no depende de punkt
from nltk.corpus import stopwords  # Colección de stopwords en español
from collections import Counter  # Para contar frecuencia de palabras
from datetime import datetime  # Para obtener la fecha y hora actual
import re  # Librería para expresiones regulares
import string  # Para manipulación de cadenas
from unidecode import unidecode  # Para eliminar acentos
from scipy.optimize import linear_sum_assignment  # Para el emparejamiento óptimo

# Descarga de datos necesarios de NLTK
import nltk
nltk.download('stopwords')

def read_docx(file_path):
    """Lee un archivo DOCX y devuelve el texto."""
    doc = Document(file_path)
    return " ".join([para.text for para in doc.paragraphs])

def clean_text(text):
    """Limpia el texto eliminando caracteres innecesarios como guiones bajos, números y saltos de línea."""
    text = unidecode(text.lower())  # Convierte a minúsculas y elimina acentos
    text = re.sub(r'\d+', '', text)  # Elimina todos los números
    text = re.sub(r'\n', ' ', text)  # Elimina saltos de línea
    text = text.translate(str.maketrans('', '', string.punctuation))  # Elimina puntuación
    text = re.sub(r'\s+', ' ', text)  # Sustituye múltiples espacios consecutivos por un solo espacio
    return text.strip()  # Elimina espacios en blanco al inicio y final

def preprocess(text):
    """Preprocesa el texto: elimina stopwords, normaliza y tokeniza usando WhitespaceTokenizer."""
    stop_words = set(stopwords.words('spanish'))
    text = clean_text(text)  # Limpia el texto
    tokenizer = WhitespaceTokenizer()  # Utiliza WhitespaceTokenizer para dividir en palabras
    words = tokenizer.tokenize(text)
    filtered_words = [word for word in words if word not in stop_words and word.strip()]  # Elimina stopwords
    return filtered_words

def generate_ngrams(text, n=2):
    """Genera n-gramas a partir de una lista de palabras."""
    return set(zip(*[text[i:] for i in range(n)]))

def extract_sections(text):
    """Divide el texto en secciones identificables. En este ejemplo, lo hacemos por líneas que comienzan con palabras clave como 'Artículo' o 'Cláusula'."""
    sections = {}
    lines = text.splitlines()
    current_section = ""
    for line in lines:
        line = line.strip()
        if line.startswith(("Artículo", "Cláusula", "Sección")):  # Ajusta según el documento
            current_section = line
            sections[current_section] = ""
        elif current_section:
            sections[current_section] += " " + line
    return sections

def calculate_similarity_matrix(sections1, sections2):
    """Calcula una matriz de similitud de coseno entre todas las secciones de dos documentos."""
    vectorizer = TfidfVectorizer()
    sec_texts1 = [text for text in sections1.values() if text.strip()]  # Filtra secciones vacías
    sec_texts2 = [text for text in sections2.values() if text.strip()]  # Filtra secciones vacías
    
    # Verifica que haya secciones válidas para evitar una matriz vacía
    if not sec_texts1 or not sec_texts2:
        return []

    # Calcula las matrices TF-IDF y la matriz de similitud de coseno
    tfidf_matrix1 = vectorizer.fit_transform(sec_texts1)
    tfidf_matrix2 = vectorizer.transform(sec_texts2)
    similarity_matrix = cosine_similarity(tfidf_matrix1, tfidf_matrix2)
    return similarity_matrix

def find_optimal_matching(similarity_matrix, threshold=0.9):
    """Encuentra el emparejamiento óptimo entre secciones usando un algoritmo de asignación."""
    if not similarity_matrix:  # Si la matriz de similitud está vacía, no hay emparejamientos posibles
        return 0, 0

    row_ind, col_ind = linear_sum_assignment(-similarity_matrix)  # Maximiza similitud
    similar_sections_count = sum(1 for i, j in zip(row_ind, col_ind) if similarity_matrix[i, j] >= threshold)
    total_matches = len(row_ind)  # Total de emparejamientos posibles

    return similar_sections_count, total_matches

# Rutas relativas
current_dir = os.path.dirname(__file__)
docs_dir = os.path.join(current_dir, "Documentos del Cliente")
output_dir = os.path.join(current_dir, "resultados")

# Crear directorio de resultados si no existe
os.makedirs(output_dir, exist_ok=True)

# Cargar documentos
files = [f for f in os.listdir(docs_dir) if f.endswith('.docx')]
documents = [read_docx(os.path.join(docs_dir, file)) for file in files]

# Preprocesamiento de documentos y extracción de secciones
processed_docs = [preprocess(doc) for doc in documents]
sectioned_docs = [extract_sections(doc) for doc in documents]

# Vectorización TF-IDF y cálculo de similitud del coseno
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform([' '.join(doc) for doc in processed_docs])
cosine_similarities = cosine_similarity(tfidf_matrix)

# Timestamp para el nombre del archivo
timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
result_file_path = os.path.join(output_dir, f"resultados_analisis_{timestamp}.txt")

# Creación de archivo de resultados
with open(result_file_path, 'w') as file:
    file.write("Análisis de Documentos\n")
    file.write("=================================\n")
    for i, file_name in enumerate(files):
        file.write(f"Documento: {file_name}\n")
        file.write(f"Total de palabras (sin stopwords): {len(processed_docs[i])}\n")
        file.write(f"Frecuencia de palabras: {Counter(processed_docs[i])}\n")

        # Similaridad del Coseno
        file.write("Similitud del Coseno con otros documentos:\n")
        for j, other_file in enumerate(files):
            if i != j:
                file.write(f"    Con {other_file}: {cosine_similarities[i][j]:.4f}\n")
        
        # Similaridad de Jaccard basada en n-gramas
        file.write("Similitud de Jaccard basada en bigramas:\n")
        ngrams_doc1 = generate_ngrams(processed_docs[i], n=2)
        for j, other_file in enumerate(files):
            if i != j:
                ngrams_doc2 = generate_ngrams(processed_docs[j], n=2)
                intersection = ngrams_doc1.intersection(ngrams_doc2)
                union = ngrams_doc1.union(ngrams_doc2)
                jaccard_similarity = len(intersection) / len(union) if union else 0
                file.write(f"    Con {other_file}: {jaccard_similarity:.4f}\n")
        
        # Análisis de Secciones
        file.write("Análisis de secciones:\n")
        for j, other_file in enumerate(files):
            if i != j:
                similarity_matrix = calculate_similarity_matrix(sectioned_docs[i], sectioned_docs[j])
                similar_sections, total_matches = find_optimal_matching(similarity_matrix)
                if total_matches > 0:
                    percentage_similar = (similar_sections / total_matches) * 100
                else:
                    percentage_similar = 0  # O un valor indicativo de que no hubo coincidencias
                file.write(f"    Secciones similares con {other_file}: {similar_sections}/{total_matches} ({percentage_similar:.2f}%)\n")
        
        file.write("\n")

print(f"Análisis completado y guardado en '{result_file_path}'.")
