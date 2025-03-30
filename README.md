# InterviewTalker

InterviewTalker is a FastAPI application that helps you practice behavioral interviews with AI assistance. It supports:
- **Uploading a PDF resume** for AI-based question answering.
- **Recording audio** and transcribing it via Deepgram.
- **Generating STAR-format responses** using OpenAI GPT.

---

## 1. Installation

1. **Clone the Repository** (or download the source code).
2. **Install Requirements**:

   ```bash
   pip install -r requirements.txt

## Project Structure
```
├── src/
│   ├── api/
│   │   └── routes.py          # API endpoints for uploading resume, transcribing audio, generating answers
│   ├── core/
│   │   └── config.py          # Pydantic-based settings (API keys, debug mode, etc.)
│   ├── main.py                # FastAPI app creation (mount static files, include router)
│   ├── services/
│   │   ├── ai_service.py      # Handles OpenAI GPT logic
│   │   ├── pdf_service.py     # Extracts text from PDFs
│   │   └── transcription_service.py
│   └── ...
├── static/
│   └── recorder.js            # Front-end script for recording microphone audio in the browser
├── templates/
│   └── index.html             # Main HTML page
├── requirements.txt
└── README.md                  # This file
```

---

## TODO

- [ ] **System Input**
  - Explore ways to capture system audio (virtual audio cable)
  - Optional: add Electron frontend for stealthy modeee

- [ ] **More file support**
  - Handle DOCX and other resume formats

- [ ] **Multilingual Support**
  - Enable resume parsing and AI responses in different languages
  - Detect resume language and route through appropriate GPT translation or prompt

- [ ] **Storage Upgrade**
  - Swap in-memory storage for a database (Postgres, sqlite, etc.)
  - Save user uploads and transcripts securely

- [ ] **User Accounts**
  - Let users log in and save their resume
