import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { map } from 'rxjs/operators';

const JSON_FILE_PATH = 'E:/Hackthon 2025/new/gaied-ai-beginners/code/src/ui/assets/request-types.json';
const STORAGE_KEY = 'requestTypesData';

@Injectable({
  providedIn: 'root',
})
export class RequestTypeService {
  private requestTypes: any[] = [];

  constructor(private http: HttpClient) {}

  // Load data from JSON file or localStorage
  loadRequestTypes(): Observable<any> {
    const storedData = localStorage.getItem(STORAGE_KEY);

    if (storedData) {
      this.requestTypes = JSON.parse(storedData);
      return of(this.requestTypes);
    } else {
      return this.http.get<any>(JSON_FILE_PATH).pipe(
        map((data) => {
          this.requestTypes = data.CommercialBankLendingService.RequestTypes;
          localStorage.setItem(STORAGE_KEY, JSON.stringify(this.requestTypes));
          return this.requestTypes;
        })
      );
    }
  }

  // Get all request types
  getRequestTypes(): Observable<any[]> {
    return of(this.requestTypes);
  }

  // Add a new request type
  addRequestType(requestType: any): Observable<any> {
    this.requestTypes.push(requestType);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(this.requestTypes));
    return of(requestType);
  }

  // Update a request type
  updateRequestType(updatedRequest: any): Observable<any> {
    const index = this.requestTypes.findIndex((req) => req.type === updatedRequest.type);
    if (index !== -1) {
      this.requestTypes[index] = updatedRequest;
      localStorage.setItem(STORAGE_KEY, JSON.stringify(this.requestTypes));
    }
    return of(updatedRequest);
  }

  // Delete a request type
  deleteRequestType(type: string): Observable<any> {
    this.requestTypes = this.requestTypes.filter((req) => req.type !== type);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(this.requestTypes));
    return of({ message: 'Deleted successfully' });
  }
}
