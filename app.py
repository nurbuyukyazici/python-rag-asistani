from flask import Flask, render_template, request, jsonify
import sqlite3
import json
import math
from foundry_local_sdk import Configuration, FoundryLocalManager

SIMILARITY_THRESHOLD = 0.30

app = Flask(__name__)

print("Modeller yukleniyor, lutfen bekleyin...")
config = Configuration(app_name="rag_projesi")
FoundryLocalManager.initialize(config)
manager = FoundryLocalManager.instance

embed_model = manager.catalog.get_model("qwen3-embedding-0.6b")
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
    recent_history = history[-2:] if history else []
    expanded_query = " ".join(recent_history + [question])

    query_embedding = embed_client.generate_embedding(expanded_query).data[0].embedding
    conn = sqlite3.connect("data/rag.db")
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
        score += keyword_matches * 0.15
        scored.append((score, content))

    scored.sort(reverse=True)
    best_score = scored[0][0]

    if best_score < SIMILARITY_THRESHOLD:
        return "Bu bilgiyi dokumanlarimda bulamadim.", best_score, None

    context = scored[0][1]
    first_sentence = context.split(".")[0].strip()
    if len(first_sentence) > 60:
        first_sentence = first_sentence[:60].strip() + "..."
    source_label = first_sentence.replace("**", "")

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


if __name__ == "__main__":
    app.run(debug=False, port=5000)