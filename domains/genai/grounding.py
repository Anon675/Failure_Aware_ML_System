import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def check_grounding(answer, retrieved_docs, embedding_model, threshold=0.65):
    """
    Semantic grounding check using cosine similarity.
    """

    if not retrieved_docs:
        return {"is_grounded": False, "similarity": 0.0}

    answer_vec = embedding_model.encode([answer])
    docs_vec = embedding_model.encode(retrieved_docs)

    similarities = cosine_similarity(answer_vec, docs_vec)[0]
    max_similarity = float(np.max(similarities))

    return {
        "is_grounded": max_similarity >= threshold,
        "similarity": max_similarity
    }
