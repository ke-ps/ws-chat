import { inject } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../services/auth.service';
import { filter, map, switchMap, take } from 'rxjs/operators';

// ============================================================
// AuthGuard - Protege las rutas que requieren autenticación
// Si el usuario no está logueado, redirige a /login
// Espera a que Firebase termine de inicializar antes de decidir
// ============================================================

export const authGuard = () => {
  const authService = inject(AuthService);
  const router = inject(Router);

  return authService.authInitialized$.pipe(
    filter((initialized) => initialized),
    take(1),
    switchMap(() => authService.currentUser$),
    take(1),
    map((user) => {
      if (user) {
        return true;
      } else {
        return router.createUrlTree(['/login']);
      }
    })
  );
};