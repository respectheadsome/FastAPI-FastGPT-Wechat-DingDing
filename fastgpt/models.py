from pydantic import BaseModel
from typing import List

class Message(BaseModel):
    user_id: str
    content: str
    timestamp: str

class Conversation(BaseModel):
    conversation_id: str
    messages: List[Message]
