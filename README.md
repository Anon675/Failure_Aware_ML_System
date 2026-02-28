# 🧠 Failure-Aware Generative AI System

## 1. Problem Statement

Modern generative AI systems often produce fluent outputs that may be:

- Ungrounded  
- Hallucinated  
- Internally inconsistent  
- Overconfident  

This project implements a **failure-aware generative inference system** designed to:

1. Detect unreliable model outputs  
2. Quantify uncertainty via structured signals  
3. Route high-risk responses to human review  
4. Support document-based and general question answering  

The system prioritizes **controlled deployment of generative models**, not unrestricted chatbot behavior.

---

## 2. System Capabilities

- Local LLM inference (Ollama-based)
- Retrieval-Augmented Generation (RAG)
- PDF ingestion
- OCR ingestion (image-based text extraction)
- Embedding-based semantic grounding validation
- Multi-generation stability detection
- Self-critique evaluation
- Composite confidence scoring
- Structured failure logging
- Human review routing
- FastAPI production backend
- Streamlit thin client interface

---

## 3. High-Level Architecture

```text
User Query
    ↓
FastAPI Service Layer
    ↓
Inference Service
    ↓
LLM Generation (Multiple Runs)
    ↓
Uncertainty Layer
    • Stability Analysis
    • Grounding Similarity
    • Self-Critique Validation
    ↓
Composite Confidence Score
    ↓
Failure Detector
    ↓
Router
    • Auto Accept
    • Human Review
```

---

## 4. Project Structure

```text
core/
├── stability_engine.py
├── failure_detector.py
├── failure_reasoner.py
├── router.py
└── logger.py

domains/genai/
├── llm_model.py
├── embedding_model.py
├── retriever.py
├── grounding.py
├── self_critique.py
└── prompt_builder.py

ingestion/
├── pdf_loader.py
├── image_loader.py
└── text_splitter.py

api/
├── main.py
├── routers/
├── services/
└── schemas/

ui/
└── streamlit_app.py

config/
└── genai_rag.yaml

human_review/
└── queue/
```

---

## 5. Uncertainty Modeling Strategy

This system does **not** rely on token-level probabilities (which are often unavailable in local LLM deployments).

Instead, it computes uncertainty using structured signals:

### 5.1 Multi-Generation Stability

The same prompt is generated multiple times.

If outputs diverge:
- `stable = False`
- Confidence decreases

---

### 5.2 Semantic Grounding Similarity

Cosine similarity is computed between:

- Generated answer embedding  
- Retrieved document embeddings  

Low similarity → weak grounding signal.

---

### 5.3 Self-Critique Evaluation

The model is prompted to evaluate its own output.

If critique returns:

```
UNSAFE
```

The output is flagged for escalation.

---

## 6. Composite Confidence Model

```text
Confidence =
    0.3 × Grounding Similarity
  + 0.4 × Stability
  + 0.3 × Self-Critique Pass
```

Routing threshold:

```text
If Confidence < 0.45 → escalate to human review
```

> Note:  
> This is a heuristic composite model, not a calibrated probabilistic confidence estimator.

---

## 7. Routing Logic

Outputs are routed based on:

- Low composite confidence  
- Explicit critique failure  
- Structured failure signals  

Possible decisions:

- `auto_accept`
- `human_review`

Escalated cases are stored in:

```text
human_review/queue/
```

---

## 8. Document Ingestion Pipeline

Supported formats:

- PDF  
- PNG / JPG (OCR-based extraction)

Processing pipeline:

```text
Document
    ↓
Text Extraction
    ↓
Chunking
    ↓
Embedding
    ↓
Vector Retrieval
    ↓
RAG Context Injection
```

If no document is provided, the system operates in hybrid general Q&A mode.

---

## 9. API Layer

FastAPI exposes:

```http
POST /ask
```

### Request

```json
{
  "question": "What is a qubit?",
  "document_path": null
}
```

### Response

```json
{
  "answer": "...",
  "confidence_score": 0.92,
  "grounding_similarity": 0.81,
  "stable": true,
  "failures": [],
  "decision": "auto_accept"
}
```

Swagger UI available at:

```
http://127.0.0.1:8000/docs
```

---

## 10. Running The System

### Start API

```bash
uvicorn api.main:app --reload
```

### Start UI

```bash
streamlit run ui/streamlit_app.py
```

---

## 11. Design Principles

This project emphasizes:

- Failure detection over blind generation  
- Explicit uncertainty modeling  
- Service-layer separation  
- Modular architecture  
- Deployment-oriented structure  

It is not optimized for:

- Maximum creative generation  
- Ultra-low latency  
- Fully calibrated probabilistic uncertainty  

---

## 12. Limitations

- Confidence model is heuristic-based  
- No entropy-based uncertainty modeling yet  
- No distributed scaling layer  
- No containerization (planned)  

---

## 13. Future Work

- Risk-based uncertainty scoring  
- Entropy-based generation disagreement metrics  
- Model versioning  
- CI/CD pipeline  
- Docker containerization  
- Observability (metrics + monitoring dashboards)  

---

## 14. Positioning

This project demonstrates:

- Applied ML system architecture  
- Generative AI orchestration  
- Uncertainty-aware deployment logic  
- Backend service engineering  
- Failure-aware routing strategy  

It serves as a bridge between:

- Applied ML Engineering  
- MLOps Foundations  
- Reliable Generative AI Infrastructure  