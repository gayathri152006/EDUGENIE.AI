from gemini_client import generate


def summarize_text(text: str) -> str:
    try:
        return generate(f"Summarize the following text in simple language, keeping the key points:\n\n{text}")
    except Exception as e:
        return f"Error in Summary: {e}"
