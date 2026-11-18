# Hoja de ruta optimizada del MVP — SaaS-O-Matic

**Vigente TASK043:** el backend se integró en main mediante PR #6, merge
`23cc43b486d20f7995a2cf29375e3f724f3c7c3f`. TASK041 estableció el shell y P-01;
TASK042 implementa localmente dashboard y gestión de clientes (listado/búsqueda,
registro, detalle e historial) con integración real y pruebas. TASK043 implementa
localmente el simulador y su integración real. Revisión/publicación, CI y despliegue
siguen pendientes; P-05 permanece abierta. Cambios sin publicar.

**Contexto TASK039B:** TASK039 auditó el backend acumulado con dictamen APTA CON
OBSERVACIONES y sin hallazgos bloqueantes. TASK039B corrige A39-01/02/03/04/06,
documenta A39-05 y revisa A39-07 a A39-11; A39-12 a A39-15 quedan diferidos o
aceptados. Runtime y Alembic comparten la resolución SQLite; las tasas FX
patológicas se rechazan antes de la caché con `503`. Backend: 579 pruebas. TASK040
publicó el backend mediante PR #6; el propietario lo fusionó. P-01 resuelta en TASK041;
P-05/despliegue sigue pendiente. Las tablas inferiores mantienen el contexto histórico.
Los estados de TASK036/037/038 inferiores conservan su contexto de planificación previa.

**TASK037 (histórico):** impuestos generales y FX EUR/USD/GBP implementados
localmente según SPEC-005 y auditados dentro de TASK039. Fuentes nacionales/UE y
Frankfurter v2 verificados; caché24h, timeout5s, snapshot exacto y límites técnicos
de plausibilidad FX en TASK039B. TASK038 se completó después; TASK039/TASK039B y
TASK040 requieren sus autorizaciones propias. Descripciones de TASK036 inferiores
son contexto previo.

| Campo | Valor |
| --- | --- |
| Versión | 1.4 (TASK043) |
| Fecha | 2026-11-18 |
| Estado | TASK041–TASK043 implementadas/validadas localmente; revisión visual APTA CON OBSERVACIONES; TASK043P en curso; auditoría independiente y entrega final pendientes |
| Base | `origin/main` en `23cc43b486d20f7995a2cf29375e3f724f3c7c3f` (PR #6 fusionado) |
| Referencia principal | Enunciado original del reto, conservado fuera de Git |
| Trazabilidad | [`../requirements/requirements-traceability.md`](../requirements/requirements-traceability.md) |

## 1. Principios

1. **Cumplimiento del reto primero.** El orden prioriza los requisitos explícitos del enunciado sobre mejoras opcionales.
2. **Menos tareas, mismos controles.** Las decisiones relacionadas se aprueban conjuntamente y se agrupan en incrementos funcionales.
3. **Backend antes que frontend.** Angular consume contratos estables; no se duplica la lógica de precios, impuestos o divisas.
4. **Trazabilidad y auditoría.** Cada incremento tiene especificación, plan, tareas, pruebas y evidencia en `ai-workspace/`.
5. **Publicación controlada.** El propietario autoriza cada operación Git y fusiona personalmente los pull requests.
6. **Sin datos inventados.** Tasas, divisas, precios y reglas no documentadas quedan como decisiones pendientes.

## 2. Estado de partida (referencia histórica TASK035)

| Elemento | Estado |
| --- | --- |
| Backend | FastAPI, SQLite, Alembic, clientes españoles, precios progresivos y simulaciones parciales. |
| Pruebas | 240 pruebas superadas en TASK034; Ruff, Ruff format, mypy y `pip check` correctos. |
| Frontend | No existe. |
| Impuestos | No implementados. |
| Divisas | No implementadas. |
| Búsqueda, detalle e historial | No implementados. |
| Previsualización | No implementada. |
| CI / despliegue | No existen. |
| Publicaciones | PR #1–#5 fusionados; último merge `b3c5ca81d23d279b478ed466757bada031aa1e1e`. |

## 3. Puertas de decisión

TASK036 aprueba Q-18–Q-21/Q-26 y el alcance futuro Q-22–Q-25, no todos sus detalles:

| Decisión | Tema | Recomendación |
| --- | --- | --- |
| Q-18 | Periodicidad mensual explícita | Persistir `billing_period = "monthly"` y etiquetar la UI. |
| Q-19 | Usuarios cero | Permitir 0 con subtotal `0.00`; revisar Q-02/PP-Q-01. |
| Q-20 | Países y validación internacional | ES, PT, FR, DE, IT y NL; algoritmo oficial solo en ES. |
| Q-21 | Almacenamiento y llamadas API | GB enteros y llamadas mensuales; sin cargos. |
| Q-22 | Impuestos | TASK037 implementado localmente: generales oficiales verificados, catálogo versionado y snapshot; vigencia desconocida NULL. |
| Q-23 | Divisas | TASK037 implementado: Frankfurter v2 verificado, EUR/USD/GBP, TTL24h y timeout5s; sin publicar. |
| Q-24 | Búsqueda, detalle e historial | Endpoints de lectura con paginación; historial inmutable. |
| Q-25 | Previsualización | `POST /simulations/preview` sin persistencia; guardado explícito. |
| Q-26 | Campos desconocidos | `extra="forbid"` en simulación y preview. |
| P-01 | Versión concreta Angular y confirmación Vitest | Resuelta TASK041/ADR 0003: Angular 22.2.6, Vitest 5.1.1; shell base local. |
| P-05 | Estrategia de despliegue y SQLite fuera de desarrollo | Pendiente; no bloquea TASK036. |

Las recomendaciones de contratos, caché, fuentes, tasas, precisión y paginación de las fases siguientes no se consideran aprobadas por inferencia. TASK036 no implementa impuestos, divisas, consultas ni preview.

## 4. Fases de referencia

Las diez fases siguientes son la descomposición funcional del reto; la sección 5 contiene la nueva secuencia autorizada como planificación.

### R1. Clientes internacionales y ampliación del modelo de simulaciones

- **Objetivo:** permitir clientes de varios países y registrar todos los datos de consumo del enunciado.
- **Requisitos:** CH-04, CH-05, CH-06, CH-08, CH-09; FR-01–FR-05, FR-12.
- **Dependencias:** Q-18, Q-19, Q-20 y Q-21 aprobadas.
- **Cambios TASK036:** seis países ISO; validación genérica 1..64 tras normalizar espacios/mayúsculas, preservando puntuación y rechazando controles; unicidad por país existente; ES compatible; migración 0003 con consumos NULL históricos, periodo mensual y usuarios desde cero. El alta internacional no depende de impuestos aún inexistentes. Véase SPEC-004.
- **Aceptación:** un cliente español y uno internacional se crean; un identificador español inválido se rechaza; una simulación guarda usuarios, almacenamiento (`storage_gb`, entero 0..1.000.000), llamadas mensuales (`api_calls_per_month`, entero 0..1.000.000.000) y periodicidad; los registros históricos no se falsean y quedan nulos si no se registraron.
- **Pruebas:** unitarias de validación, integración de migración, API `201/404/422`, regresión de clientes existentes.
- **Riesgos:** alcance internacional excesivo; migración de datos históricos; validación genérica mal presentada como oficial.
- **Auditoría/publicación:** revisión independiente del contrato y la migración antes del PR.

### R2. Motor de impuestos

- **Objetivo:** calcular el impuesto por país y el total mensual.
- **Requisitos:** CH-10; FR-06, FR-11.
- **Dependencias:** R1; Q-22 aprobada.
- **Cambios previstos:** tabla versionada de tasas aprobadas; servicio de cálculo; base imponible; redondeo; persistencia de tasa, fuente, vigencia, impuesto y total; respuesta con desglose. Fuentes propuestas: AEAT para España y Comisión Europea (VAT rates) para países UE; los valores concretos requieren aprobación.
- **Aceptación:** una simulación muestra subtotal, impuesto y total; la tasa aplicada y su fuente quedan guardadas; un país sin tasa aprobada no se simula.
- **Pruebas:** límites de redondeo, tasas conocidas, país no soportado, snapshot histórico, migración.
- **Riesgos:** tasas desactualizadas; redondeo inconsistente; confusión con asesoramiento fiscal.
- **Auditoría/publicación:** revisión independiente de la fuente de tasas y del redondeo antes del PR.

### R3. Conversión de divisas

- **Objetivo:** obtener tipos públicos y convertir el total mensual a la divisa de visualización.
- **Requisitos:** CH-12, CH-13; FR-10, FR-11.
- **Dependencias:** R2; Q-23 aprobada.
- **Cambios previstos:** puerto de proveedor; adaptador HTTP con timeout y caché; endpoint de tipos; selector de divisa; persistencia de divisa, tasa, fecha, fuente e importe convertido; atribución del proveedor.
- **Aceptación:** EUR, USD y GBP funcionan; el cambio de divisa actualiza la proyección; el guardado conserva el snapshot; un fallo del proveedor devuelve `503` sin persistir datos incompletos.
- **Pruebas:** proveedor falso, caché, timeout, EUR identidad, redondeo, error de red, contrato HTTP.
- **Riesgos:** dependencia externa; límites del proveedor; CORS si Angular llama directamente; tipos de cambio no reproducibles.
- **Auditoría/publicación:** revisión independiente del manejo de errores y de la persistencia del snapshot.

#### Comparación de proveedores de divisas

| Criterio | `open.er-api.com` | Frankfurter |
| --- | --- | --- |
| Acceso gratuito | Sí, acceso abierto | Sí |
| Credenciales | No requiere clave en el acceso abierto | No requiere clave |
| Divisas | Amplio catálogo, con EUR como base | 219 divisas y 39 activos |
| Actualización | Una actualización diaria aproximada | Varias referencias diarias de bancos centrales |
| Límites | Límites de uso y posibilidad de `429` | Límites de uso; API pública |
| Integración | JSON simple; atribución requerida | JSON simple; histórico y autoservicio |
| Errores/timeout | Requiere caché, timeout y manejo de `429` | Requiere caché, timeout y manejo de errores |
| Reproducibilidad | Persistir tasa, fecha y fuente | Persistir tasa, fecha y fuente |

**Vigente TASK036:** Frankfurter es el proveedor único preferente, condicionado a verificar documentación y adecuación vigentes en TASK037. La comparación anterior procede de TASK035, no sustituye esa verificación. No se implementarán proveedores simultáneos; caché, caducidad, precisión y errores requieren concretarse antes del código.

### R4. Consultas de clientes e historial

- **Objetivo:** cubrir dashboard, búsqueda, detalle e historial.
- **Requisitos:** CH-14, CH-15; FR-07, FR-08.
- **Dependencias:** R1–R3; Q-24 aprobada.
- **Cambios previstos:** `GET /customers` con búsqueda y paginación; `GET /customers/{id}`; `GET /customers/{id}/simulations`; esquemas de lectura; índices; ordenación; respuestas `404`.
- **Aceptación:** búsqueda por razón social e identificador fiscal; detalle con datos; historial ordenado; paginación; historial inmutable.
- **Pruebas:** búsqueda case-insensitive, normalización fiscal, paginación, orden, 404, aislamiento por cliente.
- **Riesgos:** búsqueda con `LIKE` poco eficiente; paginación inconsistente; exponer datos de otro cliente.
- **Auditoría/publicación:** revisión independiente de consultas y contratos de lectura.

### R5. Previsualización interactiva

- **Objetivo:** calcular sin persistir y guardar solo cuando el usuario lo solicite.
- **Requisitos:** CH-16; FR-09, FR-12.
- **Dependencias:** R2–R4; Q-25 aprobada.
- **Cambios previstos:** `POST /simulations/preview`; servicio de cálculo compartido con el guardado; contrato con cliente, usuarios, almacenamiento, llamadas y divisa; respuesta con desglose; pruebas de no persistencia.
- **Aceptación:** la previsualización no crea filas; el resultado coincide con el guardado; mover el slider no escribe en SQLite.
- **Pruebas:** paridad preview/guardado, no persistencia, 404, 422, error de divisa.
- **Riesgos:** duplicar lógica; diferencias de redondeo; llamadas excesivas desde Angular.
- **Auditoría/publicación:** revisión independiente de la paridad y de la ausencia de escrituras.

### R6. Arquitectura Angular y navegación

- **Objetivo:** crear la base del frontend y la navegación entre pantallas.
- **Requisitos:** CH-01, CH-11; CON-02, CON-11, NFR-06.
- **Dependencias:** P-01 aprobada; contratos backend estables.
- **Cambios previstos:** aplicación Angular standalone; Router; HttpClient; Signals; Reactive Forms; layout; configuración de API; proxy de desarrollo; componentes compartidos de carga, error, vacío, dinero y divisa; accesibilidad básica.
- **Aceptación:** la aplicación compila, se sirve y navega entre dashboard, alta, detalle y simulador; los tests base pasan.
- **Pruebas:** build, lint, TestBed, HttpTestingController, navegación.
- **Riesgos:** versión de Angular incompatible con Vitest; CORS; sobreingeniería de estado.
- **Auditoría/publicación:** revisión de estructura y configuración antes de añadir pantallas.

### R7. Frontend de clientes y dashboard

- **Objetivo:** registrar clientes y consultarlos desde la interfaz.
- **Requisitos:** CH-14, CH-15; FR-01, FR-07, FR-08.
- **Dependencias:** R4 y R6.
- **Cambios previstos:** dashboard con buscador; formulario reactivo de alta; tarjetas responsive; detalle; historial; estados de carga, vacío y error; mensajes de validación.
- **Aceptación:** se crea un cliente; se busca por nombre o identificador; se ve el detalle y el historial; la interfaz es usable en móvil y escritorio.
- **Pruebas:** componentes, formularios, HTTP, errores, responsive básico, accesibilidad.
- **Riesgos:** validaciones duplicadas; mala gestión de errores; tablas/cards no responsive.
- **Auditoría/publicación:** revisión de UX y accesibilidad antes del PR.

### R8. Frontend del simulador

- **Objetivo:** simular en tiempo real y guardar de forma explícita.
- **Requisitos:** CH-16; FR-09, FR-10, FR-12.
- **Dependencias:** R3, R5 y R6.
- **Cambios previstos:** slider de 0/1 a 1.000; entrada manual hasta 1.000.000; almacenamiento; llamadas API; selector de divisa; previsualización con debounce; desglose de subtotal, impuesto, total y conversión; botón de guardado; manejo de errores.
- **Aceptación:** mover el slider actualiza la proyección sin escribir; el guardado crea una simulación; el cambio de divisa se refleja en tiempo real; los errores del proveedor se muestran sin romper la pantalla.
- **Pruebas:** componente, debounce, cambio de divisa, guardado, errores, accesibilidad del slider.
- **Riesgos:** llamadas excesivas; redondeo visual distinto del backend; slider inaccesible.
- **Auditoría/publicación:** revisión de paridad visual/backend y de accesibilidad.

**Resultado TASK043:** SPEC-009 implementada localmente. Se conectaron cliente,
formulario, slider/manual, preview cancelable, monedas, guardado explícito e historial.
Vitest, E2E e integración real Angular–FastAPI–SQLite constan en el registro TASK043;
FX USD/GBP se consultó puntualmente fuera de la suite. La revisión visual fue APTA CON
OBSERVACIONES: V43-01–07 quedan abiertas para TASK044. La implementación no está
publicada, no se considera auditada independientemente y no equivale a entrega del MVP.

### R9. Integración y pruebas de extremo a extremo

- **Objetivo:** verificar el flujo completo y la facilidad de ejecución.
- **Requisitos:** CH-01, CH-12, CH-13, CH-16, CH-24; NFR-08, NFR-09.
- **Dependencias:** R1–R8.
- **Cambios previstos:** arranque conjunto; proxy/CORS; prueba E2E de alta, búsqueda, simulación y guardado; prueba de error de divisa; revisión responsive; README raíz/frontend/backend; `.env.example`; comandos de migración y pruebas.
- **Aceptación:** un evaluador sigue el README y completa el flujo; las pruebas backend y frontend pasan; el error del proveedor se maneja; no hay pasos ocultos.
- **Pruebas:** E2E, smoke manual, build de producción, revisión de accesibilidad y responsive.
- **Riesgos:** diferencias de entorno Windows; proveedor externo no disponible; documentación incompleta.
- **Auditoría/publicación:** auditoría independiente de integración y documentación antes del PR final.

### R10. Auditoría global y entrega

- **Objetivo:** revisar el cumplimiento completo y preparar la entrega.
- **Requisitos:** CH-17–CH-25; criterios de evaluación.
- **Dependencias:** R1–R9.
- **Cambios previstos:** auditoría independiente; revisión de requisitos, seguridad, deuda, pruebas y README; actualización de `ai-workspace/`; verificación de que el documento original no se ha publicado; decisión de despliegue.
- **Aceptación:** todos los requisitos están completados o explícitamente diferidos; no hay hallazgos bloqueantes; el README se ha verificado; las evidencias son reales.
- **Pruebas:** suite completa, build, smoke E2E, revisión de enlaces y documentos.
- **Riesgos:** auditoría tardía; hallazgos que obliguen a reabrir alcance; documentación de último momento.
- **Auditoría/publicación:** auditoría final independiente; el propietario decide el merge y la entrega.

## 5. Plan de ejecución consolidado

| Tarea propuesta | Fases | Alcance | PR | Esfuerzo orientativo |
| --- | --- | --- | --- | --- |
| TASK036 | R1 | Internacionalización, cero, consumos y mensual; calidad relacionada. | Sin publicación | Incremento actual |
| TASK037 | R2–R3 | Impuestos y divisas implementados localmente según SPEC-005. | Sin publicación | 411 pruebas y calidad satisfactorias |
| TASK038 | R4–R5 | Consultas e historial paginados y preview implementados localmente. | Sin publicación | 538 pruebas satisfactorias |
| TASK039 | Backend | Auditoría independiente del backend completo; APTA CON OBSERVACIONES. | Informe | Completada; 15 hallazgos no bloqueantes |
| TASK039B | Backend | Remediación autorizada A39-01/02/03/04/06, pruebas y documentación. | Sin publicación | 579 pruebas satisfactorias |
| TASK040 | Backend | Publicación controlada del backend. | PR #6 fusionado por el propietario | 579 pruebas satisfactorias |
| TASK041 | R6 | Base Angular, shell, navegación, HTTP y pruebas. | Local, sin publicación | Completada localmente |
| TASK042 | R7 | Dashboard, listado/búsqueda, alta, ficha e historial de clientes; integración UI real. | Local, sin publicación | Completada localmente; 35 unit, 12 E2E integrados |
| TASK043 | R8 | Simulador, preview/guardado explícito e historial; integración real. | Local, sin publicación | Completada localmente, APTA CON OBSERVACIONES visuales; revisión independiente pendiente |
| TASK043P | Publicación intermedia | Subsanación documental, validación, staging selectivo, commit y push autorizados. | Rama `feature/mvp-frontend` | En curso; PR/merge no autorizados |
| TASK044 | R9 | Investigar V43-01–07, corregir observaciones autorizadas y validar estabilidad/documentación. | Pendiente | Pendiente |
| TASK045 | Seguridad/dependencias | Reevaluar advisories npm, instalación limpia y autorización de scripts. | Pendiente | Pendiente |
| TASK046 | Auditoría | Auditoría independiente del MVP completo. | Pendiente | Pendiente |
| TASK047 | R10 | Entrega y despliegue según P-05. | Pendiente | Pendiente |

Numeración posterior provisional. La estimación agregada de TASK035 no es compromiso ni autorización para estas tareas.

### 5.1. Por qué no se crea una tarea por módulo

- Q-18 a Q-26 están relacionadas y pueden aprobarse en una sola revisión.
- Impuestos, divisas y previsualización comparten el mismo servicio de cálculo y el mismo snapshot histórico.
- Búsqueda, detalle e historial comparten contratos de lectura.
- Angular necesita contratos estables; separar cada pantalla en una tarea documental añadiría burocracia sin reducir riesgo.

### 5.2. Dependencias entre tareas

```text
TASK036 → TASK037 → TASK038 → TASK039 → TASK039B → TASK040 (integrado en main)
                                                           |
                                     TASK041 (base) → TASK042 (clientes) → TASK043 (simulador)
```

P-01 está resuelta para el stack base en TASK041; P-05 para despliegue y SQLite
fuera de desarrollo sigue pendiente. La nota de autorización previa ha sido sustituida:
TASK043 se completó localmente bajo autorización expresa; TASK043P prepara la publicación
intermedia y TASK044–TASK047 siguen pendientes de revisión/autorizaciones posteriores.

## 6. Estrategia de auditoría y publicación

| Momento | Auditoría | Publicación |
| --- | --- | --- |
| Antes de TASK036 | Revisión de decisiones Q-18–Q-26 y de la especificación. | Ninguna. |
| TASK036–TASK038 | Pruebas y revisión local; auditadas después en TASK039. | Sin autorización implícita. |
| TASK039 | Auditoría independiente backend; APTA CON OBSERVACIONES. | Informe. |
| TASK039B | Correcciones autorizadas y pruebas de regresión. | Sin publicación. |
| TASK040 | Autorización Git específica. | Publicación controlada; merge del propietario. |
| TASK041 | Especificación, plan, versiones compatibles y rama feature autorizada. | Base local revisable; sin staging/commit/push/PR. |
| TASK042 | Implementación local de clientes, SPEC-008 y pruebas autorizadas. | Local revisable; en aquel corte no autorizaba el inicio de TASK043 ni publicación. |
| TASK043 | Implementación local del simulador según SPEC-009; dictamen visual APTA CON OBSERVACIONES. | TASK043P autoriza publicación intermedia; sin PR/merge. |
| TASK043P | Subsanar contradicciones documentales; validar, stage, commit y push en la rama. | Commit y push autorizados; PR y merge no. |
| TASK044–TASK047 | Hallazgos visuales, instalación/dependencias, auditoría global y entrega. | Pendientes de TASK043P y de autorizaciones futuras. |

Reglas:

- La autorización para implementar no implica autorización para publicar.
- No se usa `git push --force`, `git reset --hard`, `git clean -fd` ni reescritura de historial.
- El propietario fusiona los PR personalmente.
- Cada tarea registra evidencias reales en `ai-workspace/01-tasks/`.
- Las auditorías no se presentan como validación automática ni como trabajo del implementador.

## 7. Estrategia de evaluación

| Criterio | Peso | Evidencias a producir |
| --- | --- | --- |
| Planificación y diseño | 35 % | Requisitos, matriz, ADRs, SPEC-001–009, planes, tareas y decisiones aprobadas. |
| Criterio técnico y calidad | 25 % | Arquitectura, suites ejecutadas, auditorías disponibles y riesgos registrados; auditoría independiente y seguridad formal pendientes. |
| Calidad del software | 30 % | Backend/frontend implementados y validados localmente; integración real; hallazgos V43-01–07 aún abiertos. |
| README y despliegue | 10 % | READMEs y arranque conjunto verificados; instalación npm ci limpia, CI y P-05/despliegue pendientes. |

No se fabricarán conversaciones, capturas ni resultados. TASK042/043 conservan capturas
de navegador y pruebas reales/interceptadas identificadas en sus informes; no equivalen a
auditoría formal ni a publicación.

## 8. Definición de terminado del MVP

El MVP se considera terminado cuando:

1. Un cliente español y uno internacional pueden registrarse con validación coherente.
2. Una simulación guarda usuarios, almacenamiento, llamadas, periodicidad mensual, impuesto, total y snapshot de divisa.
3. El dashboard permite buscar por razón social e identificador fiscal.
4. El detalle muestra tarjetas responsive e historial.
5. El simulador previsualiza en tiempo real sin escribir y guarda solo a petición.
6. El cambio de divisa funciona con una API pública y maneja errores.
7. Las pruebas backend y frontend pasan; no hay hallazgos bloqueantes.
8. El README permite arrancar backend y frontend en pocos pasos.
9. `ai-workspace/` contiene la trazabilidad real del proceso.
10. El documento original del reto no se ha publicado en GitHub.

## 9. Riesgos principales

| Riesgo | Impacto | Mitigación |
| --- | --- | --- |
| Detalles de impuestos/FX pendientes | Bloquean la parte afectada de TASK037. | Aprobarlos antes de implementar; no inferir propuestas TASK035. |
| Alcance internacional excesivo | Retrasa el MVP. | Lista corta de países y validación genérica. |
| Tasas fiscales inventadas o desactualizadas | Riesgo de credibilidad y legal. | Tabla aprobada, fuente y vigencia persistidas; aviso de estimación. |
| Dependencia del proveedor de divisas | Fallos de red o límites. | Caché, timeout, error `503`, pruebas con proveedor falso. |
| Duplicar cálculo en Angular | Inconsistencias. | Preview backend y una sola fuente de verdad. |
| Frontend demasiado ambicioso | Retrasa la entrega. | Componentes simples, standalone, sin estado global innecesario. |
| README desactualizado | Pérdida del 10 % de evaluación. | Verificación de pasos en R9 y R10. |
| Auditoría final tardía | Hallazgos costosos. | Auditorías intermedias en TASK036 y TASK038. |

## 10. Alcance excluido

No forman parte de esta hoja de ruta, salvo decisión expresa:

- Autenticación, JWT, roles o permisos.
- Stripe, cobros reales o facturación.
- Microservicios, Kubernetes o multitenancy.
- Facturas PDF, correos o notificaciones.
- IA integrada en la aplicación.
- Algoritmos fiscales internacionales oficiales más allá de España.
- Cargos por almacenamiento o llamadas API no definidos en el enunciado.

## 11. Siguiente paso

TASK040 está integrada en `main` tras el merge del propietario. TASK042 completó
localmente dashboard y gestión de clientes sin publicarlos. El siguiente incremento
planificado es TASK043 (simulador), sujeto a revisión y autorización específica del
propietario; esta tarea no autoriza su inicio.
