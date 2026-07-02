from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.connection import Base

class RoomMember(Base):
    __tablename__ = "room_members"

    id = Column(Integer, primary_key=True, autoincrement=True)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    joined_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="memberships")
    room = relationship("Room", back_populates="members")

    def __repr__(self):
        return f"<RoomMember(id={self.id}, room_id={self.room_id}, user_id={self.user_id})>"
