# Matriz de trazabilidad del reto — SaaS-O-Matic

## Delta vigente TASK039B

TASK039 completó la auditoría del backend acumulado con dictamen **APTA CON
OBSERVACIONES** y sin hallazgos bloqueantes. TASK039B corrige A39-01, A39-02,
A39-03, A39-04 y A39-06, documenta A39-05 y revisa A39-07 a A39-11; A39-12 a
A39-15 quedan diferidos o aceptados. El runtime y Alembic comparten la resolución
de `DATABASE_URL`/SQLite y las tasas FX externas patológicas se rechazan antes de
la caché con `503 application/problem+json`. La suite local tiene 579 pruebas.
El backend se publica en la rama/PR de TASK040; la integración en `main` sigue
pendiente. Angular, E2E, seguridad de despliegue y CI continúan pendientes. Esta revisión es metodológica,
no una auditoría humana externa.

## Delta vigente TASK038

CH-14/CH-15/CH-16: componentes backend implementados y verificados localmente:
búsqueda/listado/detalle/historial y previsualización sin escritura. FR-07/FR-08/FR-09
backend completados según [SPEC-006](../specs/006-customer-queries-and-preview/spec.md),
sin declarar completos dashboard, tarjetas responsive, slider ni otro flujo E2E visual.
Q-09/Q-24/Q-25/SIM-P10/SIM-P11 consolidados, paginación20/100/offset y snapshots
históricos sin catálogo/FX actuales. 538 pruebas y flujo integrado real backend.
H-01/H-02/H-03/H-04/H-05/H-08 conservados/atendidos; H-06/H-07 residuales sin cambio.
Auditoría independiente TASK039 pendiente en ese corte. Las tablas inferiores de
partida se interpretan con este delta y el de TASK037; no equivalen a implementación
de UI.

## Delta vigente TASK037

CH-07/CH-10/CH-12/CH-13 backend completados localmente en alcance aprobado:
IVA general de seis países, conversión EUR/USD/GBP por Frankfurter v2, snapshot
reproducible y caché controlada. E2E pendiente por ausencia de UI.
FR-06/FR-10/FR-11 backend completados según
[SPEC-005](../specs/005-taxes-and-currency-conversion/spec.md).
Q-05/Q-06/Q-07/Q-16/Q-17/Q-22/Q-23 y SIM-P14 resueltos en ese alcance,
sin inventar fechas efectivas fiscales. Q-08 conserva cadenas exactas y precisa
HALF_UP a dos decimales para impuestos/conversión, no tasas.
H-03 resuelto acotadamente: contexto independiente en pricing; H-01 conservado y
ampliado a límites de exponente; H-06/H-07 siguen como riesgos residuales justificados.
Las matrices de partida inferiores conservan el contexto de TASK035/036 y se
interpretan con este delta. Fuente fiscal/proveedor y limitaciones en SPEC-005/sources.md.

| Campo | Valor |
| --- | --- |
| Versión | 1.2 (TASK039B) |
| Fecha | 2026-11-18 |
| Estado | TASK040 publica el backend en rama/PR para revisión; integración en main pendiente |
| Fuente principal | Enunciado original del reto, conservado fuera de Git y no publicado en GitHub |
| Fuentes internas | Requisitos, ADRs, especificaciones 001–006, planes, tareas, código, pruebas y auditorías TASK039/TASK039B |

## 1. Propósito y método

Esta matriz relaciona cada requisito del enunciado original con los identificadores internos, las decisiones aplicables, la implementación existente, las evidencias disponibles, el trabajo pendiente y los criterios de aceptación finales.

Se distingue de forma explícita entre:

- **Backend:** existencia y verificación de la lógica, el contrato y la persistencia en el servidor.
- **Extremo a extremo (E2E):** cumplimiento visible para el usuario a través del frontend, la integración y la base de datos.

Un requisito que necesita frontend o integración **no se declara completado** aunque su backend esté terminado.

### 1.1. Estados utilizados

| Estado | Significado |
| --- | --- |
| Completado | Implementado y verificado en el nivel indicado, con evidencia disponible. |
| Parcial | Existe una parte funcional, pero falta alcance del enunciado o integración. |
| Pendiente | No existe implementación o no cubre el requisito. |
| Pendiente de decisión | Bloqueado por una decisión del propietario (Q-18 a Q-26 o P-01/P-05). |
| Fuera de alcance | Excluido expresamente del MVP. |

### 1.2. Referencias al documento original

Las referencias usan la sección y la viñeta del enunciado, no números de línea del fichero `.docx`:

- **§1:** Introducción y Filosofía del Reto.
- **§2:** Requisitos Técnicos del Sistema.
- **§2.A:** Backend (API REST & Base de Datos).
- **§2.B:** Frontend (Dashboard Comercial).
- **§3:** Entregables: espacio de trabajo con IA.
- **§4:** Criterios de Evaluación.

---

## 2. Matriz vigente y delta TASK039B

La siguiente tabla sustituye el estado de las filas afectadas de la matriz
de partida. Las demás filas permanecen sin cambio; ningún flujo E2E está completado.

| Reto | Backend actual | E2E | Evidencia y pendiente |
| --- | --- | --- | --- |
| CH-04 | Completado localmente | Pendiente | Seis países; test_customer_api/test_generic_tax_id; plan standard. |
| CH-05 | Completado | Pendiente | Algoritmos ES intactos; resto genérico no oficial. |
| CH-06 | Completado localmente | Pendiente | Consumos obligatorios; test_simulation_api; SPEC-004. |
| CH-07 | Completado localmente | Pendiente | Subtotal, impuesto, total y snapshot FX persistidos; SPEC-005. |
| CH-08 | Completado localmente | Pendiente | Cero y 15, nueve subtotales y números enormes probados. |
| CH-09 | Completado localmente | Pendiente | Monthly fijado por servidor, persistido y devuelto. |
| CH-10 | Completado localmente | Pendiente | IVA general de seis países; test_monthly_calculation; SPEC-005. |
| CH-12 | Completado localmente | Pendiente | Frankfurter v2, caché24h, timeout5s y errores 503; SPEC-005. |
| CH-13 | Completado localmente (backend) | Pendiente | Conversión y snapshot backend; selector Angular no existe. |
| CH-14 | Completado localmente (backend) | Pendiente | GET /customers con búsqueda/paginación; dashboard no existe. |
| CH-15 | Completado localmente (backend) | Pendiente | Detalle e historial backend; tarjetas responsive no existen. |
| CH-16 | Completado localmente (backend) | Pendiente | POST /simulations/preview; slider Angular no existe. |
| CH-18 | Completado en alcance actual | No aplica | SPEC-001–006, planes y tareas añadidos antes del código. |
| CH-22 | Parcial | No aplica | 579 pruebas, TASK039 y correcciones TASK039B; sin frontend, seguridad ni CI. |
| CH-24 | Parcial | Pendiente | README backend y `.env.example` alineados; frontend/despliegue pendientes. |

Q-18–Q-26 aprobadas e implementadas en el alcance backend actual; Q-22/Q-23
resueltas en TASK037 y Q-24/Q-25 en TASK038. P-01/P-05 siguen pendientes. Referencia:
[SPEC-004](../specs/004-international-customers-and-simulations/spec.md).

### Matriz de partida TASK035 (referencia previa al delta)

| ID reto | Referencia original | Requisito del enunciado | IDs internos | Decisiones aplicables | Implementación backend | Evidencia | Estado backend | Estado E2E | Trabajo pendiente | Criterio de aceptación final |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CH-01 | §2, párrafo inicial | Frontend interactivo y backend conectado a una base de datos que se comuniquen entre sí. | CON-01, CON-02, FR-07–FR-11 | ADR 0001, ADR 0002 | Backend y SQLite existen; no hay frontend. | `backend/src/saas_o_matic/presentation/app.py`; migraciones Alembic; ausencia de `frontend/` | Parcial | Pendiente | Construir Angular y verificar el flujo completo. | Un usuario puede registrar un cliente, simular y consultar el historial desde Angular contra el backend y SQLite. |
| CH-02 | §2.A, viñeta «Tecnología» | Backend con tecnología libre, preferiblemente Node.js/TypeScript o Python. | CON-01 | ADR 0001 | Python 3.13 + FastAPI implementado. | `backend/pyproject.toml`; ADR 0001 | Completado | No aplica | Ninguno. | El backend arranca con Python 3.13 y FastAPI. |
| CH-03 | §2.A, viñeta «Base de Datos» | Base de datos SQLite. | CON-01 | ADR 0001 | SQLite con SQLAlchemy y Alembic. | `backend/src/saas_o_matic/infrastructure/database.py`; `backend/alembic/` | Completado | No aplica | Ninguno. | Las tablas se crean mediante migraciones y los datos persisten. |
| CH-04 | §2.A, viñeta `POST /customers` | Registrar cliente con nombre de empresa, identificador fiscal, email, país y plan. | FR-01, FR-02 | D-02, D-03, D-15; Q-20 pendiente | Alta de clientes españoles con `standard`. | `presentation/customers/router.py`; `presentation/customers/schemas.py`; `domain/customers/`; SPEC-001 | Parcial | Pendiente | Aprobar y ampliar catálogo de países y validación genérica. | `POST /customers` acepta los cinco campos, valida país/plan/identificador y devuelve `201`; los errores usan `problem+json`. |
| CH-05 | §2.A, viñeta «Validación Algorítmica» | Validación estricta; si el país es España, comprobar DNI/NIF/CIF con el algoritmo oficial. | FR-02 | D-03 | DNI/NIF, NIE y CIF/NIF validados algorítmicamente. | `domain/customers/value_objects.py`; pruebas de clientes | Completado para ES | Pendiente | Definir validación internacional genérica sin presentarla como oficial. | Identificadores españoles válidos se aceptan; inválidos se rechazan; un cliente no español sigue la política aprobada en Q-20. |
| CH-06 | §2.A, viñeta `POST /simulations` | Registrar simulación con ID de cliente, usuarios activos, almacenamiento contratado y llamadas API estimadas. | FR-03, FR-04 | SIM-P01, SIM-P02; Q-21 pendiente | Solo `customer_id` y `user_count`. | `presentation/simulations/schemas.py`; `application/simulations/use_cases.py`; SPEC-003 | Parcial | Pendiente | Añadir almacenamiento y llamadas API con unidades/rangos aprobados. | `POST /simulations` acepta y persiste los cuatro datos; `404` para cliente inexistente; `422` para datos inválidos. |
| CH-07 | §2.A, viñeta `POST /simulations` | El cálculo debe persistirse en la base de datos. | FR-03, FR-11 | SIM-P01, SIM-P13 | Se persiste `user_subtotal_eur` como texto decimal canónico. | `infrastructure/simulations/models.py`; migración de simulaciones | Parcial | Pendiente | Persistir base, impuesto, total y snapshot de conversión cuando se aprueben. | Cada simulación conserva un cálculo reproducible con importes y metadatos históricos. |
| CH-08 | §2.A, «Algoritmo de Facturación Gradual por Tramos» | Tramos 0–10 a 10 €, 11–50 a 8 €, más de 50 a 5 €; ejemplo 15 usuarios = 140 €. | FR-05 | Q-02, PP-Q-01; Q-19 pendiente | Tramos 1–10, 11–50, >50 con `Decimal`; 0 rechazado. | `domain/pricing/schedule.py`; `domain/pricing/services.py`; `backend/tests/test_pricing.py` | Parcial | Pendiente | Decidir Q-19 y añadir prueba dedicada de 15 usuarios. | Todos los límites y el ejemplo de 15 producen el importe exacto; la política de 0 usuarios es explícita y probada. |
| CH-09 | §2.A, párrafo «coste mensual base» | El coste calculado es mensual. | FR-12, ASM-08 | Q-18 pendiente | Mensual implícito; no hay campo de periodicidad. | `user_subtotal_eur`; sin campo `billing_period` | Parcial | Pendiente | Hacer explícita la periodicidad en UI y contrato. | La interfaz y la simulación guardada indican claramente que el importe es mensual. |
| CH-10 | §2.A, párrafo «Al total resultante…» | Sumar el impuesto (Tax/IVA) correspondiente al país del cliente. | FR-06, ASM-01, ASM-04 | Q-22 pendiente | No implementado. | No hay tablas ni servicios de impuestos | Pendiente | Pendiente | Aprobar fuente, tasas, vigencia, base, redondeo y persistencia. | Una simulación muestra subtotal, impuesto y total mensual; la tasa y su fuente quedan registradas. |
| CH-11 | §2.B, viñeta «Tecnología» | Frontend con tecnología libre. | CON-02 | P-01 pendiente | No implementado. | No existe `frontend/` | Pendiente | Pendiente | Aprobar versión de Angular y crear la aplicación. | El frontend compila, se sirve y consume la API. |
| CH-12 | §2.B, «Integración con API Externa» | Conectar con una API pública de tipos de cambio, como `open.er-api.com` o similar. | FR-10 | Q-06, Q-07, Q-23 pendientes | No implementado. | No hay servicio de divisas | Pendiente | Pendiente | Aprobar proveedor, caché, timeout, divisas y manejo de errores. | El sistema obtiene tipos públicos y los usa para la visualización sin exponer secretos. |
| CH-13 | §2.B, «Integración con API Externa» | Cambiar dinámicamente la divisa de visualización (EUR, USD, GBP, etc.) y ver costes convertidos en tiempo real. | FR-10, FR-11 | Q-16, Q-17, Q-23 pendientes | No implementado. | No hay selector ni conversión | Pendiente | Pendiente | Implementar selector, conversión y snapshot de tasa. | Al cambiar la divisa, la proyección mensual se actualiza y la simulación guardada conserva la conversión aplicada. |
| CH-14 | §2.B, «Buscador y Dashboard» | Buscador por nombre de empresa o identificador fiscal. | FR-07 | Q-24 pendiente | No implementado. | Solo existe `POST /customers` | Pendiente | Pendiente | Añadir listado/búsqueda y dashboard Angular. | El usuario encuentra clientes por razón social o identificador fiscal. |
| CH-15 | §2.B, «Detalle del Cliente (Cards)» | Tarjetas responsive con datos del cliente e historial de simulaciones guardadas. | FR-08 | Q-24 pendiente | No implementado. | No hay endpoints de lectura | Pendiente | Pendiente | Añadir detalle, historial y tarjetas responsive. | El detalle muestra datos e historial; se adapta a móvil y escritorio. |
| CH-16 | §2.B, «Formulario de Simulación Interactiva» | Slider/controles para usuarios y proyección mensual en tiempo real, calculada por tramos y convertida a la divisa. | FR-09, FR-10 | Q-12, Q-19, Q-25 pendientes | No implementado; solo existe el alta persistida. | `POST /simulations` | Pendiente | Pendiente | Añadir previsualización, simulador Angular y conversión en vivo. | Mover el slider actualiza la proyección sin escribir en SQLite; guardar es una acción explícita. |
| CH-17 | §3, párrafo 2 | Incluir una carpeta `/ai-workspace` en la raíz. | CON-12 | Proceso de desarrollo | Existe con contexto, tareas y auditorías. | `ai-workspace/README.md`; `ai-workspace/01-tasks/` | Completado | No aplica | Mantener actualizado con TASK035 y siguientes. | La carpeta explica planificación, arquitectura y proceso de IA con evidencias reales. |
| CH-18 | §3, «Planificación de Funcionalidades y Specs» | Mostrar especificaciones, contratos y planes antes de programar. | CON-12 | Proceso; SPEC-001–003 | Existen requisitos, ADRs y tres especificaciones con planes y tareas. | `docs/specs/`; `docs/requirements/`; `docs/adr/` | Completado | No aplica | Añadir SPEC-004 para el backend restante y SPEC-005 para Angular. | Cada funcionalidad tiene especificación, plan, tareas, criterios y evidencia. |
| CH-19 | §3, «Definición de la Arquitectura» | Mostrar estructura de base de datos y organización de carpetas, con directrices para código limpio y modular. | CON-01, CON-02 | ADR 0001, ADR 0002 | Monolito modular con capas y puertos/adaptadores. | `docs/adr/0002-architecture.md`; árbol de `backend/src/saas_o_matic/` | Completado | No aplica | Mantener la misma disciplina en Angular. | La arquitectura es comprensible, testeable y respeta dependencias hacia dentro. |
| CH-20 | §3, «Vibe Coding y Control de Calidad» | Mostrar interacción real con IA, prompts, hilos o notas, y control de calidad. | NFR-10 | Proceso de desarrollo | Hay 32 registros históricos, auditorías y correcciones; no se fabrican conversaciones. | `ai-workspace/01-tasks/`; TASK033; PR #5 | Parcial | No aplica | Añadir evidencias de las nuevas tareas y auditorías finales. | Se puede seguir el proceso real, las correcciones humanas y las auditorías. |
| CH-21 | §4, «Capacidad de Planificación y Diseño (35 %)» | Especificaciones y pasos lógicos antes de delegar código. | CON-12 | Proceso | Documentación amplia; falta plan de frontend y cierre de requisitos. | Requisitos, ADRs, SPEC-001–003, esta matriz y la hoja de ruta | Parcial | No aplica | Aprobar decisiones y añadir SPEC-004/SPEC-005. | Existe trazabilidad completa y planes aprobados para todo el alcance. |
| CH-22 | §4, «Criterio Técnico y Control de Calidad (25 %)» | Entender, auditar y corregir el código generado; evitar deuda técnica. | NFR-01–NFR-10 | TASK033 | 240 pruebas, Ruff, mypy, auditoría independiente; hallazgos no bloqueantes abiertos. | `backend/tests/`; TASK033; `ai-workspace/README.md` | Parcial | No aplica | Resolver H-01, H-02, H-04–H-08 en incrementos; añadir pruebas de frontend. | No hay hallazgos bloqueantes y la deuda está registrada y planificada. |
| CH-23 | §4, «Calidad del Software Entregado (30 %)» | Backend robusto (validaciones, tramos, persistencia) y frontend fluido (responsive, carga/error). | FR-01–FR-12 | Q-18–Q-26 | Backend parcial; frontend inexistente. | Código y pruebas actuales | Parcial | Pendiente | Completar backend y construir Angular. | Flujo completo funcional, con validaciones, persistencia, responsive y estados de carga/error. |
| CH-24 | §4, «README y Despliegue (10 %)» | Instrucciones claras para levantar backend y frontend en local en pocos pasos. | CON-13, NFR-09 | P-05 pendiente | README raíz y backend existen, pero están desactualizados; no hay frontend. | `README.md`; `backend/README.md`; `.env.example` | Parcial | Pendiente | Actualizar README raíz, backend y crear README de frontend; verificar pasos. | Un evaluador puede arrancar backend y frontend siguiendo el README, sin pasos ocultos. |
| CH-25 | §1, párrafo 2 | Mantener control de arquitectura, calidad y seguridad durante el desarrollo asistido por IA. | ADR 0002, NFR-07, NFR-10 | Proceso de desarrollo | Hay arquitectura, pruebas y auditorías; no hay análisis de seguridad específico ni CI. | ADRs; TASK033; pruebas | Parcial | No aplica | Añadir revisión de seguridad y, si se aprueba, CI. | Las decisiones y los riesgos quedan documentados y revisados. |

---

## 3. Requisitos internos y estado resumido

| ID | Requisito | Backend | E2E | Decisión pendiente |
| --- | --- | --- | --- | --- |
| FR-01 | Alta de clientes | Completado localmente, seis países | Pendiente | Ninguna en backend; UI/integración |
| FR-02 | Validación fiscal | Completado ES; genérico internacional no oficial | Pendiente | Ninguna en backend; UI/integración |
| FR-03 | Simulaciones persistidas | Completado localmente en el alcance aprobado | Pendiente | Ninguna en backend; UI/integración |
| FR-04 | Usuarios, almacenamiento y llamadas API | Completado localmente | Pendiente | Ninguna en backend; UI/integración |
| FR-05 | Tramos progresivos | Completado localmente, 0+ | Pendiente | Ninguna en backend; UI/integración |
| FR-06 | Impuestos por país | Completado localmente, IVA general de seis países | Pendiente | Ninguna en backend; UI/integración |
| FR-07 | Búsqueda y dashboard | Backend completado localmente; dashboard no existe | Pendiente | UI Angular |
| FR-08 | Detalle e historial | Backend completado localmente; tarjetas no existen | Pendiente | UI Angular |
| FR-09 | Simulador y previsualización | Backend completado localmente; slider no existe | Pendiente | UI Angular |
| FR-10 | Divisas | Completado localmente, Frankfurter v2 EUR/USD/GBP | Pendiente | Ninguna en backend; UI/integración |
| FR-11 | Persistencia de conversión | Completado localmente con snapshot inmutable | Pendiente | Ninguna en backend; UI/integración |
| FR-12 | Periodicidad mensual | Completado localmente, `monthly` fijado por servidor | Pendiente | UI Angular |

---

## 4. Discrepancias de partida TASK035 y propuestas entonces pendientes

Estado vigente: DISC-01 a DISC-09 implementadas en el backend local en el alcance
aprobado (TASK036–TASK039B); DISC-10 (Angular) y DISC-11 (README de frontend y
despliegue) siguen pendientes; DISC-12/13 resueltas documentalmente. Las
recomendaciones de la tabla no son aprobaciones de trabajo futuro.

| ID | Discrepancia | Estado actual | Opciones | Recomendación | Decisión |
| --- | --- | --- | --- | --- | --- |
| DISC-01 | El enunciado dice «coste mensual base»; el contrato actual no tiene periodicidad. | `billing_period=monthly` persistido y devuelto. | A) Mantener implícito y etiquetar la UI; B) persistir `billing_period`. | B: explícito en contrato y UI; no cambia el algoritmo. | Q-18 implementada |
| DISC-02 | El primer tramo original empieza en 0; Q-02 aprobó mínimo 1. | 0 se acepta con subtotal `0.00`. | A) Mantener mínimo 1; B) permitir 0 con subtotal 0,00; C) permitir 0 solo en preview. | B: cumple el enunciado y no altera el cálculo de tramos. | Q-19 implementada |
| DISC-03 | El enunciado admite país; la implementación solo acepta `ES`. | Seis países: ES/PT/FR/DE/IT/NL. | A) Solo España; B) lista corta con validación genérica; C) todos los ISO con validación genérica. | B: ES, PT, FR, DE, IT y NL; algoritmo oficial solo en ES; unicidad por país. | Q-20 implementada |
| DISC-04 | El enunciado pide almacenamiento y llamadas API; el contrato solo acepta usuarios. | Campos obligatorios y persistidos; históricos NULL. | A) GB y llamadas mensuales; B) unidades libres; C) no registrarlos. | A: enteros no negativos, sin cargos; nulos en históricos. | Q-21 implementada |
| DISC-05 | El enunciado pide impuesto por país; no hay tasas aprobadas. | IVA general de seis países con fuente versionada. | A) Tabla estática versionada; B) API fiscal externa; C) configuración manual. | A: fuente oficial, vigencia, `ROUND_HALF_UP`, snapshot histórico; sin inventar tasas. | Q-22 implementada |
| DISC-06 | El enunciado pide API pública de divisas y cambio dinámico; no hay integración. | Frankfurter v2, EUR/USD/GBP y caché. | A) `open.er-api.com`; B) Frankfurter; C) otro proveedor. | Frankfurter como proveedor único aprobado; proxy backend, caché 24 h, timeout 5 s. | Q-23 implementada |
| DISC-07 | El enunciado pide buscador, detalle e historial; solo existe alta. | Endpoints de lectura paginados e historial inmutable. | A) Endpoints de lectura con paginación; B) cargar todo en memoria. | A: `GET /customers`, `GET /customers/{id}`, `GET /customers/{id}/simulations`; historial inmutable. | Q-24 implementada |
| DISC-08 | El enunciado pide proyección en tiempo real; el único endpoint persiste. | `POST /simulations/preview` sin escritura. | A) `POST /simulations/preview`; B) calcular en Angular; C) persistir cada movimiento. | A: reutiliza el servicio backend; guardado explícito; sin escrituras por slider. | Q-25 implementada |
| DISC-09 | El contrato de simulación ignora campos desconocidos. | Simulaciones `extra="forbid"`; clientes conservan `ignore` por Q-26. | A) Mantener; B) `extra="forbid"`. | B para simulaciones; Q-26 aprueba la asimetría de clientes. | Q-26 implementada |
| DISC-10 | El frontend Angular no existe. | No hay `frontend/`. | A) Angular standalone; B) otra tecnología. | A: decisión del propietario y ADR 0001. | P-01 pendiente |
| DISC-11 | El README raíz describe solo el alta de clientes y el backend README no menciona simulaciones. | Documentación desactualizada. | A) Actualizar README raíz y backend; B) dejar histórico. | A: reflejar el estado real y añadir README de frontend cuando exista. | TASK035 / TASK036 |
| DISC-12 | NFR-02 mencionaba `/api/v1`, pero la API aprobada no usa prefijo. | Contradicción documental. | A) Mantener prefijo; B) reflejar la decisión SIM-P09. | B: corregido en la versión 0.9 de requisitos. | Resuelto documentalmente |
| DISC-13 | Q-08 y Q-12 aparecían como abiertas en algunos documentos. | Resueltas en SPEC-002/SPEC-003. | A) Mantener abiertas; B) consolidarlas. | B: cadena decimal exacta y límites API/UI consolidados. | Resuelto documentalmente |
| DISC-14 | TASK033 detectó incoherencias documentales (H-08). | Parcialmente corregidas. | A) Corregir en TASK035; B) posponer. | A para el estado vigente; B para README de backend si no se autoriza. | TASK035 |

---

## 5. Hallazgos técnicos y planificación

| Hallazgo | Origen | Descripción | Incremento propuesto |
| --- | --- | --- | --- |
| H-01 | TASK033 | Trampas del contexto `Decimal`. | Corregido TASK036; contexto local y rechazo sin redondeo. |
| H-02 | TASK033 | Cobertura de regresión incompleta. | Corregido en alcance TASK036: SQL TEXT, sesión nueva, Decimal/UTC, 15 y capas. |
| H-03 | Auditoría histórica de pricing | Decisión histórica de precios; no se modifica. | Sin acción; se conserva como registro. |
| H-04 | TASK033 | Orden de ejecución. | Corregido TASK036: validar → comprobar cliente → calcular. |
| H-05 | TASK033 | Campos desconocidos. | Corregido TASK036: forbid y 422 problem+json. |
| H-06 | TASK033 | Carrera comprobación/persistencia. | Riesgo residual justificado: FK y rollback conservados; no borrado público ni traducción general de IntegrityError a 404. |
| H-07 | TASK033 | Sin CHECK monetario adicional. | Justificado TASK036: TEXT y validación exacta en aplicación; evitar CHECK parcial frágil o conversión REAL. SQL directo sigue siendo riesgo. |
| H-08 | TASK033 | Coherencia documental. | Documentación vigente actualizada TASK036; registros históricos intactos. |

---

## 6. Criterios de evaluación y evidencias

| Categoría | Peso | Evidencias actuales | Evidencias que faltan |
| --- | --- | --- | --- |
| Planificación y diseño | 35 % | Requisitos, ADRs, SPEC-001–006, planes, tareas, matriz y roadmap. | Plan y README de frontend; decisiones P-01/P-05. |
| Criterio técnico y calidad | 25 % | Arquitectura, 579 pruebas locales, Ruff/mypy, TASK039 y correcciones TASK039B. | Frontend, revisión de seguridad, CI opcional y auditoría humana externa. |
| Calidad del software entregado | 30 % | Backend de clientes, precios, simulaciones, impuestos, FX, consultas, historial y preview; SQLite; `problem+json`. | Angular responsive, flujo E2E, estados de carga/error y controles de exposición. |
| README y despliegue | 10 % | README raíz, README de backend, `.env.example` alineado, migraciones y pruebas. | README de frontend, arranque conjunto verificado y estrategia de despliegue. |

### 6.1. Evidencias que no deben fabricarse

- Conversaciones o prompts no registrados.
- Capturas de pantalla de funcionalidades inexistentes.
- Resultados de pruebas no ejecutadas.
- Tasas, tipos de cambio o datos fiscales inventados.
- Despliegues no realizados.

Las capturas y resultados reales se añadirán cuando exista la implementación correspondiente.

---

## 7. Índice de evidencias

| Evidencia | Ruta |
| --- | --- |
| Requisitos funcionales | [`functional-requirements.md`](functional-requirements.md) |
| ADR de stack | [`../adr/0001-technology-stack.md`](../adr/0001-technology-stack.md) |
| ADR de arquitectura | [`../adr/0002-architecture.md`](../adr/0002-architecture.md) |
| SPEC-001 | [`../specs/001-customer-registration/spec.md`](../specs/001-customer-registration/spec.md) |
| SPEC-002 | [`../specs/002-progressive-pricing/spec.md`](../specs/002-progressive-pricing/spec.md) |
| SPEC-003 | [`../specs/003-simulations/spec.md`](../specs/003-simulations/spec.md) |
| SPEC-004 | [`../specs/004-international-customers-and-simulations/spec.md`](../specs/004-international-customers-and-simulations/spec.md) |
| SPEC-005 | [`../specs/005-taxes-and-currency-conversion/spec.md`](../specs/005-taxes-and-currency-conversion/spec.md) |
| SPEC-006 | [`../specs/006-customer-queries-and-preview/spec.md`](../specs/006-customer-queries-and-preview/spec.md) |
| Plan de simulaciones | [`../specs/003-simulations/plan.md`](../specs/003-simulations/plan.md) |
| Tareas de simulaciones | [`../specs/003-simulations/tasks.md`](../specs/003-simulations/tasks.md) |
| Registro de tareas | [`../../ai-workspace/README.md`](../../ai-workspace/README.md) |
| Auditoría TASK039 | [`../../ai-workspace/01-tasks/TASK039-backend-independent-audit.md`](../../ai-workspace/01-tasks/TASK039-backend-independent-audit.md) |
| Correcciones TASK039B | [`../../ai-workspace/01-tasks/TASK039B-backend-audit-remediation.md`](../../ai-workspace/01-tasks/TASK039B-backend-audit-remediation.md) |
| Implementación de simulaciones | [`../../ai-workspace/01-tasks/TASK032-simulations-implementation.md`](../../ai-workspace/01-tasks/TASK032-simulations-implementation.md) |
| Código de precios | [`../../backend/src/saas_o_matic/domain/pricing/`](../../backend/src/saas_o_matic/domain/pricing/) |
| Código de simulaciones | [`../../backend/src/saas_o_matic/application/simulations/`](../../backend/src/saas_o_matic/application/simulations/) |
| Pruebas de precios | [`../../backend/tests/test_pricing.py`](../../backend/tests/test_pricing.py) |
| Pruebas de simulación | [`../../backend/tests/test_simulation_api.py`](../../backend/tests/test_simulation_api.py) |
| Pruebas de configuración SQLite | [`../../backend/tests/test_database_config.py`](../../backend/tests/test_database_config.py) |
| Pruebas de Frankfurter | [`../../backend/tests/test_frankfurter.py`](../../backend/tests/test_frankfurter.py) |
| README raíz | [`../../README.md`](../../README.md) |
| README de backend | [`../../backend/README.md`](../../backend/README.md) |
| Hoja de ruta | [`../planning/mvp-roadmap.md`](../planning/mvp-roadmap.md) |

---

## 8. Conclusión de la reconciliación

El backend del alcance aprobado está implementado y probado localmente: clientes,
precios, simulaciones, impuestos generales, conversión EUR/USD/GBP, consultas,
historial inmutable y previsualización. TASK039 lo auditó con dictamen **APTA CON
OBSERVACIONES** y TASK039B corrigió los defectos autorizados. El cumplimiento del
enunciado original sigue siendo **parcial** porque no existe frontend Angular, no
hay flujo E2E visual, no se ha desplegado y quedan riesgos aceptados o diferidos
(documentados en TASK039/TASK039B). La ruta siguiente es construir la UI sobre el
contrato backend y completar integración, seguridad de despliegue y verificación
E2E antes de la entrega.

Ningún requisito se declara completado en esta matriz si depende de una pantalla
que aún no existe, de una decisión pendiente o de una publicación no realizada.
