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

  // Load data from JSON file or localStorage
  // loadRequestTypes(): Observable<any> {
  //   return this.http.get<any>(API_ENDPOINT).pipe(
  //     map((data) => {
  //       this.requestTypes = data?.CommercialBankLendingService?.RequestTypes || [];
  //       return this.requestTypes;
  //     })
  //   );
  // }
  loadRequestTypes(): Observable<any> {
    return this.http.get<any>(API_ENDPOINT);
  }

   // Get all request types
   getRequestTypes(): Observable<any[]> {
    return this.http.get<any[]>(API_ENDPOINT);
  }

  // Add a new request type
  // addRequestType(requestType: any): Observable<any> {
  //   this.requestTypes.push(requestType);
  //   localStorage.setItem(STORAGE_KEY, JSON.stringify(this.requestTypes));
  //   return of(requestType);
  // }
  addRequestType(requestType: any): Observable<any> {
    return this.http.post<any>(POST_API_ENDPOINT, requestType);
  }
  // Update a request type
  // updateRequestType(updatedRequest: any): Observable<any> {
  //   const index = this.requestTypes.findIndex((req) => req.type === updatedRequest.type);
  //   if (index !== -1) {
  //     this.requestTypes[index] = updatedRequest;
  //     localStorage.setItem(STORAGE_KEY, JSON.stringify(this.requestTypes));
  //   }
  //   return of(updatedRequest);
  // }
  // Update a request type (using POST instead of PUT)
  // updateRequestType(updatedRequest: any): Observable<any> {
  //   return this.http.post<any>(PUT_API_ENDPOINT, updatedRequest); // Using POST as per your request
  // }
  // updateRequestType(updatedRequest: any): Observable<any> {
  //   const url = `${PUT_API_ENDPOINT}/${updatedRequest.type}`; // Ensure the correct resource is updated
  //   return this.http.put(url, { subRequestTypes: updatedRequest.subRequestTypes }); // Send only updatable fields
  // }

  updateRequestType(updatedRequest: any): Observable<any> {
    const url = `${PUT_API_ENDPOINT}/${encodeURIComponent(updatedRequest.type)}`; // Encode URL for special characters
    return this.http.put(url, { 
      type: updatedRequest.type,  // Ensure type is included
      subRequestTypes: updatedRequest.subRequestTypes 
    });
  }
  // // Delete a request type
  // deleteRequestType(type: string): Observable<any> {
  //   this.requestTypes = this.requestTypes.filter((req) => req.type !== type);
  //   localStorage.setItem(STORAGE_KEY, JSON.stringify(this.requestTypes));
  //   return of({ message: 'Deleted successfully' });
  // }
  deleteRequestType(id: string): Observable<any> {
    return this.http.delete<any>(`${Delete_API_ENDPOINT}/${id}`);
  }
}
