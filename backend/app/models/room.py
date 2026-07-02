from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.connection import Base

class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    members = relationship("RoomMember", back_populates="room")

    def __repr__(self):
        return f"<Room(id={self.id}, name={self.name})>"
