import { HttpClientModule } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { RouterModule } from '@angular/router'; 

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrl: './app.component.css', standalone: true, 
  imports: [RouterModule, HttpClientModule] 
})
export class AppComponent implements OnInit {
  title = 'ang-base-sf';

  ngOnInit() {
    console.log('AppComponent initialized');
  }
}
