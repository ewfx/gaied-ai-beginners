import { Component, OnInit } from '@angular/core';
import { PrioritizationRulesService } from '../../../services/prioritization-rules.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
export interface PrioritizationRule {
  priority: number;
  request_type: string;
  description: string;
  isEditing?: boolean; // Flag to track edit state
  isAdding?: boolean; // Flag to track add state
}

@Component({
  selector: 'app-prioritization-rules',
  templateUrl: './prioritization-rules.component.html',
  styleUrl: './prioritization-rules.component.css',
  standalone: true,
  imports:[CommonModule,FormsModule]
})
export class PrioritizationRulesComponent implements OnInit {
  priorities: PrioritizationRule[] = [];

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
    const newRule: PrioritizationRule = {
      priority: this.priorities.length + 1, // Assign a temporary priority
      request_type: '',
      description: '',
      isEditing: true,
      isAdding: true,
    };

    // Add the new rule at the beginning of the array
    this.priorities.unshift(newRule);
  }

  onEdit(rule: PrioritizationRule): void {
    rule.isEditing = true;
  }

  onSave(rule: PrioritizationRule): void {
    rule.isEditing = false;

    if (rule.isAdding) {
      // Handle adding a new rule (e.g., API call)
      console.log('Adding new rule:', rule);
      rule.isAdding = false;
      this.onAddRule(rule);
    } else {
      // Handle updating an existing rule (e.g., API call)
      console.log('Updating rule:', rule);
      this.updateExistingRule(rule);
    }
  }

  onCancel(rule: PrioritizationRule): void {
    if (rule.isAdding) {
      // Remove the rule if it was newly added and canceled
      this.priorities = this.priorities.filter((r) => r !== rule);
    } else {
      // Reset the editing state
      rule.isEditing = false;
    }
  }
  
 
  onAddRule(rule: PrioritizationRule): void {
    this.prioritizationRulesService.post(rule).subscribe(
      (response) => {
        console.log('Rule added successfully:', response);
        this.loadPriorityRules(); // Refresh the list
      },
      (error) => {
        console.error('Error adding rule:', error);
      }
    );
  }

  updateExistingRule(rule: PrioritizationRule): void {
    this.prioritizationRulesService.put(rule).subscribe(
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