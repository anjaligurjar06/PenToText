# PenToText Backend

FastAPI service for the Core Logic / AI-ML track.

## What is implemented

- Upload validation for JPG, PNG, WEBP, and PDF.
- Context-aware prompt builder for prescription, exam, notes, and general documents.
- Stable transcription response schema for frontend integration.
- Token-level confidence flags.
- Prescription field extraction for medicine, dosage, frequency, and duration.
- Starter medicine-name validation with fuzzy matching.
- Exam question parsing.
- Real OCR-first transcription through Tesseract for image uploads.
- Local fallback transcription engine only when OCR returns no readable text.

## Run locally

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

The API will be available at:

- `http://localhost:8000/health`
- `http://localhost:8000/docs`
- `POST http://localhost:8000/api/transcriptions`

## Environment

Copy `.env.example` to `.env` when you are ready to configure a hosted AI provider.

For OCR, the backend looks for `tesseract` in PATH. You can also set:

```powershell
PENTOTEXT_TESSERACT_CMD=C:\Users\vansh\Downloads\TESSERACT\tesseract.exe
```
