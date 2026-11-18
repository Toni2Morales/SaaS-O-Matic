import { AbstractControl, ValidationErrors, ValidatorFn } from '@angular/forms';

export const trimmedRequired: ValidatorFn = (
  control: AbstractControl<string>,
): ValidationErrors | null => (control.value.trim().length > 0 ? null : { required: true });

export const trimmedLegalName: ValidatorFn = (
  control: AbstractControl<string>,
): ValidationErrors | null => {
  const length = control.value.trim().length;
  if (length === 0) {
    return { required: true };
  }
  return length > 255 ? { maxlength: { requiredLength: 255, actualLength: length } } : null;
};

export const trimmedEmail: ValidatorFn = (
  control: AbstractControl<string>,
): ValidationErrors | null => {
  const email = control.value.trim();
  if (email.length === 0) {
    return null;
  }
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) ? null : { email: true };
};
