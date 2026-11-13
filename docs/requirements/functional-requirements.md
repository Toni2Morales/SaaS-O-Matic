# Requisitos funcionales — SaaS-O-Matic

| Campo | Valor |
| --- | --- |
| Versión | 0.5 (borrador para aprobación; revisión TASK010) |
| Fecha | 2026-11-13 |
| Estado | Pendiente de validación por el propietario |
| Fuente | Brief funcional proporcionado por el propietario del repositorio |

Este documento separa **requisitos funcionales**, **restricciones**, **supuestos** y **preguntas abiertas**. Todo lo que no aparece aquí como requisito no debe implementarse por iniciativa propia.

---

## 1. Requisitos funcionales

| ID | Requisito |
| --- | --- |
| FR-01 | Crear clientes con razón social, identificador fiscal, email, país y plan seleccionado. |
| FR-02 | Validar identificadores fiscales españoles (DNI/NIF/CIF) mediante sus algoritmos de comprobación. |
| FR-03 | Crear y persistir simulaciones asociadas a un cliente. |
| FR-04 | Registrar en cada simulación el número de usuarios activos, el almacenamiento contratado y las llamadas estimadas a la API. Las unidades de almacenamiento y de llamadas están pendientes de definir (ver Q-15). |
| FR-05 | Calcular el coste de usuarios mediante tramos progresivos acumulativos (ver sección 2). |
| FR-06 | Incluir en la estimación el impuesto aplicable según el país del cliente. |
| FR-07 | Ofrecer un panel de clientes con búsqueda por razón social o identificador fiscal. |
| FR-08 | Mostrar el detalle del cliente con tarjetas resumen e historial de simulaciones. |
| FR-09 | Ofrecer un simulador interactivo, incluido un control deslizante para el número de usuarios. |
| FR-10 | Mostrar conversiones de divisa (EUR como base, USD, GBP y otras divisas soportadas) usando una API pública de tipos de cambio. |
| FR-11 | Persistir, para cada simulación, el importe base en EUR, la divisa de visualización, el tipo de cambio efectivamente aplicado y la fecha y fuente del tipo de cambio cuando estén disponibles, de modo que el importe original y la conversión mostrada puedan reconstruirse. |

### Notas de interpretación

- FR-01: el "plan seleccionado" es un dato del cliente. Su catálogo, precios y efecto sobre la estimación **no están definidos** (ver Q-03).
- FR-04: almacenamiento y llamadas a la API se **registran y muestran**, pero no generan cargos (ver CON-04).
- FR-06: la tasa aplicable es configurable; la tabla de tipos y su fuente autoritativa no están definidas (ver Q-05).
- FR-11: la fecha y la fuente/proveedor del tipo de cambio se guardan cuando estén disponibles. El importe convertido es un dato derivado de estos campos y no requiere persistencia adicional para garantizar la reproducibilidad. La magnitud exacta del importe base (subtotal, subtotal con impuestos o total estimado) queda pendiente de Q-16. La obligatoriedad de la fecha y la fuente del tipo de cambio queda pendiente de Q-17.

---

## 2. Regla de negocio: tramos de usuarios

El coste se calcula por **tramos progresivos acumulativos**: cada usuario se cobra al precio del tramo en el que cae, no se aplica una tarifa plana al tramo completo.

| Tramo | Usuarios | Precio por usuario |
| --- | --- | --- |
| 1 | 1–10 | 10,00 EUR |
| 2 | 11–50 | 8,00 EUR |
| 3 | Más de 50 | 5,00 EUR |

### Ejemplos de cálculo

| Usuarios | Cálculo | Subtotal |
| --- | --- | --- |
| 1 | 1 × 10,00 | 10,00 EUR |
| 10 | 10 × 10,00 | 100,00 EUR |
| 11 | (10 × 10,00) + (1 × 8,00) | 108,00 EUR |
| 50 | (10 × 10,00) + (40 × 8,00) | 420,00 EUR |
| 51 | (10 × 10,00) + (40 × 8,00) + (1 × 5,00) | 425,00 EUR |
| 100 | (10 × 10,00) + (40 × 8,00) + (50 × 5,00) | 670,00 EUR |

### Casos límite previstos

Estos casos son candidatos a pruebas y no constituyen criterios de aceptación cerrados hasta que se apruebe la especificación correspondiente.

- Límite inferior y superior de cada tramo: 1, 10, 11, 50, 51.
- Cálculo con 0 usuarios (ver Q-02).
- Entradas negativas o no enteras: deben rechazarse en la validación.
- Importes con `Decimal` y sin errores de coma flotante. La precisión decimal y el modo de redondeo son supuestos provisionales pendientes de confirmación (ver Q-08); no se fijan dos decimales como regla aprobada.

---

## 3. Restricciones

| ID | Restricción |
| --- | --- |
| CON-01 | Backend en Python 3.13 con FastAPI, Pydantic v2, SQLAlchemy 2, SQLite y Alembic. |
| CON-02 | Frontend en Angular con TypeScript, standalone components, Signals, RxJS, Reactive Forms, Router y HttpClient. |
| CON-03 | La divisa base es EUR. |
| CON-04 | El brief no define precios de almacenamiento ni de llamadas a la API: no se inventan cargos. Solo se registran y muestran los valores introducidos. |
| CON-05 | El brief no define una tabla de impuestos ni reglas fiscales detalladas: el diseño debe permitir reglas configurables y documentar que las tasas y su fuente autoritativa están pendientes de confirmar. |
| CON-06 | La aplicación estima costes; no es un sistema de cobro ni de aprovisionamiento de suscripciones. |
| CON-07 | Autenticación, autorización, multi-tenancy, Stripe, generación de PDF y envío de correo quedan fuera de alcance salvo decisión posterior del propietario. |
| CON-08 | La API se documenta con OpenAPI. |
| CON-09 | El backend se valida con Pytest, HTTPX, Ruff y mypy. |
| CON-10 | El frontend se prueba con Vitest, sujeto a compatibilidad con la versión de Angular que se elija. |

---

## 4. Supuestos

Los siguientes puntos se asumen para poder avanzar, pero **no están confirmados** por el brief:

| ID | Supuesto |
| --- | --- |
| ASM-01 | El país del cliente determina el impuesto aplicable. |
| ASM-02 | El número de usuarios activos es un entero no negativo. El mínimo funcional (0 o 1) queda pendiente de confirmación en Q-02. |
| ASM-03 | Los tramos de precio están expresados en EUR. Como supuesto provisional, no dependen del plan contratado; esta independencia queda condicionada a la respuesta de Q-03. |
| ASM-04 | El impuesto se aplica sobre el subtotal de usuarios. |
| ASM-05 | El almacenamiento y las llamadas a la API se muestran como datos informativos, sin importe asociado. |
| ASM-06 | Las conversiones de divisa son informativas y no alteran el importe base persistido en EUR. La magnitud exacta de ese importe base se decide en Q-16. |
| ASM-07 | Los identificadores fiscales admitidos en esta fase son españoles (DNI/NIF/CIF). |

---

## 5. Preguntas abiertas

| ID | Pregunta | Impacto |
| --- | --- | --- |
| Q-01 | ¿Qué catálogo de países debe soportarse y cómo se relaciona cada país con su impuesto? | Modelo de datos y FR-06 |
| Q-02 | ¿Se permite una simulación con 0 usuarios o se exige un mínimo de 1? | Validación y casos límite |
| Q-03 | ¿Qué planes existen y qué efectos tienen sobre precios, límites o funcionalidades? | Modelo de datos y FR-01 |
| Q-04 | ¿Debe soportarse NIE además de DNI/NIF/CIF? | Validación FR-02 |
| Q-05 | ¿Cuál es la fuente autoritativa de los tipos impositivos y con qué vigencia temporal? | FR-06 y CON-05 |
| Q-06 | ¿Qué proveedor público de tipos de cambio se usará y con qué frecuencia de actualización? | FR-10 |
| Q-07 | ¿Qué divisas adicionales deben soportarse además de EUR, USD y GBP? | FR-10 |
| Q-08 | ¿Qué precisión decimal y qué ámbito y modo de redondeo deben aplicarse a los importes (por línea, por subtotal o en el total)? | Cálculo y persistencia |
| Q-09 | ¿El historial de simulaciones debe ser inmutable o editable? | Modelo y API |
| Q-10 | ¿Se requiere exportación de la estimación (CSV, PDF, etc.)? | Fuera de alcance actual |
| Q-11 | ¿Debe mantenerse una caché o archivo histórico de tipos de cambio para reutilizarlos en futuras simulaciones cuando el proveedor no esté disponible, además de la tasa aplicada que FR-11 ya persiste por simulación? | FR-11 y persistencia |
| Q-12 | ¿Existe un límite máximo de usuarios, almacenamiento o llamadas por simulación? ¿Qué rango y qué paso debe tener el control deslizante de usuarios? | Validación y FR-09 |
| Q-13 | ¿Qué reglas de validación debe cumplir el email del cliente? | FR-01 y validación |
| Q-14 | ¿Deben ser únicos el identificador fiscal y/o la razón social? ¿La unicidad sería global o por país? | FR-01, modelo de datos y API |
| Q-15 | ¿En qué unidades deben registrarse el almacenamiento contratado y las llamadas estimadas a la API? ¿Se expresan por periodo? | FR-04 y modelo de datos |
| Q-16 | ¿Qué magnitud económica debe convertirse y persistirse como importe base en EUR: el subtotal de usuarios, el subtotal con impuestos o el total estimado? | FR-06, FR-11 y modelo de datos |
| Q-17 | ¿Deben ser obligatorias la fecha y la fuente del tipo de cambio aplicado a cada simulación, o se permite persistirlas como desconocidas cuando el proveedor no las facilite? | FR-11 y trazabilidad de las conversiones |

Ninguna de estas preguntas debe resolverse por inferencia durante la implementación. Si una tarea depende de ellas, se detiene y se consulta al propietario.

---

## 6. Requisitos no funcionales propuestos

Estos requisitos son **propuestas técnicas** alineadas con el stack aprobado; requieren confirmación:

| ID | Propuesta |
| --- | --- |
| NFR-01 | Cobertura de pruebas prioritaria en el dominio (cálculo de tramos, impuestos y validación fiscal). |
| NFR-02 | API versionada (`/api/v1`) con errores en formato `application/problem+json`. |
| NFR-03 | Migraciones Alembic versionadas y verificadas en pruebas de integración. |
| NFR-04 | mypy en modo estricto al menos para el dominio. |
| NFR-05 | Registro de decisiones relevantes en ADRs. |
