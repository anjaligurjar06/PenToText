import re

from app.models.schemas import ContextMetadata, ExtractedFields
from app.services.medicine_validator import validate_medicine_name


MEDICINE_LINE_PATTERN = re.compile(
    r"\b(?P<medicine>[A-Z][A-Za-z-]{3,})\b\s+(?P<dosage>\d+\s?(?:mg|mcg|g|ml|units))",
    re.IGNORECASE,
)
FREQUENCY_PATTERN = re.compile(
    r"\b(?P<frequency>(?:once|twice|three|four|\d+\s?x|[1234]\s?times)\s+(?:daily|a day|per day)|bid|tid|qid|od|hs)\b",
    re.IGNORECASE,
)
DURATION_PATTERN = re.compile(
    r"\b(?:for\s+)?(?P<duration>\d+\s+(?:day|days|week|weeks|month|months))\b",
    re.IGNORECASE,
)
QUESTION_PATTERN = re.compile(
    r"(?:^|\n)\s*(?:q(?:uestion)?\.?\s*)?(?P<number>\d+[a-z]?)\s*[\).:-]\s*(?P<body>.*?)(?=\n\s*(?:q(?:uestion)?\.?\s*)?\d+[a-z]?\s*[\).:-]|\Z)",
    re.IGNORECASE | re.DOTALL,
)


def extract_fields(text: str, context: ContextMetadata) -> ExtractedFields:
    if context.category == "prescription":
        return _extract_prescription_fields(text)
    if context.category == "exam":
        return _extract_exam_fields(text)
    return ExtractedFields()


def _extract_prescription_fields(text: str) -> ExtractedFields:
    medicine = dosage = frequency = duration = None

    medicine_match = MEDICINE_LINE_PATTERN.search(text)
    if medicine_match:
        medicine = _clean(medicine_match.group("medicine"))
        dosage = _clean(medicine_match.group("dosage"))

    frequency_match = FREQUENCY_PATTERN.search(text)
    if frequency_match:
        frequency = _clean(frequency_match.group("frequency"))

    duration_match = DURATION_PATTERN.search(text)
    if duration_match:
        duration = _clean(duration_match.group("duration"))

    return ExtractedFields(
        medicine=medicine,
        dosage=dosage,
        frequency=frequency,
        duration=duration,
        instructions=text.strip() or None,
        medicine_validation=validate_medicine_name(medicine),
    )


def _extract_exam_fields(text: str) -> ExtractedFields:
    questions = [
        {"question_number": match.group("number"), "answer_text": match.group("body").strip()}
        for match in QUESTION_PATTERN.finditer(text)
        if match.group("body").strip()
    ]
    return ExtractedFields(questions=questions)


def _clean(value: str | None) -> str | None:
    if value is None:
        return None
    value = re.sub(r"\s+", " ", value).strip(" .,:;-")
    return value or None
