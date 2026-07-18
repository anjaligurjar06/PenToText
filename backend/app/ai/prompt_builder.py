def build_prompt(
    category: str,
    context: str = "",
    additional_context: str = ""
) -> str:
    base_instructions = """
You are a handwriting transcription assistant.

Instructions:
1. Transcribe only text that is visible in the image.
2. Do not invent missing information.
3. Mark unreadable text as [UNCLEAR].
4. Preserve abbreviations, numbers, dosage values, and units.
5. Return valid JSON only.
"""

    if category == "prescription":
        return f"""
{base_instructions}

Document category: Medical prescription
Patient condition or symptoms: {context}
Additional context: {additional_context}

Return JSON in this format:

{{
  "raw_transcription": "",
  "corrected_transcription": "",
  "medicines": [
    {{
      "name": "",
      "dosage": "",
      "frequency": "",
      "duration": ""
    }}
  ],
  "uncertain_words": []
}}
"""

    if category == "exam":
        return f"""
{base_instructions}

Document category: Exam paper
Subject: {context}
Additional context: {additional_context}

Organize the result by question number.

Return JSON in this format:

{{
  "raw_transcription": "",
  "corrected_transcription": "",
  "questions": [
    {{
      "question_number": "",
      "answer": ""
    }}
  ],
  "uncertain_words": []
}}
"""

    return f"""
{base_instructions}

Document category: {category}
Context: {context}
Additional context: {additional_context}

Return JSON in this format:

{{
  "raw_transcription": "",
  "corrected_transcription": "",
  "uncertain_words": []
}}
"""