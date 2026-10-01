from gemini_client import generate


def answer_question_with_gemini(question: str) -> str:
    try:
        return generate(f"Answer this question accurately and concisely for a student:\n\n{question}")
    except Exception as e:
        return f"Error in QnA: {e}"
