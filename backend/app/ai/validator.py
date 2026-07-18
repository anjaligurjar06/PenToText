from typing import List


def validate_image(preprocessing_result: dict) -> dict:
    warnings: List[str] = []

    blur_score = preprocessing_result["blur_score"]

    if blur_score < 50:
        warnings.append("The image appears very blurry.")

    elif blur_score < 100:
        warnings.append("The image is slightly blurry.")

    return {
        "is_valid": blur_score >= 30,
        "blur_score": blur_score,
        "warnings": warnings
    }