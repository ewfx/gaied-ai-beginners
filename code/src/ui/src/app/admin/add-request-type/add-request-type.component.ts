import { Component, OnInit } from '@angular/core';
import { RequestTypeService } from '../../../services/request-type.service';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';

interface RequestType {
  type: string;
  subRequestTypes: string[];
}
@Component({
  selector: 'app-add-request-type',
  templateUrl: './add-request-type.component.html',
  styleUrl: './add-request-type.component.css',
  standalone: true,
  imports: [CommonModule] 
})
export class AddRequestTypeComponent implements OnInit {

  requestTypes: RequestType[] = [];
  newRequestType: RequestType = { type: '', subRequestTypes: [] };
  subRequestTypeString: string = '';
  selectedRequestType: RequestType | null = null;

  constructor(private requestTypeService: RequestTypeService) { }

  ngOnInit(): void {
    this.loadRequestTypes();
  }

  // Load request types and ensure response is an array
  loadRequestTypes() {
    this.requestTypeService.loadRequestTypes().subscribe((data: any) => {
      if (data?.CommercialBankLendingService?.RequestTypes && Array.isArray(data.CommercialBankLendingService.RequestTypes)) {
        this.requestTypes = data.CommercialBankLendingService.RequestTypes;
      } else {
        console.error('API response does not contain expected RequestTypes array:', data);
        this.requestTypes = []; // Prevents NG0900 error
      }
    });
  }
// Update subRequestTypes list dynamically
updateSubtypeList() {
  this.newRequestType.subRequestTypes = this.subRequestTypeString.split(',').map(s => s.trim());
}

// Add a new request type
onAddRequestType() {
  if (this.newRequestType.type) {
    this.updateSubtypeList();
    this.requestTypeService.addRequestType(this.newRequestType).subscribe(() => {
      this.loadRequestTypes();
      this.newRequestType = { type: '', subRequestTypes: [] };
      this.subRequestTypeString = '';
    });
  }
}

// Edit request type
onEdit(request: RequestType) {
  this.selectedRequestType = { ...request };
  this.subRequestTypeString = this.selectedRequestType.subRequestTypes.join(', ');
}

// Update request type
updateRequestType() {
  if (this.selectedRequestType) {
    this.selectedRequestType.subRequestTypes = this.subRequestTypeString.split(',').map(s => s.trim());

    this.requestTypeService.updateRequestType(this.selectedRequestType).subscribe({
      next: () => {
        this.loadRequestTypes();
        this.selectedRequestType = null;
        this.subRequestTypeString = '';
      },
      error: (error) => {
        console.error('Update Error:', error);
        alert(`Update failed: ${error.error?.detail || 'Something went wrong!'}`);
      }
    });
  }
}

// Delete request type
onDelete(type: string) {
  this.requestTypeService.deleteRequestType(type).subscribe(() => {
    this.loadRequestTypes();
  });
}
}
