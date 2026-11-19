import { inject, Injectable } from '@angular/core';
import { CustomerCreateRequest, Uuid } from '../../../shared/models/api.models';
import { ApiClient } from '../../../core/http/api-client';

@Injectable({ providedIn: 'root' })
export class CustomersApiService {
  private readonly api = inject(ApiClient);

  list(limit: number, offset: number, search: string) {
    return this.api.getCustomersPage(limit, offset, search);
  }

  create(request: CustomerCreateRequest) {
    return this.api.createCustomer(request);
  }

  get(customerId: Uuid) {
    return this.api.getCustomer(customerId);
  }
}
