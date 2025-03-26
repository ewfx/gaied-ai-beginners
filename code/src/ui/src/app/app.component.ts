
import { HttpClientModule } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { RouterModule } from '@angular/router'; 
import { ApiService } from '../services/api.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrl: './app.component.css', standalone: true, 
  imports: [RouterModule, HttpClientModule] 
})
export class AppComponent  {
  title = 'email-classification-ui';
  constructor() {} 
  

  
}
