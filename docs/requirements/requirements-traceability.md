# Matriz de trazabilidad del reto — SaaS-O-Matic

## Delta vigente TASK044

TASK044 refinó mensajes, errores de campo, navegación/foco, slider y resumen móvil; amplió
Playwright para concurrencia, invalidación, guardado y respuesta definitiva distinta. La
integración real Angular–FastAPI–SQLite temporal comprobó 15 y 16 usuarios, sus parámetros,
preview, respuesta HTTP 201 e historial persistido. V43-01 se reproduce en el fixture
visual anterior; no se confirmó defecto productivo en los casos integrados. V43-02 se
reprodujo sólo en captura full-page, no como foco inicial en viewport. La revisión
independiente, publicación y despliegue permanecen pendientes; no se certifica WCAG AA.

## Delta TASK043

TASK043 implementa localmente SPEC-009: formulario reactivo, preview no persistente,
conversión EUR/USD/GBP, guardado explícito e historial. FastAPI continúa como única
autoridad económica. Pruebas simuladas, integración real Angular–FastAPI–SQLite y
consulta puntual FX constan en el informe TASK043. La revisión visual del propietario
fue APTA CON OBSERVACIONES (V43-01–07); auditoría independiente y publicación siguen
pendientes. No se declara certificación WCAG ni auditoría de seguridad completa.

## Contexto TASK042

El backend está integrado en `main` mediante PR #6 (merge `23cc43b486d20f7995a2cf29375e3f724f3c7c3f`).
TASK041 resolvió P-01 y creó shell/HTTP. TASK042 añade localmente dashboard, listado,
búsqueda/paginación, alta de seis países, ficha e historial. Vitest, Playwright y un
flujo real navegador→Angular proxy→FastAPI→SQLite temporal verificaron este alcance.
En TASK042 el simulador y preview UI seguían pendientes; TASK043 los implementa localmente.
CI y despliegue continúan pendientes.
No se declara el frontend publicado ni se cubre el MVP completo.

## Contexto del delta TASK039B

TASK039 completó la auditoría del backend acumulado con dictamen **APTA CON
OBSERVACIONES** y sin hallazgos bloqueantes. TASK039B corrige A39-01, A39-02,
A39-03, A39-04 y A39-06, documenta A39-05 y revisa A39-07 a A39-11; A39-12 a
A39-15 quedan diferidos o aceptados. El runtime y Alembic comparten la resolución
de `DATABASE_URL`/SQLite y las tasas FX externas patológicas se rechazan antes de
la caché con `503 application/problem+json`. La suite local tiene 579 pruebas.
En ese corte el backend aún no se había publicado; ese estado quedó superado por
TASK040/PR #6 y la integración en `main`. La auditoría fue metodológicamente
independiente, no una auditoría humana externa.

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
| Versión | 1.6 (TASK044) |
| Fecha | 2026-11-19 |
| Estado | Backend integrado en main; frontend TASK041–TASK044 implementado/validado localmente; auditoría independiente, publicación y despliegue pendientes |
| Fuente principal | Enunciado original del reto, conservado fuera de Git y no publicado en GitHub |
| Fuentes internas | Requisitos, ADRs, especificaciones 001–009, planes, tareas, código, pruebas y auditorías TASK039/TASK039B |

## 1. Propósito y método

Esta matriz relaciona cada requisito del enunciado original con los identificadores internos, las decisiones aplicables, la implementación existente, las evidencias disponibles, el trabajo pendiente y los criterios de aceptación finales.

Se distingue de forma explícita entre:

- **Backend:** existencia y verificación de la lógica, el contrato y la persistencia en el servidor.
- **Extremo a extremo (E2E):** cumplimiento visible para el usuario a través del frontend, la integración y la base de datos.

Un requisito que necesita frontend o integración se distingue entre implementación local,
validación E2E y entrega publicada. TASK042 verifica el subflujo de clientes y TASK043
verifica simulador, preview/guardado e historial localmente; esto no completa la auditoría
independiente, la publicación ni la entrega/despliegue definitivos del MVP.

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

## 2. Matriz vigente TASK043 y deltas previos

La siguiente tabla sustituye el estado de las filas afectadas de la matriz de partida.
TASK043 añade validación local real del simulador; no declara el MVP publicado, auditado
independientemente ni desplegado. Las tablas inferiores conservan explícitamente el
contexto histórico en que fueron redactadas.

| Reto | Backend actual | E2E | Evidencia y pendiente |
| --- | --- | --- | --- |
| CH-04 | Completado localmente | Implementado/integrado localmente TASK042 | Alta ES/PT sintética, seis países disponibles y plan standard; auditoría independiente pendiente. |
| CH-05 | Completado | Integrado localmente TASK042 | Algoritmos ES y validación genérica no oficial fuera de ES. |
| CH-06 | Completado localmente | Implementado/integrado localmente TASK043 | Usuarios, GB y llamadas mensuales con límites; comprobación real ES/PT. |
| CH-07 | Completado localmente | Guardado EUR integrado localmente TASK043 | Subtotal, impuesto, total y snapshot persistidos; escenarios no cubren todos los países. |
| CH-08 | Completado localmente | Implementado/integrado parcialmente TASK043 | Cero, 15 y cambios de usuarios comprobados; reglas monetarias se calculan en backend. |
| CH-09 | Completado localmente | Implementado/integrado localmente TASK043 | Periodicidad mensual visible, fijada/persistida por servidor. |
| CH-10 | Completado localmente | Integrado localmente TASK043 | Casos ES/PT sintéticos contrastados con tasas devueltas; alcance fiscal simplificado. |
| CH-12 | Completado localmente | Selector local TASK043; FX puntual real | Frankfurter v2, caché24h, timeout5s y errores 503; consultas USD/GBP fuera de la suite determinista. |
| CH-13 | Completado localmente (backend) | Implementado localmente TASK043 | Selector EUR/USD/GBP; conversiones puntuales reales verificadas separadas de la suite; revisión independiente pendiente. |
| CH-14 | Completado localmente (backend) | Implementado/integrado localmente TASK042 | Dashboard sin métricas inventadas, listado/búsqueda paginados; aún no publicado. |
| CH-15 | Completado localmente (backend) | Implementado/integrado localmente TASK042 | Ficha e historial paginado responsive; snapshots NULL como desconocidos. |
| CH-16 | Completado localmente (backend) | Implementado/integrado localmente TASK043 | Slider/manual, preview sin persistencia, guardado explícito e historial; 404/503 y concurrencia cubiertos; auditoría independiente pendiente. |
| CH-18 | Completado en alcance actual | Local | SPEC-001–009, planes/tareas previos al código y evidencias TASK041–TASK043. |
| CH-22 | Parcial | Parcial local | 579 Pytest, 37 Vitest, 17 E2E estándar y dos pruebas opt-in pasadas aparte; CI y auditoría independiente pendientes. |
| CH-24 | Parcial | Parcial local | READMEs documentan arranque y proxy; npm ci limpio pendiente por scripts no autorizados; CI/despliegue P-05 pendientes. |

Q-18–Q-26 aprobadas e implementadas en el alcance backend actual; Q-22/Q-23
resueltas en TASK037 y Q-24/Q-25 en TASK038. P-01 se resolvió en TASK041; P-05 sigue
pendiente. TASK043 implementa localmente la UI de simulador conforme a SPEC-009; la
instalación limpia, la auditoría independiente y la publicación no están completadas.
Referencias: [SPEC-004](../specs/004-international-customers-and-simulations/spec.md) y
[SPEC-009](../specs/009-interactive-subscription-simulator/spec.md).

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
| FR-01 | Alta de clientes | Completado localmente, seis países | Implementado/integrado localmente TASK042 | Alta ES/PT sintética y conflictos comprobados; sin publicación |
| FR-02 | Validación fiscal | Completado ES; genérico internacional no oficial | Integrado localmente TASK042 | Servidor valida; UI no duplica algoritmo fiscal |
| FR-03 | Simulaciones persistidas | Completado localmente en el alcance aprobado | Implementado/integrado localmente TASK043 | Guardado y recarga comprobados con SQLite temporal; sin publicación |
| FR-04 | Usuarios, almacenamiento y llamadas API | Completado localmente | Implementado/integrado localmente TASK043 | Límites frontend/backend; consumos informativos sin cargos |
| FR-05 | Tramos progresivos | Completado localmente, 0+ | Implementado/integrado localmente TASK043 | FastAPI calcula; UI presenta tarifas/bandas y subtotal devuelto |
| FR-06 | Impuestos por país | Completado localmente, IVA general de seis países | Implementado/integrado localmente TASK043 | Casos ES/PT sintéticos contrastados con backend |
| FR-07 | Búsqueda y dashboard | Backend completo | Implementado/integrado localmente TASK042 | — |
| FR-08 | Detalle e historial | Backend completo | Implementado/integrado localmente TASK042 | — |
| FR-09 | Simulador y previsualización | Backend completado localmente | Implementado/integrado localmente TASK043 | Slider/manual, preview cancelable, guardado explícito; auditoría independiente pendiente |
| FR-10 | Divisas | Completado localmente, Frankfurter v2 EUR/USD/GBP | Implementado localmente TASK043 | Selector y smoke FX real separados de la suite determinista |
| FR-11 | Persistencia de conversión | Completado localmente con snapshot inmutable | Implementado/integrado parcialmente TASK043 | UI real guardó EUR; conversión USD/GBP se probó como preview puntual |
| FR-12 | Periodicidad mensual | Completado localmente, `monthly` fijado por servidor | Implementado/integrado localmente TASK043 | Etiqueta mensual, persistencia e historial real |

---

## 4. Discrepancias de partida TASK035 y propuestas entonces pendientes

Estado vigente: DISC-01 a DISC-09 implementadas en el backend local en el alcance
aprobado (TASK036–TASK039B); Angular y READMEs frontend están implementados localmente
(TASK041–TASK043), pero instalación limpia, auditoría independiente, publicación,
CI y despliegue siguen pendientes. DISC-12/13 están resueltas documentalmente. Las
recomendaciones de la tabla conservan el contexto de partida TASK035 y no son
aprobaciones adicionales de trabajo futuro.

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
| Planificación y diseño | 35 % | Requisitos, ADRs, SPEC-001–009, planes, tareas, matriz y roadmap. | Revisión independiente del frontend y cierre de P-05. |
| Criterio técnico y calidad | 25 % | Backend 579 pruebas; frontend 37 Vitest/17 E2E estándar; Ruff/mypy; integración real y registros TASK039–043. | Auditoría independiente, SAST/DAST y CI. |
| Calidad del software entregado | 30 % | Angular responsive, flujos locales de clientes y simulador, estados, preview/guardado, FastAPI/SQLite real, contratos exactos. | Resolución V43-01–07, auditoría accesibilidad formal y revisión completa del MVP. |
| README y despliegue | 10 % | READMEs raíz/backend/frontend y arranque conjunto validado con datos sintéticos. | npm ci limpio, CI, estrategia P-05 y despliegue. |

### 6.1. Evidencias que no deben fabricarse

- Conversaciones o prompts no registrados.
- Capturas de pantalla de funcionalidades inexistentes.
- Resultados de pruebas no ejecutadas.
- Tasas, tipos de cambio o datos fiscales inventados.
- Despliegues no realizados.

Las capturas y resultados reales se conservan fuera del repositorio según TASK042/043;
se distingue evidencia con APIs interceptadas de la integración real. No se infieren
resultados no ejecutados ni se declara auditoría o despliegue.

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
| ADR 0003 — Angular | [`../adr/0003-angular-frontend-stack.md`](../adr/0003-angular-frontend-stack.md) |
| SPEC-007 — Frontend | [`../specs/007-angular-frontend-foundation/spec.md`](../specs/007-angular-frontend-foundation/spec.md) |
| SPEC-008 — Gestión frontend de clientes | [`../specs/008-customer-management-frontend/spec.md`](../specs/008-customer-management-frontend/spec.md) |
| SPEC-009 — Simulador interactivo | [`../specs/009-interactive-subscription-simulator/spec.md`](../specs/009-interactive-subscription-simulator/spec.md) |
| Evidencia TASK042 | [`../../ai-workspace/01-tasks/TASK042-customer-management-frontend.md`](../../ai-workspace/01-tasks/TASK042-customer-management-frontend.md) |
| Evidencia TASK043 | [`../../ai-workspace/01-tasks/TASK043-interactive-subscription-simulator.md`](../../ai-workspace/01-tasks/TASK043-interactive-subscription-simulator.md) |
| Preparación publicación TASK043P | [`../../ai-workspace/01-tasks/TASK043P-frontend-intermediate-publication.md`](../../ai-workspace/01-tasks/TASK043P-frontend-intermediate-publication.md) |
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

El backend del alcance aprobado está implementado, probado e integrado en `main`: clientes,
precios, simulaciones, impuestos generales, conversión EUR/USD/GBP, consultas,
historial inmutable y previsualización. TASK039 lo auditó con dictamen **APTA CON
OBSERVACIONES** y TASK039B corrigió los defectos autorizados. TASK041–TASK043 implementan
localmente el frontend comercial, incluido el simulador asociado a cliente, preview,
guardado explícito e historial, con FastAPI como autoridad económica. Se verificó el
flujo real Angular–FastAPI–SQLite y consultas puntuales FX; el frontend aún no se publica
ni cuenta con auditoría independiente. El cumplimiento y la entrega definitiva del MVP
siguen **parciales** por revisión V43-01–07, WCAG formal, npm ci limpio, CI y P-05/
despliegue pendientes.

Los estados «implementado/integrado localmente» no equivalen a publicación, auditoría
independiente ni entrega definitiva. Los estados históricos de TASK035–TASK042 se
conservan en sus secciones de contexto sin reescribir decisiones ni requisitos originales.
