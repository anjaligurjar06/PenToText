import re
from typing import Dict, List


DOSAGE_PATTERN = re.compile(
    r"\b\d+(?:\.\d+)?\s?(?:mg|g|mcg|ml)\b",
    re.IGNORECASE
)

FREQUENCY_PATTERN = re.compile(
    r"\b(?:once daily|twice daily|three times daily|"
    r"od|bd|bid|tds|tid|qid)\b",
    re.IGNORECASE
)

DURATION_PATTERN = re.compile(
    r"\b(?:for\s+)?\d+\s+(?:day|days|week|weeks)\b",
    re.IGNORECASE
)


def extract_medicines(
    transcription_result: Dict
) -> List[Dict[str, str]]:
    text = transcription_result.get(
        "corrected_transcription",
        transcription_result.get("raw_transcription", "")
    )

    dosage_match = DOSAGE_PATTERN.search(text)
    frequency_match = FREQUENCY_PATTERN.search(text)
    duration_match = DURATION_PATTERN.search(text)

    if not any(
        [dosage_match, frequency_match, duration_match]
    ):
        return []

    return [
        {
            "name": "",
            "dosage": (
                dosage_match.group(0)
                if dosage_match
                else ""
            ),
            "frequency": (
                frequency_match.group(0)
                if frequency_match
                else ""
            ),
            "duration": (
                duration_match.group(0)
                if duration_match
                else ""
            )
        }
    ]