# Incidencias abiertas

---

## BUG-001 · Cambio de salas - WebSocket

### Estado
Abierto

### Descripción

Al cambiar de una sala a otra el comportamiento es inconsistente.

### Comportamiento esperado

- El WebSocket anterior debe cerrarse correctamente.
- Debe abrirse una nueva conexión para la sala seleccionada.
- Los mensajes solo deben enviarse y recibirse en la sala activa.
- El cambio de sala debe funcionar con un único clic.

### Comportamiento observado

- La primera sala funciona correctamente.
- Después de cambiar de sala, a veces los mensajes solo aparecen localmente.
- En ocasiones hay que volver a hacer clic sobre la misma sala para que funcione.
- Tras varios cambios de sala aparecen comportamientos inconsistentes.

### Información obtenida durante la depuración

- El backend recibe correctamente los mensajes mediante `/ws/{room_id}`.
- El backend realiza correctamente el broadcast por sala.
- El problema parece estar en el frontend.
- El flujo actual es:

selectRoom()
→ disconnectWebSocket()
→ limpiar mensajes
→ actualizar selectedRoom
→ actualizar wsUrl
→ connectWebSocket()

Existe la sospecha de una condición de carrera durante el cambio de WebSocket.

### Restricciones

- No modificar el backend salvo que sea imprescindible.
- No reescribir el servicio completo.
- Aplicar el cambio mínimo necesario.
- Explicar primero la causa antes de modificar código.