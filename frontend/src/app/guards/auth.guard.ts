import { inject } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../services/auth.service';
import { map, take } from 'rxjs/operators';

// ============================================================
// AuthGuard - Protege las rutas que requieren autenticación
// Si el usuario no está logueado, redirige a /login
// ============================================================

export const authGuard = () => {
  const authService = inject(AuthService);
  const router = inject(Router);

  return authService.currentUser$.pipe(
    take(1), // Tomar solo el primer valor y completar
    map((user) => {
      if (user) {
        return true; // Usuario autenticado, permitir acceso
      } else {
        // No autenticado, redirigir a login
        return router.createUrlTree(['/login']);
      }
    })
  );
};