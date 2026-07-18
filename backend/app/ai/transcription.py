from typing import Any, Dict, List

import easyocr
import numpy as np


reader = easyocr.Reader(
    ["en"],
    gpu=False
)


def _run_easyocr(image: np.ndarray) -> Dict[str, Any]:
    results = reader.readtext(
        image,
        detail=1,
        paragraph=False
    )

    detected_text: List[str] = []
    uncertain_words: List[str] = []
    ocr_tokens: List[Dict[str, Any]] = []
    confidence_values: List[float] = []

    for _, text, confidence in results:
        cleaned_text = text.strip()

        if not cleaned_text:
            continue

        numeric_confidence = float(confidence)
        needs_review = numeric_confidence < 0.70

        detected_text.append(cleaned_text)
        confidence_values.append(numeric_confidence)

        ocr_tokens.append(
            {
                "text": cleaned_text,
                "confidence": round(numeric_confidence, 2),
                "needs_review": needs_review
            }
        )

        if needs_review:
            uncertain_words.append(cleaned_text)

    raw_transcription = " ".join(detected_text)

    average_confidence = (
        sum(confidence_values) / len(confidence_values)
        if confidence_values
        else 0.0
    )

    return {
        "raw_transcription": raw_transcription,
        "corrected_transcription": raw_transcription,
        "medicines": [],
        "uncertain_words": uncertain_words,
        "ocr_tokens": ocr_tokens,
        "ocr_confidence": round(average_confidence, 2)
    }


def transcribe_document(
    preprocessed_images: Dict[str, np.ndarray],
    prompt: str
) -> Dict[str, Any]:
    """
    Run EasyOCR on several image variants and select the result
    with the highest average OCR confidence.
    """

    candidate_results = []

    for variant_name, image in preprocessed_images.items():
        if variant_name == "blur_score":
            continue

        result = _run_easyocr(image)
        result["image_variant"] = variant_name
        candidate_results.append(result)

    if not candidate_results:
        return {
            "raw_transcription": "",
            "corrected_transcription": "",
            "medicines": [],
            "uncertain_words": [],
            "ocr_tokens": [],
            "ocr_confidence": 0.0,
            "image_variant": None
        }

    best_result = max(
        candidate_results,
        key=lambda item: item.get("ocr_confidence", 0.0)
    )

    return best_result