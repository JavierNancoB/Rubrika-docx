from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calcular_similitudes_sintacticas(doc1_texto, doc2_texto):
    vectorizer = CountVectorizer().fit_transform([doc1_texto, doc2_texto])
    vectors = vectorizer.toarray()
    coseno = cosine_similarity([vectors[0]], [vectors[1]])[0][0]
    set1, set2 = set(doc1_texto.split()), set(doc2_texto.split())
    jaccard = len(set1 & set2) / len(set1 | set2)
    dice = 2 * len(set1 & set2) / (len(set1) + len(set2))

    return {'coseno': coseno, 'jaccard': jaccard, 'dice': dice}
