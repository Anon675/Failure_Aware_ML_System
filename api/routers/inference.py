from fastapi import APIRouter
from api.schemas.request_response import QueryRequest, QueryResponse
from api.services.inference_service import InferenceService

router = APIRouter()
service = InferenceService()


@router.post("/ask", response_model=QueryResponse)
def ask_question(request: QueryRequest):

    result = service.run(
        question=request.question,
        document_path=request.document_path
    )

    return QueryResponse(**result)
