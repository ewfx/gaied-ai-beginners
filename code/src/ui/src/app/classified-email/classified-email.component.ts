import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import {ApiService} from '../../services/api.service';
import { ClassifiedEmailResponse } from '../Models/emailClassification';



@Component({
  selector: 'classified-email',
  templateUrl: './classified-email.component.html',
  styleUrl: './classified-email.component.css',
  standalone: true,
  imports: [CommonModule] 
})

export class ClassifiedEmailComponent implements OnInit {
  classifiedEmail: ClassifiedEmailResponse[] = [];
    constructor(private apiService: ApiService) { }
    
    ngOnInit(): void {
      this.loadClassifiedEmail();
    }

    loadClassifiedEmail() {
      this.apiService.get_classify_emails().subscribe((data: any) => {
        if (data != null) {
          this.classifiedEmail = data;
        } else {
          console.error('API response does not contain expected RequestTypes array:', data);
          this.classifiedEmail = []; // Prevents NG0900 error
        }
      });
    }
}