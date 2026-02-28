from sentence_transformers import SentenceTransformer

class EmbeddingModel:
    """
    Local embedding model using sentence-transformers.
    """

    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def encode(self, texts):
        return self.model.encode(texts)
