import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';

interface DuplicateList { 
  type: string;
  subRequestTypes: string[];
}

@Component({
  selector: 'duplicate-list',
  templateUrl: './duplicate.component.html',
  styleUrl: './duplicate.component.css',
  standalone: true,
  imports: [CommonModule]
})


export class DuplicateComponent implements OnInit {
  requestTypes: DuplicateList[] = [];
    constructor() { }
    
    ngOnInit(): void {
    }

    onEdit(request: DuplicateList) {
      // this.selectedRequestType = { ...request };
      // this.subRequestTypeString = this.selectedRequestType.subRequestTypes.join(', ');
    }

    onDelete(type: string) {
      // this.requestTypeService.deleteRequestType(type).subscribe(() => {
      //   this.loadRequestTypes();
      // });
    }
}