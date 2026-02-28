import faiss
import numpy as np

class Retriever:
    """
    Simple FAISS-based retriever.
    """

    def __init__(self, embedding_model, documents):
        self.embedding_model = embedding_model
        self.documents = documents
        self.embeddings = embedding_model.encode(documents)

        dimension = self.embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(np.array(self.embeddings))

    def retrieve(self, query, top_k=3):
        query_vec = self.embedding_model.encode([query])
        distances, indices = self.index.search(np.array(query_vec), top_k)

        return [self.documents[i] for i in indices[0]]
