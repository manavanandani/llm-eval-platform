from fastapi import FastAPI
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Load models, connect DB
    yield
    # Shutdown: Close connections

app = FastAPI(
    title="LLM Evaluation Platform",
    description="API for managing datasets, running evaluations, and tracking metrics.",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "eval-api"}

@app.post("/api/v1/evaluate/run")
def start_evaluation_run(payload: dict):
    """
    Trigger an asynchronous evaluation run for a specific prompt/model version.
    """
    # Logic: Validate payload -> Create Run ID -> Enqueue Celery Task
    return {"run_id": "mock-run-id", "status": "queued"}
