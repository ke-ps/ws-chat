from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.services.document_service import DocumentService
from app.services.ingestion_service import IngestionService
from app.services.embedding_service import EmbeddingService
from app.providers.embeddings import GeminiEmbeddingProvider
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/rooms/{room_id}/documents", tags=["documents"])


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
async def upload_document(room_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    service = DocumentService(db)
    try:
        document = service.upload_document(room_id, file)
        return DocumentResponse(
            id=document.id,
            room_id=document.room_id,
            filename=document.filename,
            original_filename=document.original_filename,
            file_size=document.file_size,
            content_type=document.content_type,
            created_at=document.created_at.isoformat() if document.created_at else None
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=list[DocumentResponse])
def list_documents(room_id: int, db: Session = Depends(get_db)):
    service = DocumentService(db)
    documents = service.get_documents_by_room(room_id)
    return [
        DocumentResponse(
            id=doc.id,
            room_id=doc.room_id,
            filename=doc.filename,
            original_filename=doc.original_filename,
            file_size=doc.file_size,
            content_type=doc.content_type,
            created_at=doc.created_at.isoformat() if doc.created_at else None
        )
        for doc in documents
    ]


@router.delete("/{document_id}")
def delete_document(room_id: int, document_id: int, db: Session = Depends(get_db)):
    service = DocumentService(db)
    document = service.get_document_by_id(document_id)
    if not document or document.room_id != room_id:
        raise HTTPException(status_code=404, detail="Document not found")
    
    service.delete_document(document_id)
    return {"detail": "Document deleted"}


@router.post("/{document_id}/ingest")
def ingest_document(room_id: int, document_id: int, db: Session = Depends(get_db)):
    document_service = DocumentService(db)
    document = document_service.get_document_by_id(document_id)
    if not document or document.room_id != room_id:
        raise HTTPException(status_code=404, detail="Document not found")

    provider = GeminiEmbeddingProvider()
    embedding_service = EmbeddingService(provider)
    ingestion_service = IngestionService(db, embedding_service)
    try:
        chunks = ingestion_service.ingest_document(document_id)
        return {
            "detail": f"Ingested {len(chunks)} chunks",
            "document_id": document_id,
            "chunks_count": len(chunks),
        }
    except (ValueError, Exception) as e:
        raise HTTPException(status_code=400, detail=str(e))
