import sqlite3
import json
import math
from foundry_local_sdk import Configuration, FoundryLocalManager

config = Configuration(app_name="rag_projesi")
FoundryLocalManager.initialize(config)
manager = FoundryLocalManager.instance

embed_model = manager.catalog.get_model("qwen3-embedding-0.6b")
embed_model.load()
embed_client = embed_model.get_embedding_client()

def cosine_similarity(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    return dot / (norm_a * norm_b)

conn = sqlite3.connect("rag.db")
cursor = conn.cursor()
cursor.execute("SELECT content, embedding FROM documents")
rows = cursor.fetchall()
conn.close()

print(f"TOPLAM KAYIT SAYISI: {len(rows)}")
print("=" * 60)

question = "GIL nedir?"
query_embedding = embed_client.generate_embedding(question).data[0].embedding

for content, embedding_json in rows:
    embedding = json.loads(embedding_json)
    score = cosine_similarity(query_embedding, embedding)
    print(f"Skor: {score:.3f} -> {content[:60]}...")

embed_model.unload()