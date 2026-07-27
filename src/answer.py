import sqlite3
import json
import math
from foundry_local_sdk import Configuration, FoundryLocalManager
SIMILARITY_THRESHOLD = 0.5

config = Configuration(app_name="rag_projesi")
FoundryLocalManager.initialize(config)
manager = FoundryLocalManager.instance

# Embedding modeli (arama için)
embed_model = manager.catalog.get_model("qwen3-embedding-0.6b")
embed_model.load()
embed_client = embed_model.get_embedding_client()

# Chat modeli (cevap üretmek için)
chat_model = manager.catalog.get_model("qwen3-0.6b")
chat_model.load()
chat_client = chat_model.get_chat_client()

def cosine_similarity(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    return dot / (norm_a * norm_b)

def get_top_chunk(query, top_k=1):
    query_embedding = embed_client.generate_embedding(query).data[0].embedding
    conn = sqlite3.connect("rag.db")
    cursor = conn.cursor()
    cursor.execute("SELECT content, embedding FROM documents")
    rows = cursor.fetchall()
    conn.close()
    scored = []
    for content, embedding_json in rows:
        embedding = json.loads(embedding_json)
        score = cosine_similarity(query_embedding, embedding)
        scored.append((score, content))
    scored.sort(reverse=True)
    return [content for score, content in scored[:top_k]]

def answer_query(question):
  SIMILARITY_THRESHOLD = 0.5

def answer_query(question):
    # 1. Adım: ilgili bilgiyi bul (skorla birlikte)
    query_embedding = embed_client.generate_embedding(question).data[0].embedding
    conn = sqlite3.connect("rag.db")
    cursor = conn.cursor()
    cursor.execute("SELECT content, embedding FROM documents")
    rows = cursor.fetchall()
    conn.close()

    scored = []
    for content, embedding_json in rows:
        embedding = json.loads(embedding_json)
        score = cosine_similarity(query_embedding, embedding)
        scored.append((score, content))
    scored.sort(reverse=True)

    best_score, best_content = scored[0]
    print(f"  (en yüksek benzerlik skoru: {best_score:.3f})")

    # Eşik kontrolü: alakasız sorularda modele hiç sormadan cevap ver
    if best_score < SIMILARITY_THRESHOLD:
        return "Bu bilgiyi dökümanlarımda bulamadım."

    # 2. Adım: modele context + soruyu ver
    system_prompt = (
        "Sana verilen bağlam bilgisini kullanarak soruyu cevapla. "
        "Sadece bağlamdaki bilgiyi kullan, kendi bilgini ekleme. "
        "Kısa ve net cevap ver."
    )
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Bağlam:\n{best_content}\n\nSoru: {question}"}
    ]
    response = chat_client.complete_chat(messages)
    return response.choices[0].message.content

# Test
questions = [
    "Python'da listeler ve tuple'lar arasındaki fark nedir?",
    "GIL nedir ve neden önemlidir?",
    "Python'da virtual environment neden kullanılır?",
    "Python'da makarna nasıl yapılır?"  # dökümanda olmayan bir soru, kontrol için
]

for q in questions:
    print(f"\nSoru: {q}")
    print(f"Cevap: {answer_query(q)}")

embed_model.unload()
chat_model.unload()