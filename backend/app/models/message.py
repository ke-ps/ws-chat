from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy import Enum as SAEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.connection import Base
from app.models.enums import SenderType


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    sender_type = Column(SAEnum(SenderType, name="sender_type"), nullable=False, default=SenderType.USER)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    room = relationship("Room", back_populates="messages")
    user = relationship("User", back_populates="messages")

    def __repr__(self):
        st = self.sender_type.value if self.sender_type else None
        return f"<Message(id={self.id}, sender_type={st}, user_id={self.user_id})>"
