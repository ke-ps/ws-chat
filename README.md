# WS-Chat

Sistema de chat Full-Stack desarrollado con **Angular**, **FastAPI**, **WebSockets**, **Firebase Authentication** y **MySQL (Aiven)**.

El objetivo de este proyecto es construir una aplicación de chat moderna, escalable y mantenible, aplicando buenas prácticas de arquitectura, desarrollo incremental y separación de responsabilidades.

---

# Objetivos

- Aprender desarrollo Full-Stack moderno.
- Aplicar una arquitectura limpia y escalable.
- Implementar comunicación en tiempo real mediante WebSockets.
- Integrar autenticación segura con Firebase.
- Persistir información en MySQL.
- Incorporar una IA como participante especial del chat.

---

# Stack tecnológico

## Backend

- Python
- FastAPI
- SQLAlchemy
- WebSockets
- PyMySQL
- Firebase Admin SDK

## Frontend

- Angular (Standalone Components)
- Angular Material
- RxJS
- TypeScript

## Base de datos

- MySQL (Aiven)

## Autenticación

- Firebase Authentication

---

# Arquitectura

El backend sigue una arquitectura por capas:

```text
app/
│
├── database/
├── models/
├── repositories/
├── services/
├── routers/
└── main.py
```

### Models

Representan las entidades de la base de datos.

### Repositories

Gestionan exclusivamente el acceso a datos.

### Services

Contienen la lógica de negocio.

### Routers

Exponen los endpoints HTTP y delegan el trabajo en los Services.

---

# Frontend

El frontend está desarrollado con Angular utilizando Standalone Components.

Estructura principal:

```text
src/app/
│
├── components/
├── guards/
├── models/
├── services/
└── environments/
```

---

# Flujo de autenticación

1. El usuario inicia sesión o se registra mediante Firebase Authentication.
2. Firebase devuelve un ID Token.
3. El frontend envía el token al backend.
4. El backend valida el token mediante Firebase Admin SDK.
5. El usuario se sincroniza con MySQL.
6. El usuario obtiene acceso al sistema de chat.

---

# Comunicación en tiempo real

La comunicación entre clientes se realiza mediante WebSockets.

Actualmente permite:

- Conexión en tiempo real.
- Envío de mensajes.
- Recepción instantánea.
- Sistema de salas.

Las siguientes fases incorporarán:

- Participantes.
- Historial de mensajes.
- Chat privado.
- Chat grupal.
- IA como participante.

---

# Base de datos

Se utiliza MySQL (Aiven).

Las tablas se crean automáticamente mediante SQLAlchemy durante el arranque del backend.

Actualmente existen entidades para:

- Usuarios
- Salas

---

# Estructura del proyecto

```text
ws-chat/
│
├── backend/
├── frontend/
├── README.md
├── AGENTS.md
└── PLAN.md
```

---

# Instalación

## 1. Clonar el repositorio

```bash
git clone https://github.com/ke-ps/ws-chat.git
cd ws-chat
```

---

## 2. Backend

```bash
cd backend

python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

---

## 3. Frontend

```bash
cd frontend

npm install

ng serve
```

La aplicación estará disponible en:

```text
http://localhost:4200
```

---

# Variables de entorno

Crear un archivo `backend/.env`.

Ejemplo:

```env
DATABASE_URL=mysql+pymysql://usuario:password@host:puerto/base_de_datos

FIREBASE_SERVICE_ACCOUNT=firebase-service-account.json
```

> **Importante:** No subir nunca el archivo `.env` ni las credenciales de Firebase al repositorio.

---

# Roadmap

El desarrollo del proyecto se realiza por fases pequeñas e independientes.

El estado actual puede consultarse en:

- `PLAN.md`

---

# Instrucciones para IA

Este proyecto incluye un archivo:

- `AGENTS.md`

que define las normas que deben seguir los asistentes de IA durante el desarrollo.

---

# Estado del proyecto

🚧 En desarrollo.

Las funcionalidades se implementan de forma incremental mediante ramas independientes para cada fase.

---

# Licencia

Este proyecto se desarrolla con fines educativos y como portfolio personal.