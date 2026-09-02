import { Routes } from '@angular/router';
export const routes: Routes = [{ path: '', loadComponent: () => import('./app').then((component) => component.App) }, { path: '**', redirectTo: '' }];
