from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .config import CORS_ORIGINS
from .database import Base, engine
from .routers import auth, documents
from app.api.transcription import router as transcription_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="PenToText AI Backend",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(documents.router)
app.include_router(transcription_router)


@app.get("/")
def root():
    return {
        "message": "PenToText AI backend is running"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }