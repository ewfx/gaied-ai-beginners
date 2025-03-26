import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

const BASE_ENDPOINT = 'http://127.0.0.1:8000';
const API_ENDPOINT = '/prioritization-rules/prioritization-rules';
const POST_API_ENDPOINT = '/prioritization-rules/prioritization-rules';
const PUT_API_ENDPOINT = '/prioritization-rules/prioritization-rules';
const Delete_API_ENDPOINT = '/prioritization-rules/prioritization-rules';

@Injectable({
  providedIn: 'root'
})
export class PrioritizationRulesService {
  
  constructor(private http: HttpClient) {}
  
   
    loadRequestTypes(): Observable<any> {
      return this.http.get<any>(BASE_ENDPOINT+API_ENDPOINT);
    }
  
     // Get all request types
     get(): Observable<any> {
      return this.http.get<any>(BASE_ENDPOINT+API_ENDPOINT);
    }
  
   
    post(rule: any): Observable<any> {
      return this.http.post<any>(BASE_ENDPOINT+POST_API_ENDPOINT, rule);
    }
  
    put(rule: any): Observable<any> {
      const url = `${BASE_ENDPOINT+PUT_API_ENDPOINT}/${encodeURIComponent(rule.priority)}`; 
      return this.http.put(url, { 
        priority: rule.priority,  
        request_type: rule.request_type,
        description: rule.description 
      });
    }
     
    delete(id: number): Observable<any> {
      return this.http.delete<any>(`${BASE_ENDPOINT+Delete_API_ENDPOINT}/${id}`);
    }
}
