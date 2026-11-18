import { ProblemDetails, ProblemFieldError } from '../../shared/models/api.models';

export class ApiError extends Error {
  constructor(
    readonly status: number,
    message: string,
    readonly problem?: ProblemDetails,
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

export function isProblemDetails(value: unknown): value is ProblemDetails {
  if (typeof value !== 'object' || value === null) {
    return false;
  }

  const candidate = value as Record<string, unknown>;
  return (
    typeof candidate['type'] === 'string' &&
    typeof candidate['title'] === 'string' &&
    typeof candidate['status'] === 'number' &&
    typeof candidate['detail'] === 'string'
  );
}

function isProblemFieldError(value: unknown): value is ProblemFieldError {
  if (typeof value !== 'object' || value === null) {
    return false;
  }

  const candidate = value as Record<string, unknown>;
  return typeof candidate['field'] === 'string' && typeof candidate['message'] === 'string';
}

export function toSafeApiError(status: number, body: unknown): ApiError {
  if (isProblemDetails(body)) {
    const message = messageForStatus(status);
    const problem: ProblemDetails = {
      type: 'about:blank',
      title: message,
      status,
      detail: message,
    };
    if (status === 422 && Array.isArray(body.errors)) {
      problem.errors = body.errors.filter(isProblemFieldError);
    }
    return new ApiError(status, message, problem);
  }

  if (status === 0) {
    return new ApiError(
      status,
      'No se pudo conectar con el servidor. Comprueba que esté iniciado.',
    );
  }

  return new ApiError(status, 'No se pudo completar la solicitud. Inténtalo de nuevo.');
}

function messageForStatus(status: number): string {
  switch (status) {
    case 400:
      return 'Los datos enviados no son válidos.';
    case 404:
      return 'No se encontró el recurso solicitado.';
    case 409:
      return 'La operación entra en conflicto con datos existentes.';
    case 422:
      return 'Revisa los datos introducidos.';
    case 503:
      return 'El servicio no está disponible temporalmente.';
    default:
      return 'El servidor no pudo completar la solicitud.';
  }
}
