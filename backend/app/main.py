# ============================================================
# PASO 1 - Imports
# ============================================================
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
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
# ============================================================
class ConnectionManager:
    """Administra las conexiones WebSocket activas, agrupadas por sala."""

    def __init__(self):
        self.rooms: Dict[int, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room_id: int):
        """Acepta una nueva conexión WebSocket y la asigna a una sala."""
        await websocket.accept()
        if room_id not in self.rooms:
            self.rooms[room_id] = []
        self.rooms[room_id].append(websocket)

    def disconnect(self, websocket: WebSocket, room_id: int):
        """Elimina una conexión WebSocket de su sala."""
        if room_id in self.rooms:
            if websocket in self.rooms[room_id]:
                self.rooms[room_id].remove(websocket)
            if not self.rooms[room_id]:
                del self.rooms[room_id]

    async def broadcast(self, message: dict, room_id: int):
        """Envía un mensaje a todos los clientes conectados a una sala."""
        if room_id in self.rooms:
            for connection in self.rooms[room_id]:
                await connection.send_json(message)


manager = ConnectionManager()


# ============================================================
# PASO 8 - Endpoint WebSocket /ws/{room_id}
# Conecta a un cliente a una sala específica
# ============================================================
@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: int):
    from app.database.connection import SessionLocal
    from app.services.room_service import RoomService

    db = SessionLocal()
    try:
        service = RoomService(db)
        room = service.get_room_by_id(room_id)
        if not room:
            await websocket.close(code=4004, reason="Room not found")
            return
    finally:
        db.close()

    await manager.connect(websocket, room_id)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            message["room_id"] = room_id
            message["timestamp"] = datetime.now().isoformat()
            await manager.broadcast(message, room_id)
    except WebSocketDisconnect:
        manager.disconnect(websocket, room_id)
    except Exception:
        manager.disconnect(websocket, room_id)