from fastapi import APIRouter
from rag.rag_system import query_rag
from api.schemas import QueryRequest

router = APIRouter()

@router.get("/chat")
def chat_get(question: str):
    return {
        "response": query_rag(question)
    }

@router.post("/chat")
def chat_post(request: QueryRequest):
    return {
        "response": query_rag(request.question)
    }
