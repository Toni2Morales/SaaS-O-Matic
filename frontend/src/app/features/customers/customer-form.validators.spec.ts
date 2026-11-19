import { FormControl } from '@angular/forms';
import { trimmedEmail, trimmedLegalName, trimmedRequired } from './customer-form.validators';

describe('customer form validators', () => {
  it('checks trimmed legal-name emptiness and the backend length range', () => {
    expect(trimmedLegalName(new FormControl('   '))).toEqual({ required: true });
    expect(trimmedLegalName(new FormControl(`  ${'a'.repeat(255)}  `))).toBeNull();
    expect(trimmedLegalName(new FormControl('a'.repeat(256)))).toEqual({
      maxlength: { requiredLength: 255, actualLength: 256 },
    });
  });

  it('rejects blank fiscal identifiers without rewriting non-empty values', () => {
    expect(trimmedRequired(new FormControl('  '))).toEqual({ required: true });
    expect(trimmedRequired(new FormControl('PT-ACME 2026'))).toBeNull();
  });

  it('checks trimmed email syntax without rewriting the entered value', () => {
    const control = new FormControl(' contacto@example.com ', { nonNullable: true });
    expect(trimmedEmail(control)).toBeNull();
    expect(control.value).toBe(' contacto@example.com ');
    expect(trimmedEmail(new FormControl('invalid-email', { nonNullable: true }))).toEqual({
      email: true,
    });
  });
});
