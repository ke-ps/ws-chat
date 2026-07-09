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


class AddMemberRequest(BaseModel):
    user_id: int

class MemberResponse(BaseModel):
    id: int
    room_id: int
    user_id: int
    joined_at: Optional[str] = None

    class Config:
        from_attributes = True

@router.post("/{room_id}/members", response_model=MemberResponse)
def add_member(room_id: int, body: AddMemberRequest, db: Session = Depends(get_db)):
    from app.services.room_member_service import RoomMemberService
    service = RoomMemberService(db)
    try:
        member = service.add_member(room_id, body.user_id)
        return MemberResponse(
            id=member.id,
            room_id=member.room_id,
            user_id=member.user_id,
            joined_at=member.joined_at.isoformat() if member.joined_at else None
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{room_id}/members", response_model=list[MemberResponse])
def list_members(room_id: int, db: Session = Depends(get_db)):
    from app.services.room_member_service import RoomMemberService
    service = RoomMemberService(db)
    try:
        members = service.get_members(room_id)
        return [
            MemberResponse(
                id=m.id,
                room_id=m.room_id,
                user_id=m.user_id,
                joined_at=m.joined_at.isoformat() if m.joined_at else None
            )
            for m in members
        ]
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


class MessageResponse(BaseModel):
    id: int
    room_id: int
    user_id: Optional[int] = None
    sender_type: str
    content: str
    user_email: Optional[str] = None
    created_at: Optional[str] = None

    class Config:
        from_attributes = True


@router.get("/{room_id}/messages", response_model=list[MessageResponse])
def list_messages(room_id: int, db: Session = Depends(get_db)):
    from app.services.message_service import MessageService
    service = MessageService(db)
    try:
        messages = service.get_messages_with_email(room_id)
        return [
            MessageResponse(
                id=m.id,
                room_id=m.room_id,
                user_id=m.user_id,
                sender_type=m.sender_type.value,
                content=m.content,
                user_email=email,
                created_at=m.created_at.isoformat() if m.created_at else None
            )
            for m, email in messages
        ]
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
