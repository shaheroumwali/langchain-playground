from pydantic import BaseModel
from typing import List


class ChatResponse(BaseModel):
    response: str


class HistoryItem(BaseModel):
    role: str
    content: str


class HistoryResponse(BaseModel):
    user_id: str
    history: List[HistoryItem]
