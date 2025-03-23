import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { FormsModule } from '@angular/forms'; // Import FormsModule for two-way binding
import { CommonModule } from '@angular/common'; // Import CommonModule for *ngIf and *ngFor

import { ApiService } from '../services/api.service';

@Component({
  selector: 'app-root',
  standalone: true, // Mark this component as standalone
  imports: [RouterOutlet, FormsModule,CommonModule], 
  providers: [ApiService], 
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'], // Fix typo: styleUrl -> styleUrls
})
export class AppComponent {
  
  }





