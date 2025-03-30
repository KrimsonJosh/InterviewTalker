from fastapi import FastAPI, Form, Request, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import os
import io

import PyPDF2
from dotenv import load_dotenv
from openai import OpenAI
import httpx

load_dotenv()  

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# OpenAI client 
client = OpenAI()

# Deepgram API Key from environment 
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY", "YOUR_DEEPGRAM_KEY_HERE")

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Hold resume text in memory for now TODO: maybe switch to db 
resume_storage = {"text": ""}
"""
--------
HELPER FUNCTION: Extract PDF text
--------
Extracts all text from a PDF file in bytes using PyPDF2. 
Returns 1 string with all pages/words concatenated.
"""
def extract_pdf_text(pdf_bytes: bytes) -> str:
    all_text = ""
    with io.BytesIO(pdf_bytes) as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        for page in reader.pages:
            page_text = page.extract_text() or "" #no text found 
            all_text += page_text + "\n"
        return all_text

"""
---------
HELPER FUNCTION: build_prompt
---------
Generates a custom prompt for the OpenAI API, using the candidate's resume
and the interview question in a STAR format.
"""
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


"""
---------
ROOT ROUTE
---------
Renders a simple HTML page (index.html) that allows input for the resume and question.
"""
@app.get("/", response_class=HTMLResponse)
async def form_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

"""
-------
/upload_resume ROUTE
-------
Handles Extraction of text from a PDF Resume and stores it
"""
@app.post("/upload_resume")
async def upload_resume(file: UploadFile = File(...)):
    try:
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")

        pdf_bytes = await file.read()

        text = extract_pdf_text(pdf_bytes)
        
        if not text.strip():
            raise HTTPException(status_code=400, detail="No text could be extracted from the PDF")

        resume_storage["text"] = text
        
        return JSONResponse({
            "message": "Resume text extracted successfully",
            "text": text
        })
        
    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"Error processing PDF: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing the PDF file")

"""
---------
/generate ROUTE
---------
Handles form submission with resume + question and returns AI-generated response (STAR format).
"""
@app.post("/generate", response_class=HTMLResponse)
async def generate_response(request: Request,
                            resume: str = Form(...),
                            question: str = Form(...)):
    print(f"Question received: {question}")
    
    # Build the prompt
    prompt = build_prompt(resume, question)
    
    # Call the OpenAI Chat Completion
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,  # Adjust if needed
    )
    
    # Extract the generated text
    star_output = response.choices[0].message.content
    # Render the same page with the AI response
    return templates.TemplateResponse("index.html", {
        "request": request,
        "resume": resume,
        "question": question,
        "response": star_output
    })

"""
---------
/transcribe ROUTE
---------
Accepts a recorded audio file, sends it to Deepgram via WebSocket,
and returns a transcript once it's available.
"""
@app.post("/transcribe")
async def transcribe_audio(audio: UploadFile = File(...)):
    try:
        # Read the audio file
        audio_content = await audio.read()
        print(f"Received audio content, size: {len(audio_content)} bytes")

        # Set up headers for Deepgram API
        headers = {
            "Authorization": f"Token {DEEPGRAM_API_KEY}",
            "Content-Type": "audio/webm"
        }

        # Send to Deepgram using REST API
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.deepgram.com/v1/listen",
                headers=headers,
                content=audio_content
            )

        # Check if request was successful
        if response.status_code == 200:
            data = response.json()
            transcript = data.get("results", {}).get("channels", [{}])[0].get("alternatives", [{}])[0].get("transcript", "")
            print("Final transcript:", transcript)
            return JSONResponse({"transcript": transcript})
        else:
            print("Deepgram API error:", response.text)
            return JSONResponse({"error": "Failed to transcribe audio"}, status_code=500)

    except Exception as e:
        print("Transcription error:", str(e))
        return JSONResponse({"error": str(e)}, status_code=500)
