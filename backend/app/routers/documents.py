from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.services.document_service import DocumentService
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/rooms/{room_id}/documents", tags=["documents"])


class RegisterDocumentRequest(BaseModel):
    filename: str
    original_filename: str
    file_size: int
    content_type: str


class DocumentResponse(BaseModel):
    id: int
    room_id: int
    filename: str
    original_filename: str
    file_size: int
    content_type: str
    created_at: Optional[str] = None

    class Config:
        from_attributes = True


@router.post("", response_model=DocumentResponse)
def register_document(
    room_id: int,
    body: RegisterDocumentRequest,
    db: Session = Depends(get_db),
):
    service = DocumentService(db)
    try:
        document = service.register_document(
            room_id=room_id,
            filename=body.filename,
            original_filename=body.original_filename,
            file_size=body.file_size,
            content_type=body.content_type,
        )
        return DocumentResponse(
            id=document.id,
            room_id=document.room_id,
            filename=document.filename,
            original_filename=document.original_filename,
            file_size=document.file_size,
            content_type=document.content_type,
            created_at=document.created_at.isoformat() if document.created_at else None,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=list[DocumentResponse])
def list_documents(room_id: int, db: Session = Depends(get_db)):
    service = DocumentService(db)
    try:
        documents = service.get_documents_by_room(room_id)
        return [
            DocumentResponse(
                id=doc.id,
                room_id=doc.room_id,
                filename=doc.filename,
                original_filename=doc.original_filename,
                file_size=doc.file_size,
                content_type=doc.content_type,
                created_at=doc.created_at.isoformat() if doc.created_at else None,
            )
            for doc in documents
        ]
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(
    room_id: int,
    document_id: int,
    db: Session = Depends(get_db),
):
    service = DocumentService(db)
    document = service.get_document(document_id)
    if not document or document.room_id != room_id:
        raise HTTPException(status_code=404, detail="Document not found")
    return DocumentResponse(
        id=document.id,
        room_id=document.room_id,
        filename=document.filename,
        original_filename=document.original_filename,
        file_size=document.file_size,
        content_type=document.content_type,
        created_at=document.created_at.isoformat() if document.created_at else None,
    )


@router.delete("/{document_id}", status_code=204)
def delete_document(
    room_id: int,
    document_id: int,
    db: Session = Depends(get_db),
):
    service = DocumentService(db)
    document = service.get_document(document_id)
    if not document or document.room_id != room_id:
        raise HTTPException(status_code=404, detail="Document not found")
    service.delete_document(document_id)
