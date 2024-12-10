# utils/semantic_analysis.py
from transformers import BertTokenizer, BertModel
import torch
import numpy as np

def cargar_modelo_bert():
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertModel.from_pretrained('bert-base-uncased')
    return tokenizer, model

def obtener_embedding(texto, tokenizer, model):
    # Convierte el texto en un vector usando BERT
    inputs = tokenizer(texto, return_tensors='pt', truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state[:, 0, :].squeeze().numpy()

def calcular_similitud_coseno(embedding1, embedding2):
    # Calcula la similitud del coseno entre dos embeddings
    dot_product = np.dot(embedding1, embedding2)
    norm1 = np.linalg.norm(embedding1)
    norm2 = np.linalg.norm(embedding2)
    return dot_product / (norm1 * norm2)

def analizar_documentos(doc1_texto, doc2_texto):
    tokenizer, model = cargar_modelo_bert()
    
    # Convertir documentos en embeddings
    emb1 = obtener_embedding(doc1_texto, tokenizer, model)
    emb2 = obtener_embedding(doc2_texto, tokenizer, model)
    
    # Calcular similitud semántica
    similitud_semantica = calcular_similitud_coseno(emb1, emb2)
    
    return similitud_semantica
