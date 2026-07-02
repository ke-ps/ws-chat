# AGENTS.md

## Propósito

Este proyecto se desarrolla por fases pequeñas y autocontenidas.

Cada solicitud implementará una única funcionalidad.

No implementar funcionalidades adicionales aunque parezcan relacionadas.

---

# Arquitectura

Mantener siempre la arquitectura existente.

Backend:

- Models
- Repositories
- Services
- Routers

La lógica debe permanecer separada por responsabilidades.

No mover archivos ni reorganizar carpetas sin que se solicite explícitamente.

---

# Responsabilidades

## Models

Solo representan las entidades de la base de datos.

No añadir lógica de negocio.

---

## Repositories

Acceso a datos exclusivamente.

Responsables de consultas SQLAlchemy y operaciones CRUD.

No implementar lógica de negocio.

---

## Services

Toda la lógica de negocio debe implementarse aquí.

Los routers nunca deben contener lógica compleja.

---

## Routers

Únicamente deben:

- recibir la petición
- validar datos
- llamar al Service correspondiente
- devolver la respuesta

---

# Base de datos

Base de datos:

- MySQL (Aiven)

ORM:

- SQLAlchemy

Las nuevas tablas deben crearse mediante `init_db()`.

No utilizar migraciones salvo que se solicite.

Mantener relaciones SQLAlchemy claras y simples.

---

# Frontend

Framework:

- Angular (Standalone Components)

No modificar el frontend salvo que la tarea lo requiera explícitamente.

No cambiar componentes existentes sin necesidad.

---

# Firebase

La autenticación se realiza mediante Firebase Authentication.

Los usuarios se sincronizan posteriormente con MySQL.

No modificar este flujo salvo que se solicite.

---

# WebSocket

El sistema de chat utiliza WebSockets.

No modificar el flujo actual salvo que la fase lo requiera.

No romper compatibilidad con funcionalidades existentes.

---

# Desarrollo

Cada fase debe:

- implementar únicamente el objetivo solicitado
- realizar los cambios mínimos necesarios
- mantener compatibilidad con el código existente

No realizar:

- refactors
- optimizaciones innecesarias
- cambios de estilo
- renombrados sin motivo
- reorganización del proyecto

---

# Código

Priorizar siempre:

- código sencillo
- legible
- mantenible
- consistente con el resto del proyecto

No duplicar lógica.

Reutilizar Services y Repositories existentes siempre que sea posible.

---

# Git

Nunca:

- realizar commits
- modificar el historial Git
- crear ramas
- hacer merge

Eso lo hará siempre el desarrollador.

---

# Al finalizar una tarea

Detenerse siempre al finalizar la fase solicitada.

Indicar únicamente:

- Archivos creados.
- Archivos modificados.
- Endpoints añadidos (si existen).
- Cómo comprobar que funciona.

No implementar la siguiente fase por iniciativa propia.

---

# Objetivo del proyecto

El proyecto evolucionará progresivamente hacia un sistema de chat en tiempo real con:

- autenticación mediante Firebase
- persistencia en MySQL
- salas
- participantes
- chat privado
- chat grupal
- invitaciones
- historial de mensajes
- IA como participante especial
- menciones mediante @IA

Toda nueva funcionalidad debe respetar la arquitectura existente y facilitar la evolución futura del sistema.