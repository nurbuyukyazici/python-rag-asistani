import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from rag_logic import cosine_similarity, keyword_bonus, should_answer


def test_cosine_similarity_identical_vectors():
    a = [1, 0, 0]
    b = [1, 0, 0]
    assert cosine_similarity(a, b) == 1.0


def test_cosine_similarity_orthogonal_vectors():
    a = [1, 0]
    b = [0, 1]
    assert cosine_similarity(a, b) == 0.0


def test_cosine_similarity_opposite_vectors():
    a = [1, 0]
    b = [-1, 0]
    assert cosine_similarity(a, b) == -1.0


def test_keyword_bonus_with_match():
    question = "GIL nedir?"
    content = "GIL, Python dilinde onemli bir mekanizmadir."
    bonus = keyword_bonus(question, content)
    assert bonus > 0


def test_keyword_bonus_without_match():
    question = "Bugun hava nasil?"
    content = "Python bir programlama dilidir."
    bonus = keyword_bonus(question, content)
    assert bonus == 0


def test_should_answer_above_threshold():
    assert should_answer(0.5, threshold=0.30) == True


def test_should_answer_below_threshold():
    assert should_answer(0.1, threshold=0.30) == False


def test_should_answer_exact_threshold():
    assert should_answer(0.30, threshold=0.30) == True