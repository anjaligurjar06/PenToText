import re
from hashlib import sha1

from app.core.config import Settings
from app.models.schemas import ContextMetadata, ImageMetadata, TokenResult, TranscriptionResponse
from app.services.field_extraction import extract_fields
from app.services.gemini_vision import transcribe_with_gemini
from app.services.ocr import recognize_text
from app.services.prompt_builder import build_transcription_prompt


class ContextAwareTranscriptionEngine:
    def __init__(self, settings: Settings):
        self.settings = settings

    async def transcribe(
        self,
        image_bytes: bytes,
        image: ImageMetadata,
        context: ContextMetadata,
    ) -> TranscriptionResponse:
        prompt = build_transcription_prompt(context)
        gemini_result = None
        if self.settings.ai_provider.lower() == "gemini":
            gemini_result = transcribe_with_gemini(image_bytes, image, context, self.settings)

        if gemini_result and gemini_result.text:
            text = gemini_result.text
            ocr_result = None
            failed = False
            mode = "gemini-vision"
        else:
            ocr_result = recognize_text(image_bytes, image, self.settings)
            failed = not bool(ocr_result.text)
            text = ocr_result.text or self._unreadable_transcription_message(
                (gemini_result.error if gemini_result else None) or ocr_result.error
            )
            mode = f"{ocr_result.provider}-ocr" if ocr_result.text else "ocr-unreadable"

        tokens = (
            [
                TokenResult(
                    text=text,
                    confidence=0.0,
                    low=True,
                    reason=(
                        (gemini_result.error if gemini_result else None)
                        or (ocr_result.error if ocr_result else None)
                        or "Text could not be read reliably."
                    ),
                )
            ]
            if failed
            else self._tokenize_with_confidence(text, context)
        )
        fields = extract_fields(text, context)
        overall_confidence = 0 if failed else self._overall_confidence(tokens)

        return TranscriptionResponse(
            document_id=sha1(image_bytes[:4096] + context.model_dump_json().encode()).hexdigest()[:16],
            title=context.title or image.filename,
            category=context.category,
            transcribed_text=text,
            tokens=tokens,
            overall_confidence=overall_confidence,
            structured_fields=fields,
            image=image,
            model_info={
                "provider": self.settings.ai_provider,
                "model": self.settings.ai_model,
                "mode": mode,
                "gemini_model": gemini_result.model if gemini_result else self.settings.gemini_model,
                "gemini_error": gemini_result.error if gemini_result else None,
                "ocr_provider": ocr_result.provider if ocr_result else None,
                "ocr_confidence": ocr_result.confidence if ocr_result else None,
                "ocr_error": ocr_result.error if ocr_result else None,
                "prompt_preview": prompt,
            },
        )

    @staticmethod
    def _unreadable_transcription_message(error: str | None) -> str:
        detail = error or "OCR could not read this image reliably."
        return (
            "No reliable text was recognized from this upload. "
            f"{detail} For messy handwriting, use a clearer image or configure a vision AI model."
        )

    def _local_demo_transcription(self, context: ContextMetadata) -> str:
        hint = context.context_hint.strip()
        extra = context.additional_context.strip()

        if context.category == "prescription":
            condition = hint or "reported symptoms"
            return (
                f"Patient evaluated for {condition}. Continue Amoxicillin 500mg three times daily "
                "for 7 days. Recheck throat culture if fever persists beyond 72 hours. "
                "Follow up in clinic next week or sooner if symptoms worsen."
            )

        if context.category == "exam":
            subject = hint or "the selected subject"
            return (
                f"1. The answer explains the core idea from {subject} using the given context. "
                "2. The working shows each step clearly and preserves the student's original reasoning. "
                f"3. Additional note: {extra or 'No extra context was provided.'}"
            )

        if context.category == "notes":
            topic = hint or "class topic"
            return (
                f"Notes on {topic}: key terms, examples, and short handwritten points were preserved. "
                f"{extra or 'Review highlighted terms against the course context.'}"
            )

        return extra or "General handwritten note transcribed into clean typed text."

    def _tokenize_with_confidence(self, text: str, context: ContextMetadata) -> list[TokenResult]:
        raw_tokens = re.findall(r"\S+", text)
        tokens: list[TokenResult] = []
        domain_terms = self._domain_terms(context)

        for raw in raw_tokens:
            normalized = raw.strip(".,:;()").lower()
            confidence = 0.93
            reason = None

            if normalized in domain_terms:
                confidence = 0.72
                reason = "domain term needs user review"
            elif any(char.isdigit() for char in normalized):
                confidence = 0.84
                reason = "numeric value should be checked"
            elif len(normalized) > 14:
                confidence = 0.76
                reason = "long handwritten word"

            low = confidence < self.settings.low_confidence_threshold
            tokens.append(
                TokenResult(
                    text=raw,
                    confidence=round(confidence, 2),
                    low=low,
                    reason=reason if low else None,
                )
            )

        return tokens

    def _domain_terms(self, context: ContextMetadata) -> set[str]:
        if context.category == "prescription":
            return {"amoxicillin", "culture", "pharyngitis"}
        if context.category == "exam":
            return {"equilibrium", "stoichiometry", "derivative", "photosynthesis"}
        return set()

    @staticmethod
    def _overall_confidence(tokens: list[TokenResult]) -> int:
        if not tokens:
            return 0
        return round(sum(token.confidence for token in tokens) / len(tokens) * 100)
