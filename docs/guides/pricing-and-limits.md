# Modelo económico, divisas y límites del MVP

## Tarifa progresiva mensual

El subtotal de usuarios se calcula acumulativamente y solo en FastAPI:

\[
P(n)=\min(n,10)\cdot10 + \min(\max(n-10,0),40)\cdot8 + \max(n-50,0)\cdot5
\]

`n` es entero de 0 a 1.000.000 según el límite técnico de API. Importe EUR exacto con
`Decimal`; el frontend explica los tramos, pero presenta la respuesta del servidor.

|  Usuarios | Subtotal EUR |
| --------: | -----------: |
|         0 |         0,00 |
|         1 |        10,00 |
|        10 |       100,00 |
|        11 |       108,00 |
|        15 |       140,00 |
|        16 |       148,00 |
|        50 |       420,00 |
|        51 |       425,00 |
|       100 |       670,00 |
| 1.000.000 | 5.000.170,00 |

Ejemplo de 15 usuarios para España: subtotal 140,00 EUR; IVA general configurado al 21 %
es 29,40 EUR; total 169,40 EUR por mes.

## Impuesto general configurado

| País         | Tipo configurado | Ámbito simplificado    |
| ------------ | ---------------: | ---------------------- |
| España       |             21 % | Península y Baleares   |
| Portugal     |             23 % | Portugal continental   |
| Francia      |             20 % | Francia metropolitana  |
| Alemania     |             19 % | Ámbito general alemán  |
| Italia       |             22 % | Tipo ordinario general |
| Países Bajos |             21 % | Países Bajos europeos  |

Son valores de un catálogo versionado (`general-vat-2026-11-17-v1`), con fuente/fecha de
verificación registradas en [SPEC-005 y fuentes](../specs/005-taxes-and-currency-conversion/sources.md)
y en snapshots. No son asesoramiento fiscal ni determinan el impuesto legal de cada
operación: no se representa región, condición B2B, inversión, exenciones ni tipos reducidos.
La fecha de vigencia queda NULL cuando la fuente no la confirma. El impuesto se redondea
con `ROUND_HALF_UP` a céntimos.

## Monedas y tipos de cambio

- EUR es base y moneda identidad (tasa 1; no requiere proveedor).
- USD y GBP son monedas de visualización admitidas.
- Angular solicita preview/guardado a FastAPI; el backend consulta Frankfurter API v2
  (`/v2/rate/EUR/USD` o `/GBP`) mediante el adaptador estándar `urllib`.
- Las tasas son referencias fechadas, recibidas una o varias veces al día; no son
  cotizaciones instantáneas o continuas de mercado.
- El caché es por proceso, solo conserva éxitos durante 24 h desde la obtención; timeout
  externo configurado: 5 s. Si no hay tasa válida, la API responde 503 controlado. No hay
  tasa ficticia de recuperación ni entrega de dato expirado.
- La conversión se aplica al total EUR con impuestos. El resultado de moneda, tasa, fecha,
  fuente y amounts quedan en snapshot inmutable JSON versión 1 (dinero/tasas como texto).
  HALF_UP a céntimos se aplica al impuesto y producto convertido; el subtotal progresivo ya
  está expresado exactamente en céntimos.

## Consumos, plan y alcance

- Países: ES, PT, FR, DE, IT, NL. Solo ES usa validación algorítmica fiscal oficial de
  DNI/NIF, NIE y CIF/NIF; los otros países pasan validación genérica, no oficial.
- Plan: `standard`, único plan MVP; no cambia los precios por usuario.
- Almacenamiento GB (0..1.000.000) y llamadas API al mes (0..1.000.000.000) se registran y
  muestran como información; no generan cargos.
- Los importes son estimaciones mensuales. No hay facturación, cobro, aprovisionamiento,
  aprobación fiscal ni verificación de identidad/existencia del titular.
- La caché y SQLite responden al alcance local/MVP; no hay certificación de escalabilidad,
  concurrencia productiva, seguridad de exposición pública ni autenticación/autorización.

Fuentes canónicas: [requisitos funcionales](../requirements/functional-requirements.md),
[ADR-0001](../adr/0001-technology-stack.md), SPEC-002/003/004/005 y el
[catálogo de tasas](../../backend/src/saas_o_matic/infrastructure/tax_catalog.py).
