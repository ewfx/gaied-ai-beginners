import { Component } from '@angular/core';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { ClassifiedEmailComponent } from '../classified-email/classified-email.component';
import { DuplicateComponent } from '../duplicate-mail/duplicate.component';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css'],
  standalone: true,
  imports: [CommonModule,ClassifiedEmailComponent,DuplicateComponent],
})
export class DashboardComponent {
  constructor(private http: HttpClient, private apiService: ApiService) {}

  

  response: Array<{ 
    email_subject: string; 
    request_type: string; 
    request_subtype: string; 
    confidence_score: number; 
    reasoning: string 
  }> = [];
  isLoading: boolean = false; 

  process_and_classify_emails() {
    this.isLoading = true;
    this.apiService.process_and_classify_emails().subscribe(
      (data) => {
        this.response = Array.isArray(data.response) ? data.response : [data.response]; 
        this.isLoading = false; 
        alert('File processed successfully!');
      });
  }

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;

    if (input.files && input.files.length > 0) {
      const file = input.files[0];
      const fileName = file.name;
      const fileExtension = fileName.split('.').pop()?.toLowerCase();

      // Validate file extension
      if (fileExtension === 'eml' || fileExtension === 'msg') {
        console.log('File selected:', file);

        // Upload the file to the server
        const formData = new FormData();
        formData.append('file', file);

        this.http.post('http://localhost:8000/upload-file/', formData).subscribe(
          (response) => {
            console.log('File uploaded successfully:', response);
            alert('File uploaded successfully!');
          },
          (error) => {
            console.error('Error uploading file:', error);
            alert('Error uploading file. Please try again.');
          }
        );
      } else {
        console.error('Invalid file type. Only .eml and .msg files are allowed.');
        alert('Invalid file type. Please upload only .eml or .msg files.');
      }
    }
  }

}