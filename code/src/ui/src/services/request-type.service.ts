import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { map } from 'rxjs/operators';

const BASE_ENDPOINT = 'http://127.0.0.1:8000';
const API_ENDPOINT = '/request-types/request-types';
const POST_API_ENDPOINT = '/request-types/request-types';
const PUT_API_ENDPOINT = '/request-types/request-types';
const Delete_API_ENDPOINT = '/request-types/request-types';

@Injectable({
  providedIn: 'root',
})
export class RequestTypeService {
  private requestTypes: any[] = [];

  constructor(private http: HttpClient) {}

 
  loadRequestTypes(): Observable<any> {
    return this.http.get<any>(BASE_ENDPOINT+API_ENDPOINT);
  }

   // Get all request types
   getRequestTypes(): Observable<any[]> {
    return this.http.get<any[]>(BASE_ENDPOINT+API_ENDPOINT);
  }

 
  addRequestType(requestType: any): Observable<any> {
    return this.http.post<any>(BASE_ENDPOINT+POST_API_ENDPOINT, requestType);
  }

  updateRequestType(updatedRequest: any): Observable<any> {
    const url = `${BASE_ENDPOINT+PUT_API_ENDPOINT}/${encodeURIComponent(updatedRequest.type)}`; 
    return this.http.put(url, { 
      type: updatedRequest.type,  
      subRequestTypes: updatedRequest.subRequestTypes 
    });
  }
   
  deleteRequestType(id: string): Observable<any> {
    return this.http.delete<any>(`${BASE_ENDPOINT+Delete_API_ENDPOINT}/${id}`);
  }
}