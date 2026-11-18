# SPEC-004 — Clientes internacionales y ampliación de simulaciones

> Ampliación vigente TASK037: [SPEC-005](../005-taxes-and-currency-conversion/spec.md)
> incorpora IVA y FX con snapshot; las exclusiones de esta SPEC describen el incremento
> TASK036. Peticiones de cuatro campos conservadas, EUR predeterminado.

| Campo | Valor |
| --- | --- |
| Estado | Implementada localmente y validada con 340 pruebas; sin publicación ni auditoría independiente |
| Base | PR #5, `b3c5ca81d23d279b478ed466757bada031aa1e1e` |
| Rama | `feature/mvp-backend` |
| Fuentes | [Requisitos](../../requirements/functional-requirements.md), ADR 0001/0002 e instrucción TASK036 |

## Decisiones y alcance

Q-18, Q-19, Q-20, Q-21 y Q-26 aprobadas. Q-02/PP-Q-01 quedan sustituidas:
dominio con enteros no negativos sin máximo comercial; API 0..1.000.000;
slider futuro 0..1.000 con entrada manual hasta 1.000.000 (Q-12/SIM-P09).
Q-22/Q-23 aprueban solo alcance futuro: impuestos oficiales configurables y un
único proveedor de divisas, preferentemente Frankfurter sujeto a verificación.
No se aprueban las propuestas anteriores de tasas, redondeo, caché ni proveedor
open.er-api.com. Q-24/Q-25 aprueban historial inmutable y preview separado,
no sus contratos detallados. P-01 (Angular/Vitest) y P-05 (despliegue y SQLite
fuera de desarrollo) siguen pendientes; no son necesarias aquí.

## Clientes

Países exactos ISO: ES, PT, FR, DE, IT, NL. Plan único obligatorio `standard`.
España mantiene SpanishTaxId y normalización algorítmica sin cambios.
Para los demás países: rechazar categorías Unicode Cc (controles), Cf (formato
invisible) y Cs (sustitutos) antes de normalizar; recortar y colapsar secuencias
de espacios Unicode a un espacio; convertir a mayúsculas; longitud final 1..64.
Conservar puntuación, guiones y caracteres significativos, sin normalización
Unicode de compatibilidad ni algoritmos nacionales ni consultas externas.
No es validación fiscal oficial. Unicidad por `(country, tax_id)` normalizado,
con el mismo 409 de duplicados. No cambiar `extra` en clientes.

## Simulaciones y contrato incompatible

`POST /simulations`: obligatorios `customer_id` UUID, `user_count` entero estricto
0..1.000.000, `storage_gb` entero estricto 0..1.000.000 y `api_calls_per_month`
entero estricto 0..1.000.000.000. `extra="forbid"`; no aceptar `billing_period`.
Servidor fija `billing_period="monthly"`. Booleanos, cadenas, decimales, nulos,
campos ausentes y desconocidos: 422 `application/problem+json`.
Respuesta 201: id, customer_id, user_count, storage_gb, api_calls_per_month,
billing_period, user_subtotal_eur (cadena exacta con dos decimales), created_at UTC.
404 cliente inexistente, 500 inesperado, sin Location. Peticiones antiguas sin
los dos consumos dejan de ser válidas. Sin cargos por esos consumos.

Validar entrada, comprobar cliente, calcular, persistir. Cero produce exactamente
`Decimal("0.00")`; tarifas intactas. Mantener casos enormes y prueba de 15 = 140.00.

## Persistencia y migración

Nueva revisión 0003, sin tocar 0001/0002. Ampliar tax_id a 64; conservar unicidad
compuesta existente. Batch SQLite para rango de usuarios y campos nuevos.
Históricos conservan todos los valores; consumos NULL, periodo mensual.
CHECK de tipos/rangos y periodo mensual; importes continúan TEXT, nunca REAL.
Verificar `foreign_key_check` tras batch. Downgrade antes de DDL rechaza clientes
no ES o identificadores de más de 9 caracteres, usuarios cero y consumos conocidos:
no descartar datos nuevos silenciosamente. Permitir ciclo sin datos incompatibles.

## Calidad y aceptación

H-01: contexto decimal local independiente de traps heredados, sin redondear,
excepción InvalidSimulationAmount y contexto llamador intacto.
H-02: SQL físico TEXT, nueva sesión, Decimal/UTC exactos, 15 usuarios y capas.
H-04: cliente antes de pricing; H-05: forbid. H-06: mantener FK/rollback y riesgo
documentado si no hay clasificación referencial fiable; nunca todo IntegrityError→404.
H-07: evaluar CHECK sencillo de texto canónico sin REAL; documentar elección.
H-08: documentación vigente; H-03 histórico intacto.

Aceptación: seis países, algoritmos ES intactos, unicidad, nueve subtotales de la
instrucción, nuevos campos estrictos, mensual, migración sin pérdida, pruebas y
calidad completas. Sin dependencias nuevas ni impuestos/divisas/lecturas/preview/UI.
Sin staging ni publicación. Registros TASK001–TASK035 inmutables.
