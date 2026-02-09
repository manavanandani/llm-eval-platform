# LLM Evaluation, Quality & Governance Platform

## Overview

A robust, enterprise-grade platform designed to evaluate, benchmark, and govern Large Language Model (LLM) outputs. This system addresses the critical problem of "silent failure" in GenAI applications by providing automated metrics, regression detection, and human-in-the-loop review workflows. It ensures that model updates, prompt changes, and RAG pipeline modifications effectively improve quality without introducing hallucinations or safety violations.

This platform treats LLM evaluation as infrastructure, not an afterthought, mirroring the rigor found in FAANG-scale ML systems.

## Core Problem Statement

Modern GenAI systems are non-deterministic and fragile. Engineering teams often struggle to answer fundamental questions:
- Is output quality improving or degrading after a prompt change?
- Are hallucinations increasing with the new model version?
- Is the system remaining cost-effective and low-latency?

Without systematic evaluation, teams rely on "vibe checks," leading to production failures, regression loops, and untrusted AI applications. This platform provides the quantitative signal needed to deploy GenAI with confidence.

## Features

### 1. Automated Evaluation Engine
The heart of the system is a flexible evaluation engine that runs a battery of tests against golden datasets.
- **Auto-Metrics**: Semantic similarity (BERTScore, cosine similarity), exact match, and regex-based structural validation.
- **LLM-as-a-Judge**: Uses superior models (e.g., GPT-4) to score outputs from smaller/faster models on criteria like "helpfulness," "conciseness," and "safety."
- **Hallucination Detection**: specialized evaluators to check for factual consistency against source contexts.

### 2. Regression Testing & Version Control
Track the performance evolution of your GenAI system over time.
- **Versioned Prompts & Models**: Every run is linked to a specific unique combination of prompt template, model version, and hyperparameters (temperature, top-p).
- **Regression Alerts**: Automatically flag when a new deployment causes a metric (e.g., accuracy) to drop below a defined baseline.
- **Diff Reports**: Side-by-side comparison of outputs to visualize exactly what changed between two versions.

### 3. Human-in-the-Loop (HITL) Review
Recognizing that automated metrics aren't perfect, the platform integrates human review as a first-class citizen.
- **Sampling & labeling**: Route low-confidence or randomly sampled outputs to human experts for "thumbs up/down" or scalar grading.
- **Feedback Loop**: Use human labels to calibrated automated judges and improve golden datasets.

### 4. Deployment Guardrails
Prevent bad updates from ever reaching production.
- **Quality Gates**: CI/CD integration that blocks deployments if evaluation scores fail to meet thresholds.
- **Safety Checks**: Pre-flight checks for PII leakage, toxicity, and policy violations.

## Architecture

The system is built as a modular microservices architecture, designed for scalability and extensibility.

- **API Service (FastAPI)**: REST endpoints for submitting evaluation runs, retrieving results, and managing datasets.
- **Evaluation Workers (Celery/Python)**: Async workers that process batches of prompts, call LLM providers, and compute metrics.
- **Metadata Store (PostgreSQL)**: Relational storage for runs, metrics, prompt versions, and user feedback.
- **Vector Store (ChromaDB/FAISS)**: Optional storage for semantic similarity checks.
- **Frontend (Streamlit/React)**: Dashboard for visualizing regression trends, comparing versions, and performing human review.

## Metrics & KPIs

We track a comprehensive set of metrics to give a 360-degree view of system health:
- **Correctness**: Alignment with golden answers.
- **Hallucination Rate**: Percentage of unsupported claims.
- **Latency p95**: Tail latency tracking to ensure valid UX.
- **Cost per Run**: Token usage and estimated spend tracking.

## Getting Started

### Prerequisites
- Python 3.10+
- Docker & Docker Compose
- API Keys for LLM Providers (OpenAI, Anthropic, etc.)

### Installation
1. Clone the repository.
   ```bash
   git clone https://github.com/manavanandani/llm-eval-platform.git
   cd llm-eval-platform
   ```
2. Set up environment variables.
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```
3. Run with Docker Compose.
   ```bash
   docker-compose up --build
   ```

## Roadmap

- [ ] **Phase 1**: Core Evaluation Engine & Metrics (Semantic Similarity, Exact Match).
- [ ] **Phase 2**: dataset Management & Versioning.
- [ ] **Phase 3**: LLM-as-a-Judge Implementation.
- [ ] **Phase 4**: Human Review Interface & Feedback Loop.
- [ ] **Phase 5**: CI/CD Integration (GitHub Actions for Quality Gates).

## License

MIT License. See [LICENSE](LICENSE) for details.
