# Failure-Aware ML System (Cross-Domain)

## What is this project?

This project is a **Failure-Aware Machine Learning System**.

Instead of blindly trusting ML predictions, this system:

- Checks **how reliable** a prediction is
- Detects **when a model might be wrong**
- Explains **why the prediction failed**
- Sends risky cases to **human review**
- Logs everything in a clean, structured way

This is how real-world ML systems work in industry.

---

## Domains Covered

The same system is applied to **three different domains**:

1. **OCR (Text from images / documents)**
2. **Medical Imaging (X-ray fracture detection)**
3. **Video Understanding (frame + vision-language models)**

Each domain plugs into the same core pipeline.

---

## Why this project matters

Most ML demos only show:
> “Model gives output”

Real companies care about:
- Wrong predictions
- Low confidence
- Edge cases
- Human intervention
- Audit trails

This project focuses on **trust, reliability, and failure handling**.

---

## Project Structure (High Level)

- `core/` → common logic for confidence, failure detection, routing
- `domains/` → OCR, Medical, Video implementations
- `config/` → thresholds, routing rules
- `human_review/` → files sent for manual checking
- `logs/` → structured logs (auto-generated)

---

## How to run (later)

```bash
python main.py
