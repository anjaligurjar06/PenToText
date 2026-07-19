import re
import json
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageEnhance, ImageOps, UnidentifiedImageError

from app.core.config import Settings
from app.models.schemas import ImageMetadata


@dataclass
class OCRResult:
    text: str
    provider: str
    used_fallback: bool
    confidence: float | None = None
    error: str | None = None


def recognize_text(image_bytes: bytes, image: ImageMetadata, settings: Settings) -> OCRResult:
    if image.content_type == "application/pdf":
        return OCRResult(
            text="",
            provider=settings.ocr_provider,
            used_fallback=True,
            error="PDF OCR requires page-to-image conversion, which is not implemented yet.",
        )

    try:
        processed = _preprocess_for_ocr(image_bytes)
    except UnidentifiedImageError as exc:
        return OCRResult(
            text="",
            provider=settings.ocr_provider,
            used_fallback=True,
            error=f"Could not read image for OCR: {exc}",
        )

    with tempfile.TemporaryDirectory(prefix="pentotext-ocr-") as tmp_dir:
        image_path = Path(tmp_dir) / "input.png"
        processed.save(image_path, format="PNG")

        if settings.ocr_provider in {"auto", "easyocr"}:
            easyocr_result = _run_easyocr(image_path, settings.easyocr_python_cmd)
            if easyocr_result.text and _looks_readable(easyocr_result.text, easyocr_result.confidence):
                return easyocr_result
            if settings.ocr_provider == "easyocr":
                return easyocr_result

        tesseract_result = _run_tesseract(image_path, settings.tesseract_cmd)
        if tesseract_result.text and _looks_readable(tesseract_result.text, tesseract_result.confidence):
            return tesseract_result

        if tesseract_result.text:
            return OCRResult(
                text="",
                provider=tesseract_result.provider,
                used_fallback=True,
                confidence=tesseract_result.confidence,
                error="OCR text was recognized, but it appears too low quality to trust. Try a clearer image or a vision model.",
            )

        return tesseract_result


def _run_easyocr(image_path: Path, python_cmd: str) -> OCRResult:
    script = (
        "import easyocr,json,sys;"
        "reader=easyocr.Reader(['en'], gpu=False, verbose=False);"
        "items=reader.readtext(sys.argv[1], detail=1, paragraph=False);"
        "print(json.dumps([{'text':str(i[1]),'confidence':float(i[2])} for i in items]))"
    )

    try:
        completed = subprocess.run(
            [python_cmd, "-c", script, str(image_path)],
            check=False,
            capture_output=True,
            text=True,
            timeout=120,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return OCRResult(
            text="",
            provider="easyocr",
            used_fallback=True,
            error=f"EasyOCR failed to run: {exc}",
        )

    if completed.returncode != 0:
        return OCRResult(
            text="",
            provider="easyocr",
            used_fallback=True,
            error=completed.stderr.strip() or "EasyOCR failed.",
        )

    try:
        items = json.loads(completed.stdout or "[]")
    except json.JSONDecodeError as exc:
        return OCRResult(
            text="",
            provider="easyocr",
            used_fallback=True,
            error=f"EasyOCR returned invalid JSON: {exc}",
        )

    lines = [str(item.get("text", "")).strip() for item in items if str(item.get("text", "")).strip()]
    confidences = [float(item.get("confidence", 0.0)) for item in items if item.get("confidence") is not None]
    text = _clean_ocr_text("\n".join(lines))
    confidence = sum(confidences) / len(confidences) if confidences else None

    return OCRResult(
        text=text,
        provider="easyocr",
        used_fallback=not bool(text),
        confidence=round(confidence, 3) if confidence is not None else None,
        error=None if text else "EasyOCR returned no readable text.",
    )


def _run_tesseract(image_path: Path, configured_cmd: str) -> OCRResult:
    tesseract_cmd = _resolve_tesseract_cmd(configured_cmd)
    if not tesseract_cmd:
        return OCRResult(
            text="",
            provider="tesseract",
            used_fallback=True,
            error="Tesseract executable was not found.",
        )

    try:
        cmd = [
            tesseract_cmd,
            str(image_path),
            "stdout",
            "--oem",
            "3",
            "--psm",
            "6",
            "-l",
            "eng",
        ]
        completed = subprocess.run(
            cmd,
            check=False,
            capture_output=True,
            text=True,
            timeout=30,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return OCRResult(
            text="",
            provider="tesseract",
            used_fallback=True,
            error=f"Tesseract failed to run: {exc}",
        )

    if completed.returncode != 0:
        return OCRResult(
            text="",
            provider="tesseract",
            used_fallback=True,
            error=completed.stderr.strip() or "Tesseract OCR failed.",
        )

    text = _clean_ocr_text(completed.stdout)
    return OCRResult(
        text=text,
        provider="tesseract",
        used_fallback=not bool(text),
        confidence=None,
        error=None if text else "Tesseract returned no readable text.",
    )


def _resolve_tesseract_cmd(configured_cmd: str) -> str | None:
    configured_path = Path(configured_cmd)
    if configured_path.exists():
        return str(configured_path)

    from_path = shutil.which(configured_cmd)
    if from_path:
        return from_path

    known_windows_path = Path.home() / "Downloads" / "TESSERACT" / "tesseract.exe"
    if known_windows_path.exists():
        return str(known_windows_path)

    return None


def _preprocess_for_ocr(image_bytes: bytes) -> Image.Image:
    with Image.open(BytesIO(image_bytes)) as source:
        image = ImageOps.exif_transpose(source).convert("RGB")

    image = _resize_for_ocr(image)
    image = ImageOps.grayscale(image)
    image = ImageOps.autocontrast(image)
    image = ImageEnhance.Contrast(image).enhance(1.8)
    image = ImageEnhance.Sharpness(image).enhance(1.4)
    return image


def _resize_for_ocr(image: Image.Image) -> Image.Image:
    width, height = image.size
    longest = max(width, height)
    if longest < 1400:
        scale = 1400 / longest
        return image.resize((round(width * scale), round(height * scale)))
    if longest > 2600:
        scale = 2600 / longest
        return image.resize((round(width * scale), round(height * scale)))
    return image


def _clean_ocr_text(text: str) -> str:
    lines = []
    for line in text.splitlines():
        line = re.sub(r"\s+", " ", line).strip()
        if line:
            lines.append(line)
    return "\n".join(lines)


def _looks_readable(text: str, confidence: float | None) -> bool:
    words = re.findall(r"[A-Za-z]{2,}", text)
    if len(words) < 3:
        return False

    weird_chars = len(re.findall(r"[^A-Za-z0-9\s.,:;()/-]", text))
    if weird_chars / max(len(text), 1) > 0.08:
        return False

    common_words = {
        "the", "and", "for", "with", "patient", "continue", "take", "daily",
        "days", "week", "weeks", "follow", "up", "medicine", "tablet", "capsule",
        "dosage", "dose", "doctor", "clinic", "fever", "pain", "throat", "cough",
        "infection", "prescription", "question", "answer", "notes", "class",
    }
    normalized_words = [word.lower() for word in words]
    common_hits = sum(1 for word in normalized_words if word in common_words)
    long_enough = sum(1 for word in normalized_words if len(word) >= 4)
    language_score = (common_hits + long_enough * 0.35) / len(normalized_words)

    if confidence is None:
        return language_score >= 0.28

    return confidence >= 0.25 and language_score >= 0.18
