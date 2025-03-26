import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import {DuplicateEmail} from '../Models/duplicateEmail';
import {ApiService} from '../../services/api.service';

@Component({
  selector: 'duplicate-list',
  templateUrl: './duplicate.component.html',
  styleUrl: './duplicate.component.css',
  standalone: true,
  imports: [CommonModule]
})


export class DuplicateComponent implements OnInit {
  duplicateEmail: DuplicateEmail[] = [];
  constructor(private apiService: ApiService) { }
  
  ngOnInit(): void {
    this.loadDuplicateEmail();
  }  
    
  loadDuplicateEmail() {
    this.apiService.get_duplicate_emails().subscribe((data: any) => {
      if (data != null) {
        this.duplicateEmail = data;
      } else {
        console.error('API response does not contain expectedduplicate array:', data);
        this.duplicateEmail = []; // Prevents NG0900 error
      }
    });
  }
}