from sqlalchemy.orm import Session
from app.repositories.room_member_repository import RoomMemberRepository
from app.repositories.room_repository import RoomRepository
from app.repositories.user_repository import UserRepository
from app.models.room_member import RoomMember
from typing import List

class RoomMemberService:

    def __init__(self, db: Session):
        self.repository = RoomMemberRepository(db)
        self.room_repo = RoomRepository(db)
        self.user_repo = UserRepository(db)

    def add_member(self, room_id: int, user_id: int) -> RoomMember:
        room = self.room_repo.find_by_id(room_id)
        if not room:
            raise ValueError("Room not found")

        user = self.user_repo.find_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        if self.repository.is_member(room_id, user_id):
            raise ValueError("User is already a member of this room")

        return self.repository.add_member(room_id, user_id)

    def get_members(self, room_id: int) -> List[RoomMember]:
        room = self.room_repo.find_by_id(room_id)
        if not room:
            raise ValueError("Room not found")
        return self.repository.get_members(room_id)
