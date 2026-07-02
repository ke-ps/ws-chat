from sqlalchemy.orm import Session
from app.models.room_member import RoomMember
from typing import List, Optional

class RoomMemberRepository:

    def __init__(self, db: Session):
        self.db = db

    def add_member(self, room_id: int, user_id: int) -> RoomMember:
        member = RoomMember(room_id=room_id, user_id=user_id)
        self.db.add(member)
        self.db.commit()
        self.db.refresh(member)
        return member

    def get_members(self, room_id: int) -> List[RoomMember]:
        return self.db.query(RoomMember).filter(RoomMember.room_id == room_id).all()

    def is_member(self, room_id: int, user_id: int) -> bool:
        return self.db.query(RoomMember).filter(
            RoomMember.room_id == room_id,
            RoomMember.user_id == user_id
        ).first() is not None
