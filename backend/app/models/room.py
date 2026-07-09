from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy import Enum as SAEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.connection import Base
from app.models.enums import RoomType

class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    room_type = Column(SAEnum(RoomType, name="room_type"), nullable=False, default=RoomType.GENERAL)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    members = relationship("RoomMember", back_populates="room")
    messages = relationship("Message", back_populates="room")

    def __repr__(self):
        return f"<Room(id={self.id}, name={self.name})>"
