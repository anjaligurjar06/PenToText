from app.ai.confidence import (
    build_token_confidence,
    calculate_overall_confidence,
)
from app.ai.extractor import extract_medicines
from app.ai.llm_corrector import correct_with_llm
from app.ai.preprocessing import preprocess_image
from app.ai.prompt_builder import build_prompt
from app.ai.transcription import transcribe_document
from app.ai.validator import validate_image


def process_document(
    image_path: str,
    category: str,
    context: str = "",
    additional_context: str = "",
) -> dict:
    """
    Run the complete PenToText AI pipeline.

    Flow:
    1. Preprocess the uploaded image.
    2. Validate image quality.
    3. Build a context-aware prompt.
    4. Run EasyOCR on multiple image variants.
    5. Correct OCR text using OpenRouter.
    6. Extract structured prescription fields.
    7. Calculate confidence values.
    8. Return a frontend-ready JSON response.
    """

    normalized_category = str(category or "").strip().lower()
    context = str(context or "").strip()
    additional_context = str(additional_context or "").strip()

    # ---------------------------------------------------------
    # Step 1: Preprocess image
    # ---------------------------------------------------------

    preprocessing_result = preprocess_image(image_path)

    # ---------------------------------------------------------
    # Step 2: Validate image quality
    # ---------------------------------------------------------

    validation_result = validate_image(preprocessing_result)

    if not validation_result.get("is_valid", False):
        return {
            "success": False,
            "error": "Image quality is too poor for transcription.",
            "warnings": validation_result.get("warnings", []),
        }

    # ---------------------------------------------------------
    # Step 3: Build document-specific prompt
    # ---------------------------------------------------------

    prompt = build_prompt(
        category=normalized_category,
        context=context,
        additional_context=additional_context,
    )

    # ---------------------------------------------------------
    # Step 4: Run EasyOCR
    # ---------------------------------------------------------

    transcription_result = transcribe_document(
        preprocessed_images=preprocessing_result,
        prompt=prompt,
    )

    raw_text = str(
        transcription_result.get(
            "raw_transcription",
            "",
        )
        or ""
    ).strip()

    uncertain_words = transcription_result.get(
        "uncertain_words",
        [],
    )

    # ---------------------------------------------------------
    # Step 5: Correct OCR text using OpenRouter
    # ---------------------------------------------------------

    correction_result = correct_with_llm(
        raw_text=raw_text,
        category=normalized_category,
        subject=context,
        additional_context=additional_context,
    )

    corrected_text = str(
        correction_result.get(
            "corrected_transcription",
            raw_text,
        )
        or raw_text
    ).strip()

    corrections = correction_result.get(
        "corrections",
        [],
    )

    # ---------------------------------------------------------
    # Step 6: Handle OCR token confidence
    # ---------------------------------------------------------

    ocr_tokens = transcription_result.get(
        "ocr_tokens",
        [],
    )

    if ocr_tokens:
        tokens = ocr_tokens
    else:
        tokens = build_token_confidence(
            corrected_text,
            uncertain_words,
        )

    overall_confidence = calculate_overall_confidence(
        tokens
    )

    # ---------------------------------------------------------
    # Step 7: Extract structured prescription fields
    # ---------------------------------------------------------

    medicines = correction_result.get(
        "medicines",
        [],
    )

    # Use regex extraction only when the LLM found no medicines.
    if (
        normalized_category == "prescription"
        and not medicines
    ):
        extraction_input = {
            **transcription_result,
            "corrected_transcription": corrected_text,
        }

        medicines = extract_medicines(
            extraction_input
        )

    # ---------------------------------------------------------
    # Step 8: Build warnings
    # ---------------------------------------------------------

    warnings = list(
        validation_result.get(
            "warnings",
            [],
        )
    )

    warnings.extend(
        correction_result.get(
            "warnings",
            [],
        )
    )

    if not raw_text:
        warnings.append(
            "No readable text was detected in the image."
        )

    if uncertain_words:
        warnings.append(
            f"{len(uncertain_words)} text segment(s) require review."
        )

    # Remove duplicate warning messages while preserving order.
    warnings = list(dict.fromkeys(warnings))

    # ---------------------------------------------------------
    # Step 9: Return final response
    # ---------------------------------------------------------

    return {
        "success": True,
        "document_type": normalized_category,
        "raw_transcription": raw_text,
        "corrected_transcription": corrected_text,
        "corrections": corrections,
        "tokens": tokens,
        "medicines": medicines,
        "overall_confidence": overall_confidence,
        "ocr_confidence": transcription_result.get(
            "ocr_confidence",
            overall_confidence,
        ),
        "image_variant": transcription_result.get(
            "image_variant"
        ),
        "llm_used": correction_result.get(
            "llm_used",
            False,
        ),
        "llm_model": correction_result.get(
            "llm_model"
        ),
        "warnings": warnings,
    }