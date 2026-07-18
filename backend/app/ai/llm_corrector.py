import base64
import io
import json
import os
import re
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
# pyrefly: ignore [missing-import]
from openai import OpenAI
from PIL import Image, ImageEnhance, ImageFilter, ImageOps, UnidentifiedImageError

try:
    # pyrefly: ignore [missing-import]
    from pillow_heif import register_heif_opener
    register_heif_opener()
except ImportError:
    pass

BASE_DIR = Path(__file__).resolve().parents[2]
ENV_PATH = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_PATH, override=True, encoding="utf-8-sig")


def _extract_json(text: str) -> dict[str, Any]:
    if not text or not text.strip():
        raise ValueError("The model returned an empty response.")

    cleaned = re.sub(r"^```(?:json)?\s*", "", text.strip(), flags=re.I)
    cleaned = re.sub(r"\s*```$", "", cleaned)

    try:
        result = json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", cleaned, flags=re.S)
        if not match:
            raise ValueError("The model did not return valid JSON.")
        result = json.loads(match.group(0))

    if not isinstance(result, dict):
        raise ValueError("The model response JSON is not an object.")
    return result


def _ensure_list(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    if value is None:
        return []
    return [value]


def _normalize_corrections(value: Any) -> list[dict[str, Any]]:
    output = []
    for item in _ensure_list(value):
        if not isinstance(item, dict):
            continue
        original = str(item.get("original", "") or "").strip()
        corrected = str(item.get("corrected", "") or "").strip()
        if not original or not corrected:
            continue
        output.append({
            "original": original,
            "corrected": corrected,
            "reason": str(item.get("reason", "") or "Likely OCR recognition error.").strip(),
            "needs_confirmation": bool(item.get("needs_confirmation", False)),
        })
    return output


def _normalize_medicines(value: Any) -> list[dict[str, Any]]:
    output = []
    for item in _ensure_list(value):
        if not isinstance(item, dict):
            continue
        medicine = {
            "name": str(item.get("name", "") or "").strip(),
            "dosage": str(item.get("dosage", "") or "").strip(),
            "frequency": str(item.get("frequency", "") or "").strip(),
            "duration": str(item.get("duration", "") or "").strip(),
            "needs_confirmation": bool(item.get("needs_confirmation", True)),
        }
        if any(medicine[key] for key in ("name", "dosage", "frequency", "duration")):
            output.append(medicine)
    return output


def _image_to_data_url(
    image_path: str,
    max_dimension: int = 2200,
    jpeg_quality: int = 92,
) -> str:
    """Normalize common image formats and return a JPEG data URL."""
    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"Image file not found: {path}")

    try:
        with Image.open(path) as opened:
            try:
                opened.seek(0)
            except EOFError:
                pass
            image = ImageOps.exif_transpose(opened)
            image.load()
    except UnidentifiedImageError as exc:
        raise ValueError(
            "Unsupported or damaged image. Use JPEG, PNG, WEBP, BMP, TIFF, GIF, "
            "or install pillow-heif for HEIC/HEIF."
        ) from exc

    if image.mode in ("RGBA", "LA") or (
        image.mode == "P" and "transparency" in image.info
    ):
        rgba = image.convert("RGBA")
        background = Image.new("RGB", rgba.size, "white")
        background.paste(rgba, mask=rgba.getchannel("A"))
        image = background
    else:
        image = image.convert("RGB")

    if max(image.size) > max_dimension:
        image.thumbnail((max_dimension, max_dimension), Image.Resampling.LANCZOS)

    buffer = io.BytesIO()
    image.save(buffer, format="JPEG", quality=jpeg_quality, optimize=True)
    encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return f"data:image/jpeg;base64,{encoded}"



def _image_variants_to_data_urls(
    image_path: str,
    max_dimension: int = 3200,
) -> list[dict[str, Any]]:
    """
    Create several complementary views for difficult handwriting.

    The vision model receives:
    1. original normalized image
    2. high-contrast grayscale image
    3. sharpened black-and-white image

    Multiple views are often more reliable than sending only one image.
    """
    path = Path(image_path)

    if not path.exists():
        raise FileNotFoundError(f"Image file not found: {path}")

    try:
        with Image.open(path) as opened:
            try:
                opened.seek(0)
            except EOFError:
                pass

            base = ImageOps.exif_transpose(opened)
            base.load()
    except UnidentifiedImageError as exc:
        raise ValueError(
            "Unsupported or damaged image. Use JPEG, PNG, WEBP, BMP, TIFF, "
            "GIF, or install pillow-heif for HEIC/HEIF."
        ) from exc

    if base.mode in ("RGBA", "LA") or (
        base.mode == "P" and "transparency" in base.info
    ):
        rgba = base.convert("RGBA")
        background = Image.new("RGB", rgba.size, "white")
        background.paste(rgba, mask=rgba.getchannel("A"))
        base = background
    else:
        base = base.convert("RGB")

    if max(base.size) > max_dimension:
        base.thumbnail(
            (max_dimension, max_dimension),
            Image.Resampling.LANCZOS,
        )

    grayscale = ImageOps.grayscale(base)
    grayscale = ImageOps.autocontrast(
        grayscale,
        cutoff=1,
    )
    grayscale = ImageEnhance.Contrast(
        grayscale
    ).enhance(1.8)

    sharpened = grayscale.filter(
        ImageFilter.UnsharpMask(
            radius=2,
            percent=180,
            threshold=3,
        )
    )

    # Adaptive-looking global threshold based on median luminance.
    histogram = sharpened.histogram()
    total = sum(histogram)
    cumulative = 0
    median_value = 180

    for index, count in enumerate(histogram):
        cumulative += count
        if cumulative >= total / 2:
            median_value = index
            break

    threshold_value = max(
        110,
        min(210, median_value - 15),
    )

    black_white = sharpened.point(
        lambda value: 255 if value > threshold_value else 0
    )

    variants = [
        ("original", base),
        ("enhanced_grayscale", grayscale.convert("RGB")),
        ("high_contrast", black_white.convert("RGB")),
    ]

    output: list[dict[str, Any]] = []

    for label, image in variants:
        buffer = io.BytesIO()
        image.save(
            buffer,
            format="JPEG",
            quality=95,
            optimize=True,
        )
        encoded = base64.b64encode(
            buffer.getvalue()
        ).decode("utf-8")

        output.append(
            {
                "label": label,
                "data_url": (
                    f"data:image/jpeg;base64,{encoded}"
                ),
            }
        )

    return output


def _build_prompt(
    raw_text: str,
    category: str = "",
    subject: str = "",
    additional_context: str = "",
) -> str:
    return f"""
You are the multimodal handwriting and document-recognition engine for PenToText.

Read the supplied image directly. It may contain neat handwriting, messy handwriting,
cursive text, printed text, screenshots, forms, labels, tables, prescriptions, medical
notes, mixed handwriting and print, shadows, low contrast, mild blur, or rotation.

You will receive multiple versions of the same document: the original,
an enhanced grayscale view, and a high-contrast view. Compare all versions
carefully before deciding each word.

The EasyOCR draft is only a weak hint. Ignore it whenever the handwriting
visible in the images suggests something else.

Category: {category or "Not provided"}
Subject/context: {subject or "Not provided"}
Additional context: {additional_context or "Not provided"}
EasyOCR draft: {raw_text or "No usable OCR draft was produced."}

Tasks:
1. First inspect the entire page, then read it line by line.
2. Compare letter shapes across all supplied image variants.
3. Transcribe every readable word in natural reading order.
4. Preserve meaningful line breaks.
5. Correct OCR errors only when supported by the image or context.
6. Never invent invisible words, medicines, dosages, diagnoses, or facts.
7. For a partly readable word, use [unclear] rather than guessing wildly.
8. Mark uncertain readings as needing confirmation.
9. Extract medicine details only when visibly present.
10. Return one valid JSON object only, without Markdown.

Return exactly:
{{
  "corrected_transcription": "complete transcription from the image",
  "corrections": [
    {{
      "original": "EasyOCR text",
      "corrected": "image-supported correction",
      "reason": "brief reason",
      "needs_confirmation": false
    }}
  ],
  "medicines": [
    {{
      "name": "visible medicine name",
      "dosage": "visible dosage or empty string",
      "frequency": "visible frequency or empty string",
      "duration": "visible duration or empty string",
      "needs_confirmation": true
    }}
  ],
  "warnings": ["unclear, cropped, blurred, rotated, or unreadable area"]
}}

If no medicine is visible, return an empty medicines list. If the image is unreadable,
do not hallucinate. Return only reliable text and add a warning.
""".strip()


def correct_with_llm(
    raw_text: str,
    image_path: str = "",
    category: str = "",
    subject: str = "",
    additional_context: str = "",
    context: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    """Use a vision-capable OpenRouter model to read the image directly."""
    if context and not additional_context:
        additional_context = context

    raw_text = str(raw_text or "").strip()
    image_path = str(image_path or "").strip()
    category = str(category or "").strip()
    subject = str(subject or "").strip()
    additional_context = str(additional_context or "").strip()

    api_key = os.getenv("OPENROUTER_API_KEY", "").strip()
    model = os.getenv(
        "OPENROUTER_VISION_MODEL",
        "google/gemini-2.5-pro",
    ).strip()

    fallback = {
        "corrected_transcription": raw_text,
        "corrections": [],
        "medicines": [],
        "warnings": [],
        "llm_used": False,
        "vision_used": False,
        "llm_model": model,
        "image_variant_count": 0,
    }

    if not api_key:
        fallback["warnings"].append(
            f"OPENROUTER_API_KEY was not found in {ENV_PATH}"
        )
        return fallback

    if "llama-3.3-70b-instruct" in model.lower():
        fallback["warnings"].append(
            "OPENROUTER_VISION_MODEL is set to a text-only model. "
            "Set it to google/gemini-2.5-pro or another image-capable model."
        )
        return fallback

    if not raw_text and not image_path:
        fallback["warnings"].append("No OCR text or image was provided.")
        return fallback

    try:
        client = OpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1",
            default_headers={
                "HTTP-Referer": os.getenv(
                    "OPENROUTER_SITE_URL", "http://127.0.0.1:8000"
                ),
                "X-OpenRouter-Title": os.getenv(
                    "OPENROUTER_APP_NAME", "PenToText"
                ),
            },
            timeout=120.0,
            max_retries=2,
        )

        prompt = _build_prompt(
            raw_text=raw_text,
            category=category,
            subject=subject,
            additional_context=additional_context,
        )

        vision_used = bool(image_path)
        image_variant_count = 0

        if vision_used:
            image_variants = _image_variants_to_data_urls(
                image_path
            )
            image_variant_count = len(image_variants)

            user_content: Any = [
                {
                    "type": "text",
                    "text": prompt,
                }
            ]

            for variant in image_variants:
                user_content.append(
                    {
                        "type": "text",
                        "text": (
                            "Image variant: "
                            f"{variant['label']}"
                        ),
                    }
                )
                user_content.append(
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": variant["data_url"],
                        },
                    }
                )
        else:
            user_content = prompt

        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a reliable multimodal document OCR system. "
                        "Read visible text directly, avoid hallucinations, and "
                        "return valid JSON only."
                    ),
                },
                {"role": "user", "content": user_content},
            ],
            temperature=0,
            max_tokens=3000,
        )

        if not response.choices:
            raise ValueError("OpenRouter returned no response choices.")

        content = response.choices[0].message.content
        if not content:
            raise ValueError("OpenRouter returned an empty message.")

        parsed = _extract_json(content)
        corrected = str(
            parsed.get("corrected_transcription", raw_text) or raw_text
        ).strip()
        warnings = [
            str(item).strip()
            for item in _ensure_list(parsed.get("warnings", []))
            if item is not None and str(item).strip()
        ]

        if not corrected:
            warnings.append("No reliable text could be transcribed from the image.")

        return {
            "corrected_transcription": corrected or raw_text,
            "corrections": _normalize_corrections(parsed.get("corrections", [])),
            "medicines": _normalize_medicines(parsed.get("medicines", [])),
            "warnings": list(dict.fromkeys(warnings)),
            "llm_used": True,
            "vision_used": vision_used,
            "llm_model": getattr(response, "model", None) or model,
            "image_variant_count": image_variant_count,
        }

    except Exception as exc:
        fallback["warnings"].append(
            "OpenRouter vision transcription failed: "
            f"{type(exc).__name__}: {exc}"
        )
        return fallback