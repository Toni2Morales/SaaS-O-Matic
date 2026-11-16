# TASK018 — Primera funcionalidad: alta de clientes

| Campo | Valor |
| --- | --- |
| ID | TASK018 |
| Título | Primera funcionalidad: alta de clientes |
| Estado | **Parcial; bloqueada en el punto de control por decisiones funcionales pendientes** |
| Fecha | 2026-11-15 |
| Rama | `feature/customer-registration` |
| Participantes | Propietario (instrucción) / OpenCode + DeepSeek (análisis, especificación y comprobaciones) |
| Autorización Git | Crear rama, documentación, implementación de partes definidas y validaciones; `git add`, `git commit`, `git push`, PR y merge no autorizados |

## 1. Objetivo y alcance

Iniciar la implementación del alta de clientes mediante `POST /customers`, respetando la arquitectura modular y manteniendo las dependencias Python aisladas en `backend/.venv`.

La tarea incluía revisar requisitos, crear la especificación, proponer el contrato HTTP e implementar únicamente las partes suficientemente definidas. No se autorizó inventar requisitos ni resolver preguntas abiertas por inferencia.

## 2. Comprobaciones iniciales

| Comprobación | Resultado |
| --- | --- |
| Rama inicial | `feature/backend-scaffold` |
| HEAD inicial | `c729d710e805f2c9e7f191d87cef9343eed1a76f` |
| Árbol de trabajo inicial | Limpio |
| PR #2 | `MERGED` |
| Fecha de merge del PR #2 | `2026-11-15T16:10:42Z` |
| Commit de merge | `be755a68a52392fd562eb3901e317bc85b1ed8e9` |
| Padres del merge | `50f80470eafc9517a277b652252391880b4a491e` y `c729d710e805f2c9e7f191d87cef9343eed1a76f` |
| `git fetch origin` | Correcto |
| `origin/main` tras fetch | `be755a68a52392fd562eb3901e317bc85b1ed8e9` |
| Rama creada | `feature/customer-registration` desde `origin/main` |
| HEAD de la nueva rama | `be755a68a52392fd562eb3901e317bc85b1ed8e9` |

No se modificó `main`, no se sobrescribieron cambios locales y no se ejecutaron operaciones destructivas.

## 3. Fuentes consultadas

- [Requisitos funcionales](../../docs/requirements/functional-requirements.md)
- [ADR 0001 — Stack tecnológico](../../docs/adr/0001-technology-stack.md)
- [ADR 0002 — Arquitectura](../../docs/adr/0002-architecture.md)
- [Evaluación inicial del repositorio](../../docs/assessment/001-repository-assessment.md)
- [README raíz](../../README.md)
- [Evolución arquitectónica](../00-project-context/architectural-evolution.md)
- [Herramientas y roles de IA](../00-project-context/ai-tools-and-roles.md)
- [TASK017 — Publicación del scaffold](TASK017-backend-publication.md)

## 4. Requisitos confirmados

- **FR-01:** crear clientes con razón social, identificador fiscal, email, país y plan seleccionado.
- **FR-02:** validar identificadores fiscales españoles DNI/NIF/CIF mediante sus algoritmos de comprobación.
- **CON-01:** backend en Python 3.13 con FastAPI, Pydantic v2, SQLAlchemy 2, SQLite y Alembic.
- **CON-08:** API documentada con OpenAPI.
- **CON-09:** validación con Pytest, HTTPX, Ruff y mypy.
- **ADR 0002:** monolito modular con dependencias dirigidas hacia el dominio; `domain` sin frameworks; `presentation` sin `domain`; modelos SQLAlchemy y esquemas Pydantic independientes; composition root provisional en `bootstrap/`.
- **TASK018:** la ruta solicitada es `POST /customers`.

No se ha tratado ASM-07, NFR-02 ni NFR-03 como decisiones aprobadas.

## 5. Decisiones pendientes

| ID | Decisión | Efecto |
| --- | --- | --- |
| D-01 / Q-01 | Catálogo y formato de países. | Tipo, validación y persistencia de `country`. |
| D-02 / Q-03 | Catálogo y formato de planes. | Tipo, validación y persistencia de `plan`. |
| D-03 / Q-04 | Soporte de NIE. | Algoritmos y formatos fiscales aceptados. |
| D-04 / Q-13 | Reglas de validación del email. | Validación y errores HTTP. |
| D-05 / Q-14 | Unicidad del identificador fiscal y ámbito. | Restricción de base de datos y duplicados. |
| D-06 / Q-14 | Unicidad de la razón social y ámbito. | Restricción de base de datos y duplicados. |
| D-07 | Normalización del identificador fiscal. | Validación y comprobación de duplicados. |
| D-08 | Obligatoriedad de los cinco datos de FR-01. | Esquema de entrada y columnas. |
| D-09 | Código de éxito y cuerpo de respuesta. | Contrato HTTP y OpenAPI. |
| D-10 | Tipo del identificador interno. | Modelo, respuesta y migración. |
| D-11 / P-09 | Política de errores HTTP. | Códigos y formato de error. |
| D-12 | Ruta definitiva: `/customers` o `/api/v1/customers`. | Ruta pública y OpenAPI. |
| D-13 / P-07 | Límite transaccional del caso de uso. | Aplicación e infraestructura. |
| D-14 | Campos de auditoría. | Modelo y migración. |

Estas decisiones afectan al contrato público, al modelo persistido o a la semántica de validación. Por ello se detuvo la implementación antes de escribir código de producto.

## 6. Especificación y contrato propuesto

Se creó [SPEC-001](../../docs/specs/001-customer-registration/spec.md), con:

- Requisitos confirmados.
- Supuestos no confirmados.
- Decisiones pendientes.
- Propuesta de contrato HTTP.
- Alternativas de errores y duplicados.
- Criterios de aceptación propuestos, no aprobados.

La propuesta usa los campos `legal_name`, `tax_id`, `email`, `country` y `plan`, con valores y catálogos pendientes. No se ha aprobado ningún esquema definitivo.

El plan técnico está en [PLAN-001](../../docs/specs/001-customer-registration/plan.md) y el desglose en [TASKS-001](../../docs/specs/001-customer-registration/tasks.md).

## 7. Implementación realizada

**No se ha implementado código de producto.**

No se crearon:

- Entidad de dominio.
- Caso de uso.
- Puerto de repositorio.
- Modelo SQLAlchemy.
- Repositorio concreto.
- Configuración de SQLite.
- Configuración de Alembic ni migración inicial.
- Router ni esquemas Pydantic de clientes.
- Composition root para clientes.
- Pruebas de la funcionalidad.

Motivo: fijar cualquiera de esos elementos habría exigido decidir por inferencia campos obligatorios, catálogos, unicidad, normalización, errores HTTP o persistencia. El punto de control obligatorio de TASK018 exige detenerse en ese caso.

## 8. Archivos creados y modificados

### Creados

- `ai-workspace/01-tasks/TASK017-backend-publication.md`
- `ai-workspace/01-tasks/TASK018-customer-registration.md`
- `docs/specs/001-customer-registration/spec.md`
- `docs/specs/001-customer-registration/plan.md`
- `docs/specs/001-customer-registration/tasks.md`

### Modificados

- `README.md`: enlace a la especificación y mención de especificaciones en la estructura.
- `ai-workspace/README.md`: TASK017/TASK018, PR #2, estados y limitaciones.
- `ai-workspace/00-project-context/ai-tools-and-roles.md`: `docs/specs/` ya existe.
- `ai-workspace/00-project-context/architectural-evolution.md`: fase 4 completada y fase 6 con especificación bloqueada.

No se modificaron `LICENSE`, `backend/pyproject.toml`, `backend/requirements.lock`, `TASKS.zip`, `.venv` ni bases SQLite.

## 9. Validaciones ejecutadas

| Comprobación | Resultado |
| --- | --- |
| Intérprete | Python 3.13.17 desde `backend/.venv/Scripts/python.exe` |
| Aislamiento | `sys.prefix != sys.base_prefix`; `ENABLE_USER_SITE=False` |
| SQLAlchemy disponible | 2.1.8 |
| Alembic disponible | 1.20.1 |
| FastAPI disponible | 0.163.1 |
| Pydantic disponible | 2.14.3 |
| Pytest | 9 pruebas superadas |
| Ruff check | Sin hallazgos |
| Ruff format check | 12 archivos ya formateados |
| mypy | Sin incidencias en 11 archivos fuente |
| `pip check` | Sin dependencias rotas |
| Lock frente a `pip freeze` | 33/33; 0 diferencias |
| `GET /health` con Uvicorn real | HTTP 200; `{"status":"ok"}` |
| `GET /openapi.json` | HTTP 200; OpenAPI 3.1.0; título `SaaS-O-Matic API`; `/health` presente |
| `/customers` en OpenAPI | Ausente, como corresponde a la implementación bloqueada |
| `git diff --check` | Sin errores |
| Espacios finales en documentos nuevos/modificados | Sin hallazgos |
| Rutas locales y secretos en documentos | Sin hallazgos |
| Enlaces relativos | 79 comprobados; 0 rotos |
| Migraciones Alembic | No implementadas; no existe configuración de Alembic |
| Bases SQLite locales | No se creó ninguna base de desarrollo |

No se instalaron dependencias nuevas.

## 10. Limitaciones y riesgos

- La funcionalidad no está implementada; solo está especificada y bloqueada.
- El contrato HTTP no está aprobado.
- El modelo persistido no está definido.
- La validación fiscal, el email, los países y los planes siguen pendientes.
- La unicidad y el tratamiento de duplicados siguen pendientes.
- El límite transaccional y la política de errores siguen pendientes.
- No hay CI configurada.
- El lock de dependencias no es estricto ni usa hashes.
- La ubicación definitiva del composition root sigue pendiente.
- La estructura global por capas puede no ser la frontera modular definitiva (P-06).

## 11. Autorizaciones Git

Se autorizaron la creación de la rama, la documentación, la implementación de las partes definidas y las validaciones. No se autorizaron `git add`, `git commit`, `git push`, creación de PR ni merge. No se escribió en `main` ni se ejecutaron comandos destructivos.

## 12. Resultado y siguiente paso

- Resultado: rama creada, TASK017 registrada, especificación 001 creada y punto de bloqueo documentado.
- Estado: parcial; no se publican cambios.
- Siguiente paso: el propietario debe resolver D-01 a D-14. Después se actualizará el contrato, se aprobará el modelo y se implementarán dominio, aplicación, infraestructura, presentación, migración y pruebas.

## 13. Referencias

- [SPEC-001](../../docs/specs/001-customer-registration/spec.md)
- [PLAN-001](../../docs/specs/001-customer-registration/plan.md)
- [TASKS-001](../../docs/specs/001-customer-registration/tasks.md)
- [Requisitos funcionales](../../docs/requirements/functional-requirements.md)
- [ADR 0002 — Arquitectura](../../docs/adr/0002-architecture.md)
- [TASK017 — Publicación del scaffold](TASK017-backend-publication.md)
