import { HttpErrorResponse, HttpInterceptorFn } from '@angular/common/http';
import { catchError, throwError } from 'rxjs';
import { toSafeApiError } from './api-error';

export const apiErrorInterceptor: HttpInterceptorFn = (_request, next) =>
  next(_request).pipe(
    catchError((error: unknown) => {
      if (error instanceof HttpErrorResponse) {
        return throwError(() => toSafeApiError(error.status, error.error));
      }

      return throwError(() => toSafeApiError(0, null));
    }),
  );
