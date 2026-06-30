# ============================================================
# services/user_service.py
# ============================================================
# Lógica de negocio para gestión de usuarios.
# Usa el repositorio para acceder a la base de datos.
# No conoce nada de Firebase ni de HTTP.
# ============================================================

from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.models.user import User
from typing import Optional


class UserService:
    """Servicio para gestionar usuarios en la base de datos."""

    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    def sync_user(self, firebase_uid: str, email: str, display_name: Optional[str] = None) -> User:
        """
        Sincroniza un usuario desde Firebase.
        Si ya existe (por firebase_uid), actualiza sus datos.
        Si no existe, lo crea.
        Nunca crea duplicados.
        """
        return self.repository.upsert(
            firebase_uid=firebase_uid,
            email=email,
            display_name=display_name
        )

    def get_user(self, firebase_uid: str) -> Optional[User]:
        """Obtiene un usuario por su firebase_uid."""
        return self.repository.find_by_firebase_uid(firebase_uid)