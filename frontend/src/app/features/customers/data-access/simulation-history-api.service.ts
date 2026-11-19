import { inject, Injectable } from '@angular/core';
import { Uuid } from '../../../shared/models/api.models';
import { ApiClient } from '../../../core/http/api-client';

@Injectable({ providedIn: 'root' })
export class SimulationHistoryApiService {
  private readonly api = inject(ApiClient);

  getPage(customerId: Uuid, limit: number, offset: number) {
    return this.api.getCustomerSimulationsPage(customerId, limit, offset);
  }
}
