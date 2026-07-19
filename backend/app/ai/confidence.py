from typing import Dict, List


def build_token_confidence(
    text: str,
    uncertain_words: List[str]
) -> List[Dict]:
    tokens = []

    uncertain_lower = {
        word.lower()
        for word in uncertain_words
    }

    for word in text.split():
        clean_word = word.strip(".,;:!?").lower()

        needs_review = clean_word in uncertain_lower

        tokens.append(
            {
                "text": word,
                "confidence": 0.55 if needs_review else 0.92,
                "needs_review": needs_review
            }
        )

    return tokens


def calculate_overall_confidence(tokens: List[Dict]) -> float:
    if not tokens:
        return 0.0

    total = sum(token["confidence"] for token in tokens)
    return round(total / len(tokens), 2)