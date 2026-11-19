export type CountryCode = 'ES' | 'PT' | 'FR' | 'DE' | 'IT' | 'NL';
export type Currency = 'EUR' | 'USD' | 'GBP';
export type PlanCode = 'standard';
export type BillingPeriod = 'monthly';
export type IsoDate = string;
export type UtcDateTime = string;
export type Uuid = string;

export interface CustomerCreateRequest {
  legal_name: string;
  tax_id: string;
  email: string;
  country: CountryCode;
  plan: PlanCode;
}

export interface CustomerResponse extends CustomerCreateRequest {
  id: Uuid;
  created_at: UtcDateTime;
}

export interface Page<T> {
  items: T[];
  total: number;
  limit: number;
  offset: number;
}

export type CustomerPageResponse = Page<CustomerResponse>;

export interface SimulationCreateRequest {
  customer_id: Uuid;
  user_count: number;
  storage_gb: number;
  api_calls_per_month: number;
  display_currency?: Currency;
}

export type SimulationPreviewRequest = Required<SimulationCreateRequest>;

export interface SimulationPreviewResponse {
  customer_id: Uuid;
  user_count: number;
  user_subtotal_eur: string;
  storage_gb: number;
  api_calls_per_month: number;
  billing_period: BillingPeriod;
  tax_country: string;
  tax_rate: string;
  tax_source: string;
  tax_catalog_version: string;
  tax_verified_on: IsoDate;
  tax_territory: string;
  tax_effective_from: IsoDate | null;
  tax_amount_eur: string;
  total_eur: string;
  display_currency: Currency;
  exchange_rate: string;
  exchange_rate_date: IsoDate | null;
  exchange_rate_obtained_at: UtcDateTime;
  exchange_rate_source: string;
  converted_total: string;
}

export interface SimulationResponse extends SimulationPreviewResponse {
  id: Uuid;
  created_at: UtcDateTime;
}

export interface HistoricalSimulationResponse {
  id: Uuid;
  customer_id: Uuid;
  user_count: number;
  storage_gb: number | null;
  api_calls_per_month: number | null;
  billing_period: BillingPeriod;
  user_subtotal_eur: string;
  created_at: UtcDateTime | null;
  tax_country: string | null;
  tax_rate: string | null;
  tax_source: string | null;
  tax_catalog_version: string | null;
  tax_verified_on: IsoDate | null;
  tax_territory: string | null;
  tax_effective_from: IsoDate | null;
  tax_amount_eur: string | null;
  total_eur: string | null;
  display_currency: Currency | null;
  exchange_rate: string | null;
  exchange_rate_date: IsoDate | null;
  exchange_rate_obtained_at: UtcDateTime | null;
  exchange_rate_source: string | null;
  converted_total: string | null;
}

export type SimulationHistoryPageResponse = Page<HistoricalSimulationResponse>;

export interface ProblemFieldError {
  field: string;
  message: string;
}

export interface ProblemDetails {
  type: string;
  title: string;
  status: number;
  detail: string;
  instance?: string | null;
  errors?: ProblemFieldError[] | null;
}
