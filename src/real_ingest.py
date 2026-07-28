import sqlite3
import json
from foundry_local_sdk import Configuration, FoundryLocalManager

config = Configuration(app_name="rag_projesi")
FoundryLocalManager.initialize(config)
manager = FoundryLocalManager.instance

model = manager.catalog.get_model("qwen3-embedding-0.6b")
model.load()
client = model.get_embedding_client()

# Dosyayı oku ve paragraflara böl (boş satırla ayrılmış her paragraf bir "chunk")
with open("data/dokumanlar.txt", "r", encoding="utf-8") as f:
    text = f.read()

chunks = [p.strip() for p in text.split("\n\n") if p.strip()]
print(f"{len(chunks)} paragraf bulundu.")

conn = sqlite3.connect("data/rag.db")
cursor = conn.cursor()

# Önceki test verilerini temizle
cursor.execute("DELETE FROM documents")

for i, chunk in enumerate(chunks):
    response = client.generate_embedding(chunk)
    embedding = response.data[0].embedding
    cursor.execute(
        "INSERT INTO documents (content, embedding) VALUES (?, ?)",
        (chunk, json.dumps(embedding))
    )
    print(f"[{i+1}/{len(chunks)}] Kaydedildi: {chunk[:50]}...")

conn.commit()
conn.close()
model.unload()
print("Gerçek dökümanlar veritabanına kaydedildi.")