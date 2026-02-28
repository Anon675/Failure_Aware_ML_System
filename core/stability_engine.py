from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class StabilityEngine:
    """
    Checks semantic stability of generated outputs.
    """

    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def is_stable(self, predictions, threshold=0.85):
        if len(predictions) < 2:
            return True

        embeddings = self.model.encode(predictions)
        similarity_matrix = cosine_similarity(embeddings)

        # Ignore diagonal
        similarities = similarity_matrix[np.triu_indices(len(predictions), k=1)]

        return all(sim >= threshold for sim in similarities)
