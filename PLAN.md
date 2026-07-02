# PLAN.md

# WS-Chat Roadmap

Estado del proyecto: 🟡 En desarrollo

---

# Fase 1 — Configuración inicial ✅

- [x] Backend FastAPI
- [x] Estructura del proyecto
- [x] Configuración SQLAlchemy
- [x] Configuración MySQL (Aiven)
- [x] CORS
- [x] Health Check

---

# Fase 2 — Frontend ✅

- [x] Angular
- [x] Angular Material
- [x] Routing
- [x] Login
- [x] Registro

---

# Fase 3 — Firebase Authentication ✅

- [x] Registro
- [x] Login
- [x] Logout
- [x] Guards
- [x] Sincronización Firebase → Backend
- [x] Persistencia de usuarios en MySQL

---

# Fase 4 — Chat en tiempo real ✅

- [x] WebSocket
- [x] Envío de mensajes
- [x] Recepción de mensajes
- [x] Broadcast
- [x] Autenticación mediante Firebase Admin SDK
- [x] Sincronización de usuarios

---

# Fase 5 — Sistema de salas

## 5.1 Crear salas ✅

- [x] Modelo Room
- [x] Repository
- [x] Service
- [x] Router
- [x] Persistencia en MySQL

## 5.2 Participantes de una sala ⏳

- [ ] Tabla RoomParticipant
- [ ] Relación Room ↔ User
- [ ] Añadir participante
- [ ] Obtener participantes

## 5.3 Unirse a una sala

- [ ] Endpoint Join Room
- [ ] Validaciones
- [ ] Evitar duplicados

## 5.4 Abandonar una sala

- [ ] Endpoint Leave Room

## 5.5 Listado de salas del usuario

- [ ] Obtener únicamente las salas donde participa

---

# Fase 6 — Mensajes persistentes

## 6.1 Modelo Message

- [ ] Tabla Message
- [ ] Relaciones

## 6.2 Persistencia

- [ ] Guardar mensajes
- [ ] Leer historial

## 6.3 Historial

- [ ] Cargar últimos mensajes al entrar

---

# Fase 7 — WebSocket por salas

- [ ] Conexión por sala
- [ ] Broadcast únicamente a participantes
- [ ] Gestión de conexiones

---

# Fase 8 — Invitaciones

- [ ] Invitar usuario
- [ ] Aceptar invitación
- [ ] Rechazar invitación

---

# Fase 9 — Chat privado

- [ ] Conversaciones privadas
- [ ] Reutilizar sistema de salas

---

# Fase 10 — IA como participante

## 10.1 Participante especial

- [ ] Crear usuario IA
- [ ] Permitir añadir IA a una sala

## 10.2 Menciones

- [ ] Detectar @IA
- [ ] Invocar IA únicamente cuando sea mencionada

## 10.3 Respuesta

- [ ] Guardar respuesta
- [ ] Enviar respuesta por WebSocket

---

# Fase 11 — Frontend de salas

- [ ] Crear sala
- [ ] Listar salas
- [ ] Entrar a sala
- [ ] Añadir participantes
- [ ] Lista de participantes

---

# Fase 12 — Mejoras

- [ ] Roles
- [ ] Administradores
- [ ] Avatar
- [ ] Estados online
- [ ] Escribiendo...
- [ ] Reacciones
- [ ] Adjuntos
- [ ] Notificaciones
- [ ] Búsqueda
- [ ] Tests

---

# Convenciones

Cada nueva funcionalidad debe cumplir:

- Mantener la arquitectura existente.
- Implementar únicamente la fase solicitada.
- No realizar refactors innecesarios.
- No modificar funcionalidades ya implementadas.
- No crear código que no sea necesario para la fase actual.

---

# Flujo de desarrollo

1. Crear rama desde `fullstack`.
2. Implementar una única fase.
3. Probar manualmente.
4. Commit.
5. Merge a `fullstack`.
6. Push de `fullstack`.
7. Push de la rama de la fase.
8. Eliminar la rama local.
9. Actualizar este archivo marcando la fase como completada.