import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { FormsModule } from '@angular/forms'; // Import FormsModule for two-way binding
import { HttpClientModule } from '@angular/common/http'; // Import HttpClientModule for API calls
import { CommonModule } from '@angular/common'; // Import CommonModule for *ngIf and *ngFor

import { ApiService } from '../services/api.service';

@Component({
  selector: 'app-root',
  standalone: true, // Mark this component as standalone
  imports: [RouterOutlet, FormsModule,CommonModule, HttpClientModule], // Import required modules
  providers: [ApiService], 
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'], // Fix typo: styleUrl -> styleUrls
})
export class AppComponent {
  title = 'email-classification-ui';
  prompt: string = ''; // User input for the prompt
  response: string | null = null; // Response from the API
  isLoading: boolean = false; // Loading state for the button

  constructor(private apiService: ApiService) {}

  classifyEmail() {
    this.isLoading = true; // Set loading state to true
    this.apiService.classify(this.prompt).subscribe(
      (data) => {
        this.response = data.response; // Set the API response
        this.isLoading = false; // Reset loading state
      },
      (error) => {
        console.error('Error:', error);
        this.response = 'An error occurred while classifying the email.';
        this.isLoading = false; // Reset loading state
      }
    );
  }
}

