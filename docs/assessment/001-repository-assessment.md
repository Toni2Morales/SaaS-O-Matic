# 001 — Evaluación inicial del repositorio

| Campo | Valor |
| --- | --- |
| Fecha | 2026-11-12 |
| Alcance | Inspección del repositorio y preparación de los fundamentos documentales |
| Rama | `docs/project-foundation` |
| Estado | Completado; pendiente de revisión y aprobación |

Este documento distingue de forma explícita entre **hechos verificados** (observados ejecutando comandos) y **recomendaciones** (propuestas que requieren aprobación).

---

## 1. Hechos verificados

### 1.1 Identidad del repositorio

| Elemento | Valor observado |
| --- | --- |
| Repositorio | `Toni2Morales/SaaS-O-Matic` (público) |
| URL remota | `https://github.com/Toni2Morales/SaaS-O-Matic.git` |
| Rama por defecto | `main` |
| Descripción | vacía en el momento de la inspección |
| Licencia | MIT |
| Issues / Wiki | habilitados / habilitado |

El repositorio se llamaba originalmente `Sass-O-Matic` y fue renombrado a `SaaS-O-Matic` por el propietario antes de esta tarea. La carpeta local conserva el nombre antiguo; no se modificó.

### 1.2 Estado de Git en la inspección

```text
## docs/project-foundation
* docs/project-foundation  8371f9f
  main                     8371f9f [origin/main]
```

| Elemento | Valor observado |
| --- | --- |
| Commit base | `8371f9f608ce6e06984cc501d8240e1b7edf34d5` — "Initial commit" |
| Autor del commit | `Antonio Morales <107318721+Toni2Morales@users.noreply.github.com>` |
| Committer del commit | `GitHub <noreply@github.com>` (creado desde la interfaz web) |
| Número de commits | 1 |
| Árbol de trabajo | limpio, sin ficheros sin seguimiento |
| Ramas remotas | solo `main` |
| Pull requests | ninguno |
| Protección de `main` | no configurada (HTTP 404 al consultar la API) |

Configuración de Git relevante en la máquina del propietario: `core.autocrlf=true`, `core.ignorecase=true`, `pull.ff=only`, `init.defaultBranch=main`. La identidad de Git quedó configurada globalmente por el propietario antes de esta tarea.

### 1.3 Contenido inicial

| Fichero | Estado |
| --- | --- |
| `README.md` | Una línea: `# Sass-O-Matic`. Sin descripción, alcance ni instrucciones. |
| `.gitignore` | Plantilla oficial de GitHub para Python (220 líneas), sin sección Node/Angular. |
| `LICENSE` | Texto MIT estándar, Copyright (c) 2026 Antonio Morales. |

No existía código de aplicación, pruebas, especificaciones, ADRs, configuración de backend/frontend, ni workflows de CI.

### 1.4 Entorno de desarrollo observado

| Herramienta | Versión observada |
| --- | --- |
| Python | 3.15.0 |
| Node.js | 24.22.0 |
| npm | 11.19.1 |
| Git | 2.56.0.windows.2 |
| GitHub CLI | autenticado como `Toni2Morales` (scopes `gist`, `read:org`, `repo`, `workflow`) |

**Discrepancia detectada:** la versión de proyecto aprobada es Python 3.13, pero el intérprete instalado en la máquina es 3.15.0. No se modificó el entorno. Debe resolverse antes del scaffold del backend (ver RSK-01).

---

## 2. Evaluación del `.gitignore` inicial

| Área | Cobertura inicial | Observación |
| --- | --- | --- |
| Entornos virtuales Python | Completa | `.venv`, `venv/`, `env/`, `ENV/` |
| Cachés y bytecode Python | Completa | `__pycache__/`, `*.py[codz]` |
| Pytest y coverage | Completa | `.pytest_cache/`, `.coverage*`, `htmlcov/`, `coverage.xml` |
| Cachés de Ruff y mypy | Completa | `.ruff_cache/`, `.mypy_cache/` |
| Variables de entorno | **Parcial** | Solo `.env` y `.envrc`; `.env.local` habría quedado versionado |
| Bases SQLite | **Parcial** | Solo `db.sqlite3` y su journal |
| Dependencias Node/Angular | **Ausente** | Sin `node_modules/` |
| Artefactos y caché Angular | **Ausente** | Sin `.angular/`, `out-tsc/`, `*.tsbuildinfo` |
| Coverage de frontend | **Ausente** | Existía `cover/`, no `coverage/` |
| Configuración de IDE | **Ausente** | `.idea/` y `.vscode/` comentados |
| Ficheros temporales del sistema | **Ausente** | Sin `Thumbs.db`, `Desktop.ini`, `.DS_Store` |
| Patrones demasiado amplios | **Riesgo** | `lib/`, `var/`, `target/`, `parts/` podían ocultar código en un monorepo |

### Cambios aplicados en esta tarea

1. `.env.*` ignorado con excepción explícita para `!.env.example`.
2. Reglas SQLite ampliadas (`*.db`, `*.sqlite`, `*.sqlite3`) más ficheros `-journal`, `-wal` y `-shm`, con excepciones para fixtures en `**/tests/**/fixtures/**` (raíz o dentro de `backend/`).
3. Sección Node/Angular: `node_modules/`, `.angular/`, `out-tsc/`, `dist/`, `coverage/`, `*.tsbuildinfo`, `.eslintcache` y logs de npm/yarn/pnpm. **Nota histórica:** estos patrones generales de `dist/` y `coverage/` fueron acotados posteriormente en TASK006; el comportamiento actual está en el punto 2 de la sección 6.
4. Patrones de empaquetado Python anclados a la raíz (`/lib/`, `/var/`, `/build/`, etc.) para no ocultar directorios de código anidados.
5. Sección de IDE y sistema operativo (`.idea/`, `.vscode/*` con excepciones, `Thumbs.db`, `Desktop.ini`, `.DS_Store`, `*.swp`).

Se conservaron todas las reglas Python útiles de la plantilla original.

---

## 3. Recomendaciones (no aplicadas en esta tarea)

| ID | Recomendación | Motivo |
| --- | --- | --- |
| REC-01 | Proteger `main` con revisión obligatoria y checks de CI. | Evitar escrituras accidentales; hoy no hay protección. |
| REC-02 | Añadir workflows de CI (Ruff, mypy, Pytest, Vitest, build). | Se acordó explícitamente dejarlos fuera de esta rama. |
| REC-03 | Fijar Python 3.13 mediante `.python-version` y `requires-python` en `pyproject.toml`. | El entorno local tiene 3.15.0; hay riesgo de incompatibilidad de dependencias. |
| REC-04 | Verificar la compatibilidad de Vitest con la versión de Angular que se elija. | Angular ha incorporado soporte para Vitest en versiones recientes; la compatibilidad con la versión que se elija no está verificada. |
| REC-05 | Definir la fuente autoritativa de tipos impositivos y del proveedor de divisas. | Requisitos FR-06 y FR-10 sin datos. |
| REC-06 | Añadir `docs/specs/` con una especificación por funcionalidad antes de implementar. | El flujo de trabajo definido, aún pendiente de aprobación formal, exige especificación previa. |

---

## 4. Riesgos identificados

| ID | Riesgo | Severidad | Estado |
| --- | --- | --- | --- |
| RSK-01 | Python local 3.15 frente al objetivo 3.13 | Alta | Abierto |
| RSK-02 | Reglas fiscales y de divisas sin fuente definida | Alta | Abierto (requiere decisión del propietario) |
| RSK-03 | Precios de almacenamiento y API no definidos | Media | Mitigado: no se asignan cargos |
| RSK-04 | SQLite no reproduce la semántica de una base de datos de producción | Media | Aceptado para el alcance actual |
| RSK-05 | `core.autocrlf=true` sin normalización previa | Baja | Mitigado con `.gitattributes` |

---

## 5. Correcciones posteriores a la revisión independiente (TASK004)

Tras la revisión independiente de la TASK003 se aplicaron estas correcciones, todas documentales:

1. **ADR 0002:** se eliminó la contradicción entre FR-11 y P-08 (la conversión es reconstruible con importe base, divisa, tasa, fecha y fuente) y se aclaró que `presentation` no importa `domain`: los errores de dominio se traducen a errores de aplicación.
2. **ADR 0001 y ADR 0002:** se corrigió la autoría (OpenCode/DeepSeek) y se separó el estado de la decisión del estado del documento.
3. **Requisitos:** ASM-02 y ASM-03 quedaron como supuestos provisionales; se añadieron Q-13 (validación de email), Q-14 (unicidad) y Q-15 (unidades de almacenamiento y llamadas); FR-04 y FR-11 se precisaron sin inventar unidades ni reglas.
4. **Proceso, README y AGENTS:** los prefijos de rama se alinearon con `docs/`, `feature/`, `fix/`, `test/` y `refactor/`; se redujo la duplicación y el proceso queda como fuente principal.
5. **`.gitignore`:** se retiraron comentarios heredados que contradecían las reglas efectivas de IDE y se eliminó el patrón redundante `ENV/`.
6. **`.editorconfig`:** el límite de 100 se ajustó a 88 de forma provisional, a la espera de configurar Ruff en `pyproject.toml`.
7. **`.env.example`:** se marcó como plantilla provisional.
8. **Vitest:** se retiró la afirmación de sustitución universal de Karma y se mantuvo la verificación como pendiente.
9. **`docs/specs/`:** se indica explícitamente que todavía no existe y se creará en una tarea posterior.

---

## 6. Correcciones posteriores a la auditoría final (TASK006)

1. **ADR 0002:** se separó el diagrama de dependencias de la composición. `presentation` depende de `application`, `application` de `domain`, `infrastructure` solo de `domain`, y el composition root se documenta fuera de las cuatro capas.
2. **`.gitignore`:** las excepciones de fixtures cubren `tests/` en la raíz y dentro de `backend/`, y las extensiones `.db`, `.sqlite` y `.sqlite3`; `dist/` se ancló a la raíz y a `frontend/`, y `coverage/` a `frontend/`; se restauró `ENV/`.
3. **Requisitos:** Q-11 se reformuló para distinguir la tasa por simulación de una caché histórica; Q-08 incluye la precisión decimal; se añadió Q-16 para la magnitud del importe base; los dos decimales quedan como supuesto provisional.
4. **AGENTS:** se añadió Pydantic a las prohibiciones del dominio y un enlace a ADR 0002 como fuente principal.

---

## 7. Correcciones posteriores a TASK007 (TASK008)

1. **Proceso, AGENTS, contexto de roles y README:** la política Git se revisó en TASK008. El propietario define el alcance, autoriza expresamente las operaciones Git y conserva la decisión final; los agentes pueden ejecutar `git add`, `git commit`, `git push` y crear PR con autorización expresa, pero nunca fusionan. Las operaciones destructivas, incluido `git push --force-with-lease`, quedan prohibidas de forma absoluta.
2. **ADR 0002:** la ubicación definitiva del composition root se incluyó entre los detalles provisionales pendientes de concretar durante el scaffold.
3. **Requisitos:** se añadió Q-17 para la obligatoriedad de la fecha y la fuente del tipo de cambio, sin modificar FR-11.
4. **Referencias:** se sustituyeron las menciones que presuponían una revisión ya abierta por «esta rama» en este documento y en el contexto de evolución.
5. **Evaluación histórica:** se aclaró que los patrones generales de `dist/` y `coverage/` fueron acotados posteriormente en TASK006.

---

## 8. Resultado

El repositorio pasa de contener únicamente los ficheros iniciales a disponer de una base documental y de configuración compartida, sin código de aplicación ni dependencias. El alcance funcional sigue pendiente de las respuestas a las preguntas abiertas de [`docs/requirements/functional-requirements.md`](../requirements/functional-requirements.md).
