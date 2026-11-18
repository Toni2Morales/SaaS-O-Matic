# Requisitos funcionales — SaaS-O-Matic

| Campo | Valor |
| --- | --- |
| Versión | 1.3 (TASK039B) |
| Fecha | 2026-11-18 |
| Estado | Componentes backend del alcance MVP implementados localmente y auditados en TASK039; correcciones TASK039B aplicadas; sin publicación; frontend y despliegue pendientes. |
| Fuente | Enunciado original del reto facilitado por el propietario (documento externo no versionado) y brief funcional del propietario |

Este documento separa **requisitos funcionales**, **restricciones**, **supuestos** y **preguntas abiertas**. Todo lo que no aparece aquí como requisito no debe implementarse por iniciativa propia.

El enunciado original del reto es la referencia principal del alcance. El documento se conserva fuera de Git y no se incorpora al repositorio. La reconciliación completa entre el enunciado, los requisitos internos, la implementación y las evidencias está en [`requirements-traceability.md`](requirements-traceability.md). La planificación propuesta está en [`../planning/mvp-roadmap.md`](../planning/mvp-roadmap.md).

---

## Decisiones vigentes TASK036 (sustituyen propuestas TASK035)

Q-18: mensual persistido y fijado por servidor. Q-19 sustituye Q-02/PP-Q-01:
usuarios enteros no negativos, sin máximo de dominio; API 0..1.000.000;
slider futuro 0..1.000 con entrada manual hasta 1.000.000 (Q-12/SIM-P09).
Q-20: ES/PT/FR/DE/IT/NL, validación oficial solo ES, genérica fuera de ES,
unicidad por país. Q-21: consumos estrictos obligatorios nuevos, NULL históricos,
GB 0..1.000.000 y llamadas mensuales 0..1.000.000.000; sin cargos.
Q-26: simulaciones con `extra="forbid"`, no clientes.
Q-22/Q-23 vigentes TASK037: seis tipos generales contrastados oficialmente,
catálogo versionado, ROUND_HALF_UP a céntimos. Frankfurter v2 verificado como único
proveedor, EUR/USD/GBP, TTL 24 h desde obtención y timeout 5 s. EUR identidad sin red.
Q-16: base conversión = total EUR con impuestos. Q-17/SIM-P14: snapshot fiscal y
FX exacto con fechas/fuentes/versionado; históricos desconocidos NULL, sin backfill.
Véanse [SPEC-005](../specs/005-taxes-and-currency-conversion/spec.md) y sus fuentes.
Q-09/Q-24/Q-25 y SIM-P10/SIM-P11 vigentes TASK038: listado/búsqueda/detalle e
historial inmutable con limit20/máximo100/offset, orden estable y NULL históricos;
preview sin escrituras con mismo cálculo de guardado. Contratos en
[SPEC-006](../specs/006-customer-queries-and-preview/spec.md).
P-01/P-05 siguen pendientes para frontend/despliegue.
Contrato y reglas genéricas exactas: [SPEC-004](../specs/004-international-customers-and-simulations/spec.md).

## 1. Requisitos funcionales

| ID | Requisito |
| --- | --- |
| FR-01 | Crear clientes con razón social, identificador fiscal, email, país y plan seleccionado. |
| FR-02 | Validar identificadores fiscales españoles (DNI/NIF/CIF/NIE) mediante sus algoritmos de comprobación. |
| FR-03 | Crear y persistir simulaciones asociadas a un cliente registrado. |
| FR-04 | Registrar usuarios activos, almacenamiento en GB (0..1.000.000) y llamadas API mensuales (0..1.000.000.000), enteros estrictos. Consumos obligatorios nuevos y NULL históricos, sin cargos adicionales. |
| FR-05 | Calcular el coste de usuarios mediante tramos progresivos acumulativos (ver sección 2). |
| FR-06 | Incluir en la estimación el impuesto aplicable según el país del cliente. |
| FR-07 | Ofrecer un panel de clientes con búsqueda por razón social o identificador fiscal. |
| FR-08 | Mostrar el detalle del cliente con tarjetas resumen e historial de simulaciones. |
| FR-09 | Ofrecer un simulador interactivo, incluido un control deslizante para el número de usuarios y la previsualización sin persistencia. |
| FR-10 | Mostrar conversiones de divisa (EUR como base, USD, GBP y otras divisas soportadas) usando una API pública de tipos de cambio. |
| FR-11 | Persistir, para cada simulación, el importe base en EUR, la divisa de visualización, el tipo de cambio efectivamente aplicado y la fecha y fuente del tipo de cambio cuando estén disponibles, de modo que el importe original y la conversión mostrada puedan reconstruirse. |
| FR-12 | Estimaciones mensuales con `billing_period="monthly"` fijado por servidor, devuelto y persistido; etiqueta de UI futura. |

### Notas de interpretación

- FR-01: el "plan seleccionado" es un dato obligatorio del cliente. El catálogo del MVP aprobado en D-02 contiene únicamente `standard`; no existen precios ni prestaciones adicionales asociados al plan, no modifica los tramos progresivos de usuarios y no se introducirán otros planes sin una decisión posterior. La razón social se recorta, no puede quedar vacía y debe tener entre 1 y 255 caracteres después del recorte (D-15).
- FR-02: DNI/NIF, CIF/NIF y NIE conforme a D-03; algoritmos solo en ES. PT/FR/DE/IT/NL usan validación genérica de SPEC-004, no fiscal oficial.
- FR-04: GB y llamadas mensuales aprobados en Q-21; se registran sin cargos.
- FR-06: tipos generales ES21/PT23/FR20/DE19/IT22/NL21 verificados; catálogo versionado, impuesto HALF_UP a céntimos. Sin regímenes especiales ni asesoramiento tributario; fecha efectiva desconocida NULL.
- FR-09: la previsualización se calcula sin persistencia. El guardado es una acción explícita; cada movimiento del control deslizante no debe crear registros (Q-25).
- FR-10/FR-11: EUR base, USD/GBP, Frankfurter v2 de referencia (no continuo), caché 24 h y timeout 5 s; conversión del total con IVA. Snapshot persiste también resultado convertido; no altera EUR.
- FR-12: periodicidad mensual explícita en contrato y persistencia desde TASK036.

---

## 2. Regla de negocio: tramos de usuarios

El coste se calcula por **tramos progresivos acumulativos**: cada usuario se cobra al precio del tramo en el que cae, no se aplica una tarifa plana al tramo completo.

| Tramo | Usuarios | Precio por usuario |
| --- | --- | --- |
| 1 | 1–10 | 10,00 EUR |
| 2 | 11–50 | 8,00 EUR |
| 3 | Más de 50 | 5,00 EUR |

> Q-19 aprobada en TASK036 sustituye Q-02/PP-Q-01: cero usuarios produce exactamente `Decimal("0.00")`. Las tarifas y los límites de unidades facturadas no cambian.

### Ejemplos de cálculo

| Usuarios | Cálculo | Subtotal |
| --- | --- | --- |
| 0 | Sin usuarios | 0,00 EUR |
| 1 | 1 × 10,00 | 10,00 EUR |
| 10 | 10 × 10,00 | 100,00 EUR |
| 11 | (10 × 10,00) + (1 × 8,00) | 108,00 EUR |
| 15 | (10 × 10,00) + (5 × 8,00) | 140,00 EUR |
| 50 | (10 × 10,00) + (40 × 8,00) | 420,00 EUR |
| 51 | (10 × 10,00) + (40 × 8,00) + (1 × 5,00) | 425,00 EUR |
| 100 | (10 × 10,00) + (40 × 8,00) + (50 × 5,00) | 670,00 EUR |

El ejemplo de 15 usuarios coincide con el enunciado y tiene pruebas dedicadas desde TASK036.

### Casos límite previstos

- Límite inferior y superior de cada tramo: 1, 10, 11, 50, 51.
- Cero usuarios admitido con subtotal exacto 0.00; negativos y tipos no enteros rechazados.
- Entradas negativas o no enteras: deben rechazarse en la validación.
- Importes con `Decimal` exacto en EUR, sin `float`; no se aplica redondeo de negocio en el cálculo del subtotal. La serialización HTTP se resolvió en SPEC-003 como cadena decimal exacta (Q-08).

---

## 3. Restricciones

| ID | Restricción |
| --- | --- |
| CON-01 | Backend en Python 3.13 con FastAPI, Pydantic v2, SQLAlchemy 2, SQLite y Alembic. |
| CON-02 | Frontend en Angular con TypeScript, standalone components, Signals, RxJS, Reactive Forms, Router y HttpClient. |
| CON-03 | La divisa base es EUR. |
| CON-04 | El brief no define precios de almacenamiento ni de llamadas a la API: no se inventan cargos. Solo se registran y muestran los valores introducidos. |
| CON-05 | El brief no define reglas fiscales detalladas. Tabla general de seis países y fuentes resueltas en TASK037/SPEC-005; cualquier ampliación requiere aprobación y verificación, sin inventar reglas. |
| CON-06 | La aplicación estima costes; no es un sistema de cobro ni de aprovisionamiento de suscripciones. |
| CON-07 | Autenticación, autorización, multi-tenancy, Stripe, generación de PDF y envío de correo quedan fuera de alcance salvo decisión posterior del propietario. |
| CON-08 | La API se documenta con OpenAPI. |
| CON-09 | El backend se valida con Pytest, HTTPX, Ruff y mypy. |
| CON-10 | El frontend se prueba con Vitest, sujeto a compatibilidad con la versión de Angular que se elija. |
| CON-11 | La interfaz debe ser responsive, accesible de forma básica y mostrar estados de carga, vacío y error. |
| CON-12 | La entrega debe incluir el directorio `ai-workspace/` con planificación, arquitectura, evidencias del proceso asistido por IA y resultados de calidad. |
| CON-13 | El README debe permitir ejecutar backend y frontend en pocos pasos, con variables de entorno y migraciones documentadas. |
| CON-14 | El documento original del reto no se versiona en el repositorio; se cita como fuente externa y no se publica en GitHub. |

---

## 4. Supuestos

Los siguientes supuestos proceden del brief original; las decisiones posteriores
de las secciones anteriores y SPEC-004/005/006 prevalecen cuando los confirman o sustituyen:

| ID | Supuesto |
| --- | --- |
| ASM-01 | El país del cliente determina el impuesto aplicable. |
| ASM-02 | Sustituido por Q-19: entero no negativo, sin máximo comercial de dominio. |
| ASM-03 | Los tramos de precio están expresados en EUR. No dependen del plan contratado; esta independencia queda confirmada por D-02. |
| ASM-04 | El impuesto se aplica sobre el subtotal de usuarios. |
| ASM-05 | El almacenamiento y las llamadas a la API se muestran como datos informativos, sin importe asociado. |
| ASM-06 | Las conversiones de divisa son informativas y no alteran el importe base persistido en EUR. |
| ASM-07 | Sustituido por Q-20: ES algorítmico; PT/FR/DE/IT/NL genérico sin validación oficial. |
| ASM-08 | Las estimaciones representan un coste mensual, conforme al enunciado original y a FR-12. |
| ASM-09 | La fuente de tipos de cambio es una API pública de referencia, no una fuente de mercado en tiempo real ni una garantía contractual. |

---

## 5. Preguntas abiertas

| ID | Pregunta | Estado / impacto |
| --- | --- | --- |
| Q-01 | Países e impuesto | Resuelta para seis países en Q-20/Q-22/SPEC-005; no países adicionales. |
| Q-02 | ¿Se admite 0 usuarios? | Sí; Q-19/TASK036 sustituye el mínimo previo. |
| Q-03 | ¿Qué planes existen y qué efectos tienen sobre precios, límites o funcionalidades? | Resuelta por D-02 en TASK020. |
| Q-04 | ¿Debe soportarse NIE además de DNI/NIF/CIF? | Resuelta por D-03: sí. |
| Q-05 | Fuente fiscal y vigencia | Resuelta alcance TASK037: fuentes oficiales nacionales/UE, fecha consulta 2026-11-17, fecha efectiva NULL si no verificada. Sin actualización automática fiscal. |
| Q-06 | Proveedor y actualización | Frankfurter v2, referencia publicada una o varias veces al día; no tiempo real continuo; caché 24 h desde obtención. |
| Q-07 | Divisas | EUR/USD/GBP iniciales; otras fuera del alcance aprobado. |
| Q-08 | Representación monetaria HTTP | Cadenas exactas; importes a dos decimales, tasas con precisión original; impuesto/FX HALF_UP (SPEC-005). |
| Q-09 | ¿El historial de simulaciones debe ser inmutable o editable? | Inmutable por API, implementado TASK038; no edición ni borrado. |
| Q-10 | ¿Se requiere exportación de la estimación (CSV, PDF, etc.)? | Fuera de alcance actual. |
| Q-11 | Caché y resiliencia | Memoria 24 h por proceso, solo éxitos; no servir expirados ni reutilizar snapshots como fallback. Sin tasa válida: 503; EUR sigue operativo. |
| Q-12 | ¿Qué límites de usuarios aplican en API y UI? | Dominio 0+ sin máximo comercial; API 0..1.000.000; slider 0..1.000 y entrada manual hasta 1.000.000. |
| Q-13 | ¿Qué reglas de validación debe cumplir el email del cliente? | Resuelta en SPEC-001: `EmailStr` de Pydantic. |
| Q-14 | ¿Deben ser únicos el identificador fiscal y/o la razón social? ¿La unicidad sería global o por país? | Resuelta por D-05/D-06: identificador fiscal único por país; razón social no única. |
| Q-15 | ¿En qué unidades deben registrarse el almacenamiento contratado y las llamadas estimadas a la API? ¿Se expresan por periodo? | Resuelta por Q-21: GB y llamadas mensuales. |
| Q-16 | Importe base de conversión | Total EUR con impuesto; resultado convertido también persistido (TASK037). |
| Q-17 | Fecha y fuente de conversión | Obligatorias para USD/GBP; EUR source identity, tasa 1 y fecha de publicación NULL; obtención UTC registrada. |
| Q-18 | Periodicidad mensual | Aprobada e implementada localmente TASK036. |
| Q-19 | Cero usuarios | Aprobada e implementada localmente TASK036; sustituye Q-02/PP-Q-01. |
| Q-20 | Países | Aprobada e implementada localmente TASK036; seis países, ES algorítmico. |
| Q-21 | Consumos | Aprobada e implementada localmente TASK036. |
| Q-22 | Impuestos | Verificados e implementados localmente; general por país, snapshot y HALF_UP; véase SPEC-005. |
| Q-23 | Divisas | Frankfurter v2 verificado e implementado; EUR/USD/GBP, TTL24h, timeout5s, tasas exactas y snapshot. |
| Q-24 | Consultas e historial | Implementado TASK038: tres GET, paginación20/100/offset, búsqueda Unicode casefold y orden estable; NULL históricos sin backfill. |
| Q-25 | Previsualización | POST /simulations/preview implementado sin escrituras, mismo cuerpo y CalculateSimulation/MonthlyEstimator; guardado explícito. |
| Q-26 | Campos desconocidos | Simulaciones `extra="forbid"` implementado; clientes sin cambios. |

### 5.1 Decisiones de negocio aprobadas

| ID | Decisión |
| --- | --- |
| D-02 | El catálogo de planes del MVP contiene únicamente `standard`. El campo `plan` es obligatorio y no tiene valor por defecto. Cualquier otro valor se rechaza. No existen precios ni prestaciones adicionales asociados al plan, no modifica los tramos progresivos de precio por número de usuarios y no se introducirán otros planes sin una decisión posterior. |
| D-15 | `legal_name` es obligatorio. Eliminar espacios iniciales y finales con `strip()`; rechazar cadenas vacías o compuestas únicamente por espacios; aceptar entre 1 y 255 caracteres después del recorte; conservar los espacios interiores; persistir y devolver el valor normalizado. |

### 5.2 Decisiones de implementación consolidadas

Estas decisiones ya fueron aprobadas o registradas en las especificaciones y tareas indicadas. No convierten en completos los requisitos que aún dependen de frontend, impuestos, divisas o lectura de datos.

| Decisión | Estado | Referencia |
| --- | --- | --- |
| Representación monetaria HTTP como cadena decimal exacta | Aprobada | Q-08, SPEC-003 |
| Máximo técnico de API de 1.000.000 de usuarios | Aprobada | Q-12, SPEC-003 |
| Slider de 0 a 1.000, entrada manual hasta 1.000.000 | Aprobada | Q-12/SIM-P09, TASK036 |
| Persistencia de simulaciones | Aprobada | SIM-P01, SPEC-003 |
| Cliente registrado obligatorio | Aprobada | SIM-P02, SPEC-003 |
| HTTP 404 para cliente inexistente | Aprobada | SIM-P15, SPEC-003 |
| Texto decimal canónico en SQLite | Aprobada | SIM-P13, SPEC-003 |
| API sin prefijo de versión | Aprobada | SIM-P09, SPEC-003 |
| Alcance parcial del primer incremento de simulaciones | Aprobada | SPEC-003 |

### 5.3 Propuestas de TASK035 (no constituyen decisiones vigentes)

| ID | Recomendación | Justificación |
| --- | --- | --- |
| Q-18 | Hacer explícita la periodicidad mensual en la UI y en el contrato; persistir `billing_period = "monthly"` en la siguiente migración. | Evita ambigüedad histórica y no altera el algoritmo de precios. |
| Q-19 | Permitir 0 usuarios con subtotal `0.00` en previsualización y simulación; mantener el rechazo de negativos y no enteros. | El enunciado original empieza en 0; es una ampliación de validación, no del algoritmo. Requiere revisar Q-02/PP-Q-01. |
| Q-20 | Soportar ES, PT, FR, DE, IT y NL; ISO 3166-1 alfa-2; algoritmo oficial solo para ES; validación genérica normalizada para el resto; unicidad `(country, tax_id)`. | Demuestra internacionalización sin inventar algoritmos fiscales. |
| Q-21 | `storage_gb` entero 0..1.000.000; `api_calls_per_month` entero 0..1.000.000.000; obligatorios en altas nuevas y nulos en registros históricos. | Unidades simples, sin cargos inventados y sin falsear datos antiguos. |
| Q-22 | Tabla estática versionada de tasas aprobadas; tasa como decimal exacto en texto; base = subtotal; `ROUND_HALF_UP` a 2 decimales; persistir tasa, fuente, vigencia, impuesto y total; sin API fiscal externa. Fuentes propuestas: AEAT para España y Comisión Europea (VAT rates) para países UE; los valores concretos los aprueba el propietario. | Sencillo, verificable y reproducible; no se inventan tasas. |
| Q-23 | `open.er-api.com` como proveedor principal, caché de 24 h, timeout de 5 s, EUR/USD/GBP mínimo, proxy backend y persistencia de divisa, tasa, fecha, fuente e importe convertido. Frankfurter como alternativa. | Cumple el requisito, evita CORS y permite reproducibilidad; atribución visible. |
| Q-24 | `GET /customers` con búsqueda, `GET /customers/{id}` y `GET /customers/{id}/simulations`; paginación offset 20/100; orden configurable; historial inmutable; sin edición ni borrado. | Cubre dashboard, detalle e historial sin complejidad innecesaria. |
| Q-25 | `POST /simulations/preview` sin persistencia, con `customer_id`, usuarios, almacenamiento, llamadas y divisa; reutiliza el mismo servicio de cálculo; guardado explícito. | Evita escrituras por cada movimiento del slider y duplicar lógica en Angular. |
| Q-26 | `extra="forbid"` en simulación y previsualización; documentar el cambio como ruptura interna antes del frontend. | Evita ignorar campos comerciales desconocidos y mejora la detección de errores. |

La tabla conserva propuestas TASK035, no las aprueba por sí misma. Decisiones vigentes al inicio y en SPEC-005/006: Frankfurter, caché24h, HALF_UP y paginación20/100/offset; no open.er-api.com ni ordenación configurable por el usuario.

---

## 6. Requisitos no funcionales propuestos

Estos requisitos son **propuestas técnicas** alineadas con el stack aprobado; requieren confirmación:

| ID | Propuesta |
| --- | --- |
| NFR-01 | Cobertura de pruebas prioritaria en el dominio (cálculo de tramos, impuestos y validación fiscal). |
| NFR-02 | API documentada con OpenAPI y errores en formato `application/problem+json`. El MVP actual no usa prefijo `/api/v1` (decisión SIM-P09); cualquier versionado futuro requiere decisión. |
| NFR-03 | Migraciones Alembic versionadas y verificadas en pruebas de integración. |
| NFR-04 | mypy en modo estricto al menos para el dominio. |
| NFR-05 | Registro de decisiones relevantes en ADRs. |
| NFR-06 | Interfaz responsive, con estados de carga, vacío y error, y accesibilidad básica (etiquetas, foco, teclado y contraste). |
| NFR-07 | Los errores de la API no exponen trazas internas ni datos sensibles. |
| NFR-08 | La integración con la API pública de divisas tiene timeout, caché, manejo de errores y pruebas con un proveedor falso. |
| NFR-09 | El README raíz, el README de backend y el README de frontend permiten ejecutar el sistema en local con pasos verificables. |
| NFR-10 | La entrega incluye evidencias reales de pruebas, auditorías y revisiones humanas; no se fabrican conversaciones ni resultados. |

---

## 7. Estado actual de implementación

La distinción entre backend y extremo a extremo es deliberada. Ningún requisito que necesite frontend o integración se declara completado.

| Requisito | Backend | Extremo a extremo | Observación |
| --- | --- | --- | --- |
| FR-01 | Completado localmente | Pendiente | Seis países y único plan `standard`. |
| FR-02 | Completado localmente | Pendiente | Algoritmos ES intactos; resto genérico no oficial. |
| FR-03 | Completado backend local | Pendiente | Consumos, mensual, snapshot y lectura histórica inmutable. |
| FR-04 | Completado localmente | Pendiente | Usuarios, GB y llamadas mensuales; históricos NULL. |
| FR-05 | Completado localmente | Pendiente | Cero admitido; tarifas intactas. |
| FR-06 | Completado localmente en alcance simplificado | Pendiente | IVA general de seis países; no regímenes especiales. |
| FR-07 | Completado backend local | Pendiente | Listado/búsqueda Unicode paginados; dashboard visual pendiente. |
| FR-08 | Completado backend local | Pendiente | Detalle e historial inmutable con NULL; tarjetas responsive pendientes. |
| FR-09 | Completado backend local | Pendiente | Preview sin persistencia y guardado explícito; slider/formulario Angular pendiente. |
| FR-10 | Completado backend local | Pendiente | EUR/USD/GBP, API pública y caché; UI pendiente. |
| FR-11 | Completado localmente | Pendiente | Snapshot exacto impuesto/total/FX; históricos desconocidos NULL. |
| FR-12 | Completado localmente | Pendiente | Mensual explícito; UI pendiente. |

### 7.1 Estado técnico verificado

- Backend FastAPI con health/OpenAPI, creación de clientes/simulaciones, GET /customers, GET /customers/{customer_id}, GET /customers/{customer_id}/simulations y POST /simulations/preview.
- SQLite con migraciones Alembic para clientes y simulaciones.
- 240 pruebas automatizadas superadas en TASK034, además de Ruff, Ruff format, mypy y `pip check`.
- TASK036: 340 pruebas superadas localmente; Ruff/formato/mypy/pip check correctos, 35 pines sin cambios. Sin publicación.
- TASK037: 411 pruebas superadas; Ruff/formato/mypy/pip check correctos; 35 pines intactos. Fuentes y smoke Frankfurter reales separados de la suite offline.
- TASK038: 538 pruebas superadas localmente, sin migraciones ni dependencias nuevas; flujo completo backend y ausencia de DML en preview probados.
- TASK039: auditoría del backend acumulado con dictamen APTA CON OBSERVACIONES; 15 hallazgos, ninguno bloqueante.
- TASK039B: correcciones autorizadas A39-01/02/03/04/06 y documentación de A39-05; 579 pruebas superadas, Ruff/formato/mypy/pip check correctos, 35 pines sin cambios. Sin publicación.
- No existe frontend Angular, no hay CI y no hay despliegue.
- El PR #5 fue fusionado por el propietario en `b3c5ca81d23d279b478ed466757bada031aa1e1e`.
- La auditoría TASK033 emitió veredicto **APTA CON OBSERVACIONES**, sin hallazgos críticos, altos, medios ni bloqueantes.

---

## 8. Alcance excluido

El enunciado original no exige y el MVP no debe incorporar sin una decisión expresa:

- Autenticación, JWT, roles o permisos.
- Stripe, cobros reales, facturación o conciliación de pagos.
- Microservicios, Kubernetes o infraestructura distribuida.
- Facturas PDF, envío de correos o notificaciones.
- Multitenancy.
- IA integrada en la aplicación.
- Aprovisionamiento de suscripciones o integración con proveedores SaaS.
- Algoritmos fiscales internacionales oficiales más allá de España.
- Cargos por almacenamiento o llamadas API no definidos en el enunciado.

Las recomendaciones opcionales de la hoja de ruta no se convierten en requisitos obligatorios por el hecho de aparecer en este documento.

---

## 9. Trazabilidad y planificación

- Matriz completa del reto: [`requirements-traceability.md`](requirements-traceability.md).
- Hoja de ruta optimizada: [`../planning/mvp-roadmap.md`](../planning/mvp-roadmap.md).
- Especificaciones: [`SPEC-001`](../specs/001-customer-registration/spec.md), [`SPEC-002`](../specs/002-progressive-pricing/spec.md) y [`SPEC-003`](../specs/003-simulations/spec.md).
- Registro de tareas y auditorías: [`ai-workspace/README.md`](../../ai-workspace/README.md).

## 10. Historial de cambios

| Versión | Fecha | Cambio |
| --- | --- | --- |
| 0.8 | 2026-11-16 | Revisión TASK027; Q-02, Q-08 y Q-12 registradas. |
| 0.9 | 2026-11-17 | Reconciliación TASK035: FR-12, estado actual, Q-18 a Q-26, NFR-02 corregida, alcance excluido y enlaces de trazabilidad. |
| 1.0 | 2026-11-17 | TASK036: aprobaciones delimitadas, internacionalización, cero, consumos, mensual y forbid; SPEC-004; impuestos/divisas futuros sin detalles inferidos. |
| 1.1 | 2026-11-17 | TASK037: IVA general verificado, Frankfurter v2 único, caché y snapshot fiscal/FX; Q-16/Q-17/SIM-P14; SPEC-005. |
| 1.2 | 2026-11-18 | TASK038: Q-09/Q-24/Q-25/SIM-P10/SIM-P11, consultas paginadas Unicode, historial y preview; FR-07/08/09 backend, no UI. |
| 1.3 | 2026-11-18 | TASK039/TASK039B: auditoría APTA CON OBSERVACIONES, correcciones autorizadas, SQLite compartido y límites FX; 579 pruebas. |
