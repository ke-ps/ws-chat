import os
import fitz
from sqlalchemy.orm import Session
from app.services.document_service import DocumentService


class PDFExtractionError(Exception):
    pass


class PDFExtractionService:

    def __init__(self, db: Session):
        self.document_service = DocumentService(db)

    def extract_text(self, document_id: int) -> str:
        document = self.document_service.get_document_by_id(document_id)
        if not document:
            raise PDFExtractionError(f"Document with id {document_id} not found")

        file_path = os.path.join("uploads", str(document.room_id), document.filename)

        if not os.path.exists(file_path):
            raise PDFExtractionError(f"PDF file not found on disk: {file_path}")

        try:
            with fitz.open(file_path) as doc:
                text = ""
                for page in doc:
                    text += page.get_text()
            return text
        except Exception as e:
            raise PDFExtractionError(f"Error reading PDF file: {e}")
