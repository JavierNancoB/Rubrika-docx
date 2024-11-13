from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from text_cleaner import preprocess  # Importar preprocess
import re

# Función para extraer y comparar cláusulas clave en los documentos
def extract_clauses(doc):
    # Buscar puntos y subcláusulas (por ejemplo, cláusulas que contienen un punto D o E)
    clauses = {}
    
    # Extraer texto alrededor de posibles subcláusulas usando expresiones regulares
    pattern = re.compile(r'([A-Za-z\s]*\s*PUNTO\s+[A-D])[:.\n]?.*?(?=PUNTO\s+[A-D]|$)', re.IGNORECASE)
    matches = pattern.findall(doc)
    
    for match in matches:
        # Extraer el punto y el contenido
        point = match[0].strip()
        content = match[1].strip()
        clauses[point] = content
    
    return clauses

# Función para comparar las cláusulas entre dos documentos
def compare_clauses(doc1, doc2):
    clauses1 = extract_clauses(doc1)
    clauses2 = extract_clauses(doc2)

    differences = {}
    for point, content1 in clauses1.items():
        content2 = clauses2.get(point)
        if content2 is None:
            differences[point] = (content1, "No existe en el segundo documento")
        elif content1 != content2:
            differences[point] = (content1, content2)

    for point, content2 in clauses2.items():
        if point not in clauses1:
            differences[point] = ("No existe en el primer documento", content2)

    return differences

def preprocess_placeholders(doc):
    # Reemplazar nombres
    doc = re.sub(r'\b[DN][OAON]+\b', '[NOMBRE_REPRESENTANTE]', doc)
    # Reemplazar RUT
    doc = re.sub(r'\b\d{1,2}\.\d{3}\.\d{3}-[0-9K]\b', '[RUT]', doc)
    # Reemplazar fecha
    doc = re.sub(r'\b\d{1,2}/\d{1,2}/\d{4}\b', '[FECHA]', doc)
    # Reemplazar direcciones
    doc = re.sub(r'Isidora Goyenechea.*?,', '[DIRECCION_EMPRESA]', doc)
    return doc

def calculate_similarity(para1, para2):
    # Limpia y calcula similitud entre dos párrafos
    clean_para1 = preprocess(para1)
    clean_para2 = preprocess(para2)

    # Si deseas usar TF-IDF para la similitud
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([' '.join(clean_para1), ' '.join(clean_para2)])
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    return similarity[0][0]  # Regresa la similitud

def analyze_paragraphs(doc1, doc2):
    paragraphs1 = doc1.split('\n')  # Divide el documento en párrafos usando saltos de línea
    paragraphs2 = doc2.split('\n')
    total_paragraphs1 = len(paragraphs1)
    total_paragraphs2 = len(paragraphs2)
    similar_paragraphs = sum(1 for p1 in paragraphs1 if p1 in paragraphs2)  # Compara si el párrafo está en el otro documento.
    return similar_paragraphs, total_paragraphs1, total_paragraphs2

def word_level_levenshtein(words1, words2):
    # Crear una matriz de tamaño (len(words1)+1) x (len(words2)+1)
    d = [[0 for _ in range(len(words2) + 1)] for _ in range(len(words1) + 1)]
    for i in range(len(words1) + 1):
        d[i][0] = i
    for j in range(len(words2) + 1):
        d[0][j] = j
    for i in range(1, len(words1) + 1):
        for j in range(1, len(words2) + 1):
            if words1[i - 1] == words2[j - 1]:
                cost = 0
            else:
                cost = 1
            d[i][j] = min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + cost)
    return d[-1][-1]

def dice_similarity(set1, set2):
    if not set1 or not set2:
        return 0.0
    return 2 * len(set1.intersection(set2)) / (len(set1) + len(set2))

# Función para contar la cantidad de párrafos en un documento antes de normalizar
# Función para contar la cantidad de párrafos en un documento antes de normalizar
def count_paragraphs(doc):
    # Normalizar saltos de línea y retornos de carro
    doc = doc.replace('\r\n', '\n').replace('\r', '\n')
    # Divide el documento en líneas
    lines = doc.split('\n')
    paragraphs = []
    current_paragraph = []

    for line in lines:
        # Si la línea no está vacía, agrégala al párrafo actual
        if line.strip():
            current_paragraph.append(line.strip())
        # Si la línea está vacía y hay contenido en el párrafo actual, finaliza el párrafo
        elif current_paragraph:
            paragraphs.append(" ".join(current_paragraph))
            current_paragraph = []

    # Agrega el último párrafo si existe
    if current_paragraph:
        paragraphs.append(" ".join(current_paragraph))

    return len(paragraphs)

