from sqlalchemy.orm import Session
from app.repositories.room_repository import RoomRepository
from app.models.room import Room
from typing import List, Optional

class RoomService:

    def __init__(self, db: Session):
        self.repository = RoomRepository(db)

    def get_room_by_id(self, room_id: int) -> Optional[Room]:
        return self.repository.find_by_id(room_id)

    def create_room(self, name: str) -> Room:
        room = Room(name=name)
        return self.repository.create(room)

    def get_all_rooms(self) -> List[Room]:
        return self.repository.find_all()
