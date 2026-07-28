import math


def cosine_similarity(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    return dot / (norm_a * norm_b)


def keyword_bonus(question, content, bonus_per_word=0.15):
    question_words = set(w.lower() for w in question.split() if len(w) > 2)
    content_lower = content.lower()
    matches = sum(1 for w in question_words if w in content_lower)
    return matches * bonus_per_word


def should_answer(score, threshold=0.30):
    return score >= threshold