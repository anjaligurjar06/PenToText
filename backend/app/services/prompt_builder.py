from app.models.schemas import ContextMetadata


CATEGORY_INSTRUCTIONS = {
    "prescription": (
        "Transcribe the prescription exactly, preserve medication names, dosage, "
        "frequency, duration, and doctor instructions. Return uncertain words with "
        "lower confidence and extract medicine fields."
    ),
    "exam": (
        "Transcribe the exam response without rewriting the student's meaning. "
        "Group content by visible question number when possible."
    ),
    "notes": (
        "Transcribe class notes while preserving abbreviations, formulas, headings, "
        "and topic-specific terminology."
    ),
    "general": (
        "Transcribe the handwritten note into readable digital text and preserve line order."
    ),
    "other": (
        "Transcribe the handwritten document into readable digital text and preserve structure."
    ),
}


def build_transcription_prompt(context: ContextMetadata) -> dict[str, str]:
    category_instruction = CATEGORY_INSTRUCTIONS.get(context.category, CATEGORY_INSTRUCTIONS["general"])
    system = (
        "You are PenToText, a context-aware handwriting transcription engine. "
        "Return faithful transcription, token confidence, and structured fields. "
        "Do not invent missing content; flag uncertainty instead."
    )
    user = "\n".join(
        [
            category_instruction,
            f"Document title: {context.title or 'Untitled'}",
            f"Document category: {context.category}",
            f"Primary context hint: {context.context_hint or 'None provided'}",
            f"Additional context: {context.additional_context or 'None provided'}",
            "Expected JSON keys: transcribed_text, tokens, overall_confidence, structured_fields.",
        ]
    )
    return {"system": system, "user": user}

