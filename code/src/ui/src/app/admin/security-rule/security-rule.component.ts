import { Component, OnInit } from '@angular/core';
import { SecurityRuleService, SecurityRule } from '../../../services/security-rule.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-security-rule',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './security-rule.component.html',
  styleUrl: './security-rule.component.css',
})
export class SecurityRuleComponent implements OnInit {
  securityRules: (SecurityRule & { rulesString: string })[] = []; // Add rulesString for UI
  newRule: SecurityRule & { rulesString: string } = { collection: '', rules: [], rulesString: '' };

  constructor(private securityRuleService: SecurityRuleService) {}

  ngOnInit(): void {
    this.loadSecurityRules();
  }

  // Load all security rules
  loadSecurityRules(): void {
    this.securityRuleService.getAllSecurityRules().subscribe(
      (data) => {
        // Map rules array to a comma-separated string for UI
        this.securityRules = data.map((rule) => ({
          ...rule,
          rulesString: rule.rules.join(', '), // Convert array to string
        }));
        console.log('Security Rules:', this.securityRules);
      },
      (error) => {
        console.error('Error loading security rules:', error);
      }
    );
  }

  // Add a new security rule
  addSecurityRule(): void {
    // Convert rulesString to an array before saving
    const newRuleToSave: SecurityRule = {
      collection: this.newRule.collection,
      rules: this.newRule.rulesString.split(',').map((rule) => rule.trim()), // Convert string to array
    };

    this.securityRuleService.createSecurityRule(newRuleToSave).subscribe(
      (data) => {
        console.log('New Rule Added:', data);
        this.loadSecurityRules(); // Refresh the list
        this.newRule = { collection: '', rules: [], rulesString: '' }; // Reset the form
      },
      (error) => {
        console.error('Error adding security rule:', error);
      }
    );
  }

  // Update an existing security rule
  updateSecurityRule(rule: SecurityRule & { rulesString: string }): void {
    // Convert rulesString to an array before saving
    const updatedRuleToSave: SecurityRule = {
      collection: rule.collection,
      rules: rule.rulesString.split(',').map((rule) => rule.trim()), // Convert string to array
    };

    this.securityRuleService.updateSecurityRule(rule.collection, updatedRuleToSave).subscribe(
      (data) => {
        console.log('Rule Updated:', data);
        this.loadSecurityRules(); // Refresh the list
      },
      (error) => {
        console.error('Error updating security rule:', error);
      }
    );
  }

  // Delete a security rule
  deleteSecurityRule(collectionName: string): void {
    this.securityRuleService.deleteSecurityRule(collectionName).subscribe(
      (data) => {
        console.log('Rule Deleted:', data.message);
        this.loadSecurityRules(); // Refresh the list
      },
      (error) => {
        console.error('Error deleting security rule:', error);
      }
    );
  }
}