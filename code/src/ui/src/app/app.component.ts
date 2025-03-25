import { Component } from '@angular/core';
import { RouterModule, RouterOutlet } from '@angular/router';
import { FormsModule } from '@angular/forms'; // Import FormsModule for two-way binding
import { HttpClientModule } from '@angular/common/http'; // Import HttpClientModule for API calls
import { CommonModule } from '@angular/common'; // Import CommonModule for *ngIf and *ngFor
import { ApiService } from '../services/api.service';

@Component({
  selector: 'app-root',
  standalone: true, // Mark this component as standalone
  imports: [
    RouterModule, 
    RouterOutlet, 
    FormsModule,
    CommonModule,
    HttpClientModule
  ], 
  providers: [ApiService], 
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'], // Fix typo: styleUrl -> styleUrls
})
export class AppComponent {
  title = 'email-classification-ui';
  prompt: string = ''; // User input for the prompt
  response: Array<{ 
    email_subject: string; 
    request_type: string; 
    request_subtype: string; 
    confidence_score: number; 
    reasoning: string 
  }> = [];
  isLoading: boolean = false; // Loading state for the button

  constructor(private apiService: ApiService) {}

  process_and_classify_emails() {
    this.apiService.process_and_classify_emails().subscribe(
      (data) => {
        this.response = Array.isArray(data.response) ? data.response : [data.response]; 
        this.isLoading = false; 
      });

  }
}

