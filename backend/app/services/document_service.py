from sqlalchemy.orm import Session
from app.repositories.document_repository import DocumentRepository
from app.repositories.room_repository import RoomRepository
from app.models.document import Document
from typing import List, Optional
import os
import uuid
from fastapi import UploadFile


class DocumentService:

    def __init__(self, db: Session):
        self.repository = DocumentRepository(db)
        self.room_repository = RoomRepository(db)

    def upload_document(self, room_id: int, file: UploadFile) -> Document:
        # Verificar que la sala existe
        room = self.room_repository.find_by_id(room_id)
        if not room:
            raise ValueError("Room not found")

        # Verificar que el archivo es un PDF
        if not file.filename or not file.filename.lower().endswith(".pdf"):
            raise ValueError("Only PDF files are allowed")

        # Generar nombre único para evitar colisiones
        file_extension = os.path.splitext(file.filename)[1].lower()
        unique_filename = f"{uuid.uuid4()}{file_extension}"

        # Crear directorio de uploads si no existe
        uploads_dir = os.path.join("uploads", str(room_id))
        os.makedirs(uploads_dir, exist_ok=True)

        # Guardar el archivo en disco
        file_path = os.path.join(uploads_dir, unique_filename)
        file_content = file.file.read()
        with open(file_path, "wb") as f:
            f.write(file_content)

        # Registrar en la base de datos
        document = Document(
            room_id=room_id,
            filename=unique_filename,
            original_filename=file.filename,
            file_size=len(file_content),
            content_type=file.content_type or "application/pdf"
        )
        return self.repository.create(document)

    def get_documents_by_room(self, room_id: int) -> List[Document]:
        return self.repository.find_by_room(room_id)

    def get_document_by_id(self, document_id: int) -> Optional[Document]:
        return self.repository.find_by_id(document_id)

    def delete_document(self, document_id: int) -> bool:
        document = self.repository.find_by_id(document_id)
        if not document:
            return False

        # Eliminar archivo del disco
        file_path = os.path.join("uploads", str(document.room_id), document.filename)
        if os.path.exists(file_path):
            os.remove(file_path)

        # Eliminar de la base de datos
        self.repository.delete(document)
        return True
