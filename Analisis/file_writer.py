from functions import word_level_levenshtein, dice_similarity, compare_clauses, count_paragraphs
from text_cleaner import generate_ngrams
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def write_all_results(file_path, files, processed_docs, raw_docs):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([' '.join(doc) for doc in processed_docs])
    cosine_similarities = cosine_similarity(tfidf_matrix)

    with open(file_path, 'w') as file:
        file.write("Análisis de Documentos\n")
        file.write("=================================\n")
        for i, file_name in enumerate(files):
            file.write(f"Documento: {file_name}\n")
            file.write(f"Total de palabras (sin stopwords): {len(processed_docs[i])}\n\n")

            # Contar la cantidad de párrafos en el documento original antes de normalizar
            original_paragraph_count = count_paragraphs(raw_docs[i])
            file.write(f"Cantidad de párrafos (antes de normalizar): {original_paragraph_count}\n\n")

        for i in range(len(files)):
            for j in range(i + 1, len(files)):
                file_name_i = files[i]
                file_name_j = files[j]
                file.write(f"Comparaciones entre {file_name_i} y {file_name_j}\n")
                
                # Similitud en n-gramas y otras métricas de similitud
                ngrams_doc1 = generate_ngrams(processed_docs[i], n=2)
                ngrams_doc2 = generate_ngrams(processed_docs[j], n=2)
                intersection = ngrams_doc1.intersection(ngrams_doc2)
                union = ngrams_doc1.union(ngrams_doc2)
                common_words_count = len(intersection)
                file.write(f"Cantidad de palabras repetidas: {common_words_count} palabras en común\n")
                file.write(f"Similitud del Coseno: {cosine_similarities[i][j]:.4f}\n")
                jaccard_similarity = len(intersection) / len(union) if union else 0
                file.write(f"Similitud de Jaccard basada en bigramas: {jaccard_similarity:.4f}\n")
                dice_similarity_score = dice_similarity(ngrams_doc1, ngrams_doc2)
                file.write(f"Similitud de Dice basada en bigramas: {dice_similarity_score:.4f}\n")
                lev_similarity = word_level_levenshtein(processed_docs[i], processed_docs[j])
                file.write(f"Similitud de Levenshtein a nivel de palabra: {lev_similarity} ediciones\n")

                # Comparación de cláusulas específicas
                doc1_text = " ".join(processed_docs[i])
                doc2_text = " ".join(processed_docs[j])
                clause_differences = compare_clauses(doc1_text, doc2_text)
                if clause_differences:
                    file.write("Diferencias específicas en cláusulas:\n")
                    for clause, diff in clause_differences.items():
                        file.write(f"  {clause}:\n")
                        file.write(f"    Documento 1: {diff[0]}\n")
                        file.write(f"    Documento 2: {diff[1]}\n")
                else:
                    file.write("No se encontraron diferencias específicas en las cláusulas.\n")

                file.write("\n")
