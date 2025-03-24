// import { Routes } from '@angular/router';

// export const routes: Routes = [];

import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { RequestTypeComponent } from './add-request-type/add-request-type.component';
import { PrioritizationRulesComponent } from './prioritization-rules/prioritization-rules.component';

export const routes: Routes = [
//   { path: '', component: EmailClassificationComponent },
  { path: 'menu1', component: RequestTypeComponent },
//   { path: 'menu2', component: PrioritizationRulesComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
