import { Routes } from '@angular/router';
import { authGuard } from './guards/auth.guard';

export const routes: Routes = [
  // Redirigir la raíz a /chat (que a su vez redirige a login si no está autenticado)
  {
    path: '',
    redirectTo: 'chat',
    pathMatch: 'full'
  },
  // Ruta de login
  {
    path: 'login',
    loadComponent: () =>
      import('./components/login/login.component').then(m => m.LoginComponent)
  },
  // Ruta de registro
  {
    path: 'register',
    loadComponent: () =>
      import('./components/register/register.component').then(m => m.RegisterComponent)
  },
  // Ruta del chat (protegida por authGuard)
  {
    path: 'chat',
    loadComponent: () =>
      import('./components/chat/chat.component').then(m => m.ChatComponent),
    canActivate: [authGuard]
  },
  // Cualquier otra ruta unknown redirige a login
  {
    path: '**',
    redirectTo: 'login'
  }
];