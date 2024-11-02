from collections import Counter
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from text_cleaner import generate_ngrams, preprocess  # Importar preprocess

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

    # Aquí se deben definir cómo comparar los párrafos. Este es solo un ejemplo.
    similar_paragraphs = sum(1 for p1 in paragraphs1 if p1 in paragraphs2)  # Compara si el párrafo está en el otro documento.

    return similar_paragraphs, total_paragraphs1, total_paragraphs2

def word_level_levenshtein(words1, words2):
    # Crear una matriz de tamaño (len(words1)+1) x (len(words2)+1)
    d = [[0 for _ in range(len(words2) + 1)] for _ in range(len(words1) + 1)]

    # Llenar la primera columna y la primera fila de la matriz
    for i in range(len(words1) + 1):
        d[i][0] = i
    for j in range(len(words2) + 1):
        d[0][j] = j

    # Recorrer la matriz llenando según la distancia mínima
    for i in range(1, len(words1) + 1):
        for j in range(1, len(words2) + 1):
            if words1[i - 1] == words2[j - 1]:
                cost = 0
            else:
                cost = 1
            d[i][j] = min(d[i - 1][j] + 1,   # eliminación
                          d[i][j - 1] + 1,   # inserción
                          d[i - 1][j - 1] + cost)  # sustitución

    return d[-1][-1]

def calculate_paragraph_similarity(para1, para2):
    """Calcula la similitud entre dos párrafos."""
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([para1, para2])
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    return similarity[0][0]  # Devuelve la similitud


def write_all_results(file_path, files, processed_docs):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([' '.join(doc) for doc in processed_docs])
    cosine_similarities = cosine_similarity(tfidf_matrix)

    with open(file_path, 'w') as file:
        file.write("Análisis de Documentos\n")
        file.write("=================================\n")

        # Primero escribimos los totales de palabras
        for i, file_name in enumerate(files):
            file.write(f"Documento: {file_name}\n")
            file.write(f"Total de palabras (sin stopwords): {len(processed_docs[i])}\n\n")

        # Escribir comparaciones evitando duplicados
        for i in range(len(files)):
            for j in range(i + 1, len(files)):  # Solo comparamos con los documentos siguientes
                file_name_i = files[i]
                file_name_j = files[j]
                file.write(f"Comparaciones entre {file_name_i} y {file_name_j}\n")

                # Cantidad de palabras repetidas
                words_in_doc_i = set(processed_docs[i])
                words_in_doc_j = set(processed_docs[j])
                common_words_count = len(words_in_doc_i.intersection(words_in_doc_j))
                file.write(f"Cantidad de palabras repetidas: {common_words_count} palabras en común\n")

                # Similaridad del Coseno
                file.write(f"Similitud del Coseno: {cosine_similarities[i][j]:.4f}\n")

                # Similaridad de Jaccard basada en bigramas
                ngrams_doc1 = generate_ngrams(processed_docs[i], n=2)
                ngrams_doc2 = generate_ngrams(processed_docs[j], n=2)
                intersection = ngrams_doc1.intersection(ngrams_doc2)
                union = ngrams_doc1.union(ngrams_doc2)
                jaccard_similarity = len(intersection) / len(union) if union else 0
                file.write(f"Similitud de Jaccard basada en bigramas: {jaccard_similarity:.4f}\n")

                # Similaridad de Levenshtein a nivel de palabra
                lev_similarity = word_level_levenshtein(processed_docs[i], processed_docs[j])
                file.write(f"Similitud de Levenshtein a nivel de palabra: {lev_similarity} ediciones\n")

                file.write("\n")


