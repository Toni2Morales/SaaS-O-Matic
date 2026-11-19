import { HttpClient, HttpParams } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { API_BASE_URL } from '../config/api.config';
import {
  CustomerCreateRequest,
  CustomerPageResponse,
  CustomerResponse,
  SimulationHistoryPageResponse,
  SimulationPreviewRequest,
  SimulationPreviewResponse,
  SimulationResponse,
  Uuid,
} from '../../shared/models/api.models';

@Injectable({ providedIn: 'root' })
export class ApiClient {
  private readonly http = inject(HttpClient);
  private readonly baseUrl = inject(API_BASE_URL);

  getCustomersPage(limit = 20, offset = 0, search?: string) {
    let params = new HttpParams().set('limit', limit).set('offset', offset);
    if (search !== undefined && search.length > 0) {
      params = params.set('search', search);
    }

    return this.http.get<CustomerPageResponse>(`${this.baseUrl}/customers`, { params });
  }

  createCustomer(request: CustomerCreateRequest) {
    return this.http.post<CustomerResponse>(`${this.baseUrl}/customers`, request);
  }

  getCustomer(customerId: Uuid) {
    return this.http.get<CustomerResponse>(
      `${this.baseUrl}/customers/${encodeURIComponent(customerId)}`,
    );
  }

  getCustomerSimulationsPage(customerId: Uuid, limit = 20, offset = 0) {
    const params = new HttpParams().set('limit', limit).set('offset', offset);
    return this.http.get<SimulationHistoryPageResponse>(
      `${this.baseUrl}/customers/${encodeURIComponent(customerId)}/simulations`,
      { params },
    );
  }

  previewSimulation(request: SimulationPreviewRequest) {
    return this.http.post<SimulationPreviewResponse>(
      `${this.baseUrl}/simulations/preview`,
      request,
    );
  }

  createSimulation(request: SimulationPreviewRequest) {
    return this.http.post<SimulationResponse>(`${this.baseUrl}/simulations`, request);
  }
}
