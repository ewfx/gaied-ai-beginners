import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PrioritizationRulesComponent } from './prioritization-rules.component';

describe('PrioritizationRulesComponent', () => {
  let component: PrioritizationRulesComponent;
  let fixture: ComponentFixture<PrioritizationRulesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PrioritizationRulesComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PrioritizationRulesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
