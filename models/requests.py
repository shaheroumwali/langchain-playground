from typing import Optional
from pydantic import BaseModel


class ChatRequest(BaseModel):
    user_id: str
    message: str
    topic: Optional[str] = None
