import json
import mimetypes
import os
import uuid

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from google import genai
from google.genai import types
from sqlalchemy import desc
from sqlalchemy.orm import Session

from .. import models, schemas
from ..config import GEMINI_API_KEY, UPLOAD_DIR
from ..database import get_db
from ..deps import get_current_user

router = APIRouter(prefix="/documents", tags=["documents"])

ALLOWED_CATEGORIES = {"prescription", "exam", "notes", "general"}
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".pdf"}

CATEGORY_DESCRIPTIONS = {
    "prescription": "a handwritten medical prescription",
    "exam": "a handwritten exam paper",
    "notes": "handwritten class or lecture notes",
    "general": "a general handwritten note",
}

_gemini_client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None


def _run_transcription(
    file_path: str, category: str, context: str | None, notes: str | None
) -> tuple[str, int | None, str]:
    """Transcribes the uploaded handwritten document via Gemini's vision model.

    Returns (transcript_text, confidence, status). status is "done" on success
    or "error" if the key is missing or the API call failed — callers should
    still persist the document rather than failing the whole upload, since the
    file itself was already saved.
    """
    if not _gemini_client:
        return (
            "GEMINI_API_KEY is not set in backend/.env — get a free key from "
            "https://aistudio.google.com/apikey to enable real transcription.",
            None,
            "error",
        )

    doc_kind = CATEGORY_DESCRIPTIONS.get(category, "a handwritten document")
    context_lines = []
    if context:
        context_lines.append(f"Context: {context}")
    if notes:
        context_lines.append(f"Additional notes: {notes}")
    context_block = "\n".join(context_lines)

    prompt = (
        f"Transcribe {doc_kind} from the attached image.\n"
        f"{context_block}\n"
        "Read the handwriting carefully, using the context above to resolve ambiguous "
        "words or domain-specific terms. Respond with ONLY a JSON object with exactly "
        'two keys: "transcript" (the full transcribed text, preserving line breaks) '
        'and "confidence" (your estimated transcription accuracy as an integer 0-100).'
    )

    try:
        mime_type = mimetypes.guess_type(file_path)[0] or "application/octet-stream"
        uploaded_file = _gemini_client.files.upload(
            file=file_path, config=types.UploadFileConfig(mime_type=mime_type)
        )
        response = _gemini_client.models.generate_content(
            model="gemini-flash-latest",
            contents=[uploaded_file, prompt],
            config=types.GenerateContentConfig(response_mime_type="application/json"),
        )
        # Gemini's response_mime_type=json sometimes appends stray trailing
        # characters after the JSON object, so parse only the first value.
        data, _ = json.JSONDecoder().raw_decode(response.text.strip())
        transcript = str(data.get("transcript", "")).strip()
        confidence = max(0, min(100, int(data.get("confidence", 70))))
        return transcript or "No text detected in the image.", confidence, "done"
    except Exception as e:
        return f"Transcription failed: {e}", None, "error"


@router.post("", response_model=schemas.DocumentOut, status_code=status.HTTP_201_CREATED)
def create_document(
    title: str = Form(...),
    category: str = Form(...),
    context: str = Form(None),
    notes: str = Form(None),
    file: UploadFile = File(...),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if category not in ALLOWED_CATEGORIES:
        raise HTTPException(status_code=400, detail=f"category must be one of {sorted(ALLOWED_CATEGORIES)}")

    ext = os.path.splitext(file.filename or "")[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"file extension must be one of {sorted(ALLOWED_EXTENSIONS)}")

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    stored_name = f"{uuid.uuid4().hex}{ext}"
    stored_path = os.path.join(UPLOAD_DIR, stored_name)
    with open(stored_path, "wb") as out:
        out.write(file.file.read())

    transcript_text, confidence, doc_status = _run_transcription(stored_path, category, context, notes)

    doc = models.Document(
        owner_id=current_user.id,
        title=title,
        category=category,
        context=context,
        notes=notes,
        file_path=stored_name,
        transcript_text=transcript_text,
        confidence=confidence,
        status=doc_status,
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc


@router.get("", response_model=list[schemas.DocumentOut])
def list_documents(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return (
        db.query(models.Document)
        .filter(models.Document.owner_id == current_user.id)
        .order_by(desc(models.Document.created_at))
        .all()
    )


def _get_owned_document(doc_id: str, current_user: models.User, db: Session) -> models.Document:
    doc = db.get(models.Document, doc_id)
    if not doc or doc.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc


@router.get("/{doc_id}", response_model=schemas.DocumentOut)
def get_document(
    doc_id: str,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return _get_owned_document(doc_id, current_user, db)


@router.patch("/{doc_id}", response_model=schemas.DocumentOut)
def update_document(
    doc_id: str,
    payload: schemas.DocumentUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    doc = _get_owned_document(doc_id, current_user, db)
    if payload.title is not None:
        doc.title = payload.title
    if payload.transcript_text is not None:
        doc.transcript_text = payload.transcript_text
    db.commit()
    db.refresh(doc)
    return doc


@router.delete("/{doc_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(
    doc_id: str,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    doc = _get_owned_document(doc_id, current_user, db)
    file_path = os.path.join(UPLOAD_DIR, doc.file_path)
    db.delete(doc)
    db.commit()
    if os.path.exists(file_path):
        os.remove(file_path)
