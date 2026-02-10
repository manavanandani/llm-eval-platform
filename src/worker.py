from celery import Celery
import os
import time
import random
from src.database.models import SessionLocal, EvaluationRun, EvaluationResult

celery_app = Celery(
    "eval_worker",
    broker=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
    backend=os.getenv("REDIS_URL", "redis://localhost:6379/0")
)

# Mock Golden Dataset
DATASET = [
    {"input": "What is 2+2?", "expected": "4"},
    {"input": "Capital of France?", "expected": "Paris"},
    {"input": "Who wrote Hamlet?", "expected": "Shakespeare"},
]

@celery_app.task
def run_evaluation_task(run_id: str, model_name: str, prompt_template: str):
    """
    Worker task that simulates running an evaluation suite.
    """
    db = SessionLocal()
    try:
        run = EvaluationRun(id=run_id, model_name=model_name, prompt_template=prompt_template)
        db.add(run)
        
        total_latency = 0
        correct_count = 0
        
        for case in DATASET:
            # Simulate LLM Call
            start = time.time()
            time.sleep(random.uniform(0.1, 0.5)) # Latency
            latency_ms = (time.time() - start) * 1000
            total_latency += latency_ms
            
            # Simulate Output (80% chance of being correct)
            is_correct = random.random() > 0.2
            output = case["expected"] if is_correct else "Wrong Answer"
            
            result = EvaluationResult(
                run_id=run.id,
                input_text=case["input"],
                output_text=output,
                expected_text=case["expected"],
                is_correct=is_correct,
                latency_ms=latency_ms
            )
            db.add(result)
            if is_correct:
                correct_count += 1
        
        # Update Run Summary
        run.avg_accuracy = correct_count / len(DATASET)
        run.avg_latency = total_latency / len(DATASET)
        db.commit()
        
        return {"run_id": run.id, "accuracy": run.avg_accuracy}
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
