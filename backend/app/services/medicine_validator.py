from difflib import SequenceMatcher
from functools import lru_cache
from pathlib import Path

from app.models.schemas import MedicineValidation


DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "drug_names.txt"


@lru_cache
def load_drug_names() -> list[str]:
    if not DATA_FILE.exists():
        return []
    return [
        line.strip()
        for line in DATA_FILE.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    ]


def _similarity(left: str, right: str) -> float:
    return SequenceMatcher(None, left.lower(), right.lower()).ratio()


def validate_medicine_name(name: str | None) -> MedicineValidation | None:
    if not name:
        return None

    candidates = load_drug_names()
    if not candidates:
        return MedicineValidation(original=name, score=0.0, status="unmatched")

    best_name = max(candidates, key=lambda candidate: _similarity(name, candidate))
    score = _similarity(name, best_name)

    if score >= 0.92:
        status = "matched"
    elif score >= 0.75:
        status = "suggested"
    else:
        status = "unmatched"

    return MedicineValidation(
        original=name,
        matched_name=best_name if status != "unmatched" else None,
        score=round(score, 3),
        status=status,
    )

