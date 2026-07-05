from sqlalchemy.orm import Session
from app.repositories.message_repository import MessageRepository
from app.repositories.room_repository import RoomRepository
from app.repositories.user_repository import UserRepository
from app.models.message import Message
from typing import List, Tuple


class MessageService:

    def __init__(self, db: Session):
        self.repository = MessageRepository(db)
        self.room_repo = RoomRepository(db)
        self.user_repo = UserRepository(db)

    def send_message(self, room_id: int, user_id: int, content: str) -> Message:
        room = self.room_repo.find_by_id(room_id)
        if not room:
            raise ValueError("Room not found")

        user = self.user_repo.find_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        message = Message(room_id=room_id, user_id=user_id, content=content)
        return self.repository.create(message)

    def get_messages(self, room_id: int) -> List[Message]:
        room = self.room_repo.find_by_id(room_id)
        if not room:
            raise ValueError("Room not found")
        return self.repository.find_by_room(room_id)

    def get_messages_with_email(self, room_id: int) -> List[Tuple[Message, str]]:
        room = self.room_repo.find_by_id(room_id)
        if not room:
            raise ValueError("Room not found")
        return self.repository.find_by_room_with_email(room_id)
