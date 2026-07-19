from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "PenToText API"
    api_prefix: str = "/api"
    max_upload_bytes: int = 20 * 1024 * 1024
    low_confidence_threshold: float = 0.78
    ai_provider: str = "local"
    ai_model: str = "vision-model-placeholder"
    gemini_api_key: str = ""
    gemini_model: str = "gemini-3.5-flash"
    gemini_fallback_models: str = "gemini-3.1-flash-lite,gemini-2.5-flash-lite,gemini-flash-latest"
    ocr_provider: str = "auto"
    tesseract_cmd: str = "tesseract"
    easyocr_python_cmd: str = "python"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="PENTOTEXT_",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
