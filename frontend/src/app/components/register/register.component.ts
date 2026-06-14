import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatDividerModule } from '@angular/material/divider';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    MatCardModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatDividerModule
  ],
  templateUrl: './register.component.html',
  styleUrl: './register.component.scss'
})
export class RegisterComponent {
  // --------------------------------------------------------
  // Inyectar servicios
  // --------------------------------------------------------
  private authService = inject(AuthService);
  private router = inject(Router);

  // --------------------------------------------------------
  // Datos del formulario
  // --------------------------------------------------------
  email = '';
  password = '';
  confirmPassword = '';
  errorMessage = '';
  loading = false;

  // --------------------------------------------------------
  // Registro con Firebase Auth
  // --------------------------------------------------------
  onRegister(): void {
    if (!this.email || !this.password || !this.confirmPassword) {
      this.errorMessage = 'Por favor, completa todos los campos';
      return;
    }

    if (this.password !== this.confirmPassword) {
      this.errorMessage = 'Las contraseñas no coinciden';
      return;
    }

    if (this.password.length < 6) {
      this.errorMessage = 'La contraseña debe tener al menos 6 caracteres';
      return;
    }

    this.loading = true;
    this.errorMessage = '';

    this.authService.register(this.email, this.password)
      .then(() => {
        // Registro exitoso, redirigir al chat
        this.router.navigate(['/chat']);
      })
      .catch((error) => {
        this.errorMessage = this.getErrorMessage(error.code);
      })
      .finally(() => {
        this.loading = false;
      });
  }

  // --------------------------------------------------------
  // Navegar a login
  // --------------------------------------------------------
  goToLogin(): void {
    this.router.navigate(['/login']);
  }

  // --------------------------------------------------------
  // Traducir errores de Firebase a mensajes legibles
  // --------------------------------------------------------
  private getErrorMessage(code: string): string {
    const errors: Record<string, string> = {
      'auth/email-already-in-use': 'Ya existe una cuenta con este email',
      'auth/invalid-email': 'El formato del email no es válido',
      'auth/weak-password': 'La contraseña es demasiado débil',
      'auth/operation-not-allowed': 'El registro está desactivado'
    };
    return errors[code] || 'Error al registrar. Inténtalo de nuevo.';
  }
}