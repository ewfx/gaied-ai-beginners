import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { Test1Component } from './test1/test1.component';
import { Test2Component } from './test2/test2.component';
import { ComingSoonComponent } from './coming-soon/coming-soon.component';
import { AdminComponent } from './admin/admin.component';
import { AddRequestTypeComponent } from './admin/add-request-type/add-request-type.component';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { PrioritizationRulesComponent } from './admin/prioritization-rules/prioritization-rules.component';

@NgModule({
  declarations: [
    AppComponent,
    Test1Component,
    Test2Component,
    ComingSoonComponent,
    AdminComponent,
    AddRequestTypeComponent,
    PrioritizationRulesComponent    
  ],
  imports: [
    BrowserModule,
    NgbModule,
    FormsModule,
    HttpClientModule,
    AppRoutingModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
