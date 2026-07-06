from datetime import datetime
from typing import Optional

from app.services.message_service import MessageService
from app.services.ai_service import AIService
from app.repositories.user_repository import UserRepository


class ChatService:
    def __init__(
        self,
        message_service: MessageService,
        ai_service: AIService,
        user_repository: UserRepository,
    ) -> None:
        self._message_service = message_service
        self._ai_service = ai_service
        self._user_repository = user_repository

    def process_message(
        self,
        room_id: int,
        sender_email: str,
        content: str,
        message_id: Optional[str] = None,
    ) -> tuple[Optional[dict], Optional[dict]]:
        user = self._user_repository.find_by_email(sender_email) if sender_email else None

        if user:
            self._message_service.send_message(
                room_id=room_id,
                user_id=user.id,
                content=content,
            )

        now = datetime.now().isoformat()

        user_message: dict = {
            "sender": sender_email,
            "content": content,
            "room_id": room_id,
            "timestamp": now,
        }
        if message_id:
            user_message["id"] = message_id

        ai_message: Optional[dict] = None

        stripped = content
        for prefix in ("@IA ", "@ia ", "@IA\n", "@ia\n"):
            if content.startswith(prefix):
                stripped = content[len(prefix):].strip()
                break

        if stripped != content:
            prompt = stripped or ""
            if prompt:
                result = self._ai_service.ask(prompt)
                ai_message = {
                    "sender": "IA",
                    "content": result,
                    "room_id": room_id,
                    "timestamp": datetime.now().isoformat(),
                }

        return user_message, ai_message
