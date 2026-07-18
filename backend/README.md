# PenToText Backend

AI-powered backend for converting printed and handwritten medical notes into structured, readable text.

The backend accepts an uploaded image, improves the image for recognition, extracts an initial OCR draft, uses a multimodal vision model to interpret handwriting, validates the result, and returns structured transcription data through a FastAPI API.

## What We Built

The backend implements an end-to-end transcription pipeline:

1. Accept an uploaded note or prescription image.
2. Validate the file type and upload size.
3. Correct image orientation and normalize the image.
4. Create enhanced image variants for difficult handwriting.
5. Run OCR to obtain an initial text draft.
6. Send the image and OCR context to a multimodal vision model.
7. Correct uncertain or incomplete OCR text.
8. Extract useful fields such as medicine names and note content.
9. Validate the generated result.
10. Return the transcription, confidence information, and extracted fields as JSON.

## Main Features

- Printed-text recognition
- Handwritten-text recognition
- Medical-note and prescription processing
- Image preprocessing and enhancement
- OCR fallback support
- Multimodal AI transcription
- Confidence scoring
- Medicine-name extraction and validation
- Structured API responses
- FastAPI Swagger documentation
- Environment-based configuration

## Technologies Used

### Backend

- Python
- FastAPI
- Uvicorn
- Pydantic

### AI and OCR

- EasyOCR
- Tesseract OCR
- Gemini Vision or another configured multimodal vision model
- OpenRouter-compatible model integration
- Prompt-based transcription and correction

### Image Processing

- Pillow
- OpenCV
- NumPy

## Project Structure

```text
backend/
├── app/
│   ├── ai/
│   │   ├── confidence.py
│   │   ├── context_corrector.py
│   │   ├── extractor.py
│   │   ├── llm_corrector.py
│   │   ├── pipeline.py
│   │   ├── preprocessing.py
│   │   ├── prompt_builder.py
│   │   ├── transcription.py
│   │   └── validator.py
│   ├── api/
│   │   └── transcription.py
│   ├── core/
│   │   └── config.py
│   ├── data/
│   │   └── drug_names.txt
│   ├── models/
│   ├── schemas/
│   ├── services/
│   │   ├── field_extraction.py
│   │   ├── gemini_vision.py
│   │   ├── image_processing.py
│   │   ├── medicine_validator.py
│   │   ├── ocr.py
│   │   ├── prompt_builder.py
│   │   └── transcription.py
│   └── main.py
├── requirements.txt
└── README.md
```

## How the Pipeline Works

```text
Uploaded image
      ↓
File validation
      ↓
Orientation correction and preprocessing
      ↓
Enhanced image variants
      ↓
OCR draft
      ↓
Multimodal vision transcription
      ↓
Context correction and field extraction
      ↓
Confidence scoring and validation
      ↓
Structured JSON response
```

EasyOCR or Tesseract provides an initial draft when possible. The vision model also examines the image directly, which improves recognition of handwritten text that traditional OCR may miss.

## Installation

Open a terminal inside the `backend` directory.

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Create a local `.env` file inside the `backend` directory and add the configuration required by your selected AI provider.

Example variable names used by the project may include:

```env
PENTOTEXT_AI_PROVIDER=your-provider
PENTOTEXT_AI_MODEL=your-model
PENTOTEXT_GEMINI_API_KEY=your-api-key
PENTOTEXT_LOW_CONFIDENCE_THRESHOLD=0.78
PENTOTEXT_MAX_UPLOAD_BYTES=20971520
PENTOTEXT_OCR_PROVIDER=auto
PENTOTEXT_TESSERACT_CMD=tesseract
PENTOTEXT_EASYOCR_PYTHON_CMD=python
```

## Run the Backend

From the `backend` directory:

```bash
uvicorn app.main:app --reload
```

The API is normally available at:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

## API Output

A transcription response may include:

- recognized text
- corrected text
- extracted fields
- medicine names
- OCR confidence
- overall confidence
- AI model information
- validation warnings

The exact response structure is defined by the schemas in the application.

## Supported Images

Support depends on the installed Pillow and image-processing libraries. Common formats include:

- JPEG
- PNG
- BMP
- TIFF
- WEBP

Image quality, lighting, handwriting clarity, cropping, and resolution can affect transcription accuracy.

## Current Limitations

- Very unclear handwriting may still require manual review.
- Medical abbreviations can be ambiguous.
- OCR and AI output should not be treated as medical advice.
- Production deployment should include authentication, rate limiting, monitoring, and secure secret management.

## Privacy and Safety

Medical images may contain sensitive information. Do not store uploaded images or transcription results longer than necessary. Production deployments should use encrypted transport, controlled access, secure logging, and an appropriate data-retention policy.

## Team Contribution

This backend contribution focuses on:

- AI/ML transcription workflow
- handwriting-aware image processing
- OCR integration
- multimodal vision-model integration
- prompt engineering
- confidence estimation
- medicine extraction and validation
- FastAPI transcription endpoints

