from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .config import CORS_ORIGINS
from .database import Base, engine
from .routers import auth, documents

Base.metadata.create_all(bind=engine)

app = FastAPI(title="PenToText API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(documents.router)


@app.get("/health")
def health():
    return {"status": "ok"}
