# TASK015 — Auditoría técnica del scaffold Python

| Campo | Valor |
| --- | --- |
| ID | TASK015 |
| Tipo | Auditoría técnica |
| Estado | Completada; informe del agente |
| Fecha de registro | 2026-11-15 |
| Autor | OpenCode + DeepSeek |
| Revisión independiente | No consta |
| Veredicto | **APTA CON OBSERVACIONES** |

## 1. Alcance

Auditoría de solo lectura de los cambios de TASK014 antes del primer commit del backend: estado Git, inventario de 21 archivos, entorno virtual, dependencias, arquitectura, FastAPI, pruebas, documentación y preparación del PR #2.

No se modificaron archivos ni se ejecutaron `git add`, `git commit`, `git push`, creación de PR, merge, instalaciones o actualizaciones de dependencias. El informe se materializó en TASK016 porque TASK015 no creó archivos.

## 2. Fuentes

- Instrucción TASK015 facilitada en la sesión de OpenCode; no está en `TASKS.zip`.
- Respuesta final de TASK015 en la sesión.
- Estado del repositorio y documentos revisados durante la auditoría.
- [TASK014-backend-scaffold.md](../01-tasks/TASK014-backend-scaffold.md).

No se reconstruyeron prompts ni conversaciones históricas.

## 3. Estado Git

| Comprobación | Resultado |
| --- | --- |
| Rama | `feature/backend-scaffold` |
| HEAD | `50f80470eafc9517a277b652252391880b4a491e` |
| `origin/main` | `50f80470eafc9517a277b652252391880b4a491e` |
| Relación con `origin/main` | `0` por delante y `0` por detrás |
| `main` local | `8371f9f608ce6e06984cc501d8240e1b7edf34d5`; 2 commits por detrás |
| Upstream de la rama | Ninguno |
| Archivos staged | Ninguno |
| Archivos previstos | 21: 5 modificados y 16 nuevos |
| `LICENSE` | Sin cambios; hash `2d6d43827eb9ab4ce0eea57959a98aafa3390a40` |
| `backend/.venv` | No versionado; ignorado |
| `TASKS.zip` | Sin seguimiento y fuera del inventario; no ignorado en el momento de la auditoría |

Los 21 archivos previstos por TASK014 eran los únicos cambios destinados a publicación. No existía commit de TASK014 ni PR #2 en la sesión.

## 4. Hallazgos

No se detectaron hallazgos bloqueantes. Se registraron dos hallazgos medios y cuatro bajos.

### M1 — El procedimiento documentado no es un lock estricto

**Ubicaciones:** `backend/README.md:40`, `backend/README.md:44`, `README.md:72`, `backend/pyproject.toml:2`, `backend/requirements.lock:1-33`.

`python -m pip install -e ".[dev]" -c requirements.lock` aplica el archivo como restricciones, no como un conjunto cerrado. Pip puede incorporar paquetes no listados si aparecen nuevas dependencias. La build isolation fija `setuptools==84.2.1` en `pyproject.toml`, pero esa dependencia no está en el lock. Tampoco se usan hashes.

Para el grafo actual, las 9 dependencias declaradas estaban en el lock, el lock contenía 33 paquetes y `pip freeze` coincidía 33/33. La reproducibilidad práctica era alta; la garantía estricta no estaba demostrada. La afirmación de “reinstalación reproducible” era más fuerte que el procedimiento.

### M2 — La prueba de arquitectura no cubría `presentation → domain`

**Ubicaciones:** `backend/tests/test_architecture.py:15`, `docs/adr/0002-architecture.md:66`, `backend/README.md:106`.

El ADR 0002 prohíbe que `presentation` importe `domain`. El conjunto `FORBIDDEN_BY_LAYER["presentation"]` solo contenía `bootstrap` e `infrastructure`. El código actual no violaba la regla, pero la prueba no habría detectado una violación futura.

### B1 — Puntos ciegos del análisis estático

**Ubicación:** `backend/tests/test_architecture.py:19-29`.

El analizador no procesaba `from . import ...`, no expandía `from saas_o_matic import application` y no detectaba imports dinámicos. Sí detectaba imports absolutos normales como `import fastapi`, `from fastapi import ...` e `import saas_o_matic.application`. La prueba no era trivial, pero era incompleta.

### B2 — Directorio de trabajo inconsistente en `backend/README.md`

**Ubicación:** `backend/README.md:13-18`.

El texto decía que todos los comandos se ejecutaban desde `backend/`, pero el bloque incluía `cd backend`. Si el usuario ya estaba en `backend/`, el comando fallaba.

### B3 — Redacción contradictoria en TASK013

**Ubicación:** `ai-workspace/01-tasks/TASK013-documentation-publication.md:92`.

La línea etiquetaba como “Decisión pendiente” algo que ya se había “realizado en TASK014”. La distinción entre la decisión original y su materialización posterior no era clara.

### B4 — `TASKS.zip` no estaba ignorado

**Ubicaciones:** `TASKS.zip`, `ai-workspace/01-tasks/TASK014-backend-scaffold.md:93`.

El archivo estaba sin seguimiento y fuera de los 21, pero `git check-ignore -v TASKS.zip` no devolvía coincidencia y `.gitignore` no contenía una regla para él. Un `git add .` podía incluirlo.

## 5. Reproducibilidad de dependencias

| Comprobación | Resultado |
| --- | --- |
| Python | 3.13.17 |
| Intérprete | `backend\.venv\Scripts\python.exe` |
| `sys.prefix` / `sys.base_prefix` | Distintos |
| `ENABLE_USER_SITE` | `False` |
| Origen de dependencias | `backend\.venv\Lib\site-packages` |
| `pip check` | Sin dependencias rotas |
| `pip freeze --exclude-editable` frente al lock | 33/33; 0 diferencias |
| Dependencias declaradas en el lock | 9/9 |
| Dependencias de build en el lock | No: `setuptools==84.2.1` queda fuera |

No se detectaron dependencias globales accidentales. La instalación actual era coherente. La estrategia documentada no garantizaba estrictamente el mismo conjunto de artefactos en una reinstalación.

## 6. Pruebas arquitectónicas

Estado actual de las capas:

- `domain/`, `application/` e `infrastructure/` solo contenían docstrings.
- `presentation/` contenía `app.py` y `health.py`; no importaba `domain`.
- `bootstrap/main.py` importaba `presentation.app` y actuaba como composition root provisional.
- Ninguna capa importaba `bootstrap` ni `infrastructure`.

Las pruebas detectaban imports absolutos de frameworks y capas, pero no cubrían `presentation → domain` ni los casos de B1. El composition root seguía identificado como provisional en el ADR 0002 y en `backend/README.md`.

## 7. FastAPI y pruebas

| Comprobación | Resultado |
| --- | --- |
| Pytest | 4 pruebas superadas |
| Ruff check | Sin hallazgos |
| Ruff format check | 12 archivos ya formateados |
| mypy | Sin errores en 11 archivos fuente |
| `/health` real con Uvicorn | HTTP 200; `{"status":"ok"}` |
| `/openapi.json` real con Uvicorn | HTTP 200; OpenAPI 3.1.0; título `SaaS-O-Matic API`; ruta `/health` presente |

`create_app()` estaba en `presentation/app.py`; `bootstrap/main.py` contenía `app = create_app()` y era el punto de entrada ASGI. No se encontró lógica de negocio ni acceso a base de datos. Las pruebas usaban `httpx.ASGITransport`.

## 8. Documentación

- `backend/README.md` cubría creación y activación de `.venv`, política de PowerShell, comprobación del intérprete, instalación, ejecución, pruebas, estructura, reglas de dependencia y alcance.
- Se comprobaron 54 enlaces locales en los documentos afectados; 0 rotos. Los enlaces externos no se validaron por red.
- `ai-workspace/README.md:71-72` incluía TASK013 y TASK014.
- El merge commit de PR #1 coincidía con `50f8047`.
- P-02 seguía “aplicada en TASK014; pendiente de revisión del resultado”. No se cerró.
- La ubicación definitiva del composition root seguía pendiente.

## 9. Limitaciones

- El informe fue elaborado por OpenCode + DeepSeek; no es una validación independiente.
- No consta revisión humana independiente de TASK015.
- La reproducibilidad estricta de dependencias no estaba garantizada.
- El análisis arquitectónico era estático y no cubría imports dinámicos.
- Los enlaces externos no se comprobaron por red.
- TASK015 no creó archivos; este informe se materializó en TASK016.

## 10. Referencias

- [TASK015-backend-scaffold-audit.md](../01-tasks/TASK015-backend-scaffold-audit.md)
- [TASK014-backend-scaffold.md](../01-tasks/TASK014-backend-scaffold.md)
- [TASK016-scaffold-corrections.md](../01-tasks/TASK016-scaffold-corrections.md)
- [ADR 0001 — Stack tecnológico](../../docs/adr/0001-technology-stack.md)
- [ADR 0002 — Arquitectura](../../docs/adr/0002-architecture.md)
- `backend/README.md`
- `backend/pyproject.toml`
- `backend/requirements.lock`
