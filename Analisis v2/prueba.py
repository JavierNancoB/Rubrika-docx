from transformers import BertTokenizer, BertModel
import torch

# Inicializa el tokenizer y el modelo BERT
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

# Texto de ejemplo para codificar
text = "Hello, how are you doing today?"

# Tokeniza el texto
inputs = tokenizer(text, return_tensors="pt", max_length=512, truncation=True, padding='max_length')

# Genera embeddings utilizando BERT
with torch.no_grad():
    outputs = model(**inputs)

# Obtiene el embedding del token CLS, que es una buena representación general del estado de la secuencia
cls_embedding = outputs.last_hidden_state[:, 0, :]

print(cls_embedding)
