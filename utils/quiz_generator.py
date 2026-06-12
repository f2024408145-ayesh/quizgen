"""
Quiz generation using GitHub Models API — Free with GitHub account.
"""

import urllib.request
import urllib.error
import json
import re

API_URL = "https://models.inference.ai.azure.com/chat/completions"
MODEL = "gpt-4o-mini"
API_KEY = "your_github_token_here"


def generate_quiz(text: str, num_questions: int = 10, difficulty: str = "medium") -> list[dict]:
    prompt = f"""You are an expert quiz maker. Given the following text, generate exactly {num_questions} multiple-choice questions at {difficulty} difficulty level.

TEXT:
{text[:6000]}

Rules:
- Each question must have exactly 4 options labeled A, B, C, D.
- Clearly mark the correct answer.
- Add a short explanation (1-2 sentences) for each answer.
- Return ONLY valid JSON — no markdown, no commentary, no code fences.
- The JSON must be a list of objects with keys: "question", "options", "answer", "explanation".
- "options" is an object with keys "A", "B", "C", "D".
- "answer" is exactly one of: "A", "B", "C", "D".

Example format:
[
  {{
    "question": "What is X?",
    "options": {{"A": "...", "B": "...", "C": "...", "D": "..."}},
    "answer": "B",
    "explanation": "Because..."
  }}
]
"""

    payload = json.dumps({
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 4000,
    }).encode("utf-8")

    req = urllib.request.Request(
        API_URL, data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"API error {e.code}:\n{body[:300]}")
    except Exception as e:
        raise RuntimeError(f"Network error: {e}\n\nCheck your internet connection.")

    try:
        raw = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError):
        raise RuntimeError(f"Unexpected response:\n{str(data)[:300]}")

    raw = re.sub(r"```[a-z]*", "", raw).strip().strip("`").strip()

    try:
        questions = json.loads(raw)
    except json.JSONDecodeError:
        match = re.search(r'\[.*\]', raw, re.DOTALL)
        if match:
            questions = json.loads(match.group())
        else:
            raise RuntimeError(f"Could not parse response.\nOutput:\n{raw[:400]}")

    validated = []
    for q in questions:
        if (
            isinstance(q, dict)
            and "question" in q
            and "options" in q
            and "answer" in q
            and isinstance(q["options"], dict)
            and len(q["options"]) >= 4
            and q.get("answer") in ("A", "B", "C", "D")
        ):
            validated.append({
                "question": q["question"],
                "options": {k: q["options"][k] for k in ("A", "B", "C", "D")},
                "answer": q["answer"],
                "explanation": q.get("explanation", ""),
            })

    if not validated:
        raise RuntimeError("Got 0 valid questions. Please try again.")

    return validated
