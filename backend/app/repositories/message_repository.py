from sqlalchemy.orm import Session
from app.models.message import Message
from app.models.user import User
from typing import List, Tuple


class MessageRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, message: Message) -> Message:
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        return message

    def find_by_room(self, room_id: int) -> List[Message]:
        return (
            self.db.query(Message)
            .filter(Message.room_id == room_id)
            .order_by(Message.created_at.asc())
            .all()
        )

    def find_by_room_with_email(self, room_id: int) -> List[Tuple[Message, str]]:
        return (
            self.db.query(Message, User.email)
            .join(User, Message.user_id == User.id)
            .filter(Message.room_id == room_id)
            .order_by(Message.created_at.asc())
            .all()
        )
