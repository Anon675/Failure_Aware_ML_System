import argparse
import yaml
import os

# Core
from core.stability_engine import StabilityEngine
from core.failure_detector import FailureDetector
from core.failure_reasoner import FailureReasoner
from core.router import Router
from core.logger import SystemLogger

# GenAI
from domains.genai.llm_model import LLMModel
from domains.genai.preprocess import preprocess
from domains.genai.signals import extract_signals
from domains.genai.embedding_model import EmbeddingModel
from domains.genai.retriever import Retriever
from domains.genai.grounding import check_grounding
from domains.genai.self_critique import SelfCritique

# Ingestion
from ingestion.pdf_loader import load_pdf
from ingestion.image_loader import load_image_text
from ingestion.text_splitter import split_text


def load_yaml(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)


def main():
    parser = argparse.ArgumentParser("Failure-Aware Document Assistant v3.5")
    parser.add_argument("--input", required=True, help="Question")
    parser.add_argument("--doc", required=False, help="Optional document path")
    args = parser.parse_args()

    config = load_yaml("config/genai_rag.yaml")["genai_rag"]

    stability_engine = StabilityEngine()
    failure_detector = FailureDetector()
    failure_reasoner = FailureReasoner()
    router = Router()
    logger = SystemLogger()

    embedding_model = EmbeddingModel()
    model = LLMModel(config["model_name"])
    critique_engine = SelfCritique()

    query = preprocess(args.input)

    # -------- Document Ingestion --------
    documents = []

    if args.doc:
        ext = os.path.splitext(args.doc)[1].lower()

        if ext == ".pdf":
            raw_text = load_pdf(args.doc)
        elif ext in [".png", ".jpg", ".jpeg"]:
            raw_text = load_image_text(args.doc)
        else:
            print("Unsupported file type.")
            return

        documents = split_text(raw_text)

    # If no doc provided → general assistant mode
    if not documents:
        documents = [""]  # dummy

    retriever = Retriever(embedding_model, documents)
    retrieved_docs = retriever.retrieve(query, config["top_k"])

    context_block = "\n\n".join(retrieved_docs)

    max_retries = 2
    attempt = 0

    while attempt <= max_retries:

        prompt = f"""
You are a document-aware assistant.

If document context is relevant, use it.
Otherwise answer normally.

Context:
{context_block}

Question:
{query}

Answer clearly:
"""

        predictions = []

        for _ in range(config["num_generations"]):
            text = model.generate(prompt, config["temperature"])
            predictions.append(text)

        final_prediction = predictions[0]
        stable = stability_engine.is_stable(predictions)

        grounding_result = check_grounding(
            final_prediction,
            retrieved_docs,
            embedding_model
        )

        critique_result = critique_engine.evaluate(
            model,
            query,
            final_prediction,
            context_block
        )

        confidence_score = (
            0.3 * grounding_result["similarity"] +
            0.4 * (1.0 if stable else 0.0) +
            0.3 * (1.0 if critique_result["is_safe"] else 0.0)
        )

        base_failures = failure_detector.detect(
            inference_result={"error": None},
            confidence_result={"is_low": confidence_score < 0.45},
            domain_signals=extract_signals(final_prediction)
        )

        failures = base_failures

        if not critique_result["is_safe"]:
            failures.append("self_critique_failed")

        if not failures:
            break

        attempt += 1

    explanations = failure_reasoner.explain(failures)

    log_record = {
        "domain": "document_genai_v3.5",
        "input": query,
        "document_used": bool(args.doc),
        "confidence_score": confidence_score,
        "grounding_similarity": grounding_result["similarity"],
        "stable": stable,
        "attempts": attempt,
        "failures": failures,
        "explanations": explanations
    }

    decision = router.route(failures, log_record)
    log_record["decision"] = decision

    logger.log(log_record)

    print("\n--- RESULT (Document-Aware GenAI v3.5) ---")
    print("Decision:", decision)
    print("Confidence Score:", round(confidence_score, 3))
    print("Failures:", failures)
    print("\nAnswer:\n", final_prediction)


if __name__ == "__main__":
    main()
