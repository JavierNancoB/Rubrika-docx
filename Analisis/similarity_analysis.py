from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.optimize import linear_sum_assignment

def calculate_similarity_matrix(paragraphs1, paragraphs2):
    """Calcula la matriz de similitud de coseno entre los párrafos de dos documentos."""
    vectorizer = TfidfVectorizer()
    tfidf_matrix1 = vectorizer.fit_transform(paragraphs1)
    tfidf_matrix2 = vectorizer.transform(paragraphs2)
    similarity_matrix = cosine_similarity(tfidf_matrix1, tfidf_matrix2)
    return similarity_matrix

def find_optimal_matching(similarity_matrix, threshold=0.7):
    """Encuentra el emparejamiento óptimo entre párrafos usando un algoritmo de asignación con umbral de similitud."""
    row_ind, col_ind = linear_sum_assignment(-similarity_matrix)  # Maximiza similitud
    similar_paragraphs = 0
    unmatched_paragraphs = set(range(len(similarity_matrix)))

    for i, j in zip(row_ind, col_ind):
        if similarity_matrix[i, j] >= threshold:
            similar_paragraphs += 1
            unmatched_paragraphs.discard(i)
            unmatched_paragraphs.discard(j)

    total_matches = len(row_ind)
    return similar_paragraphs, len(unmatched_paragraphs)

def analyze_paragraphs(paragraphs1, paragraphs2, threshold=0.7):
    """Analiza y cuenta los párrafos similares y no correlacionados entre dos documentos."""
    similarity_matrix = calculate_similarity_matrix(paragraphs1, paragraphs2)
    similar_count, unmatched_count = find_optimal_matching(similarity_matrix, threshold=threshold)
    
    total_paragraphs = max(len(paragraphs1), len(paragraphs2))
    unmatched_in_doc1 = max(0, len(paragraphs1) - similar_count)
    unmatched_in_doc2 = max(0, len(paragraphs2) - similar_count)

    return {
        'similar_paragraphs': similar_count,
        'unmatched_doc1': unmatched_in_doc1,
        'unmatched_doc2': unmatched_in_doc2,
        'similarity_percentage': (similar_count / total_paragraphs) * 100
    }
