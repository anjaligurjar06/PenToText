from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.transcription import router as transcription_router


app = FastAPI(
    title="PenToText AI Backend",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(transcription_router)


@app.get("/")
def root():
    return {
        "message": "PenToText AI backend is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }