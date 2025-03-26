import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import {ClassifiedEmailComponent} from '../classified-email/classified-email.component';
import {DuplicateComponent} from '../duplicate-mail/duplicate.component'

@Component({
  selector: 'dashboard',
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.css',
  standalone: true,
  imports: [CommonModule, ClassifiedEmailComponent,DuplicateComponent] 
})

export class DashboardComponent  {

}