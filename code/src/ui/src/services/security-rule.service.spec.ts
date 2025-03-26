import { TestBed } from '@angular/core/testing';

import { SecurityRuleService } from './security-rule.service';

describe('SecurityRuleService', () => {
  let service: SecurityRuleService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(SecurityRuleService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
