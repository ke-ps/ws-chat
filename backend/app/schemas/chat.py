from dataclasses import dataclass
from typing import Optional


@dataclass
class ChatMessage:
    sender: str
    content: str
    room_id: int
    timestamp: str
    id: Optional[str] = None


@dataclass
class ChatResult:
    user_message: Optional[ChatMessage] = None
    ai_message: Optional[ChatMessage] = None
