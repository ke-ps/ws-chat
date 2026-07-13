from typing import Optional

from app.providers.ai import AIProvider
from app.models.enums import RoomType
from app.services.room_service import RoomService
from app.services.rag_service import RAGService


class AIService:
    def __init__(
        self,
        provider: AIProvider,
        rag_service: Optional[RAGService] = None,
        room_service: Optional[RoomService] = None,
    ) -> None:
        self._provider = provider
        self._rag_service = rag_service
        self._room_service = room_service

    def ask(self, prompt: str, room_id: int) -> str:
        if self._room_service and self._rag_service:
            room = self._room_service.get_room_by_id(room_id)
            if room and room.room_type == RoomType.RAG:
                if not self._rag_service.has_relevant_context(prompt):
                    return self._rag_service.no_context_message()
                enriched = self._rag_service.generate(prompt)
                return self._provider.ask(enriched)

        return self._provider.ask(prompt)
