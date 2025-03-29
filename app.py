from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
templates = Jinja2Templates(directory = "templates")
app = FastAPI()
client = OpenAI()


'''
------
SIMPLE PROMPT FOR AI GEN RESPONSES 
-----
'''
def build_prompt(resume: str, question: str) -> str:
    return f"""
            You are an interview assistant helping candidates answer behavioral questions using their resume.

            Resume:
            {resume}

            Behavioral Interview Question:
            "{question}"

            Respond using the STAR format:
            - Situation
            - Task
            - Action
            - Result

            Be concise but thoughtful. Keep it professional and realistic.
            """

@app.get("/", response_class=HTMLResponse)
async def form_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate", response_class=HTMLResponse)
async def generate_response(request: Request,
                            resume: str = Form(...),
                            question: str = Form(...)):
    prompt = build_prompt(resume, question)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo", # Free GPT api 
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
    )
    star_output = response.choices[0].message.content

    return templates.TemplateResponse("index.html", {
        "request": request,
        "resume": resume,
        "question": question,
        "response": star_output
    })

    