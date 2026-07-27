import sqlite3
import json
import math
from foundry_local_sdk import Configuration, FoundryLocalManager

config = Configuration(app_name="rag_projesi")
FoundryLocalManager.initialize(config)
manager = FoundryLocalManager.instance

model = manager.catalog.get_model("qwen3-embedding-0.6b")
model.load()
client = model.get_embedding_client()

def cosine_similarity(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    return dot / (norm_a * norm_b)

def get_top_chunk(query, top_k=1):
    # Soruyu embedding'e çevir
    query_embedding = client.generate_embedding(query).data[0].embedding

    # Veritabanındaki tüm kayıtları çek
    conn = sqlite3.connect("rag.db")
    cursor = conn.cursor()
    cursor.execute("SELECT content, embedding FROM documents")
    rows = cursor.fetchall()
    conn.close()

    # Her kayıt için benzerlik hesapla
    scored = []
    for content, embedding_json in rows:
        embedding = json.loads(embedding_json)
        score = cosine_similarity(query_embedding, embedding)
        scored.append((score, content))

    # En yüksek benzerlikten düşüğe sırala
    scored.sort(reverse=True)
    return scored[:top_k]

# Test sorusu
query = "SQLite nedir?"
results = get_top_chunk(query, top_k=1)

print(f"Soru: {query}")
for score, content in results:
    print(f"Benzerlik: {score:.3f} -> {content}")

model.unload()