import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { map } from 'rxjs/operators';

//const JSON_FILE_PATH = 'E:/Hackthon 2025/new/gaied-ai-beginners/code/src/ui/assets/request-types.json';
const API_ENDPOINT = 'http://127.0.0.1:8000/request-types/request-types';
const POST_API_ENDPOINT = 'http://127.0.0.1:8000/request-types/request-types';
const PUT_API_ENDPOINT = 'http://127.0.0.1:8000/request-types/request-types';
const Delete_API_ENDPOINT = 'http://127.0.0.1:8000/request-types/request-types';
const STORAGE_KEY = 'requestTypesData';

@Injectable({
  providedIn: 'root',
})
export class RequestTypeService {
  private requestTypes: any[] = [];

  constructor(private http: HttpClient) {}

 
  loadRequestTypes(): Observable<any> {
    return this.http.get<any>(API_ENDPOINT);
  }

   // Get all request types
   getRequestTypes(): Observable<any[]> {
    return this.http.get<any[]>(API_ENDPOINT);
  }

 
  addRequestType(requestType: any): Observable<any> {
    return this.http.post<any>(POST_API_ENDPOINT, requestType);
  }

  updateRequestType(updatedRequest: any): Observable<any> {
    const url = `${PUT_API_ENDPOINT}/${encodeURIComponent(updatedRequest.type)}`; 
    return this.http.put(url, { 
      type: updatedRequest.type,  
      subRequestTypes: updatedRequest.subRequestTypes 
    });
  }
   
  deleteRequestType(id: string): Observable<any> {
    return this.http.delete<any>(`${Delete_API_ENDPOINT}/${id}`);
  }
}
