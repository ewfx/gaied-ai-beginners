import { Routes } from '@angular/router';
import { DashboardComponent } from './dashboard/dashboard.component'; // Adjust the path as needed
import { AdminComponent } from './admin/admin.component'; // Adjust the path as needed

export const routes: Routes = [
  { path: 'dashboard', component: DashboardComponent },
  { path: '', redirectTo: '/dashboard', pathMatch: 'full' },
  { path: 'admin', component:AdminComponent, pathMatch: 'full' },
];