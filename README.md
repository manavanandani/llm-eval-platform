# LLM Evaluation, Quality & Governance Platform

## Overview

This repository contains a production-grade platform designed to evaluate, benchmark, and govern Large Language Model (LLM) outputs. As GenAI systems become integral to enterprise applications, the lack of systematic evaluation leads to silent failures, regression loops, and untrusted deployments. This platform addresses these challenges by treating evaluation as a core infrastructure component, providing clear quantitative signals on model performance, safety, and cost.

## Problem Statement

Modern Generative AI systems are non-deterministic and fragile. Engineering teams often face significant challenges:
*   **Silent Regressions:** Minor prompt changes or model updates often degrade performance in specific edge cases without detection.
*   **Hallucinations:** Systems may confidently generate incorrect information, damaging trust.
*   **Lack of Visibility:** Metrics regarding cost, latency, and quality are often anecdotal rather than systematic.

This platform solves these issues by enabling rigor and reproducibility in the evaluation process, similar to traditional software integration testing.

## Solution Architecture

The system is architected as a set of modular microservices to ensure scalability and separation of concerns.

```mermaid
graph TD
    User[User / CI Pipeline] -->|Submit Run| API[API Service (FastAPI)]
    API -->|Enqueue Job| Queue[(Redis Message Queue)]
    API -->|Store Metadata| DB[(PostgreSQL)]
    
    subgraph Worker Cluster
        Worker[Celery Evaluator Worker] -->|Fetch Job| Queue
        Worker -->|Inference Call| LLM_Provider[LLM Provider (OpenAI/Anthropic)]
        Worker -->|Compute Metrics| Metric_Engine[Metric Computation Engine]
        Worker -->|Save Results| DB
    end
    
    subgraph Analysis & Governance
        Dashboard[Streamlit Dashboard] -->|Read Metrics| DB
        Human[Human Reviewer] -->|Label/Audit| Dashboard
        CI[CI/CD Gate] -->|Query Pass/Fail| API
    end
```

## Core Features

### 1. Automated Evaluation Engine
The evaluation engine runs a battery of tests against defined "golden datasets" to provide objective quality metrics.
*   **Semantic Similarity:** Uses embedding-based metrics (BERTScore, Cosine Similarity) to measure alignment with reference answers.
*   **LLM-as-a-Judge:** Orchestrates superior models (e.g., GPT-4) to grade outputs from optimization targets on qualitative criteria such as helpfulness, conciseness, and tone.
*   **Structural Validation:** Enforces JSON schemas, regex patterns, and format constraints to ensure downstream system compatibility.

### 2. Regression Testing & Version Control
Track the evolution of system performance over time to prevent degradation.
*   **Prompt & Model Versioning:** Every evaluation run is inextricably linked to a specific configuration snapshot (prompt template + model version + hyperparameters).
*   **Regression Alerts:** Automated logic detects statistically significant drops in key metrics compared to a baseline, triggering alerts or blocking deployments.
*   **Diff Reports:** Detailed side-by-side visualization of input/output pairs changed between versions.

### 3. Human-in-the-Loop (HITL) Review
Integrates human expertise where automated metrics fall short.
*   **Sampling Strategy:** Intelligent sampling routes low-confidence or high-variance outputs to human reviewers.
*   **Feedback Loop:** Human labels (Thumbs Up/Down, Likert Scale) are fed back into the system to fine-tune the "Judge" models and improve the quality of golden datasets.

### 4. Deployment Guardrails
Enforce quality standards before production release.
*   **CI/CD Integration:** API endpoints allow build pipelines to query evaluation results and fail builds if quality thresholds are not met.
*   **Safety & Policy Checks:** Pre-flight checks for PII leakage, toxicity, and adherence to content policies.

## Tech Stack

*   **API & Backend:** Python 3.10+, FastAPI
*   **Task Queue:** Celery, Redis
*   **Database:** PostgreSQL (Relational metadata), ChromaDB (Vector storage for similarity)
*   **Frontend/Dashboard:** Streamlit
*   **Infrastructure:** Docker, Docker Compose

## Getting Started

### Prerequisites
*   Python 3.10 or higher
*   Docker and Docker Compose
*   Access to LLM Provider APIs (OpenAI, Anthropic, or Local)

### Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/manavanandani/llm-eval-platform.git
    cd llm-eval-platform
    ```

2.  Configure environment variables:
    ```bash
    cp .env.example .env
    # Edit .env to include your OPENAI_API_KEY and database credentials
    ```

3.  Start the services using Docker Compose:
    ```bash
    docker-compose up --build -d
    ```

4.  Access the dashboard:
    Navigate to `http://localhost:8501` in your browser.

5.  Access the API documentation:
    Navigate to `http://localhost:8000/docs`.

## Usage Guide

### Defining a Dataset
Upload a CSV or JSONL file containing your test cases. Each record should include an `input_prompt` and optionally an `expected_output` or `reference_context`.

### Running an Evaluation
Submit a POST request to `/api/v1/evaluate/run` with the dataset ID and your prompt configuration. The system will asynchronously process the batch and calculate metrics.

### Analyzing Results
Use the Dashboard to view the "Run Comparison" page. Select your baseline run and your candidate run to see a delta of metrics (e.g., Accuracy: +2.5%, Latency: -100ms).

## License
MIT License. See [LICENSE](LICENSE) for details.
