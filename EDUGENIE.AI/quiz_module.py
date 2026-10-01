import json
import re
from gemini_client import generate


def clean_json_block(text: str) -> str:
    """Remove Markdown ```json fences if present."""
    return re.sub(r"```(?:json)?\s*(.*?)```", r"\1", text, flags=re.DOTALL).strip()


def generate_quiz(text: str) -> list:
    prompt = f"""You are a quiz generator.
From the following passage or topic, create 3 multiple-choice questions. Each question must include:
- "question": the question text
- "options": a list of exactly 4 option strings (no "A)" prefixes)
- "answer": the correct answer, which must exactly match one of the options

Return ONLY valid JSON like:
[{{"question": "What is ...?", "options": ["w", "x", "y", "z"], "answer": "x"}}]

Passage or topic:
{text}"""
    raw = generate(prompt, json_mode=True)
    quiz = json.loads(clean_json_block(raw))
    if isinstance(quiz, dict):
        quiz = quiz.get("questions") or quiz.get("quiz") or [quiz]
    for q in quiz:  # if the model answered with a letter, map it to the option text
        opts, ans = q["options"], str(q["answer"]).strip()
        if ans not in opts and len(ans) == 1 and ans.upper() in "ABCD":
            ans = opts["ABCD".index(ans.upper())]
        q["answer"] = ans
    return quiz
