from typing import Optional
from pydantic import BaseModel
from datetime import datetime

# Shared properties
class ChatMessageBase(BaseModel):
    content: Optional[str] = None
    event_id: int

class ChatMessageCreate(ChatMessageBase):
    content: str
    event_id: int

class ChatMessageUpdate(ChatMessageBase):
    pass

class ChatMessageInDBBase(ChatMessageBase):
    id: int
    sender_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ChatMessage(ChatMessageInDBBase):
    pass
