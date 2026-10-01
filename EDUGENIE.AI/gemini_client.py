"""Shared Gemini helper used by qna, quiz, summary and learning-path modules."""
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv(override=True)  # .env wins over any old Windows variable
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
_client = None


def _get_client():
    global _client
    if _client is None:
        key = (os.getenv("GEMINI_API_KEY") or "").strip().strip('"').strip("'")
        if not key:
            raise RuntimeError("GEMINI_API_KEY is missing. Add it to your .env file.")
        print(f"[debug] key starts with {key[:4]}, length {len(key)}")
        _client = genai.Client(api_key=key)
    return _client


def generate(prompt: str, json_mode: bool = False) -> str:
    config = types.GenerateContentConfig(response_mime_type="application/json") if json_mode else None
    resp = _get_client().models.generate_content(model=MODEL, contents=prompt, config=config)
    if not resp.text:
        raise RuntimeError("Gemini returned an empty response (it may have been blocked).")
    return resp.text.strip()