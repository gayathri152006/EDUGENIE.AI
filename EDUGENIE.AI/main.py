from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from explanation_module import explain_topic
from learning_path import get_learning_recommendations
from qna import answer_question_with_gemini
from quiz_module import generate_quiz
from summary_module import summarize_text

app = FastAPI(title="EduGenie")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


class TopicIn(BaseModel):
    topic: str


class TextIn(BaseModel):
    text: str


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request, "index.html")


@app.get("/qa")
def qa(question: str = Query(..., min_length=1)):
    return {"answer": answer_question_with_gemini(question)}


@app.post("/explain")
@app.post("/explain/")
def explain(body: TopicIn):
    if not body.topic.strip():
        return JSONResponse({"error": "Please provide a topic."}, status_code=400)
    return {"topic": body.topic, "explanation": explain_topic(body.topic)}


@app.post("/summarize")
@app.post("/summarize/")
def summarize(body: TextIn):
    if not body.text.strip():
        return JSONResponse({"error": "Please provide text to summarize."}, status_code=400)
    return {"summary": summarize_text(body.text)}


@app.post("/quiz")
def quiz(body: TextIn):
    if not body.text.strip():
        return JSONResponse({"error": "Please provide a topic or text for the quiz."}, status_code=400)
    try:
        return {"quiz": generate_quiz(body.text)}
    except Exception as e:
        return JSONResponse({"error": f"Could not generate quiz: {e}"}, status_code=500)


@app.get("/learn/recommendations")
def learn(topic: str = Query(..., min_length=1)):
    return {"topic": topic, "recommendation": get_learning_recommendations(topic)}
