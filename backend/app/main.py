# ============================================================
# PASO 1 - Imports
# ============================================================
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict
import json
from datetime import datetime

# ============================================================
# PASO 2 - Crear la app FastAPI
# ============================================================
app = FastAPI()

# ============================================================
# PASO 3 - Configurar CORS
# Permite que el frontend Angular (puerto 4200) se conecte
# ============================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# PASO 4 - Inicializar base de datos
# Crear tablas al arrancar la aplicación
# ============================================================
@app.on_event("startup")
def on_startup():
    from app.database.connection import init_db
    init_db()


# ============================================================
# PASO 5 - Registrar routers
# ============================================================
from app.routers.auth import router as auth_router
from app.routers.rooms import router as rooms_router
app.include_router(auth_router)
app.include_router(rooms_router)


# ============================================================
# PASO 6 - Endpoints HTTP
# ============================================================

@app.get("/health")
def health():
    """Endpoint de verificación - GET /health"""
    return {"status": "ok"}


# ============================================================
# PASO 7 - WebSocket Manager
# Gestiona las conexiones WebSocket agrupadas por sala
# y mantiene la lista de usuarios conectados en memoria
# ============================================================
class ConnectionManager:
    """Administra las conexiones WebSocket activas, agrupadas por sala.
    Mantiene la lista de usuarios conectados (email, displayName) en memoria.
    Cuando la lista cambie, envía la lista actualizada a todos los
    clientes de la sala mediante un mensaje tipo 'user_list'."""

    def __init__(self):
        self.rooms: Dict[int, List[WebSocket]] = {}
        # room_id -> {email: {"email": str, "displayName": str}}
        self.room_users: Dict[int, Dict[str, dict]] = {}

    async def connect(self, websocket: WebSocket, room_id: int, email: str, display_name: str):
        """Acepta una nueva conexión WebSocket, la asigna a una sala
        y añade el usuario a la lista de conectados."""
        await websocket.accept()
        if room_id not in self.rooms:
            self.rooms[room_id] = []
            self.room_users[room_id] = {}
        self.rooms[room_id].append(websocket)
        self.room_users[room_id][email] = {
            "email": email,
            "displayName": display_name or email,
        }
        await self._broadcast_user_list(room_id)

    def disconnect(self, websocket: WebSocket, room_id: int, email: str):
        """Elimina una conexión WebSocket de su sala y el usuario
        de la lista de conectados."""
        if room_id in self.rooms:
            if websocket in self.rooms[room_id]:
                self.rooms[room_id].remove(websocket)
            if room_id in self.room_users:
                self.room_users[room_id].pop(email, None)
            if not self.rooms[room_id]:
                del self.rooms[room_id]
                self.room_users.pop(room_id, None)

    async def broadcast(self, message: dict, room_id: int):
        """Envía un mensaje a todos los clientes conectados a una sala."""
        if room_id in self.rooms:
            for connection in self.rooms[room_id]:
                await connection.send_json(message)

    async def _broadcast_user_list(self, room_id: int):
        """Envía la lista de usuarios conectados (displayName) a todos
        los clientes de la sala."""
        users_dict = self.room_users.get(room_id, {})
        users = sorted(
            [u["displayName"] for u in users_dict.values()],
            key=str.lower,
        )
        await self.broadcast({"type": "user_list", "users": users}, room_id)


manager = ConnectionManager()


# ============================================================
# PASO 8 - Endpoint WebSocket /ws/{room_id}
# Conecta a un cliente a una sala específica
# ============================================================
@app.websocket("/ws/{room_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    room_id: int,
    email: str = Query(...),
    displayName: str = Query(""),
):
    from app.database.connection import SessionLocal
    from app.services.room_service import RoomService
    from app.services.message_service import MessageService
    from app.repositories.user_repository import UserRepository

    db = SessionLocal()
    try:
        service = RoomService(db)
        room = service.get_room_by_id(room_id)
        if not room:
            await websocket.close(code=4004, reason="Room not found")
            return
        user_repo = UserRepository(db)
    finally:
        db.close()

    await manager.connect(websocket, room_id, email, displayName)
    try:
      while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            message["room_id"] = room_id
            message["timestamp"] = datetime.now().isoformat()

            # Persist message in database
            sender_email = message.get("sender", "")
            user = user_repo.find_by_email(sender_email) if sender_email else None
            if user:
                db = SessionLocal()
                try:
                    msg_service = MessageService(db)
                    msg_service.send_message(
                        room_id=room_id,
                        user_id=user.id,
                        content=message.get("content", "")
                    )
                finally:
                    db.close()

            await manager.broadcast(message, room_id)
    except WebSocketDisconnect:
        manager.disconnect(websocket, room_id, email)
        await manager._broadcast_user_list(room_id)
    except Exception:
        manager.disconnect(websocket, room_id, email)
        await manager._broadcast_user_list(room_id)