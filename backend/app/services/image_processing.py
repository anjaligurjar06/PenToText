from io import BytesIO
from fastapi import HTTPException, UploadFile
from PIL import Image, UnidentifiedImageError

from app.core.config import Settings
from app.models.schemas import ImageMetadata


ALLOWED_CONTENT_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
    "application/pdf",
}


async def read_and_validate_upload(file: UploadFile, settings: Settings) -> tuple[bytes, ImageMetadata]:
    raw = await file.read()
    if not raw:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    if len(raw) > settings.max_upload_bytes:
        raise HTTPException(status_code=413, detail="File exceeds the 20MB upload limit.")

    content_type = file.content_type or "application/octet-stream"
    if content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=415,
            detail="Unsupported file type. Upload JPG, PNG, WEBP, or PDF.",
        )

    width = height = None
    detected_format = None
    if content_type != "application/pdf":
        try:
            with Image.open(BytesIO(raw)) as image:
                width, height = image.size
                detected_format = image.format
        except UnidentifiedImageError as exc:
            raise HTTPException(status_code=400, detail="Could not read uploaded image.") from exc

    metadata = ImageMetadata(
        filename=file.filename or "document",
        content_type=content_type,
        size_bytes=len(raw),
        width=width,
        height=height,
        format=detected_format,
    )
    return raw, metadata

