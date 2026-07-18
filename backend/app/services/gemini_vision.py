import base64
import json
import urllib.error
import urllib.request
from dataclasses import dataclass

from app.core.config import Settings
from app.models.schemas import ContextMetadata, ImageMetadata
from app.services.prompt_builder import build_transcription_prompt


@dataclass
class GeminiResult:
    text: str
    model: str
    error: str | None = None


def transcribe_with_gemini(
    image_bytes: bytes,
    image: ImageMetadata,
    context: ContextMetadata,
    settings: Settings,
) -> GeminiResult:
    if not settings.gemini_api_key:
        return GeminiResult(text="", model=settings.gemini_model, error="Gemini API key is not configured.")

    if image.content_type == "application/pdf":
        return GeminiResult(text="", model=settings.gemini_model, error="Gemini image mode currently expects an image upload, not PDF.")

    errors: list[str] = []
    for model in _candidate_models(settings):
        result = _call_gemini_model(image_bytes, image, context, settings, model)
        if result.text:
            return result
        if result.error:
            errors.append(f"{model}: {result.error}")

    return GeminiResult(
        text="",
        model=settings.gemini_model,
        error="All Gemini models failed. " + " | ".join(errors),
    )


def _candidate_models(settings: Settings) -> list[str]:
    models = [settings.gemini_model]
    models.extend(
        model.strip()
        for model in settings.gemini_fallback_models.split(",")
        if model.strip()
    )
    deduped: list[str] = []
    for model in models:
        if model not in deduped:
            deduped.append(model)
    return deduped


def _call_gemini_model(
    image_bytes: bytes,
    image: ImageMetadata,
    context: ContextMetadata,
    settings: Settings,
    model: str,
) -> GeminiResult:
    prompt = build_transcription_prompt(context)
    instruction = "\n".join(
        [
            prompt["system"],
            prompt["user"],
            "Read the handwriting in the image.",
            "Return only the final transcription text.",
            "If a word is unclear, write [unclear] instead of guessing.",
            "For prescriptions, preserve medicine names, dosage, frequency, duration, and instructions.",
        ]
    )

    payload = {
        "model": model,
        "input": [
            {"type": "text", "text": instruction},
            {
                "type": "image",
                "data": base64.b64encode(image_bytes).decode("utf-8"),
                "mime_type": image.content_type,
            },
        ],
    }
    request = urllib.request.Request(
        "https://generativelanguage.googleapis.com/v1beta/interactions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "x-goog-api-key": settings.gemini_api_key,
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            body = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        return GeminiResult(text="", model=model, error=f"Gemini HTTP {exc.code}: {detail}")
    except Exception as exc:
        return GeminiResult(text="", model=model, error=f"Gemini request failed: {exc}")

    try:
        data = json.loads(body)
    except json.JSONDecodeError as exc:
        return GeminiResult(text="", model=model, error=f"Gemini returned invalid JSON: {exc}")

    text = _extract_text(data)
    if not text:
        return GeminiResult(text="", model=model, error="Gemini returned no transcription text.")

    return GeminiResult(text=text.strip(), model=model)


def _extract_text(data: dict) -> str:
    if isinstance(data.get("output_text"), str):
        return data["output_text"]

    chunks: list[str] = []
    for candidate in data.get("candidates", []):
        content = candidate.get("content", {})
        for part in content.get("parts", []):
            if isinstance(part.get("text"), str):
                chunks.append(part["text"])

    output = data.get("output")
    if isinstance(output, list):
        for item in output:
            if isinstance(item, dict) and isinstance(item.get("text"), str):
                chunks.append(item["text"])

    return "\n".join(chunk.strip() for chunk in chunks if chunk.strip())
