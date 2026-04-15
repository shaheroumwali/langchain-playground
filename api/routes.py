from fastapi import APIRouter, HTTPException

from models.requests import ChatRequest
from models.responses import ChatResponse, HistoryResponse, HistoryItem
from services.llm_service import create_llm, create_prompt, send_message
from services.memory_service import SQLiteMemory
from services.conversation_helper import ConversationEnricher, ConversationContext
from utils.helpers import truncate_response

router = APIRouter()

# Initialize singletons used by the API
_llm = create_llm()
_prompt = create_prompt()
_memory = SQLiteMemory()


@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    """Send a message and get a response with multi-turn conversation support."""
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


@router.get("/chat/{user_id}/stats")
def get_conversation_stats(user_id: str):
    """Get conversation statistics and analytics."""
    try:
        stats = _memory.get_conversation_stats(user_id)
        return {
            "status": "success",
            "data": stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/chat/{user_id}/topics")
def get_conversation_topics(user_id: str):
    """Get topics discussed in the conversation."""
    try:
        topics = _memory.get_conversation_topics(user_id)
        return {
            "status": "success",
            "user_id": user_id,
            "topics": topics,
            "total_topics": len(topics)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/chat/{user_id}/export")
def export_conversation(user_id: str, format: str = "markdown"):
    """Export conversation in different formats (text, markdown, json)."""
    try:
        exported = _memory.export_conversation(user_id, format=format)
        return {
            "status": "success",
            "user_id": user_id,
            "format": format,
            "conversation": exported
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/chat/{user_id}/helper-context")
def get_helper_context(user_id: str):
    """Get the helper context information for a user's conversation."""
    try:
        history = _memory.get_history(user_id)
        conversation_context = ConversationContext(user_id)
        
        if not history:
            return {
                "status": "success",
                "user_id": user_id,
                "message": "No conversation history yet",
                "context": {}
            }
        
        # Extract helper information
        topics = conversation_context.extract_key_topics(history)
        summary = conversation_context.format_conversation_summary(history)
        turn_info = ConversationEnricher.add_turn_counter(history)
        
        return {
            "status": "success",
            "user_id": user_id,
            "turn_count": len([h for h in history if h[0] == "user"]),
            "conversation_summary": summary,
            "key_topics": topics,
            "helper_info": turn_info,
            "message_count": len(history)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/chat/{user_id}/last-n")
def get_last_n_messages(user_id: str, n: int = 5):
    """Get the last n messages from conversation history."""
    try:
        if n < 1 or n > 50:
            raise ValueError("n must be between 1 and 50")
        
        history = _memory.get_last_n_messages(user_id, n)
        items = [HistoryItem(role=role, content=content) for role, content in history]
        
        return {
            "status": "success",
            "user_id": user_id,
            "count": len(items),
            "messages": items
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
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


@router.get("/health")
def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "LangChain Python Tutor with Multi-turn Conversations"
    }
