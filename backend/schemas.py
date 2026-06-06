from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class Message(BaseModel):
    sender: str  # "user" or "agent"
    agent_name: Optional[str] = None  # "DiscoveryAgent", etc.
    content: str
    timestamp: str

class ConsultationStartRequest(BaseModel):
    industry: Optional[str] = None
    company_name: Optional[str] = None
    company_size: Optional[str] = None
    template_key: Optional[str] = None  # if loading a template directly

class MessageRequest(BaseModel):
    content: str

class SessionResponse(BaseModel):
    id: str
    industry: Optional[str] = None
    company_name: Optional[str] = None
    company_size: Optional[str] = None
    status: str
    current_step: int
    messages: List[Message]
    created_at: datetime

    class Config:
        from_attributes = True

class APIKeyRequest(BaseModel):
    gemini_api_key: str
