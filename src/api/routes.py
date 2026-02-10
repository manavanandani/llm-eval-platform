from fastapi import APIRouter
from pydantic import BaseModel
from src.worker import run_evaluation_task
import uuid

router = APIRouter()

class EvalRequest(BaseModel):
    model_name: str
    prompt_template: str

@router.post("/evaluate/run")
def trigger_eval(req: EvalRequest):
    run_id = str(uuid.uuid4())
    # Trigger Async Task
    run_evaluation_task.delay(run_id, req.model_name, req.prompt_template)
    return {"run_id": run_id, "status": "queued"}
