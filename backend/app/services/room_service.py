from sqlalchemy.orm import Session
from app.repositories.room_repository import RoomRepository
from app.models.room import Room
from typing import List

class RoomService:

    def __init__(self, db: Session):
        self.repository = RoomRepository(db)

    def create_room(self, name: str) -> Room:
        room = Room(name=name)
        return self.repository.create(room)

    def get_all_rooms(self) -> List[Room]:
        return self.repository.find_all()
