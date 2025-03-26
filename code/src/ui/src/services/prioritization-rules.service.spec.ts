import { TestBed } from '@angular/core/testing';

import { PrioritizationRulesService } from './prioritization-rules.service';

describe('PrioritizationRulesService', () => {
  let service: PrioritizationRulesService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(PrioritizationRulesService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
