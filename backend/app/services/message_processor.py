from datetime import datetime
from typing import Optional

from app.services.message_service import MessageService
from app.services.ai_service import AIService
from app.repositories.user_repository import UserRepository
from app.schemas.chat import ChatMessage, ChatResult


class MessageProcessor:
    def __init__(
        self,
        message_service: MessageService,
        ai_service: AIService,
        user_repository: UserRepository,
    ) -> None:
        self._message_service = message_service
        self._ai_service = ai_service
        self._user_repository = user_repository

    def process(
        self,
        room_id: int,
        sender_email: str,
        content: str,
        message_id: Optional[str] = None,
    ) -> ChatResult:
        user = self._user_repository.find_by_email(sender_email) if sender_email else None

        if user:
            self._message_service.send_message(
                room_id=room_id,
                user_id=user.id,
                content=content,
            )

        user_message = ChatMessage(
            sender=sender_email,
            content=content,
            room_id=room_id,
            timestamp=datetime.now().isoformat(),
            id=message_id,
        )

        ai_message = self._process_ai_mention(content, room_id)

        return ChatResult(user_message=user_message, ai_message=ai_message)

    def _process_ai_mention(self, content: str, room_id: int) -> Optional[ChatMessage]:
        stripped = content
        for prefix in ("@IA ", "@ia ", "@IA\n", "@ia\n"):
            if content.startswith(prefix):
                stripped = content[len(prefix):].strip()
                break

        if stripped == content:
            return None

        prompt = stripped or ""
        if not prompt:
            return None

        result = self._ai_service.ask(prompt, room_id)
        self._message_service.save_ai_message(room_id=room_id, content=result)

        return ChatMessage(
            sender="IA",
            content=result,
            room_id=room_id,
            timestamp=datetime.now().isoformat(),
            sender_type="AI",
        )
