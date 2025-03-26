import { Routes, provideRouter } from '@angular/router';
import {ComingSoonComponent} from './coming-soon/coming-soon.component';
import {AdminComponent} from './admin/admin.component';
import {DuplicateComponent} from './admin/duplicate-mail/duplicate.component';
import {ClassifiedEmailComponent} from './classified-email/classified-email.component';

export const routes: Routes = [
    {path: '',component: ClassifiedEmailComponent},
    {path: 'classified-email', component: ClassifiedEmailComponent},
    {path: 'comingsoon',component: ComingSoonComponent},
    {path: 'admin',component: AdminComponent},
    {path: 'duplicate', component: DuplicateComponent}];
    

export const appRoutingProviders = [provideRouter(routes)];
