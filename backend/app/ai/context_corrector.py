from typing import Dict


def correct_with_context(
    raw_text: str,
    category: str,
    context: str = "",
    additional_context: str = ""
) -> Dict:
    """
    Temporary rule-based correction layer.

    This will later be replaced by an LLM/VLM call.
    """

    corrected_text = raw_text.strip()

    replacements = {
        "thibat": "throat",
        "sbub": "swab",
        "thvat": "throat"
    }

    words = corrected_text.split()
    corrected_words = []

    corrections = []

    for word in words:
        clean_word = word.lower().strip(".,;:")

        if clean_word in replacements:
            replacement = replacements[clean_word]

            corrected_words.append(replacement)

            corrections.append(
                {
                    "original": word,
                    "suggestion": replacement,
                    "needs_confirmation": True
                }
            )
        else:
            corrected_words.append(word)

    corrected_text = " ".join(corrected_words)

    return {
        "corrected_transcription": corrected_text,
        "corrections": corrections
    }