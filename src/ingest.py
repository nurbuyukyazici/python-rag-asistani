import sqlite3
import json
from foundry_local_sdk import Configuration, FoundryLocalManager

# Foundry Local'i başlat
config = Configuration(app_name="rag_projesi")
FoundryLocalManager.initialize(config)
manager = FoundryLocalManager.instance

# Embedding modelini indir ve yükle
model = manager.catalog.get_model("qwen3-embedding-0.6b")
model.download(lambda p: print(f"\rİndiriliyor: {p:.0f}%", end="", flush=True))
print()
model.load()
print("Embedding modeli hazır.")

client = model.get_embedding_client()

# Şimdilik test için birkaç örnek cümle (sonra gerçek dökümanlarınla değiştireceğiz)
chunks = [
    "Foundry Local, yapay zeka modellerini internete bağlanmadan bilgisayarda çalıştırmayı sağlar.",
    "RAG, önce ilgili bilgiyi bulup sonra modele vererek daha doğru cevap üretme yöntemidir.",
    "SQLite, tek dosyadan oluşan basit ve sunucu gerektirmeyen bir veritabanıdır."
]

conn = sqlite3.connect("rag.db")
cursor = conn.cursor()

for chunk in chunks:
    response = client.generate_embedding(chunk)
    embedding = response.data[0].embedding
    cursor.execute(
        "INSERT INTO documents (content, embedding) VALUES (?, ?)",
        (chunk, json.dumps(embedding))
    )
    print(f"Kaydedildi: {chunk[:40]}...")

conn.commit()
conn.close()
model.unload()
print("Tüm örnek veriler veritabanına kaydedildi.")