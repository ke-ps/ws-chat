import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, firstValueFrom } from 'rxjs';
import { Message } from '../models/message.model';
import { Room } from '../models/room.model';

// ============================================================
// ORDEN DE EJECUCIÓN - Cómo funciona el chat:
// ============================================================
// 1. El componente (ChatComponent) se carga y muestra la lista de mensajes
// 2. El usuario escribe un mensaje y pulsa "Enviar"
// 3. ChatComponent llama a chatService.sendMessage()
// 4. ChatService:
//    a. Crea el mensaje con id, contenido, sender y timestamp
//    b. Lo añade al BehaviorSubject (actualiza la lista en la UI)
//    c. Envía el mensaje al servidor WebSocket
// 5. El servidor recibe el mensaje y hace broadcast a TODOS los clientes
// 6. Todos los clientes reciben el mensaje en onmessage y lo añaden a su lista
// ============================================================

@Injectable({
  providedIn: 'root'
})
export class ChatService {
  private http = inject(HttpClient);
  private apiUrl = 'http://localhost:8000';

  // --------------------------------------------------------
  // PASO 1 - BehaviorSubject: almacena la lista de mensajes
  // Observable público para que el componente se suscriba
  // --------------------------------------------------------
  private messagesSubject = new BehaviorSubject<Message[]>([]);
  messages$: Observable<Message[]> = this.messagesSubject.asObservable();

  // --------------------------------------------------------
  // PASO 2 - Salas
  // --------------------------------------------------------
  private roomsSubject = new BehaviorSubject<Room[]>([]);
  rooms$: Observable<Room[]> = this.roomsSubject.asObservable();

  private selectedRoomIdSubject = new BehaviorSubject<number | null>(null);
  selectedRoomId$: Observable<number | null> = this.selectedRoomIdSubject.asObservable();

  // --------------------------------------------------------
  // PASO 2b - Usuarios conectados en tiempo real
  // --------------------------------------------------------
  private connectedUsersSubject = new BehaviorSubject<string[]>([]);
  connectedUsers$: Observable<string[]> = this.connectedUsersSubject.asObservable();

  // --------------------------------------------------------
  // PASO 3 - Configuración WebSocket
  // --------------------------------------------------------
  private ws: WebSocket | null = null;
  private wsUrl = '';
  private useWebSocket = true;
  private userEmail = '';
  private userDisplayName = '';

  constructor() {
    // No auto-conectar - esperar a que el usuario seleccione una sala
  }

  // --------------------------------------------------------
  // Establecer datos del usuario para la conexión WebSocket
  // --------------------------------------------------------
  setUserEmail(email: string): void {
    this.userEmail = email;
  }

  setUserDisplayName(displayName: string): void {
    this.userDisplayName = displayName;
  }

  // --------------------------------------------------------
  // Cargar salas desde el backend
  // --------------------------------------------------------
  async loadRooms(): Promise<void> {
    try {
      const rooms = await firstValueFrom(this.http.get<Room[]>(`${this.apiUrl}/rooms`));
      this.roomsSubject.next(rooms);
    } catch (error) {
      console.error('Error al cargar salas:', error);
    }
  }

  // --------------------------------------------------------
  // Crear una sala nueva en el backend
  // --------------------------------------------------------
  async createRoom(name: string): Promise<Room> {
    const room = await firstValueFrom(
      this.http.post<Room>(`${this.apiUrl}/rooms`, { name })
    );
    await this.loadRooms();
    return room;
  }

  // --------------------------------------------------------
  // Cargar historial de mensajes de una sala
  // --------------------------------------------------------
  private async loadMessages(roomId: number): Promise<void> {
    try {
      const data = await firstValueFrom(
        this.http.get<any[]>(`${this.apiUrl}/rooms/${roomId}/messages`)
      );
      const messages: Message[] = data.map((m) => ({
        id: String(m.id),
        content: m.content,
        sender: m.user_email || String(m.user_id),
        senderType: m.sender_type || 'USER',
        timestamp: new Date(m.created_at)
      }));
      this.messagesSubject.next(messages);
    } catch (error) {
      console.error('Error al cargar mensajes:', error);
    }
  }

  // --------------------------------------------------------
  // Seleccionar una sala y conectar WebSocket
  // --------------------------------------------------------
  async selectRoom(roomId: number): Promise<void> {
    if (this.selectedRoomIdSubject.getValue() === roomId && this.ws) {
      return;
    }
    this.disconnectWebSocket();
    this.messagesSubject.next([]);
    this.connectedUsersSubject.next([]);
    this.selectedRoomIdSubject.next(roomId);
    await this.loadMessages(roomId);
    this.wsUrl = `ws://localhost:8000/ws/${roomId}`;
    this.connectWebSocket();
  }

  // --------------------------------------------------------
  // PASO 4 - Enviar mensaje
  // sender = email del usuario autenticado con Firebase
  // --------------------------------------------------------
  sendMessage(content: string, sender: string): void {
    const message: Message = {
      id: crypto.randomUUID(),
      content,
      sender,
      senderType: 'USER',
      timestamp: new Date()
    };

    const currentMessages = this.messagesSubject.getValue();
    this.messagesSubject.next([...currentMessages, message]);

    if (this.useWebSocket && this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({ id: message.id, content, sender }));
    }
  }

  // --------------------------------------------------------
  // PASO 5 - Conectar al servidor WebSocket
  // --------------------------------------------------------
  private connectWebSocket(): void {
    if (!this.useWebSocket || !this.wsUrl || this.ws) {
      return;
    }
    const params = new URLSearchParams({
      email: this.userEmail,
      displayName: this.userDisplayName,
    });
    const url = `${this.wsUrl}?${params.toString()}`;
    const ws = new WebSocket(url);
    this.ws = ws;

    ws.onopen = () => {
      console.log('WebSocket conectado a sala', this.selectedRoomIdSubject.getValue());
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);

      if (data.type === 'user_list') {
        this.connectedUsersSubject.next(data.users);
        return;
      }

      const message: Message = {
        id: data.id || crypto.randomUUID(),
        content: data.content,
        sender: data.sender,
        senderType: data.sender_type || 'USER',
        timestamp: new Date(data.timestamp)
      };
      const currentMessages = this.messagesSubject.getValue();
      const exists = currentMessages.some(m => m.id === message.id);
      if (!exists) {
        this.messagesSubject.next([...currentMessages, message]);
      }
    };

    ws.onerror = (error) => {
      console.error('Error WebSocket:', error);
    };

    ws.onclose = () => {
      console.log('WebSocket desconectado');
      if (this.ws === ws) {
        this.ws = null;
      }
    };
  }

  // --------------------------------------------------------
  // PASO 6 - Desconectar
  // --------------------------------------------------------
  disconnectWebSocket(): void {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }
}