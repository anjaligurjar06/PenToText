import os
from pathlib import Path

from app.ai.llm_corrector import correct_with_llm


IMAGE_PATH = "path/to/your/handwritten_image.jpg"

result = correct_with_llm(
    image_path=IMAGE_PATH,
    raw_text="",
    category="handwritten note",
    subject="general handwritten document",
)

print("Model:", result.get("llm_model"))
print("Vision used:", result.get("vision_used"))
print("Image variants:", result.get("image_variant_count"))
print("Transcription:")
print(result.get("corrected_transcription"))
print("Warnings:")
print(result.get("warnings"))