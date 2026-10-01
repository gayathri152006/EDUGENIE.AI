import os
import requests
from dotenv import load_dotenv, dotenv_values

print("Windows env vars that may override your .env:")
for name in ("GEMINI_API_KEY", "GOOGLE_API_KEY"):
    v = os.environ.get(name)
    print(f"  {name}:", f"{v[:4]}... (len {len(v)})" if v else "not set")

print("\nValues in .env file:")
vals = dotenv_values(".env")
for k, v in vals.items():
    print(f"  {k}:", f"{v[:4]}... (len {len(v)})" if v else "EMPTY")

load_dotenv(override=True)
key = (os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY") or "").strip().strip('"').strip("'")

r = requests.get(
    "https://generativelanguage.googleapis.com/v1beta/models",
    params={"key": key},
)
print("\nGoogle replied:", r.status_code)
print("KEY WORKS" if r.status_code == 200 else r.text[:300])