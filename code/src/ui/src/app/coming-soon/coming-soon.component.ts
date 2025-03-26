import { Component, Input, input } from '@angular/core';

@Component({
  selector: 'coming-soon',
  templateUrl: './coming-soon.component.html',
  styleUrl: './coming-soon.component.css'
})
export class ComingSoonComponent {
  @Input() componentName="No Name";
  targetDate: Date = new Date();
  currentDate :Date = new Date();
  
  timeRemaining: any = {
    days: 0,
    hours: 0,
    minutes: 0,
    seconds: 0
  };
  intervalId: any;

  ngOnInit(): void {
    this.targetDate.setDate(this.currentDate.getDate() + 10);    
    this.calculateTimeRemaining();
    this.intervalId = setInterval(() => this.calculateTimeRemaining(), 1000);
  }

  ngOnDestroy(): void {
    if (this.intervalId) {
      clearInterval(this.intervalId);
    }
  }

  calculateTimeRemaining(): void {
    const now = new Date();
    const difference = this.targetDate.getTime() - now.getTime();

    if (difference <= 0) {
      this.timeRemaining = {
        days: 0,
        hours: 0,
        minutes: 0,
        seconds: 0
      };
      clearInterval(this.intervalId);
      return;
    }

    const days = Math.floor(difference / (1000 * 60 * 60 * 24));
    const hours = Math.floor((difference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((difference % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((difference % (1000 * 60)) / 1000);

    this.timeRemaining = { days, hours, minutes, seconds };
  }
}
