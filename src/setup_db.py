import sqlite3

# Veritabanı dosyasını oluştur (yoksa yaratır)
conn = sqlite3.connect("rag.db")
cursor = conn.cursor()

# Dökümanları ve embedding'lerini tutacak tablo
cursor.execute("""
CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    embedding TEXT NOT NULL
)
""")

conn.commit()
conn.close()
print("Veritabanı ve tablo oluşturuldu: rag.db")