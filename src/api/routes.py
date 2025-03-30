from fastapi import APIRouter, Request, Form, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from src.services.pdf_service import PDFService
from src.services.transcription_service import TranscriptionService
from src.services.ai_service import AIService

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Initialize services
pdf_service = PDFService()
transcription_service = TranscriptionService()
ai_service = AIService()

# In-memory storage for resume (TODO: switch to database)
resume_storage = {"text": ""}

@router.get("/", response_class=HTMLResponse)
async def form_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/upload_resume")
async def upload_resume(file: UploadFile = File(...)):
    try:
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")

        pdf_bytes = await file.read()
        text = pdf_service.extract_text(pdf_bytes)
        
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
        raise HTTPException(status_code=500, detail=f"Error processing the PDF file: {str(e)}")

@router.post("/generate", response_class=HTMLResponse)
async def generate_response(request: Request,
                          resume: str = Form(...),
                          question: str = Form(...)):
    try:
        star_output = await ai_service.generate_response(resume, question)
        return templates.TemplateResponse("index.html", {
            "request": request,
            "resume": resume,
            "question": question,
            "response": star_output
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/transcribe")
async def transcribe_audio(audio: UploadFile = File(...)):
    try:
        audio_content = await audio.read()
        transcript = await transcription_service.transcribe_audio(audio_content)
        return JSONResponse({"transcript": transcript})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 