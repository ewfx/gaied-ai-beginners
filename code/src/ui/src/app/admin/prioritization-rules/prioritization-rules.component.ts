import { Component, OnInit } from '@angular/core';
import { PrioritizationRulesService } from '../../../services/prioritization-rules.service';

@Component({
  selector: 'app-prioritization-rules',
  templateUrl: './prioritization-rules.component.html',
  styleUrl: './prioritization-rules.component.css'
})
export class PrioritizationRulesComponent {

  priorities: any[] = [];
  newRule = { priority: '', request_type: '', description: '' };
  updateRule = { priority: '', request_type: '', description: '' };

  constructor(private prioritizationRulesService: PrioritizationRulesService) {}

  ngOnInit(): void {
    this.loadPriorityRules();
  }

  loadPriorityRules(): void {
    this.prioritizationRulesService.get().subscribe(
      (data) => {
        if (data && data.PrioritizationRules) {
          this.priorities = data.PrioritizationRules;
        } else {
          console.error('Invalid API response structure:', data);
          this.priorities = []; // Fallback to an empty array
        }
      },
      (error) => {
        console.error('Error loading request types:', error);
      }
    );
  }

  addRule(): void {
    this.prioritizationRulesService.post(this.newRule).subscribe(
      (response) => {
        console.log('Rule added successfully:', response);
        this.loadPriorityRules(); // Refresh the list
      },
      (error) => {
        console.error('Error adding rule:', error);
      }
    );
  }

  updateExistingRule(): void {
    this.prioritizationRulesService.put(this.updateRule).subscribe(
      (response) => {
        console.log('Rule updated successfully:', response);
        this.loadPriorityRules(); // Refresh the list
      },
      (error) => {
        console.error('Error updating rule:', error);
      }
    );
  }

  deleteRule(id: number): void {
    this.prioritizationRulesService.delete(id).subscribe(
      (response) => {
        console.log('Rule deleted successfully:', response);
        this.loadPriorityRules(); // Refresh the list
      },
      (error) => {
        console.error('Error deleting rule:', error);
      }
    );
  }
}
