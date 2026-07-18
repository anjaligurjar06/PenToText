from typing import List, Optional
from pydantic import BaseModel


class MedicineField(BaseModel):
    name: Optional[str] = None
    dosage: Optional[str] = None
    frequency: Optional[str] = None
    duration: Optional[str] = None


class TokenConfidence(BaseModel):
    text: str
    confidence: float
    needs_review: bool


class TranscriptionResponse(BaseModel):
    document_type: str
    raw_transcription: str
    corrected_transcription: str
    tokens: List[TokenConfidence]
    medicines: List[MedicineField]
    overall_confidence: float
    warnings: List[str]