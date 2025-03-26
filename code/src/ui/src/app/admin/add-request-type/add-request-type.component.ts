import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RequestTypeService } from '../../../services/request-type.service';

export interface RequestType {
  type: string;
  subRequestTypes: string[];
  subRequestTypesString?: string; // Temporary string for editing
  isEditing?: boolean; // Flag to track edit state
  isAdding?: boolean; // Flag to track add state
}

@Component({
  selector: 'app-add-request-type',
  standalone: true,
  imports: [FormsModule,CommonModule],
  templateUrl: './add-request-type.component.html',
  styleUrls: ['./add-request-type.component.css'],
})
export class AddRequestTypeComponent implements OnInit {
  requestTypes: RequestType[] = [];

  constructor(private requestTypeService: RequestTypeService) {}

  ngOnInit(): void {
    this.loadRequestTypes();
  }

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

  onAddRequestType(): void {
    const newRequest: RequestType = {
      type: '',
      subRequestTypes: [],
      subRequestTypesString: '',
      isEditing: true, 
      isAdding:true
    };

    // Add the new request at the beginning of the array
    this.requestTypes.unshift(newRequest);
  }


  OnAdd(request: RequestType): void {
    
      this.requestTypeService.addRequestType(request).subscribe(() => {
        this.loadRequestTypes();
       
      });
    }
  

  onEdit(request: RequestType): void {
     request.subRequestTypesString = request.subRequestTypes.join(', ');
    request.isEditing = true;
  }

  onSave(request: RequestType): void {
    request.isEditing = false;    
    request.subRequestTypes = request.subRequestTypesString
      ? request.subRequestTypesString.split(',').map((s) => s.trim())
      : [];
    if(request.isAdding)
      this.OnAdd(request);
    else
      this.updateRequestType(request);
    
  }

  updateRequestType(request: RequestType): void {
  
      this.requestTypeService.updateRequestType(request).subscribe({
        next: () => {
          this.loadRequestTypes();
        },
        error: (error) => {
          console.error('Update Error:', error);
          alert(`Update failed: ${error.error?.detail || 'Something went wrong!'}`);
        }
      });
    }
  

  onCancel(request: RequestType): void {
    if (!request.type && !request.subRequestTypes.length) {
      // If the request is empty, remove it from the array
      this.requestTypes = this.requestTypes.filter((r) => r !== request);
    } else {
      request.isEditing = false;
      // Reset the subRequestTypesString to the original value
      request.subRequestTypesString = request.subRequestTypes.join(', ');
    }
  }

  onDelete(type: string) {
    this.requestTypeService.deleteRequestType(type).subscribe(() => {
      this.loadRequestTypes();
    });
  }
}