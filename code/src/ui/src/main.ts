// import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';

// import { AppModule } from './app/app.module';

import {bootstrapApplication} from '@angular/platform-browser';
import { importProvidersFrom } from '@angular/core';
import {provideRouter} from '@angular/router';
import {AppComponent} from './app/app.component';
import {routes} from './app/app.routes';
import { HttpClientModule } from '@angular/common/http';


// platformBrowserDynamic().bootstrapModule(AppModule)
//   .catch(err => console.error(err));

bootstrapApplication(AppComponent, {
  providers: [provideRouter(routes),
  importProvidersFrom(HttpClientModule)
  ]
}).catch(err => console.error(err));
