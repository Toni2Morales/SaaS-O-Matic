import { ApiError, isProblemDetails, toSafeApiError } from './api-error';

describe('Problem Details mapping', () => {
  it('recognizes the backend ProblemDetails shape', () => {
    expect(
      isProblemDetails({
        type: 'about:blank',
        title: 'Invalid',
        status: 422,
        detail: 'Bad request',
      }),
    ).toBe(true);
    expect(isProblemDetails({ title: 'Invalid', status: 422 })).toBe(false);
  });

  it('preserves controlled 422 field messages and status', () => {
    const error = toSafeApiError(422, {
      type: 'about:blank',
      title: 'Datos no válidos',
      status: 422,
      detail: 'La petición no cumple el esquema esperado.',
      errors: [
        { field: 'body.email', message: 'Dirección no válida' },
        null,
        { field: 42, message: 'unexpected value' },
      ],
    });

    expect(error).toBeInstanceOf(ApiError);
    expect(error.status).toBe(422);
    expect(error.problem?.errors?.[0]?.field).toBe('body.email');
    expect(error.problem?.errors).toHaveLength(1);
    expect(error.message).toBe('Revisa los datos introducidos.');
    expect(error.problem?.detail).toBe('Revisa los datos introducidos.');
  });

  it('maps the remaining controlled client statuses to safe Spanish messages', () => {
    const cases = [
      [400, 'Los datos enviados no son válidos.'],
      [404, 'No se encontró el recurso solicitado.'],
      [409, 'La operación entra en conflicto con datos existentes.'],
    ] as const;

    for (const [status, expectedMessage] of cases) {
      const error = toSafeApiError(status, {
        type: 'about:blank',
        title: 'Backend title',
        status,
        detail: 'Backend detail',
      });
      expect(error.message).toBe(expectedMessage);
      expect(error.problem?.detail).toBe(expectedMessage);
    }
  });

  it('does not expose internal server details or unexpected response bodies', () => {
    const serverError = toSafeApiError(500, {
      type: 'about:blank',
      title: 'Internal',
      status: 500,
      detail: 'database password leaked',
    });
    expect(serverError.message).toBe('El servidor no pudo completar la solicitud.');
    expect(serverError.problem?.detail).not.toContain('password');
    expect(
      toSafeApiError(503, {
        type: 'about:blank',
        title: 'Provider unavailable',
        status: 503,
        detail: 'Upstream service internals',
      }).message,
    ).toBe('El servicio no está disponible temporalmente.');
    expect(toSafeApiError(503, '<html>proxy failure</html>').message).toContain(
      'No se pudo completar',
    );
    expect(toSafeApiError(0, null).message).toContain('No se pudo conectar');
  });
});
