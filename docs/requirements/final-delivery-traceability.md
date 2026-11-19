# Reconciliación final de requisitos y entregables del reto — TASK047F

Esta matriz complementa, no reemplaza ni altera, los requisitos y la matriz histórica
canónica [`requirements-traceability.md`](requirements-traceability.md). El documento privado
original no se abre ni se publica; esta reconciliación usa exclusivamente el resumen
autorizado por el propietario en TASK047 y fuentes públicas/versionadas.

## Corte de entrega TASK047F — Windows 10

El propietario sustituyó los hitos pendientes TASK047/TASK047A2/B/C por una campaña final
local en Windows 10. Las filas FR01–FR11 siguientes conservan la evidencia histórica TASK046
y sus límites; la ejecución nueva se detalla en
[`informe TASK047F`](../../ai-workspace/01-tasks/TASK047F-final-windows-delivery-report.md)
y debe actualizarse allí sin sumar ejecuciones previas como si fueran la misma campaña.

GitHub Actions se conserva manual para uso futuro, pero no se despachó durante TASK047F.
A47-01 (overflow Linux de 14 px, primera corrección insuficiente), A47-02 (Angular health en
Windows runner) y A47-03 (propiedad PID Bash en Ubuntu) siguen pendientes y aplazados por
decisión expresa del propietario. No se presentan como resueltos. La evidencia de aceptación
de esta entrega se limita a la campaña clon limpio Windows 10 y no demuestra soporte
multiplataforma ni aptitud para producción pública.

## Requisitos funcionales FR01–FR11

| ID / requisito                          | Estado de entrega                                          | Especificación                                                                                                                                                                                  | Código representativo                                                                              | Pruebas/evidencia                                                                                            | Limitaciones                                                                                                                               |
| --------------------------------------- | ---------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------ |
| FR01 Alta de clientes                   | Implementado e integrado; alta local verificada TASK046    | [SPEC-001](../specs/001-customer-registration/spec.md), [SPEC-004](../specs/004-international-customers-and-simulations/spec.md), [SPEC-008](../specs/008-customer-management-frontend/spec.md) | `presentation/customers/router.py`; `domain/customers/value_objects.py`; `customer-create-page.ts` | `test_customer_api.py`, `test_customer_use_case.py`, `customer-create-page.spec.ts`; TASK046 integración 1/1 | Seis países; plan solo standard. Datos sintéticos y API, sin verificación de titularidad.                                                  |
| FR02 Validación fiscal española         | Implementado y probado por algoritmo                       | SPEC-001/SPEC-004                                                                                                                                                                               | `SpanishTaxId.parse`, `GenericTaxId.parse`                                                         | `test_spanish_tax_id.py`, `test_generic_tax_id.py`; TASK046 invalid/valid                                    | ES DNI/NIF/NIE/CIF; otros países validación de forma no oficial. No valida existencia del contribuyente.                                   |
| FR03 Persistir simulaciones asociadas   | Implementado, guardado/historial/reload integrados TASK046 | [SPEC-003](../specs/003-simulations/spec.md), [SPEC-006](../specs/006-customer-queries-and-preview/spec.md), SPEC-009                                                                           | `CreateSimulation`; `simulations/models.py`; simulation page                                       | `test_simulation_api.py`, `test_simulation_repository.py`; TASK046 1/1                                       | Sin editar/borrar; SQLite local y límites de concurrencia.                                                                                 |
| FR04 Usuarios, storage GB, llamadas API | Implementado; validado en contratos y E2E                  | SPEC-003/004/009                                                                                                                                                                                | `SimulationCreateRequest`, `SimulationModel`                                                       | `test_simulation_schemas.py`; `simulator.spec.ts`; integración TASK046                                       | 0..1M users, 0..1M GB, 0..1B calls; storage/calls no se facturan; históricos NULL.                                                         |
| FR05 Pricing progresivo acumulativo     | Implementado y comprobado en límites                       | [SPEC-002](../specs/002-progressive-pricing/spec.md), SPEC-009                                                                                                                                  | `domain/pricing/`; `MonthlyEstimator`                                                              | `test_pricing.py`, `test_monthly_calculation.py`; TASK046 valores 0..1M                                      | Solo users, EUR exacto/Decimal; importes oficiales proceden de backend.                                                                    |
| FR06 Impuestos por país                 | Implementado con catálogo general versionado; E2E ES/PT    | [SPEC-005](../specs/005-taxes-and-currency-conversion/spec.md)                                                                                                                                  | `infrastructure/tax_catalog.py`; `calculation.py`                                                  | `test_monthly_calculation.py`, `test_tax_fx_migration.py`; TASK046 integración fixture                       | Seis tasas generales simplificadas, no régimen fiscal individual ni asesoramiento.                                                         |
| FR07 Búsqueda de clientes               | Implementado server-side; E2E nombre/tax ID                | SPEC-006/SPEC-008                                                                                                                                                                               | `customers/queries.py`; `customers-page.ts`                                                        | `test_customer_api.py`, `customers-page.spec.ts`; TASK046                                                    | Limit/offset, sin orden arbitrario; SQLite puede escanear tablas.                                                                          |
| FR08 Ficha e historial                  | Implementado; integrado y persistente                      | SPEC-006/SPEC-008                                                                                                                                                                               | customer detail/history pages; query use cases                                                     | `test_query_use_cases.py`, `customer-detail-page.spec.ts`, E2E TASK046                                       | Históricos desconocidos permanecen NULL; no recalcular; sin edición/eliminación.                                                           |
| FR09 Simulador interactivo              | Implementado; preview, slider/manual, guardado explícito   | [SPEC-009](../specs/009-interactive-subscription-simulator/spec.md), SPEC-010                                                                                                                   | `simulation-page.ts`, preview/create routes                                                        | `simulation-page.spec.ts`, `simulator.spec.ts`, TASK046 integración 1/1                                      | Preview depende del backend; las tasas pueden cambiar antes del save.                                                                      |
| FR10 API pública FX y display currency  | Implementado vía backend; integración determinista TASK046 | SPEC-005/009                                                                                                                                                                                    | `infrastructure/frankfurter.py`; API client                                                        | `test_frankfurter.py`, `simulation-page.spec.ts`, integración fixture                                        | Frankfurter v2, EUR/USD/GBP, referencia fechada/caché 24h; no cotización continua. Consulta live no repetida TASK047.                      |
| FR11 Persistir economía y FX            | Implementado con snapshot JSON texto versionado            | SPEC-005/006                                                                                                                                                                                    | `calculation_snapshot` y `MonthlyCalculation.snapshot()`                                           | `test_tax_fx_migration.py`, repository/history tests; TASK046 reload                                         | Snapshots históricos NULL no se reconstruyen. `calculation_snapshot` es JSON en TEXT, no columnas independientes para todos los atributos. |

## Entregables originales de ingeniería/evaluación

| Entregable/requisito del reto                                  | Estado y evidencia                                                                          | Limitaciones / pendiente                                                                                            |
| -------------------------------------------------------------- | ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| Código en repositorio GitHub público                           | Implementado/verificado vía `gh repo view`; PR #7 merged en main                            | No se crea release ni entrega externa en TASK047.                                                                   |
| Espacio de trabajo IA                                          | Implementado: `ai-workspace/`, tareas, auditorías, roles y contexto                         | No todas las interacciones originales están disponibles; faltan documentos históricos concretos según índice.       |
| Planificación, SDD, reglas antes de código                     | Implementado: requisitos, ADR, SPEC 001–010, planes/tasks enlazados                         | Algunas tareas antiguas solo constan como parcial/no hay informe original; no reconstruir.                          |
| Contratos/API/validación/arquitectura/base de datos            | Implementado en OpenAPI, ADR y código/migraciones                                           | Estado y decisiones pendientes se conservan según fuente canónica.                                                  |
| Prompts e interacciones reales con IA                          | Parcialmente acreditado por instrucciones e informes versionados                            | Conversaciones/capturas privadas no disponibles para agente. Debe aportarlas/autorizar propietario; no se fabrican. |
| Desarrollo iterativo/auditoría/correcciones/supervisión humana | Evidencia documental y PR #1–#7, TASK039/045                                                | Informes de agente no se presentan como revisión externa/humana.                                                    |
| README y ejecución local en pocos pasos                        | Script Windows probado localmente; guía manual y scripts incluidos                          | Linux requiere run Actions; macOS no probado; clon limpio final aún pendiente.                                      |
| Calidad y control                                              | Validación histórica TASK046 579 backend, 40 Vitest, 79 Playwright/20 skips y 1 integración | TASK047 debe obtener pruebas actuales/clon y runs CI; no equiparar con historia.                                    |
| Criterios ponderados 35/25/30/10                               | Abordados con specs/audits, CI, integración y Quick Start                                   | Autoevaluación final no es nota oficial; evidencias privadas incompletas deben penalizarse.                         |

## Requisitos originales por grupos

- **Backend §2.A:** REST, SQLite, alta de cliente con país/plan, algoritmo ES, simulación
  persistida, consumos y pricing/tax: FR01–FR06, implementados con límites anteriores.
- **Frontend §2.B:** dashboard, búsqueda, ficha, historial, controles interactivos, FX y
  carga/error: FR07–FR10, implementados; interacción FX mediada por FastAPI, no Angular→FX.
- **Entregable §3:** repo público y `ai-workspace` existen; planificación/arquitectura/
  iteración/auditoría son trazables. Las capturas de chat auténticas siguen pendientes de
  aportación humana y no se sustituyen por informes retrospectivos.
- **README/ejecución:** script local probado parcialmente/Windows; aceptación final requiere
  clon limpio literal y runners Linux/Windows.
- **Ponderación §4:** Planning/design (35), technical judgement/QA (25), software (30),
  README/local startup (10). La valoración TASK047 debe justificar cada puntaje y no es
  calificación del propietario del reto.

## Estado de instalación/entrega

La campaña final de clon limpio en Windows 10, resultados y veredicto se encuentran en
`TASK047F-final-windows-delivery-report.md`. No usar los resultados históricos TASK046/TASK047
como sustituto de esa campaña. Los workflows ahora requieren despacho manual y no se ejecutan
como parte del criterio de entrega local.

## Deuda técnica y riesgos heredados

- **A39-07 (pendiente de autorización):** errores inesperados devuelven 500 genérico y no
  disponen de logging estructurado. No se añadió logging en TASK047.
- **A39-08 (pendiente de autorización):** `CalculateSimulation` depende del puerto general
  de repositorio de clientes aunque solo consulta el país; no se creó puerto estrecho.
- **A39-11 (diferido):** la búsqueda con LIKE/UDF puede escanear tabla; coste lineal aceptado
  para volumen MVP.
- **A39-12/P-05:** sin auth, autorización, multi-tenancy, CORS/proxy productivo ni límites
  globales. No exponer servicio con datos reales; el reto exige arranque local, no cloud.
- **A39-13:** migraciones SQLite 0003/0004 incluyen DDL no transaccional; backup y prueba
  en copia antes de migrar datos valiosos. Downgrade puede bloquear pérdida de snapshots.
- **A39-14/15:** lock global serializa FX y caché se pierde/no se comparte entre procesos.
- Otros límites: dependencia de proveedor FX, historial no editable, plan/countries fijos,
  sin cobros, cobertura automatizada parcial y WCAG no certificada. Son límites/riesgos
  documentados, no defectos corregidos ni evidencia de escalabilidad.
