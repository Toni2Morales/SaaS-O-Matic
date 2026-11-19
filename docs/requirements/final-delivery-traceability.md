# Reconciliación final de requisitos y entregables del reto — TASK047F

Esta matriz complementa, no reemplaza ni altera, los requisitos y la matriz histórica
canónica [`requirements-traceability.md`](requirements-traceability.md). El documento privado
original no se abre ni se publica; esta reconciliación usa exclusivamente el resumen
autorizado por el propietario en TASK047 y fuentes públicas/versionadas.

## Corte de entrega TASK047F — Windows 10

El propietario sustituyó los hitos pendientes TASK047/TASK047A2/B/C por una campaña final
local en Windows 10. Las filas FR01–FR11 conservan la evidencia TASK046 y añaden una columna
con la campaña real TASK047F; no se suman runs como si fueran una sola ejecución. El informe
nuevo y sus tiempos se detallan en
[`informe TASK047F`](../../ai-workspace/01-tasks/TASK047F-final-windows-delivery-report.md)
y debe actualizarse allí sin sumar ejecuciones previas como si fueran la misma campaña.

GitHub Actions se conserva manual para uso futuro, pero no se despachó durante TASK047F.
A47-01 (overflow Linux de 14 px, primera corrección insuficiente), A47-02 (Angular health en
Windows runner) y A47-03 (propiedad PID Bash en Ubuntu) siguen pendientes y aplazados por
decisión expresa del propietario. No se presentan como resueltos. La evidencia de aceptación
de esta entrega se limita a la campaña clon limpio Windows 10 y no demuestra soporte
multiplataforma ni aptitud para producción pública.

## Requisitos funcionales FR01–FR11

| ID / requisito                  | Estado de entrega                 | Especificación / código representativo                  | Evidencia histórica TASK046             | Campaña Windows 10 TASK047F                                                    | Limitaciones                                                              |
| ------------------------------- | --------------------------------- | ------------------------------------------------------- | --------------------------------------- | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------- |
| FR01 Alta de clientes           | Implementado e integrado          | SPEC-001/004/008; `customer-create-page.ts`             | API/UI; integración 1/1                 | ES y PT registrados por HTTP; PT también mediante UI                           | Seis países; `standard` único; identidades sintéticas                     |
| FR02 Validación fiscal española | Implementado algorítmicamente     | `SpanishTaxId.parse`, `GenericTaxId.parse`              | ES válido/inválido E2E                  | CIF/NIF ES inválido rechazado por UI/API; PT se trata genérico                 | No comprueba titular/existencia; internacional no oficial                 |
| FR03 Persistir simulaciones     | Implementado                      | SPEC-003/006/009; `CreateSimulation`                    | Guardado/historial/reload integración   | Preview mantuvo count; save aumentó count; historial se recuperó tras reinicio | Sin editar/borrar; SQLite local/concurrencia                              |
| FR04 Usuarios, GB, llamadas API | Implementado                      | `SimulationCreateRequest`, `SimulationModel`            | Contrato E2E                            | 250 GB/100.000 llamadas y 15/16 usuarios en API/UI                             | Sin cargos de storage/calls; rangos técnicos e históricos NULL            |
| FR05 Pricing progresivo         | Implementado                      | SPEC-002/009; `MonthlyEstimator`                        | Límites 0..1M                           | 15: 140,00 EUR; 16: 148,00 EUR subtotal                                        | Solo usuarios; Decimal/EUR desde backend                                  |
| FR06 Impuestos                  | Catálogo general versionado       | SPEC-005; `tax_catalog.py`                              | E2E ES/PT fixture                       | ES 21%: 29,40 y 31,08; total 169,40/179,08                                     | Campaña principal verificó ES; sin regímenes especiales                   |
| FR07 Búsqueda                   | Server-side                       | SPEC-006/008; queries/customer page                     | E2E nombre/tax ID                       | UI y API buscaron nombre y B12345674                                           | Limit/offset; posible escaneo SQLite                                      |
| FR08 Ficha e historial          | Implementado/integrado            | SPEC-006/008; detail/history pages                      | Historial persistente                   | Ficha, count, historial antes/después y reload verificados                     | Históricos desconocidos NULL; no edición                                  |
| FR09 Simulador                  | Implementado                      | SPEC-009/010; `simulation-page.ts`                      | Slider/manual/preview/save              | Slider 15→16, entrada manual, preview sin DML y guardado explícito UI/API      | Preview puede variar si cambia FX antes del guardado                      |
| FR10 FX / display currency      | Backend Frankfurter v2            | SPEC-005/009; `frankfurter.py`                          | TASK046 fixture/integración             | UI real seleccionó USD/GBP; rates source `frankfurter`, fecha 2026-11-19       | Referencia fechada, caché 24 h, no mercado continuo; externa puede fallar |
| FR11 Snapshot económico/FX      | Implementado JSON TEXT versionado | `calculation_snapshot`, `MonthlyCalculation.snapshot()` | EUR/USD/GBP guardados/reload históricos | Save/restart comprobó snapshot EUR; USD/GBP se verificaron como preview live   | Esta campaña no guardó USD/GBP; históricos NULL no se reconstruyen        |

## Entregables originales de ingeniería/evaluación

| Entregable/requisito del reto                                  | Estado y evidencia                                                                    | Limitaciones / pendiente                                                                                            |
| -------------------------------------------------------------- | ------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| Código en repositorio GitHub público                           | Público; PR #7 merge en main verificado                                               | No se crea release ni entrega externa en TASK047F.                                                                  |
| Espacio de trabajo IA                                          | Implementado: `ai-workspace/`, tareas, auditorías, roles y contexto                   | No todas las interacciones originales están disponibles; faltan documentos históricos concretos según índice.       |
| Planificación, SDD, reglas antes de código                     | Implementado: requisitos, ADR, SPEC 001–010, planes/tasks enlazados                   | Algunas tareas antiguas solo constan como parcial/no hay informe original; no reconstruir.                          |
| Contratos/API/validación/arquitectura/base de datos            | Implementado en OpenAPI, ADR y código/migraciones                                     | Estado y decisiones pendientes se conservan según fuente canónica.                                                  |
| Prompts e interacciones reales con IA                          | Parcialmente acreditado por instrucciones e informes versionados                      | Conversaciones/capturas privadas no disponibles para agente. Debe aportarlas/autorizar propietario; no se fabrican. |
| Desarrollo iterativo/auditoría/correcciones/supervisión humana | Evidencia documental y PR #1–#7, TASK039/045                                          | Informes de agente no se presentan como revisión externa/humana.                                                    |
| README y ejecución local en pocos pasos                        | Quick Start, README y clon limpio Windows 10 ejecutados y cronometrados               | Linux/macOS/Windows 11 no se declaran compatibles; instalación manual autónoma solo documentada.                    |
| Calidad y control                                              | Campaña TASK047F: 579 Pytest, 40 Vitest, 79 Playwright/20 skips, 2 FX live y E2E PASS | GitHub Actions falla históricos A47; no confundir local con CI ni WCAG completa.                                    |
| Criterios ponderados 35/25/30/10                               | Abordados con specs/audits, CI, integración y Quick Start                             | Autoevaluación final no es nota oficial; evidencias privadas incompletas deben penalizarse.                         |

## Requisitos originales por grupos

- **Backend §2.A:** REST, SQLite, alta de cliente con país/plan, algoritmo ES, simulación
  persistida, consumos y pricing/tax: FR01–FR06, implementados con límites anteriores.
- **Frontend §2.B:** dashboard, búsqueda, ficha, historial, controles interactivos, FX y
  carga/error: FR07–FR10, implementados; interacción FX mediada por FastAPI, no Angular→FX.
- **Entregable §3:** repo público y `ai-workspace` existen; planificación/arquitectura/
  iteración/auditoría son trazables. Las capturas de chat auténticas siguen pendientes de
  aportación humana y no se sustituyen por informes retrospectivos.
- **README/ejecución:** clon limpio literal y Quick Start verificados en Windows 10. Runners
  Linux/Windows no son parte de la campaña final por decisión del propietario.
- **Ponderación §4:** Planning/design (35), technical judgement/QA (25), software (30),
  README/local startup (10). La valoración TASK047 debe justificar cada puntaje y no es
  calificación del propietario del reto.

## Estado de instalación/entrega

La campaña de clon limpio en Windows 10 pasó; tiempos, comandos y resultados están en el
informe `TASK047F-final-windows-delivery-report.md`. No usar resultados TASK046/TASK047 como
sustituto de la campaña. Los workflows requieren despacho manual y no se ejecutaron.

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
