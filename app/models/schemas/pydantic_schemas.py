from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Chat Schemas
class ChatMessage(BaseModel):
    role: str # 'user' ya 'assistant'
    content: str

class ChatRequest(BaseModel):
    message: str
    user_id: str

class ChatResponse(BaseModel):
    response: str