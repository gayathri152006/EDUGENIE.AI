# EduGenie – Gemini-powered learning assistant

## Setup (VS Code)
1. Install Python 3.10+ (tick "Add Python to PATH"). Open the `EduGenie` folder in VS Code (File > Open Folder).
2. Open a terminal (Ctrl+`) and create a virtual environment:
   - Windows: `python -m venv venv` then `venv\Scripts\activate`
   - Mac/Linux: `python3 -m venv venv` then `source venv/bin/activate`
   - In VS Code choose the interpreter: Ctrl+Shift+P > "Python: Select Interpreter" > the `venv` one.
3. `pip install -r requirements.txt`
4. Get a key at https://aistudio.google.com/apikey. Copy `.env.example` to `.env` and paste the key.

## Run
`uvicorn main:app --reload` then open http://127.0.0.1:8000

The first "Explain" request downloads LaMini-Flan-T5-783M (~3 GB) and may take a few minutes.
If the local model fails to load, explanations fall back to Gemini automatically.

## Test
Use the dropdown in the page, or Swagger UI at http://127.0.0.1:8000/docs.
- Ask: "Which is the largest ocean?"
- Explain: "Binary search algorithm"
- Summarize: paste any long paragraph
- Quiz: "Pythagoras theorem" (pick answers, click Check answer)
- Learning path: "SQL"

curl checks:
    curl "http://127.0.0.1:8000/qa?question=Which%20is%20the%20largest%20ocean"
    curl -X POST http://127.0.0.1:8000/quiz -H "Content-Type: application/json" -d '{"text":"Solar System"}'

## Troubleshooting
- "GEMINI_API_KEY is missing": `.env` must be in the EduGenie folder (not `.env.example`).
- 404 model not found: set `GEMINI_MODEL` in `.env` to a currently available model.
