from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.api.routes import router as eval_router
from src.database.models import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create Tables
    init_db()
    yield

app = FastAPI(
    title="LLM Evaluation Platform",
    description="API for managing datasets, running evaluations, and tracking metrics.",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(eval_router, prefix="/api/v1")

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "eval-api"}
