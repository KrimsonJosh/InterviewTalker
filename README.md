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
   python -m venv venv
   pip install -r requirements.txt
   uvicorn src.main:app --reload

   ON A SEPERATE TERMINAL
   npm i
   npm start


## Project Structure
```
.
├── electron // frontend
│   ├── index.html
│   ├── main.js
│   ├── package.json
│   └── renderer.js
├── README.md
├── requirements.txt
├── src
│   ├── api // rest api
│   ├── core // config
│   ├── main.py // run
│   ├── services // gpt, pdf, transcribingw/deepgram
│   └── utils
├── static // stuff for recording audio
│   ├── app.js
│   └── recorder.js
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
