import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface SecurityRule {
  collection: string;
  rules: string[];
}

@Injectable({
  providedIn: 'root',
})
export class SecurityRuleService {
  private apiUrl = 'http://localhost:8000/security-rules/security-rules'; // Base URL for the API

  constructor(private http: HttpClient) {}

  // 1. Get all security rules
  getAllSecurityRules(): Observable<SecurityRule[]> {
    return this.http.get<SecurityRule[]>(this.apiUrl);
  }

  // 2. Get a single security rule by collection name
  getSecurityRule(collectionName: string): Observable<SecurityRule> {
    return this.http.get<SecurityRule>(`${this.apiUrl}/${collectionName}`);
  }

  // 3. Create a new security rule
  createSecurityRule(newRule: SecurityRule): Observable<SecurityRule> {
    return this.http.post<SecurityRule>(this.apiUrl, newRule);
  }

  // 4. Update an existing security rule by collection name
  updateSecurityRule(
    collectionName: string,
    updatedRule: SecurityRule
  ): Observable<SecurityRule> {
    return this.http.put<SecurityRule>(
      `${this.apiUrl}/${collectionName}`,
      updatedRule
    );
  }

  // 5. Delete a security rule by collection name
  deleteSecurityRule(collectionName: string): Observable<{ message: string }> {
    return this.http.delete<{ message: string }>(
      `${this.apiUrl}/${collectionName}`
    );
  }
}