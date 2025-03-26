// filepath: email-classification-ui/src/app/services/api.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class ApiService {
  private baseUrl = 'http://127.0.0.1:8000'; // FastAPI backend URL

  constructor(private http: HttpClient) {}

  // Call the classify endpoint
  classify(prompt: string): Observable<any> {
    const payload = { prompt };
    return this.http.post(`${this.baseUrl}/classify/`, payload);
  }

  classyfyContent(prompt: string): Observable<any> {    
    return this.http.get(`${this.baseUrl}/classify-content/{prompt}`);
  }

  process_and_classify_emails(): Observable<any> {    
    return this.http.get(`${this.baseUrl}/process_and_classify_emails`);
  }

  get_classify_emails(): Observable<any> {    
    return this.http.get(`${this.baseUrl}/classified-mails`);
  }
}