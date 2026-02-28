from pydantic import BaseModel
from typing import Optional, List


class QueryRequest(BaseModel):
    question: str
    document_path: Optional[str] = None


class QueryResponse(BaseModel):
    answer: str
    confidence_score: float
    grounding_similarity: float
    stable: bool
    failures: List[str]
    decision: str
