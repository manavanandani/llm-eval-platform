from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Integer, Float, ForeignKey, JSON, DateTime, func, Boolean
from sqlalchemy.orm import declarative_base, relationship
import uuid
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/evaldb")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class EvaluationRun(Base):
    __tablename__ = "evaluation_runs"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    model_name = Column(String)
    prompt_template = Column(String)
    avg_accuracy = Column(Float)
    avg_latency = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    results = relationship("EvaluationResult", back_populates="run")

class EvaluationResult(Base):
    __tablename__ = "evaluation_results"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    run_id = Column(String, ForeignKey("evaluation_runs.id"))
    input_text = Column(String)
    output_text = Column(String)
    expected_text = Column(String)
    is_correct = Column(Boolean)
    latency_ms = Column(Float)
    
    run = relationship("EvaluationRun", back_populates="results")

def init_db():
    Base.metadata.create_all(bind=engine)
