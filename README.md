🧠 Failure-Aware Generative AI System





📌 Overview

This project implements a Failure-Aware Generative AI Inference System designed to:

Detect unreliable LLM outputs

Quantify uncertainty using structured signals

Route high-risk responses to human review

Support document-based and general question answering

Unlike traditional chatbots, this system prioritizes:

Reliability over fluency
Controlled generation over blind response

🚀 Key Features
🔍 Hybrid Generation Engine

Local LLM inference via Ollama

Retrieval-Augmented Generation (RAG)

General fallback mode

🧪 Uncertainty Modeling

Multi-generation stability detection

Embedding-based semantic grounding validation

Self-critique verification

Composite confidence scoring

📄 Document Intelligence

PDF ingestion

OCR support (images)

Chunked embedding retrieval

Context-aware answering

🏗 Production Architecture

FastAPI backend

Pydantic schemas

Modular service layer

Swagger API documentation

Streamlit thin client

🏛 System Architecture
User Query
    ↓
FastAPI Service
    ↓
Inference Engine
    ↓
LLM (Multiple Generations)
    ↓
Uncertainty Layer
    • Stability
    • Grounding Similarity
    • Self-Critique
    ↓
Composite Confidence
    ↓
Failure Detection
    ↓
Router (Auto Accept / Human Review)
📂 Project Structure
core/               # Failure detection engines
domains/genai/      # LLM, embeddings, retrieval, grounding
ingestion/          # PDF + OCR loaders
api/                # FastAPI backend
ui/                 # Streamlit client
config/             # YAML configuration
human_review/       # Escalation queue
📊 Confidence Model

Confidence is computed as:

Confidence =
    0.3 × Grounding Similarity
  + 0.4 × Stability
  + 0.3 × Self-Critique Pass

Routing threshold:

if Confidence < 0.45 → potential escalation

Note: This is a structured heuristic model, not calibrated probabilistic confidence.

🌐 API Layer
POST /ask
Request
{
  "question": "What is a qubit?",
  "document_path": null
}
Response
{
  "answer": "...",
  "confidence_score": 0.92,
  "grounding_similarity": 0.81,
  "stable": true,
  "failures": [],
  "decision": "auto_accept"
}

Swagger UI:

http://127.0.0.1:8000/docs
🖥 Running The System
1️⃣ Start API
uvicorn api.main:app --reload
2️⃣ Start UI
streamlit run ui/streamlit_app.py
🧠 Design Principles

Separation of concerns (Core / Service / API / UI)

Failure-awareness over blind generation

Modular architecture

Production-style inference service

Explicit uncertainty modeling

⚠ Limitations

Confidence model is heuristic-based

No entropy-based uncertainty yet

No distributed scaling

No containerization (planned)

🔮 Future Work

Risk-based uncertainty scoring

Entropy-based disagreement modeling

CI/CD pipeline

Docker containerization

Observability metrics layer

Cloud deployment