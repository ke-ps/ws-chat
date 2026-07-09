from sqlalchemy.orm import Session
from app.repositories.document_repository import DocumentRepository
from app.repositories.room_repository import RoomRepository
from app.models.document import Document
from typing import List


class DocumentService:

    def __init__(self, db: Session):
        self.repository = DocumentRepository(db)
        self.room_repo = RoomRepository(db)

    def register_document(
        self,
        room_id: int,
        filename: str,
        original_filename: str,
        file_size: int,
        content_type: str,
    ) -> Document:
        room = self.room_repo.find_by_id(room_id)
        if not room:
            raise ValueError("Room not found")

        document = Document(
            room_id=room_id,
            filename=filename,
            original_filename=original_filename,
            file_size=file_size,
            content_type=content_type,
        )
        return self.repository.create(document)

    def get_document(self, document_id: int) -> Document | None:
        return self.repository.find_by_id(document_id)

    def get_documents_by_room(self, room_id: int) -> List[Document]:
        room = self.room_repo.find_by_id(room_id)
        if not room:
            raise ValueError("Room not found")
        return self.repository.find_by_room(room_id)

    def delete_document(self, document_id: int) -> bool:
        document = self.repository.find_by_id(document_id)
        if not document:
            return False
        self.repository.delete(document)
        return True
