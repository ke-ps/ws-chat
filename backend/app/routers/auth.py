# ============================================================
# routers/auth.py
# ============================================================
# Router para sincronizar usuarios de Firebase con MySQL.
#
# Flujo:
# 1. Frontend obtiene el idToken de Firebase (FirebaseAuth)
# 2. Frontend envía POST /auth/sync con el token en header
# 3. Backend verifica el token con Firebase Admin SDK
# 4. Backend crea/actualiza el usuario en MySQL
# 5. Devuelve el usuario sincronizado
# ============================================================

from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.services.user_service import UserService
from firebase_admin import auth as firebase_auth
from firebase_admin.credentials import Certificate
from firebase_admin import initialize_app
import os
from typing import Optional

router = APIRouter(prefix="/auth", tags=["auth"])

# ============================================================
# Inicializar Firebase Admin SDK
# Necesita el archivo de credentials del service account
# Descargar desde: Firebase Console > Project Settings >
# Service Accounts > Generate new private key
# ============================================================
def get_firebase_app():
    """Inicializa Firebase Admin una sola vez."""
    if not hasattr(get_firebase_app, '_app'):
        cred_path = os.getenv("FIREBASE_SERVICE_ACCOUNT", "firebase-service-account.json")
        if not os.path.exists(cred_path):
            raise RuntimeError(
                f"No se encontró el archivo de credenciales de Firebase: {cred_path}. "
                "Descarga el service account desde Firebase Console > Project Settings > "
                "Service Accounts > Generate new private key y guárdalo como "
                f"{cred_path} en la raíz del backend."
            )
        cred = Certificate(cred_path)
        get_firebase_app._app = initialize_app(cred)
    return get_firebase_app._app


# ============================================================
# Modelo de respuesta
# ============================================================
class UserResponse:
    def __init__(self, uid: str, email: str, display_name: Optional[str],
                 created_at: str, updated_at: str):
        self.uid = uid
        self.email = email
        self.display_name = display_name
        self.created_at = created_at
        self.updated_at = updated_at


# ============================================================
# POST /auth/sync
# Verifica el token de Firebase y sincroniza con MySQL
# ============================================================
@router.post("/sync")
def sync_user(
    authorization: str = Header(...),  # "Bearer <idToken>"
    db: Session = Depends(get_db)
):
    """
    Sincroniza un usuario autenticado en Firebase con MySQL.

    Headers necesarios:
      Authorization: Bearer <idToken de Firebase>

    Devuelve el usuario creado/actualizado en MySQL.
    """
    # 1. Extraer el token del header "Bearer <token>"
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Formato de autorización inválido")

    id_token = authorization.replace("Bearer ", "")

    # Inicializar Firebase Admin SDK si no lo está
    get_firebase_app()

    try:
        # 2. Verificar el token con Firebase Admin SDK
        decoded_token = firebase_auth.verify_id_token(id_token)
        firebase_uid = decoded_token["uid"]
        email = decoded_token.get("email", "")
        display_name = decoded_token.get("name", None)

    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token de Firebase inválido: {str(e)}")

    # 3. Sincronizar con MySQL (crear o actualizar)
    user_service = UserService(db)
    user = user_service.sync_user(
        firebase_uid=firebase_uid,
        email=email,
        display_name=display_name
    )

    # 4. Devolver respuesta
    return {
        "uid": user.firebase_uid,
        "email": user.email,
        "display_name": user.display_name,
        "created_at": user.created_at.isoformat() if user.created_at else None,
        "updated_at": user.updated_at.isoformat() if user.updated_at else None,
    }


# ============================================================
# GET /auth/me
# Obtiene los datos del usuario actual desde MySQL
# ============================================================
@router.get("/me")
def get_me(
    authorization: str = Header(...),
    db: Session = Depends(get_db)
):
    """Obtiene el usuario actual desde MySQL."""
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Formato de autorización inválido")

    id_token = authorization.replace("Bearer ", "")

    try:
        decoded_token = firebase_auth.verify_id_token(id_token)
        firebase_uid = decoded_token["uid"]
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token de Firebase inválido: {str(e)}")

    user_service = UserService(db)
    user = user_service.get_user(firebase_uid)

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return {
        "uid": user.firebase_uid,
        "email": user.email,
        "display_name": user.display_name,
    }