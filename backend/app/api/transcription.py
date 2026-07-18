import os
import shutil
import tempfile

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.ai.pipeline import process_document


router = APIRouter(
    prefix="/api",
    tags=["transcription"]
)


@router.post("/transcribe")
async def transcribe(
    file: UploadFile = File(...),
    category: str = Form(...),
    context: str = Form(""),
    additional_context: str = Form("")
):
    allowed_types = {
        "image/jpeg",
        "image/jpg",
        "image/png"
    }

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Only JPG and PNG images are supported."
        )

    file_extension = os.path.splitext(
        file.filename or ""
    )[1]

    if not file_extension:
        file_extension = ".jpg"

    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=file_extension
        ) as temp_file:
            shutil.copyfileobj(
                file.file,
                temp_file
            )

            temp_path = temp_file.name

        result = process_document(
            image_path=temp_path,
            category=category,
            context=context,
            additional_context=additional_context
        )

        if not result.get("success", False):
            raise HTTPException(
                status_code=422,
                detail=result
            )

        return result

    finally:
        await file.close()

        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)