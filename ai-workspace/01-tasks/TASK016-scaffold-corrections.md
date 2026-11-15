# TASK016 — Correcciones finales del scaffold antes del PR #2

| Campo | Valor |
| --- | --- |
| ID | TASK016 |
| Título | Correcciones finales del scaffold antes del PR #2 |
| Estado | Completada; cambios locales pendientes de revisión |
| Fecha | 2026-11-15 |
| Participantes | Propietario (solicitud y autorización de implementación) / OpenCode + DeepSeek (materialización) |
| Autorización Git | Implementación y registros documentales autorizados; `git add`, `git commit`, `git push`, PR y merge no autorizados |

## 1. Objetivo y alcance

Resolver los hallazgos M1, M2 y B1–B4 de TASK015 antes de la publicación del PR #2, manteniendo el backend funcional y el aislamiento de Python 3.13 mediante `backend/.venv`.

No se implementaron funcionalidades de negocio ni se amplió el alcance. No se modificaron `LICENSE`, `TASKS.zip`, las versiones aprobadas de las dependencias ni el ADR 0002.

## 2. Instrucciones y fuentes

| Tipo de fuente | Referencia | Estado |
| --- | --- | --- |
| Instrucción original | Instrucción TASK016 facilitada en la sesión de OpenCode | Disponible; no está en `TASKS.zip` |
| Auditoría previa | [TASK015-audit.md](../02-audits/TASK015-audit.md) | Disponible; informe del agente |
| Fuente arquitectónica | [ADR 0002](../../docs/adr/0002-architecture.md) | Disponible |
| Informe del agente | Este registro y respuesta final de la sesión | Disponible; no es validación independiente |

## 3. Herramientas y participantes

- Propietario: solicitó las correcciones y autorizó la implementación y los registros.
- ChatGPT: no consta escritura en el repositorio ni ejecución de comandos en TASK016.
- OpenCode + DeepSeek: materializó las correcciones y ejecutó las comprobaciones.
- Herramientas: Git, PowerShell, Python 3.13 de `backend/.venv`, Pytest, Ruff, mypy, pip y Uvicorn/HTTPX.

## 4. Plan y decisiones

Plan:

1. Confirmar el estado Git y los 21 archivos previstos de TASK014.
2. Corregir M1 documentando el alcance real de `requirements.lock` y añadiendo una verificación de versiones instaladas y dependencias de build.
3. Corregir M2 y B1 ampliando la prueba de arquitectura y añadiendo pruebas del analizador.
4. Corregir B2 aclarando el directorio de trabajo en `backend/README.md`.
5. Corregir B3 separando la decisión pendiente de TASK013 de su materialización en TASK014.
6. Resolver B4 mediante una exclusión local en `.git/info/exclude`, sin modificar el `.gitignore` compartido.
7. Crear los registros de TASK015 y TASK016 y actualizar el índice.
8. Ejecutar las validaciones finales con el intérprete de `backend/.venv`.

Decisiones:

- No se adoptó una estrategia de lock estricto con hashes porque requeriría una herramienta adicional y autorización específica. Se documentaron sus ventajas, límites y coste.
- No se añadieron dependencias ni se regeneraron versiones.
- La regla `presentation → domain` se incorporó a la prueba; el ADR no se modificó.
- `TASKS.zip` se excluyó localmente en `.git/info/exclude`; la regla no se versiona.
- El staging futuro debe ser explícito por rutas.

## 5. Archivos afectados

### Creados por TASK016

- `ai-workspace/01-tasks/TASK015-backend-scaffold-audit.md`
- `ai-workspace/02-audits/TASK015-audit.md`
- `ai-workspace/01-tasks/TASK016-scaffold-corrections.md`

### Modificados por TASK016

- `backend/README.md`: alcance de `requirements.lock`, verificación de dependencias, dependencias de build, límites y directorio de trabajo.
- `backend/tests/test_architecture.py`: regla `presentation → domain`, resolución de imports relativos y pruebas del analizador.
- `README.md`: nota sobre restricciones frente a lock estricto.
- `ai-workspace/01-tasks/TASK013-documentation-publication.md`: separación entre decisión pendiente y materialización.
- `ai-workspace/README.md`: índice de TASK015/TASK016 y limitaciones actualizadas.
- `.git/info/exclude`: exclusión local de `TASKS.zip`; no versionado.

No se modificaron `LICENSE`, `backend/pyproject.toml`, `backend/requirements.lock` ni las versiones de dependencias.

## 6. Validaciones ejecutadas

| Comprobación | Resultado |
| --- | --- |
| Pytest | 9 pruebas superadas |
| Ruff check | Sin hallazgos |
| Ruff format check | 12 archivos ya formateados |
| mypy | Sin errores en 11 archivos fuente |
| `pip check` | Sin dependencias rotas |
| Lock frente a `pip freeze` | 33/33; 0 diferencias |
| Dependencias de build | `setuptools==84.2.1`; fuera del lock |
| `/health` | HTTP 200; `{"status":"ok"}` |
| `/openapi.json` | OpenAPI 3.1.0; título `SaaS-O-Matic API`; `/health` presente |
| `git diff --check` | Sin errores |
| Enlaces locales | 134 comprobados en 35 archivos Markdown; 0 rotos |
| `.venv`, cachés y `TASKS.zip` | Fuera del inventario; `TASKS.zip` excluido localmente |
| Dependencias globales | No detectadas; `ENABLE_USER_SITE=False` |

La comprobación de `/health` y `/openapi.json` se ejecutó con Uvicorn real sobre un puerto local efímero; el proceso se detuvo al terminar.

## 7. Hallazgos y correcciones

- **M1 — reproducibilidad:** corregido documentalmente. Se distingue restricciones de lock estricto, se documenta la build isolation, se añade una comprobación de `pip freeze` frente al lock y se enumeran límites y alternativas no adoptadas. Persisten la ausencia de hashes y la falta de cobertura de la build isolation.
- **M2 — `presentation → domain`:** corregido. `FORBIDDEN_BY_LAYER["presentation"]` incluye `domain` y una prueba de regresión verifica la detección.
- **B1 — análisis de imports:** corregido para imports absolutos, `from paquete import capa`, imports relativos resolubles y pruebas controladas. Los imports dinámicos siguen fuera del alcance del análisis estático y se documentan como limitación.
- **B2 — directorio de trabajo:** corregido. La guía comienza en la raíz, entra en `backend/` y aclara que los comandos posteriores se ejecutan allí.
- **B3 — redacción de TASK013:** corregido sin reescribir los hechos históricos.
- **B4 — `TASKS.zip`:** resuelto localmente con `.git/info/exclude`; no se modificó el `.gitignore` compartido. El staging debe ser explícito.

## 8. Autorizaciones Git

Se autorizaron la implementación de las correcciones y la creación de los registros documentales. No se autorizaron `git add`, `git commit`, `git push`, creación de PR ni merge. El merge corresponde exclusivamente al propietario. No se ejecutaron operaciones destructivas ni se escribió en `main`.

## 9. Resultado y decisiones pendientes

- Resultado: correcciones aplicadas localmente; backend funcional; validaciones superadas.
- Decisiones pendientes: revisión del propietario, autorización de staging/commit/push y creación del PR #2.
- Limitaciones abiertas: el lock no es estricto ni usa hashes; la build isolation queda fuera; el análisis de arquitectura no cubre imports dinámicos; no consta revisión independiente humana.
- PR #2: no se ha creado. No debe afirmarse su existencia hasta que el propietario lo autorice y se cree realmente.

## 10. Inventario propuesto para el PR #2

Modificados (5):

```text
README.md
ai-workspace/00-project-context/architectural-evolution.md
ai-workspace/README.md
docs/adr/0001-technology-stack.md
docs/adr/0002-architecture.md
```

Nuevos (19):

```text
ai-workspace/01-tasks/TASK013-documentation-publication.md
ai-workspace/01-tasks/TASK014-backend-scaffold.md
ai-workspace/01-tasks/TASK015-backend-scaffold-audit.md
ai-workspace/01-tasks/TASK016-scaffold-corrections.md
ai-workspace/02-audits/TASK015-audit.md
backend/README.md
backend/pyproject.toml
backend/requirements.lock
backend/src/saas_o_matic/__init__.py
backend/src/saas_o_matic/application/__init__.py
backend/src/saas_o_matic/bootstrap/__init__.py
backend/src/saas_o_matic/bootstrap/main.py
backend/src/saas_o_matic/domain/__init__.py
backend/src/saas_o_matic/infrastructure/__init__.py
backend/src/saas_o_matic/presentation/__init__.py
backend/src/saas_o_matic/presentation/app.py
backend/src/saas_o_matic/presentation/health.py
backend/tests/test_architecture.py
backend/tests/test_health.py
```

Total: **24 rutas**. No incluye `TASKS.zip`, `backend/.venv/`, cachés ni `egg-info`. `.git/info/exclude` no forma parte del PR.

## 11. Referencias

- [TASK015-audit.md](../02-audits/TASK015-audit.md)
- [TASK015-backend-scaffold-audit.md](TASK015-backend-scaffold-audit.md)
- [TASK014-backend-scaffold.md](TASK014-backend-scaffold.md)
- [ADR 0001 — Stack tecnológico](../../docs/adr/0001-technology-stack.md)
- [ADR 0002 — Arquitectura](../../docs/adr/0002-architecture.md)
- `backend/README.md`
- `backend/tests/test_architecture.py`
