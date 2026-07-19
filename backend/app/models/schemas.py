from typing import Any, Literal
from pydantic import BaseModel, Field


DocumentCategory = Literal["prescription", "exam", "notes", "general", "other"]


class ContextMetadata(BaseModel):
    title: str = ""
    category: DocumentCategory = "general"
    context_hint: str = ""
    additional_context: str = ""


class TokenResult(BaseModel):
    text: str
    confidence: float = Field(ge=0.0, le=1.0)
    low: bool = False
    reason: str | None = None


class MedicineValidation(BaseModel):
    original: str
    matched_name: str | None = None
    score: float = Field(ge=0.0, le=1.0)
    status: Literal["matched", "suggested", "unmatched"]


class ExtractedFields(BaseModel):
    medicine: str | None = None
    dosage: str | None = None
    frequency: str | None = None
    duration: str | None = None
    instructions: str | None = None
    questions: list[dict[str, str]] = Field(default_factory=list)
    medicine_validation: MedicineValidation | None = None


class ImageMetadata(BaseModel):
    filename: str
    content_type: str
    size_bytes: int
    width: int | None = None
    height: int | None = None
    format: str | None = None


class TranscriptionResponse(BaseModel):
    document_id: str
    title: str
    category: DocumentCategory
    transcribed_text: str
    tokens: list[TokenResult]
    overall_confidence: int = Field(ge=0, le=100)
    structured_fields: ExtractedFields
    image: ImageMetadata
    model_info: dict[str, Any] = Field(default_factory=dict)

