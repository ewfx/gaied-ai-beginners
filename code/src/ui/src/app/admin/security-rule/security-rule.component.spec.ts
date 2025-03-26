import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SecurityRuleComponent } from './security-rule.component';

describe('SecurityRuleComponent', () => {
  let component: SecurityRuleComponent;
  let fixture: ComponentFixture<SecurityRuleComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SecurityRuleComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(SecurityRuleComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
