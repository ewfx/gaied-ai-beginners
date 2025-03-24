import { bootstrapApplication } from '@angular/platform-browser';
import { AppComponent } from './app/app.component';
import { importProvidersFrom } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { provideRouter, Routes } from '@angular/router';
import { RequestTypeComponent } from './app/add-request-type/add-request-type.component';

const routes: Routes = [
  { path: '', component: RequestTypeComponent },
];

bootstrapApplication(AppComponent, {
  providers: [
    importProvidersFrom(HttpClientModule),
    provideRouter(routes),
  ]
}).catch(err => console.error(err));
