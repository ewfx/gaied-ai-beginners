import { Component } from '@angular/core';
import { AddRequestTypeComponent } from './add-request-type/add-request-type.component';
import { PrioritizationRulesComponent } from './prioritization-rules/prioritization-rules.component';

@Component({
  selector: 'app-admin',
  templateUrl: './admin.component.html',
  styleUrl: './admin.component.css',
  standalone: true,
  imports: [AddRequestTypeComponent,PrioritizationRulesComponent]
})
export class AdminComponent {

}
