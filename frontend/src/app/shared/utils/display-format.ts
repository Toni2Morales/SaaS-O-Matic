import { Currency } from '../models/api.models';

const currencySymbols: Record<Currency, string> = {
  EUR: '€',
  USD: 'US$',
  GBP: '£',
};

const decimalPattern = /^(-?)(\d+)(?:\.(\d+))?$/;

function formatExactDecimal(value: string): { formatted: string; fraction: string } | null {
  const match = decimalPattern.exec(value);
  if (!match) {
    return null;
  }

  const [, sign, integerDigits, fraction = ''] = match;
  if (integerDigits === undefined) {
    return null;
  }
  const grouped = integerDigits.replace(/\B(?=(\d{3})+(?!\d))/g, '.');
  return {
    formatted: `${sign}${grouped}`,
    fraction,
  };
}

export function formatMoney(value: string | null, currency: Currency | null): string {
  if (value === null || currency === null) {
    return 'No registrado';
  }

  const decimal = formatExactDecimal(value);
  if (!decimal) {
    return 'No disponible';
  }

  const amount = decimal.fraction ? `${decimal.formatted},${decimal.fraction}` : decimal.formatted;
  return `${amount}\u00a0${currencySymbols[currency]}`;
}

export function formatExactRate(value: string | null): string {
  if (value === null) {
    return 'No registrado';
  }
  const decimal = formatExactDecimal(value);
  if (!decimal) {
    return 'No disponible';
  }
  return decimal.fraction ? `${decimal.formatted},${decimal.fraction}` : decimal.formatted;
}

export function formatPercentRate(value: string | null): string {
  if (value === null || !/^-?\d+(?:\.\d+)?$/.test(value)) {
    return value === null ? 'No registrado' : 'No disponible';
  }
  const negative = value.startsWith('-');
  const unsigned = negative ? value.slice(1) : value;
  const [whole = '0', fraction = ''] = unsigned.split('.');
  const digits = `${whole}${fraction}`;
  const decimalPosition = whole.length + 2;
  const padded = digits.padEnd(decimalPosition + 1, '0');
  const integer = (padded.slice(0, decimalPosition) || '0').replace(/^0+(?=\d)/, '');
  const remainder = padded.slice(decimalPosition).replace(/0+$/, '');
  const grouped = integer.replace(/\B(?=(\d{3})+(?!\d))/g, '.');
  return `${negative ? '-' : ''}${grouped}${remainder ? `,${remainder}` : ''} %`;
}

export function formatDateOnly(value: string | null): string {
  if (value === null) {
    return 'No registrado';
  }
  const match = /^(\d{4})-(\d{2})-(\d{2})$/.exec(value);
  if (!match) {
    return 'No disponible';
  }
  const [, year, month, day] = match;
  if (!year || !month || !day) {
    return 'No disponible';
  }
  const date = new Date(Date.UTC(Number(year), Number(month) - 1, Number(day)));
  if (date.toISOString().slice(0, 10) !== value) {
    return 'No disponible';
  }
  return new Intl.DateTimeFormat('es-ES', { dateStyle: 'medium', timeZone: 'UTC' }).format(date);
}

export function formatDateTime(value: string | null): string {
  if (value === null) {
    return 'No registrado';
  }
  const date = new Date(value);
  if (!Number.isFinite(date.getTime())) {
    return 'No disponible';
  }
  return new Intl.DateTimeFormat('es-ES', {
    dateStyle: 'medium',
    timeStyle: 'short',
  }).format(date);
}
