import { Routes, provideRouter } from '@angular/router';
import {AdminComponent} from './admin/admin.component';
import {DuplicateComponent} from './duplicate-mail/duplicate.component';
import {ClassifiedEmailComponent} from './classified-email/classified-email.component';
import {DashboardComponent} from './dashboard/dashboard.component';

export const routes: Routes = [
    {path: '',component: DashboardComponent},
    {path: 'dashboard', component: DashboardComponent},
    {path: 'admin',component: AdminComponent}];
    

export const appRoutingProviders = [provideRouter(routes)];
