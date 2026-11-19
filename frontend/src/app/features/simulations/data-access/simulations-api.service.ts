import { inject, Injectable } from '@angular/core';
import { ApiClient } from '../../../core/http/api-client';
import { SimulationPreviewRequest } from '../../../shared/models/api.models';

@Injectable({ providedIn: 'root' })
export class SimulationsApiService {
  private readonly api = inject(ApiClient);

  preview(request: SimulationPreviewRequest) {
    return this.api.previewSimulation(request);
  }

  create(request: SimulationPreviewRequest) {
    return this.api.createSimulation(request);
  }
}
