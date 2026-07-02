from sqlalchemy.orm import Session
from app.models.room import Room
from typing import List

class RoomRepository:

    def __init__(self, db: Session):
        self.db = db

    def find_all(self) -> List[Room]:
        return self.db.query(Room).all()

    def create(self, room: Room) -> Room:
        self.db.add(room)
        self.db.commit()
        self.db.refresh(room)
        return room
