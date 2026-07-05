import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatListModule } from '@angular/material/list';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatIconModule } from '@angular/material/icon';
import { combineLatest } from 'rxjs';
import { map } from 'rxjs/operators';
import { AuthService } from '../../services/auth.service';
import { ChatService } from '../../services/chat.service';
import { Message } from '../../models/message.model';
import { User } from '../../models/user.model';

// ============================================================
// ChatComponent - Solo se encarga de la UI
// NO tiene lógica de conexión ni comunicación
// Todo eso está en ChatService
// ============================================================

@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    MatCardModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatListModule,
    MatToolbarModule,
    MatIconModule
  ],
  templateUrl: './chat.component.html',
  styleUrl: './chat.component.scss'
})
export class ChatComponent implements OnInit {
  // --------------------------------------------------------
  // Inyectar servicios
  // --------------------------------------------------------
  private authService = inject(AuthService);
  private chatService = inject(ChatService);
  private router = inject(Router);

  // --------------------------------------------------------
  // Datos del componente
  // --------------------------------------------------------
  messages$ = this.chatService.messages$;
  rooms$ = this.chatService.rooms$;
  selectedRoomId$ = this.chatService.selectedRoomId$;
  connectedUsers$ = this.chatService.connectedUsers$;
  selectedRoomName$ = combineLatest([this.rooms$, this.selectedRoomId$]).pipe(
    map(([rooms, id]) => rooms.find(r => r.id === id)?.name || '')
  );
  newMessage = '';
  currentUser: User | null = null;
  newRoomName = '';
  roomError = '';
  creatingRoom = false;

  // --------------------------------------------------------
  // Obtener el nombre del usuario autenticado
  // --------------------------------------------------------
  get username(): string {
    return this.currentUser?.displayName || this.currentUser?.email || 'Usuario';
  }

  ngOnInit(): void {
    this.authService.currentUser$.subscribe((user) => {
      this.currentUser = user;
      if (user) {
        this.chatService.setUserEmail(user.email);
        this.chatService.setUserDisplayName(user.displayName || user.email);
      }
    });

    this.chatService.loadRooms();
  }

  // --------------------------------------------------------
  // Seleccionar una sala
  // --------------------------------------------------------
  selectRoom(roomId: number): void {
    this.chatService.selectRoom(roomId);
  }

  // --------------------------------------------------------
  // Crear sala
  // --------------------------------------------------------
  async createRoom(): Promise<void> {
    const name = this.newRoomName.trim();
    this.roomError = '';

    if (!name) {
      this.roomError = 'El nombre de la sala no puede estar vacío';
      return;
    }

    this.creatingRoom = true;
    try {
      const room = await this.chatService.createRoom(name);
      this.newRoomName = '';
      this.chatService.selectRoom(room.id);
    } catch (error: any) {
      this.roomError = error.message || 'Error al crear la sala';
    } finally {
      this.creatingRoom = false;
    }
  }

  // --------------------------------------------------------
  // Enviar mensaje - llama al service, no hace nada más
  // --------------------------------------------------------
  sendMessage(): void {
    if (this.newMessage.trim() && this.currentUser) {
      this.chatService.sendMessage(this.newMessage, this.currentUser.email);
      this.newMessage = '';
    }
  }

  // --------------------------------------------------------
  // Cerrar sesión
  // --------------------------------------------------------
  logout(): void {
    this.authService.logout().then(() => {
      this.router.navigate(['/login']);
    });
  }

  // --------------------------------------------------------
  // trackBy para optimizar el render de la lista
  // --------------------------------------------------------
  trackByMessageId(index: number, message: Message): string {
    return message.id;
  }
}