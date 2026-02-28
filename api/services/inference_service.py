import yaml
import os

from core.stability_engine import StabilityEngine
from core.failure_detector import FailureDetector
from core.failure_reasoner import FailureReasoner
from core.router import Router

from domains.genai.llm_model import LLMModel
from domains.genai.preprocess import preprocess
from domains.genai.signals import extract_signals
from domains.genai.embedding_model import EmbeddingModel
from domains.genai.retriever import Retriever
from domains.genai.grounding import check_grounding
from domains.genai.self_critique import SelfCritique

from ingestion.pdf_loader import load_pdf
from ingestion.image_loader import load_image_text
from ingestion.text_splitter import split_text


def load_yaml(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)


class InferenceService:

    def __init__(self):
        config = load_yaml("config/genai_rag.yaml")["genai_rag"]

        self.config = config
        self.embedding_model = EmbeddingModel()
        self.model = LLMModel(config["model_name"])
        self.stability_engine = StabilityEngine()
        self.failure_detector = FailureDetector()
        self.failure_reasoner = FailureReasoner()
        self.router = Router()
        self.critique_engine = SelfCritique()

    def ingest_document(self, path):
        if not path:
            return []

        ext = os.path.splitext(path)[1].lower()

        if ext == ".pdf":
            raw_text = load_pdf(path)
        elif ext in [".png", ".jpg", ".jpeg"]:
            raw_text = load_image_text(path)
        else:
            return []

        return split_text(raw_text)

    def run(self, question, document_path=None):

        query = preprocess(question)

        documents = self.ingest_document(document_path)

        if not documents:
            documents = [""]

        retriever = Retriever(self.embedding_model, documents)
        retrieved_docs = retriever.retrieve(query, self.config["top_k"])
        context_block = "\n\n".join(retrieved_docs)

        prompt = f"""
You are a document-aware assistant.

If context is relevant, use it.
Otherwise answer normally.

Context:
{context_block}

Question:
{query}

Answer clearly:
"""

        predictions = []

        for _ in range(self.config["num_generations"]):
            text = self.model.generate(prompt, self.config["temperature"])
            predictions.append(text)

        final_prediction = predictions[0]
        stable = self.stability_engine.is_stable(predictions)

        grounding_result = check_grounding(
            final_prediction,
            retrieved_docs,
            self.embedding_model
        )

        critique_result = self.critique_engine.evaluate(
            self.model,
            query,
            final_prediction,
            context_block
        )

        confidence_score = (
            0.3 * grounding_result["similarity"] +
            0.4 * (1.0 if stable else 0.0) +
            0.3 * (1.0 if critique_result["is_safe"] else 0.0)
        )

        base_failures = self.failure_detector.detect(
            inference_result={"error": None},
            confidence_result={"is_low": confidence_score < 0.45},
            domain_signals=extract_signals(final_prediction)
        )

        failures = base_failures

        if not critique_result["is_safe"]:
            failures.append("self_critique_failed")

        decision = self.router.route(failures)

        return {
            "answer": final_prediction,
            "confidence_score": confidence_score,
            "grounding_similarity": grounding_result["similarity"],
            "stable": stable,
            "failures": failures,
            "decision": decision
        }
