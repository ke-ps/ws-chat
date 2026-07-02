from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.services.room_service import RoomService
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/rooms", tags=["rooms"])

class CreateRoomRequest(BaseModel):
    name: str

class RoomResponse(BaseModel):
    id: int
    name: str
    created_at: Optional[str] = None

    class Config:
        from_attributes = True

@router.post("", response_model=RoomResponse)
def create_room(body: CreateRoomRequest, db: Session = Depends(get_db)):
    service = RoomService(db)
    room = service.create_room(body.name)
    return RoomResponse(
        id=room.id,
        name=room.name,
        created_at=room.created_at.isoformat() if room.created_at else None
    )

@router.get("", response_model=list[RoomResponse])
def list_rooms(db: Session = Depends(get_db)):
    service = RoomService(db)
    rooms = service.get_all_rooms()
    return [
        RoomResponse(
            id=room.id,
            name=room.name,
            created_at=room.created_at.isoformat() if room.created_at else None
        )
        for room in rooms
    ]
