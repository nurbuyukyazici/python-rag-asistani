import urllib.request
import json
import time

questions = [
    "GIL nedir?",
    "Virtual environment neden kullanılır?",
    "Tuple ile liste arasındaki fark nedir?",
    "List comprehension nedir?",
    "Bugün hava nasıl?"
]

times = []

print("Performans testi basliyor...\n")

for q in questions:
    payload = json.dumps({"message": q, "history": []}).encode("utf-8")
    req = urllib.request.Request(
        "http://localhost:5000/api/chat",
        data=payload,
        headers={"Content-Type": "application/json"}
    )
    start = time.time()
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read())
    elapsed = time.time() - start
    times.append(elapsed)
    print(f"Soru: {q}")
    print(f"Sure: {elapsed:.2f} saniye\n")

avg = sum(times) / len(times)
print("=" * 40)
print(f"Ortalama cevap suresi: {avg:.2f} saniye")
print(f"En hizli: {min(times):.2f} saniye")
print(f"En yavas: {max(times):.2f} saniye")