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
    MatToolbarModule
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
  newMessage = '';
  currentUser: User | null = null;

  // --------------------------------------------------------
  // Obtener el nombre del usuario autenticado
  // --------------------------------------------------------
  get username(): string {
    return this.currentUser?.displayName || this.currentUser?.email || 'Usuario';
  }

  ngOnInit(): void {
    // Obtener el usuario actual de Firebase
    this.authService.currentUser$.subscribe((user) => {
      this.currentUser = user;
    });
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