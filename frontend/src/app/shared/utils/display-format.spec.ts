import {
  formatDateOnly,
  formatDateTime,
  formatExactRate,
  formatMoney,
  formatPercentRate,
} from './display-format';

describe('exact display formatting', () => {
  it('localizes currency separators without converting the decimal value to Number', () => {
    expect(formatMoney('169.40', 'EUR')).toBe('169,40\u00a0€');
    expect(formatMoney('1250.003400', 'USD')).toBe('1.250,003400\u00a0US$');
    expect(formatMoney('98765432101234567890.00000001', 'GBP')).toBe(
      '98.765.432.101.234.567.890,00000001\u00a0£',
    );
  });

  it('distinguishes a recorded zero, null, and malformed amount', () => {
    expect(formatMoney('0.00', 'EUR')).toBe('0,00\u00a0€');
    expect(formatMoney(null, 'EUR')).toBe('No registrado');
    expect(formatMoney('1e6', 'EUR')).toBe('No disponible');
    expect(formatMoney('12.3', null)).toBe('No registrado');
  });

  it('preserves all exchange-rate digits while localizing only the separator', () => {
    expect(formatExactRate('1.234567890123456789')).toBe('1,234567890123456789');
    expect(formatExactRate(null)).toBe('No registrado');
    expect(formatExactRate('NaN')).toBe('No disponible');
  });

  it('formats tax fractions as exact percentages using string operations', () => {
    expect(formatPercentRate('0.21')).toBe('21 %');
    expect(formatPercentRate('0.235')).toBe('23,5 %');
    expect(formatPercentRate(null)).toBe('No registrado');
    expect(formatPercentRate('invalid')).toBe('No disponible');
  });

  it('keeps date-only calendar values independent of the local timezone', () => {
    expect(formatDateOnly('2026-01-02')).toBe('2 ene 2026');
    expect(formatDateOnly(null)).toBe('No registrado');
    expect(formatDateOnly('2026-02-30')).toBe('No disponible');
  });

  it('formats timestamps in es-ES local time and handles invalid or absent dates', () => {
    expect(formatDateTime('2026-11-18T12:00:00Z')).toContain('18 nov 2026');
    expect(formatDateTime('not-a-date')).toBe('No disponible');
    expect(formatDateTime(null)).toBe('No registrado');
  });
});
