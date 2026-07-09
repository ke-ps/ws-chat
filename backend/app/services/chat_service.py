from typing import Optional

from app.services.message_processor import MessageProcessor
from app.schemas.chat import ChatResult


class ChatService:
    def __init__(self, message_processor: MessageProcessor) -> None:
        self._message_processor = message_processor

    def process_message(
        self,
        room_id: int,
        sender_email: str,
        content: str,
        message_id: Optional[str] = None,
    ) -> ChatResult:
        return self._message_processor.process(
            room_id=room_id,
            sender_email=sender_email,
            content=content,
            message_id=message_id,
        )
