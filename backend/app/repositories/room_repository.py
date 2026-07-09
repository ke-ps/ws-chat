from sqlalchemy.orm import Session
from app.models.room import Room
from app.models.enums import RoomType
from typing import List, Optional

class RoomRepository:

    def __init__(self, db: Session):
        self.db = db

    def find_by_id(self, room_id: int) -> Optional[Room]:
        return self.db.query(Room).filter(Room.id == room_id).first()

    def find_by_room_type(self, room_type: RoomType) -> Optional[Room]:
        return self.db.query(Room).filter(Room.room_type == room_type).first()

    def find_all(self) -> List[Room]:
        return self.db.query(Room).all()

    def create(self, room: Room) -> Room:
        self.db.add(room)
        self.db.commit()
        self.db.refresh(room)
        return room
