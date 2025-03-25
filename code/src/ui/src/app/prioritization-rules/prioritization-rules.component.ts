import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';  
import { HttpClient, HttpClientModule, HttpErrorResponse } from '@angular/common/http';

interface PrioritizationRule {
  priority: number;
  request_type: string[];
  description: string;
}

@Component({
  selector: 'app-prioritization-rules',
  standalone: true,   
  imports: [CommonModule, FormsModule, HttpClientModule],  
  templateUrl: './prioritization-rules.component.html',
  styleUrls: ['./prioritization-rules.component.css']
})
export class PrioritizationRulesComponent implements OnInit {
  apiUrl = 'http://127.0.0.1:8000/prioritization-rules/prioritization-rules';
  rules: PrioritizationRule[] = [];
  // newRule: PrioritizationRule = { priority: null, request_type: [], description: '' };
  newRule: PrioritizationRule = { priority: 0, request_type: [], description: '' };
  selectedRule: PrioritizationRule | null = null;
  requestTypeString = '';
  errorMessage: string | null = null; 

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    this.getRules();
  }

  /** GET: Fetch all prioritization rules */
  getRules(): void {
    this.http.get<{ PrioritizationRules: PrioritizationRule[] }>(this.apiUrl).subscribe({
      next: response => {
        this.rules = response.PrioritizationRules;
      },
      error: (error: HttpErrorResponse) => {
        this.handleError(error, 'Error fetching rules');
      }
    });
  }

  /** POST: Add a new prioritization rule */
  addRule() {
    this.errorMessage = null; // Clear previous errors before submitting
    this.newRule.request_type = this.requestTypeString.split(',').map(type => type.trim());

    this.http.post(this.apiUrl, this.newRule).subscribe({
      next: (response) => {
        console.log('Rule added successfully:', response);
        this.getRules();  // Refresh the list
        this.resetForm(); // Reset form
      },
      error: (error: HttpErrorResponse) => {
        this.handleError(error, 'Error adding rule');
      }
    });
  }

  /** Edit selected rule */
  editRule(rule: PrioritizationRule): void {
    this.errorMessage = null;
    this.selectedRule = { ...rule };
    this.requestTypeString = rule.request_type.join(', ');
  }

  /** PUT: Update existing prioritization rule */
  updateRule(): void {
    this.errorMessage = null;
    if (!this.selectedRule) return;

    this.selectedRule.request_type = this.requestTypeString.split(',').map(type => type.trim());

    this.http.put(`${this.apiUrl}/${this.selectedRule.priority}`, this.selectedRule).subscribe({
      next: () => {
        this.getRules();
        this.selectedRule = null;
      },
      error: (error: HttpErrorResponse) => {
        this.handleError(error, 'Error updating rule');
      }
    });
  }

  /** DELETE: Remove a prioritization rule */
  // deleteRule(priority: number): void {
  //   this.http.delete(`${this.apiUrl}/${priority}`).subscribe({
  //     next: () => this.getRules(),
  //     error: (error: HttpErrorResponse) => {
  //       this.handleError(error, 'Error deleting rule');
  //     }
  //   });
  // }
  deleteRule(priority: number | null): void {
    if (priority === null) {
      console.warn('Cannot delete rule with null priority');
      return;
    }
    this.http.delete(`${this.apiUrl}/${priority}`).subscribe({
      next: () => this.getRules(),
      error: (error: HttpErrorResponse) => {
        this.handleError(error, 'Error deleting rule');
      }
    });
  }
  /** Reset form */
  resetForm(): void {
    this.newRule = { priority: 0, request_type: [], description: '' };
    this.requestTypeString = '';
  }

  /** Handle API errors */
  private handleError(error: HttpErrorResponse, defaultMessage: string) {
    console.error(defaultMessage, error.error.detail);
    
    if (error.status === 400) {
      this.errorMessage = error.error?.detail || 'Validation error: Duplicate priority!';
    } else if (error.status === 500) {
      this.errorMessage = error.error?.detail || 'Server error. Please try again later.';
    } else {
      this.errorMessage = 'An unexpected error occurred.';
    }
  }
}
