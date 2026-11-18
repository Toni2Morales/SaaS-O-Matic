# TASK035 — Reconciliación de requisitos y planificación final del MVP

| Campo | Valor |
| --- | --- |
| ID | TASK035 |
| Título | Reconciliación de requisitos y planificación final del MVP |
| Estado | Completada (análisis y documentación); sin implementación ni publicación |
| Fecha | 2026-11-17 |
| Rama | `docs/mvp-reconciliation` |
| Base | `origin/main` en `b3c5ca81d23d279b478ed466757bada031aa1e1e` (PR #5 fusionado) |
| Autorización Git | Sin autorización de `git add`, commit, push, PR ni merge |
| Documento original | Enunciado del reto facilitado por el propietario; conservado fuera de Git y no publicado en GitHub |

## 1. Objetivo y alcance

Reconciliar el estado actual de SaaS-O-Matic con el enunciado original del reto, actualizar los requisitos globales y establecer una hoja de ruta optimizada hasta la entrega final del MVP.

La tarea es exclusivamente analítica y documental:

- No implementa funcionalidades.
- No modifica código fuente, pruebas, configuración, dependencias, migraciones ni `LICENSE`.
- No crea TASK036.
- No ejecuta `git add`, commit, push, creación de PR, merge, rebase ni operaciones destructivas.
- No publica el documento original del reto.

## 2. Estado Git

### 2.1. Estado inicial

- Rama inicial: `feature/simulations`.
- HEAD inicial: `3629843881d5ade962b2d1a287b49e98d35b89b0`.
- `origin/main` tras `git fetch origin`: `b3c5ca81d23d279b478ed466757bada031aa1e1e`.
- `main` local: `8371f9f608ce6e06984cc501d8240e1b7edf34d5`; no se modificó.
- Sin archivos staged.
- Único archivo no seguido: `Prueba Devs con IA.docx`.
- PR #5 verificado como `MERGED`, con merge commit `b3c5ca81d23d279b478ed466757bada031aa1e1e`.

### 2.2. Estado final

- Rama: `docs/mvp-reconciliation`, creada desde `origin/main`.
- HEAD: `b3c5ca81d23d279b478ed466757bada031aa1e1e`.
- Sin archivos staged.
- El documento original sigue sin seguimiento y no se ha añadido a Git.
- Los cambios de esta tarea son únicamente documentales.

## 3. Fuentes consultadas

- Enunciado original del reto, extraído del `.docx` local sin incorporarlo al repositorio.
- `AGENTS.md`.
- `README.md` raíz y `backend/README.md`.
- `docs/requirements/functional-requirements.md`.
- `docs/adr/0001-technology-stack.md` y `docs/adr/0002-architecture.md`.
- `docs/assessment/001-repository-assessment.md`.
- `docs/process/ai-assisted-development.md`.
- `docs/specs/001-customer-registration/spec.md`, `plan.md` y `tasks.md`.
- `docs/specs/002-progressive-pricing/spec.md`, `plan.md` y `tasks.md`.
- `docs/specs/003-simulations/spec.md`, `plan.md` y `tasks.md`.
- `ai-workspace/README.md`, `ai-workspace/00-project-context/` y registros TASK001–TASK032.
- Código y pruebas actuales del backend en modo lectura.
- PR #5 y su commit de merge.

## 4. Archivos creados y modificados

### 4.1. Creados

- `docs/requirements/requirements-traceability.md`.
- `docs/planning/mvp-roadmap.md`.
- `ai-workspace/01-tasks/TASK035-mvp-reconciliation.md`.

### 4.2. Modificados

- `docs/requirements/functional-requirements.md`.
- `docs/specs/001-customer-registration/spec.md`.
- `docs/specs/001-customer-registration/plan.md`.
- `docs/specs/001-customer-registration/tasks.md`.
- `docs/specs/002-progressive-pricing/spec.md`.
- `docs/specs/002-progressive-pricing/plan.md`.
- `docs/specs/002-progressive-pricing/tasks.md`.
- `docs/specs/003-simulations/spec.md`.
- `docs/specs/003-simulations/plan.md`.
- `docs/specs/003-simulations/tasks.md`.
- `ai-workspace/README.md`.
- `README.md`.

No se modificaron archivos de código, pruebas, configuración, dependencias, migraciones ni `LICENSE`.

## 5. Matriz de cumplimiento del reto

La matriz completa está en [`docs/requirements/requirements-traceability.md`](../../docs/requirements/requirements-traceability.md).

Resumen:

| Estado | Requisitos del reto |
| --- | --- |
| Completado en backend | CH-02, CH-03, CH-05 (España), CH-17, CH-18, CH-19 |
| Parcial | CH-01, CH-04, CH-06, CH-07, CH-08, CH-09, CH-20, CH-21, CH-22, CH-23, CH-24, CH-25 |
| Pendiente | CH-10, CH-11, CH-12, CH-13, CH-14, CH-15, CH-16 |
| Pendiente de decisión | Q-18 a Q-26; P-01 y P-05 |
| Fuera de alcance | Autenticación, JWT, roles, Stripe, microservicios, Kubernetes, PDF, correos, multitenancy e IA integrada |

Ningún requisito que dependa de frontend o integración se declara completado.

## 6. Discrepancias detectadas

| ID | Discrepancia | Decisión |
| --- | --- | --- |
| DISC-01 | El enunciado dice «coste mensual»; el contrato actual no tiene periodicidad. | Q-18 |
| DISC-02 | El primer tramo original empieza en 0; Q-02 aprobó mínimo 1. | Q-19 |
| DISC-03 | El enunciado admite país; la implementación solo acepta `ES`. | Q-20 |
| DISC-04 | El enunciado pide almacenamiento y llamadas API; el contrato solo acepta usuarios. | Q-21 |
| DISC-05 | El enunciado pide impuesto por país; no hay tasas aprobadas. | Q-22 |
| DISC-06 | El enunciado pide API pública de divisas y cambio dinámico; no hay integración. | Q-23 |
| DISC-07 | El enunciado pide buscador, detalle e historial; solo existe alta. | Q-24 |
| DISC-08 | El enunciado pide proyección en tiempo real; el único endpoint persiste. | Q-25 |
| DISC-09 | El contrato de simulación ignora campos desconocidos. | Q-26 |
| DISC-10 | No existe frontend Angular. | P-01 |
| DISC-11 | README raíz y backend están desactualizados. | TASK035 / TASK036 |
| DISC-12 | NFR-02 mencionaba `/api/v1`; la API aprobada no usa prefijo. | Corregido en requisitos 0.9 |
| DISC-13 | Q-08 y Q-12 aparecían como abiertas en algunos documentos. | Consolidadas en requisitos 0.9 |
| DISC-14 | H-08: incoherencias documentales. | Corregidas parcialmente en TASK035 |

## 7. Decisiones existentes consolidadas

- Q-08: representación monetaria HTTP como cadena decimal exacta.
- Q-12: máximo técnico de API de 1.000.000 de usuarios.
- Slider de 1 a 1.000 usuarios con entrada manual para cantidades superiores.
- Persistencia de simulaciones.
- Cliente registrado obligatorio.
- HTTP 404 para cliente inexistente.
- Texto decimal canónico en SQLite.
- API sin prefijo de versión.
- Alcance parcial del primer incremento de simulaciones.

Estas decisiones ya estaban aprobadas o registradas en SPEC-002/SPEC-003. No convierten en completos los requisitos parciales.

## 8. Decisiones nuevas pendientes

| ID | Tema | Recomendación |
| --- | --- | --- |
| Q-18 | Periodicidad mensual | Persistir `billing_period = "monthly"` y etiquetar la UI. |
| Q-19 | Usuarios cero | Permitir 0 con subtotal `0.00`; revisar Q-02/PP-Q-01. |
| Q-20 | Países y validación internacional | ES, PT, FR, DE, IT y NL; algoritmo oficial solo en ES. |
| Q-21 | Almacenamiento y llamadas API | GB enteros y llamadas mensuales; sin cargos; nulos en históricos. |
| Q-22 | Impuestos | Tabla estática versionada; base subtotal; `ROUND_HALF_UP`; snapshot histórico. |
| Q-23 | Divisas | `open.er-api.com`, caché 24 h, timeout 5 s, proxy backend y snapshot. |
| Q-24 | Búsqueda, detalle e historial | Endpoints de lectura con paginación; historial inmutable. |
| Q-25 | Previsualización | `POST /simulations/preview` sin persistencia; guardado explícito. |
| Q-26 | Campos desconocidos | `extra="forbid"` en simulación y preview. |

Ninguna de estas recomendaciones se considera aprobada. La aprobación conjunta corresponde al propietario.

## 9. Hallazgos técnicos

| Hallazgo | Estado | Incremento propuesto |
| --- | --- | --- |
| H-01: trampas del contexto `Decimal` | Abierto, no bloqueante | TASK036, con impuestos y divisas. |
| H-02: cobertura de regresión | Abierto, no bloqueante | TASK036; incluir 15 usuarios y casos nuevos. |
| H-03: decisión histórica de pricing | Conservado | Sin cambios. |
| H-04: orden de cálculo y comprobación del cliente | Abierto, no bloqueante | TASK036; unificar preview/guardado. |
| H-05: campos desconocidos ignorados | Abierto, no bloqueante | TASK036; `extra="forbid"`. |
| H-06: potencial condición de carrera | Abierto, no bloqueante | TASK036; manejo de conflicto. |
| H-07: sin restricciones monetarias en SQLite | Abierto, no bloqueante | TASK036; validación canónica y pruebas. |
| H-08: incoherencias documentales | Parcialmente corregido | TASK035 y TASK036. |

## 10. Hoja de ruta optimizada

La hoja de ruta completa está en [`docs/planning/mvp-roadmap.md`](../../docs/planning/mvp-roadmap.md).

| Tarea propuesta | Fases | Alcance | PR | Esfuerzo orientativo |
| --- | --- | --- | --- | --- |
| TASK036 | R1–R5 | Backend: internacionalización, campos de simulación, impuestos, divisas, lectura, historial y preview. | PR #6 | 6–8 días ideales |
| TASK037 | R6–R7 | Angular base, navegación, dashboard, alta y detalle de clientes. | PR #7 | 4–5 días ideales |
| TASK038 | R8–R9 | Simulador Angular, integración, E2E, README y despliegue local. | PR #8 | 4–5 días ideales |
| TASK039 | R10 | Auditoría final independiente y preparación de la entrega. | Sin PR de código | 1–2 días ideales |

Total orientativo: **15–20 días ideales**; con 20 % de contingencia, **18–24 días**. Es una estimación de planificación, no un compromiso.

## 11. Estrategia de evaluación

| Criterio | Peso | Evidencias actuales | Evidencias pendientes |
| --- | --- | --- | --- |
| Planificación y diseño | 35 % | Requisitos, ADRs, SPEC-001–003, planes, tareas, matriz y hoja de ruta. | SPEC-004/005, aprobación de Q-18–Q-26. |
| Criterio técnico y calidad | 25 % | Arquitectura, 240 pruebas, Ruff, mypy, auditoría TASK033, deuda registrada. | Pruebas de frontend, resolución de H-01/H-02/H-04–H-08, revisión de seguridad. |
| Calidad del software | 30 % | Backend de clientes, precios y simulaciones. | Impuestos, divisas, búsqueda, historial, preview y Angular. |
| README y despliegue | 10 % | README raíz, README de backend, `.env.example`, comandos. | README de frontend, arranque conjunto verificado y despliegue. |

No se fabricarán conversaciones, capturas ni resultados. Las evidencias de UI se generarán cuando exista la UI.

## 12. Validaciones

| Comprobación | Resultado |
| --- | --- |
| `git status --short` | 12 archivos modificados, 3 rutas nuevas y el `.docx` no seguido; sin archivos staged. |
| `git diff --cached --name-only` | Vacío. |
| `git diff --check` | Sin errores de espacios finales ni conflictos de whitespace. |
| Enlaces relativos en los 15 Markdown afectados | 0 enlaces rotos. |
| Espacios finales en los 15 Markdown afectados | 0 líneas con espacios finales. |
| Inventario de rutas cambiadas | Todas dentro de las rutas autorizadas; 0 rutas inesperadas. |
| Cambios en código, pruebas, configuración, dependencias, migraciones o `LICENSE` | 0. |
| Cambios en registros TASK001–TASK032 | 0. |
| Archivos `TASK036*` | 0. |
| Documento original en Git | No seguido; no staged. |
| Pruebas de software | No ejecutadas; la tarea es documental y no modifica código. |
| Paquetes instalados | Ninguno. |

La validación auxiliar se ejecutó con `backend/.venv/Scripts/python.exe` y biblioteca estándar, sin instalar dependencias.

## 13. Riesgos y bloqueantes

- **Bloqueante de decisión:** Q-18 a Q-26, P-01 y P-05 deben aprobarse antes de implementar el alcance correspondiente.
- **Riesgo de alcance:** la internacionalización y los impuestos pueden crecer más de lo que exige el reto; se limita a una lista corta y validación genérica.
- **Riesgo fiscal:** no se inventan tasas; la tabla debe ser aprobada y versionada.
- **Riesgo de divisas:** dependencia de un proveedor externo; se mitiga con caché, timeout y errores controlados.
- **Riesgo de frontend:** Angular puede retrasar la entrega; se construye sobre contratos estables y con componentes simples.
- **Riesgo documental:** el README de backend sigue desactualizado; se actualizará cuando la tarea lo autorice.
- **Riesgo de auditoría:** una auditoría final tardía puede descubrir deuda costosa; se proponen auditorías intermedias.

## 14. Propuesta de alcance para TASK036

TASK036 sería una tarea de especificación e implementación del backend restante, agrupando las fases R1–R5:

1. Aprobar y documentar Q-18 a Q-26.
2. Ampliar el catálogo de países y la validación fiscal internacional sin algoritmos oficiales fuera de España.
3. Añadir almacenamiento, llamadas API y periodicidad mensual a la simulación.
4. Implementar impuestos con tabla versionada y snapshot histórico.
5. Implementar divisas con proveedor público, caché y snapshot.
6. Añadir lectura de clientes, búsqueda, detalle e historial.
7. Añadir `POST /simulations/preview` sin persistencia.
8. Resolver H-01, H-02, H-04, H-05, H-06 y H-07 en el alcance que corresponda.
9. Actualizar pruebas, documentación y README de backend.
10. No crear el frontend; TASK037 se encarga de Angular.

TASK036 no se ha creado en esta tarea. Su autorización y publicación corresponden al propietario.

## 15. Confirmaciones

- No se ejecutó `git add`.
- No se ejecutó commit, push, creación de PR, merge, rebase ni operación destructiva.
- No hay archivos staged.
- No se modificó código fuente, pruebas, configuración, dependencias, migraciones ni `LICENSE`.
- No se creó el archivo de TASK036.
- No se modificaron los registros TASK001–TASK032.
- El documento original del reto no se añadió a Git y no se publicó en GitHub.
- No se instalaron paquetes ni se ejecutaron pruebas de software innecesarias.

## 16. Conclusión

El backend tiene una base sólida y una trazabilidad documental buena, pero el MVP frente al enunciado original sigue siendo parcial. La prioridad debe ser completar el contrato backend que necesita Angular, construir después la interfaz y reservar una auditoría final independiente. La aprobación conjunta de Q-18 a Q-26 es el siguiente paso.
