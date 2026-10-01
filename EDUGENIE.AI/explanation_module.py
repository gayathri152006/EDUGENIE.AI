"""Concept explanation using the local LaMini-Flan-T5-783M model (falls back to Gemini)."""
import threading
from gemini_client import generate

MODEL_NAME = "MBZUAI/LaMini-Flan-T5-783M"
_tok = _model = None
_lock = threading.Lock()


def _load():
    global _tok, _model
    with _lock:
        if _model is None:
            from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
            _tok = AutoTokenizer.from_pretrained(MODEL_NAME)
            _model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
            _model.eval()


def explain_topic(topic: str) -> str:
    prompt = f"Explain the concept of '{topic}' in a simple and clear way for a school student."
    try:
        import torch
        _load()
        inputs = _tok(prompt, return_tensors="pt")
        with torch.no_grad():
            out = _model.generate(**inputs, max_new_tokens=200, temperature=0.7,
                                  top_k=50, top_p=0.95, do_sample=True)
        text = _tok.decode(out[0], skip_special_tokens=True).strip()
        if text:
            return text
    except Exception as e:  # local model unavailable -> cloud fallback
        print(f"[explain] local model failed ({e}); using Gemini fallback")
    try:
        return generate(prompt)
    except Exception as e:
        return f"Error in explanation: {e}"
