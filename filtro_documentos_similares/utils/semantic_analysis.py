# utils/semantic_analysis.py
from transformers import BertTokenizer, BertModel
import torch
import numpy as np
import os
import shutil
from config import RUTA_UNIFICADOS, RUTA_SEMANTICAMENTE_EQUIVALENTES

def cargar_modelo_bert():
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertModel.from_pretrained('bert-base-uncased')
    return tokenizer, model

def obtener_embedding(texto, tokenizer, model):
    inputs = tokenizer(texto, return_tensors='pt', truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state[:, 0, :].squeeze().numpy()

def calcular_similitud_coseno(embedding1, embedding2):
    dot_product = np.dot(embedding1, embedding2)
    norm1 = np.linalg.norm(embedding1)
    norm2 = np.linalg.norm(embedding2)
    return dot_product / (norm1 * norm2)

def mover_a_semanticamente_equivalentes(doc1, doc2):
    # Mueve los documentos semánticamente equivalentes a la subcarpeta correspondiente
    shutil.move(os.path.join(RUTA_UNIFICADOS, doc1), os.path.join(RUTA_SEMANTICAMENTE_EQUIVALENTES, doc1))
    shutil.move(os.path.join(RUTA_UNIFICADOS, doc2), os.path.join(RUTA_SEMANTICAMENTE_EQUIVALENTES, doc2))

def analizar_semantico():
    tokenizer, model = cargar_modelo_bert()
    documentos = os.listdir(RUTA_UNIFICADOS)
    
    for i, doc1 in enumerate(documentos):
        for doc2 in documentos[i + 1:]:
            with open(os.path.join(RUTA_UNIFICADOS, doc1), 'r', encoding='utf-8') as f1:
                doc1_texto = f1.read()
            with open(os.path.join(RUTA_UNIFICADOS, doc2), 'r', encoding='utf-8') as f2:
                doc2_texto = f2.read()
            
            emb1 = obtener_embedding(doc1_texto, tokenizer, model)
            emb2 = obtener_embedding(doc2_texto, tokenizer, model)
            similitud_semantica = calcular_similitud_coseno(emb1, emb2)
            
            # Si cumplen con el umbral de similitud semántica, se consideran equivalentes
            if similitud_semantica > 0.85:  # Umbral de ejemplo
                mover_a_semanticamente_equivalentes(doc1, doc2)
                print(f"Documentos {doc1} y {doc2} movidos a 'semanticamente_equivalentes/' (Similitud: {similitud_semantica:.2f})")
