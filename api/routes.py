from fastapi import APIRouter, HTTPException

from models.requests import ChatRequest
from models.responses import ChatResponse, HistoryResponse, HistoryItem
from services.llm_service import create_llm, create_prompt, send_message
from services.memory_service import SQLiteMemory
from utils.helpers import truncate_response

router = APIRouter()

# Initialize singletons used by the API
_llm = create_llm()
_prompt = create_prompt()
_memory = SQLiteMemory()


@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    try:
        user_input = req.message if not req.topic else f"{req.message} (topic: {req.topic})"
        response = send_message(user_input, _prompt, _llm, _memory, req.user_id)
        return ChatResponse(response=truncate_response(response, 500))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/chat/{user_id}", response_model=HistoryResponse)
def get_history(user_id: str):
    """Retrieve conversation history for a user."""
    try:
        history = _memory.get_history(user_id)
        items = [HistoryItem(role=role, content=content) for role, content in history]
        return HistoryResponse(user_id=user_id, history=items)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/chat/{user_id}")
def clear_history(user_id: str):
    """Clear conversation history for a user."""
    try:
        _memory.clear(user_id)
        return {"status": "success", "message": f"Cleared history for user {user_id}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
