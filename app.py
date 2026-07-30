from flask import Flask, render_template, request, jsonify
import sqlite3
import json
import math
import logging
from foundry_local_sdk import Configuration, FoundryLocalManager
import config

stats = {"total_questions": 0, "answered": 0, "not_found": 0}

logging.basicConfig(
    filename=config.LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    encoding="utf-8"
)

app = Flask(__name__)

print("Modeller yukleniyor, lutfen bekleyin...")
fl_config = Configuration(app_name="rag_projesi")
FoundryLocalManager.initialize(fl_config)
manager = FoundryLocalManager.instance

embed_model = manager.catalog.get_model(config.EMBEDDING_MODEL)
embed_model.download()
embed_model.load()
embed_client = embed_model.get_embedding_client()

print("Modeller hazir, sunucu basliyor...")


def cosine_similarity(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    return dot / (norm_a * norm_b)


def answer_query(question, history):
    recent_history = history[-config.HISTORY_LENGTH:] if history else []
    expanded_query = " ".join(recent_history + [question])

    query_embedding = embed_client.generate_embedding(expanded_query).data[0].embedding
    conn = sqlite3.connect(config.DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT content, embedding FROM documents")
    rows = cursor.fetchall()
    conn.close()

    question_words = set(w.lower() for w in expanded_query.split() if len(w) > 2)

    scored = []
    for content, embedding_json in rows:
        embedding = json.loads(embedding_json)
        score = cosine_similarity(query_embedding, embedding)
        content_lower = content.lower()
        keyword_matches = sum(1 for w in question_words if w in content_lower)
        score += keyword_matches * config.KEYWORD_BONUS_WEIGHT
        scored.append((score, content))

    scored.sort(reverse=True)
    best_score = scored[0][0]

    stats["total_questions"] += 1

    if best_score < config.SIMILARITY_THRESHOLD:
        stats["not_found"] += 1
        logging.info(f"SORU: {question} | SKOR: {best_score:.3f} | SONUC: BULUNAMADI")
        return "Bu bilgiyi dokumanlarimda bulamadim.", best_score, None

    context = scored[0][1]
    first_sentence = context.split(".")[0].strip()
    if len(first_sentence) > 60:
        first_sentence = first_sentence[:60].strip() + "..."
    source_label = first_sentence.replace("**", "")

    stats["answered"] += 1
    logging.info(f"SORU: {question} | SKOR: {best_score:.3f} | KAYNAK: {source_label}")
    return context, best_score, source_label


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    question = data.get("message", "").strip()
    history = data.get("history", [])

    if not question:
        return jsonify({"answer": "Lutfen bir soru yaz.", "score": 0})

    answer, score, source = answer_query(question, history)
    return jsonify({"answer": answer, "score": round(score, 3), "source": source})


@app.route("/stats")
def get_stats():
    return jsonify(stats)
@app.route("/health")
def health_check():
    try:
        test_embedding = embed_client.generate_embedding("test").data[0].embedding
        embedding_ok = len(test_embedding) > 0
    except Exception:
        embedding_ok = False

    conn = sqlite3.connect(config.DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM documents")
    doc_count = cursor.fetchone()[0]
    conn.close()

    status = "healthy" if embedding_ok and doc_count > 0 else "unhealthy"

    return jsonify({
        "status": status,
        "embedding_model_ok": embedding_ok,
        "documents_in_db": doc_count
    })


if __name__ == "__main__":
    app.run(debug=config.FLASK_DEBUG, port=config.FLASK_PORT)