from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from explanation_module import explain_topic
from qna import answer_question
from summary_module import summarize_text
from quiz_module import generate_quiz
from learning_path import get_learning_recommendations

app = FastAPI(
    title="EduGenie Learning Assistant",
    description="AI-powered Educational Learning Assistant",
    version="1.0"
)

# Static Files
app.mount("/static", StaticFiles(directory="static"), name="static")

# HTML Templates
templates = Jinja2Templates(directory="templates")


# -------------------------
# Home Page
# -------------------------
@app.get("/", response_class=HTMLResponse)
def home(request: Request):

    return templates.TemplateResponse(
        name="index.html",
        context={"request": request}
    )


# -------------------------
# Question Answering
# -------------------------
@app.post("/qna")
def qna(question: str = Form(...)):

    answer = answer_question(question)

    return {
        "question": question,
        "answer": answer
    }


# -------------------------
# Explanation Module
# -------------------------
@app.post("/explanation")
def explanation(topic: str = Form(...)):

    explanation = explain_topic(topic)

    return {
        "topic": topic,
        "explanation": explanation
    }


# -------------------------
# Summary Module
# -------------------------
@app.post("/summary")
def summary(text: str = Form(...)):

    summary = summarize_text(text)

    return {
        "summary": summary
    }


# -------------------------
# Quiz Module
# -------------------------
@app.post("/quiz")
def quiz(text: str = Form(...)):

    return generate_quiz(text)


# -------------------------
# Learning Path
# -------------------------
@app.post("/learning-path")
def learning_path(topic: str = Form(...)):

    recommendation = get_learning_recommendations(topic)

    return {
        "topic": topic,
        "learning_path": recommendation
    }