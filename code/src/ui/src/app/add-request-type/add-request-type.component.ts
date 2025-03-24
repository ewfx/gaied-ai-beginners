import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RequestTypeService } from '../../services/request-type.service';
interface RequestType {
  type: string;
  subRequestTypes: string[];
}
@Component({
  selector: 'app-request-type',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './add-request-type.component.html',
  styleUrls: ['./add-request-type.component.css'],
})
export class RequestTypeComponent implements OnInit {
  requestTypes: any[] = [];
 // newRequestType = { type: '', subRequestTypes: '' };
  //newRequestType: { type: string; subRequestTypes: string[] } = { type: '', subRequestTypes: [] };
  newRequestType: { type: string; subRequestTypes: string | string[] } = { type: '', subRequestTypes: '' };
  subRequestTypeString: string = '';
  //selectedRequestType = null;
  selectedRequestType: RequestType | null = { type: '', subRequestTypes: [] };

  constructor(private requestTypeService: RequestTypeService) {}
  ngOnInit(): void {
    this.requestTypeService.loadRequestTypes().subscribe((data) => {
      this.requestTypes = data;
    });
    // this.selectedRequestType = {
    //   type: 'Loan Application',
    //   subRequestTypes: ['Personal Loan', 'Business Loan']
    // };
  }
  // ngOnInit(): void {
  //   this.loadRequestTypes();
  // }

  loadRequestTypes() {
    this.requestTypeService.loadRequestTypes().subscribe((data: any[]) => {
      this.requestTypes = data;
    });
  }

 
  addRequestType() {
    if (this.newRequestType.type) {
      // Ensure subRequestTypes is always an array
      if (typeof this.newRequestType.subRequestTypes === 'string') {
        this.newRequestType.subRequestTypes = this.newRequestType.subRequestTypes.split(',').map(s => s.trim());
      }
  
      this.requestTypeService.addRequestType(this.newRequestType).subscribe(() => {
        this.loadRequestTypes();
        this.newRequestType = { type: '', subRequestTypes: '' }; // Reset with correct type
      });
    }
  }
  
  // editRequestType(requestType: any) {
  //   this.selectedRequestType = { ...requestType };
  // }
  editRequestType(request: RequestType) {
    this.selectedRequestType = { ...request };
    
    // Convert subRequestTypes array into a string for editing
    this.subRequestTypeString = this.selectedRequestType.subRequestTypes.join(', ');
  }
  // updateRequestType() {
  //   if (this.selectedRequestType) {
  //     this.requestTypeService.updateRequestType(this.selectedRequestType).subscribe(() => {
  //       this.loadRequestTypes();
  //       this.selectedRequestType = { type: '', subRequestTypes: [] };
  //     });
  //   }
  // }
  updateSubtypeList() {
    if (this.selectedRequestType) {
      this.selectedRequestType.subRequestTypes = this.subRequestTypeString.split(',').map(subType => subType.trim());
    }
  }
  updateRequestType() {
    if (this.selectedRequestType) {
      // Convert the comma-separated string to an array before saving
      this.selectedRequestType.subRequestTypes = this.selectedRequestType.subRequestTypes
        .toString()
        .split(',')
        .map(subType => subType.trim());
  
      // Find the index of the selected request type
      const index = this.requestTypes.findIndex(req => req.type === this.selectedRequestType!.type);
  
      if (index !== -1) {
        this.requestTypes[index] = { ...this.selectedRequestType };
      }
  
      // Clear the selectedRequestType after updating
      this.selectedRequestType = null;
      this.selectedRequestType = { type: '', subRequestTypes: [] };
    }
  }
  
  deleteRequestType(type: string) {
    this.requestTypeService.deleteRequestType(type).subscribe(() => {
      this.loadRequestTypes();
    });
  }
}
