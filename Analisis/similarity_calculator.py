from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.optimize import linear_sum_assignment

def calculate_similarity_matrix(sections1, sections2):
    vectorizer = TfidfVectorizer()
    sec_texts1 = [text for text in sections1.values() if text.strip()]
    sec_texts2 = [text for text in sections2.values() if text.strip()]
    if not sec_texts1 or not sec_texts2:
        return []
    tfidf_matrix1 = vectorizer.fit_transform(sec_texts1)
    tfidf_matrix2 = vectorizer.transform(sec_texts2)
    return cosine_similarity(tfidf_matrix1, tfidf_matrix2)

def find_optimal_matching(similarity_matrix, threshold=0.9):
    if not similarity_matrix:
        return 0, 0
    row_ind, col_ind = linear_sum_assignment(-similarity_matrix)
    similar_sections_count = sum(1 for i, j in zip(row_ind, col_ind) if similarity_matrix[i, j] >= threshold)
    total_matches = len(row_ind)
    return similar_sections_count, total_matches
