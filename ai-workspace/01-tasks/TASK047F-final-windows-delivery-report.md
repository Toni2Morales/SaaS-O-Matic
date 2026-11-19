# TASK047F — Informe final de entrega Windows 10

> **BORRADOR DE CAMPAÑA — no emitir aún veredicto final.** La campaña desde clon limpio,
> suites locales finales e integración funcional de TASK047F están pendientes. Este archivo
> se publica como destino del informe y se completará con resultados observados antes del
> commit 3; no atribuir los resultados históricos a la campaña nueva.

## 1. Resumen ejecutivo y decisión de alcance

El propietario sustituyó la búsqueda de compatibilidad multiplataforma de TASK047/TASK047A2/
TASK047B/TASK047C por una entrega reproducible en Windows 10. A47-01/02/03 se mantienen
pendientes y aplazados. Los workflows de Actions se mantienen solo manuales, sin alterar los
jobs; no se despacharon durante TASK047F.

## 2. Entorno Windows 10 observado

| Herramienta                               | Versión observada                                                                                 |
| ----------------------------------------- | ------------------------------------------------------------------------------------------------- |
| Windows                                   | Windows 10 Pro 22H2, build 19045, x64                                                             |
| PowerShell                                | 5.1.19041.6456, Desktop                                                                           |
| Git                                       | 2.56.0.windows.2                                                                                  |
| Python Launcher / Python                  | `py -3.13`: Python 3.13.17; el `python` global por defecto es 3.15.0 y no se usa para el proyecto |
| pip del Python 3.13                       | 26.2.2                                                                                            |
| Node.js / npm                             | 24.22.0 / 11.19.1                                                                                 |
| Angular / Angular CLI                     | 22.2.6 / 22.2.6                                                                                   |
| TypeScript / RxJS                         | 6.0.3 / 7.8.2                                                                                     |
| FastAPI / Pydantic / SQLAlchemy / Alembic | 0.163.1 / 2.14.3 / 2.1.8 / 1.20.1, dentro de `backend/.venv`                                      |
| SQLite runtime                            | 3.50.4, biblioteca SQLite de Python; no se requiere CLI SQLite independiente                      |
| pytest / Ruff / mypy                      | 9.2.0 / 0.17.5 / 2.4.1                                                                            |
| Vitest / Playwright Test                  | 5.1.1 / 1.65.1                                                                                    |
| Edge / Chrome instalados                  | 157.0.4341.60 / 157.0.8103.79                                                                     |
| Browsers Playwright instalados            | Chromium 159.0.8154.6; Firefox 159.0; WebKit 27.2                                                 |

Los rangos compatibles se obtienen de `backend/pyproject.toml`, `frontend/package.json`,
`.nvmrc` y scripts. No se infieren requisitos mínimos de hardware. Edge/Chrome se anotan como
instalados; E2E se ejecuta con los browsers gestionados por Playwright. No se presenta el
host como Windows 11 ni se afirma compatibilidad verificada en otros OS.

Prerrequisitos oficiales: [Git for Windows](https://git-scm.com/download/win),
[Python Windows](https://www.python.org/downloads/windows/) 3.13,
[Node.js](https://nodejs.org/en/download) 24. No se requiere instalar globalmente Angular,
SQLite ni Playwright. GitHub repository public: `Toni2Morales/SaaS-O-Matic`.

## 3. Quick Start

El comando aprobado es `git clone`, `cd SaaS-O-Matic`, `start.ps1` tras instalar los
prerrequisitos. El clone de aceptación de esta tarea debe fijar expresamente
`docs/final-delivery`; la instrucción de README usa la rama principal como pidió el
propietario. Aplicación `http://127.0.0.1:4200`, Swagger `/docs`, health `/health`.

Resultados nuevos, duración primera/segunda ejecución, HTTP status, migraciones, parada,
persistencia y puertos se incorporarán aquí después de la campaña. DB temporal del clone y
datos sintéticos solamente.

## 4. Calidad y verificación funcional

### Evidencia histórica (no contar como TASK047F)

- TASK046: backend Pytest 579/579; Vitest 40/40; Playwright Windows 79 PASS/20 opt-in skips;
  integraciones dedicadas 2/2 (real UI/API/SQLite y recuperación tras reinicio); axe nueve
  estados Chromium sin violaciones detectadas.
- TASK047A posterior al cambio: suite Windows 79 PASS/20 skips; capturas Chromium a 320/390/
  1440 px; Quality CI volvió a fallar las mismas seis aserciones a 320 px y 334 px document
  width. La corrección `.field-heading` no resolvió A47-01.
- TASK047F debe anotar separadamente una única campaña nueva en el clon publicado, comandos,
  tests reales PASS/FAIL/skips, cobertura, audits, axe, matriz 320/375/390/768/1024/1440 y
  comprobación Frankfurter live. Fixtures identificados como datos deterministas, nunca FX
  real.

## 5. Integración FX

Frankfurter v2 es consumido por FastAPI con tasas de referencia fechadas, caché 24 h desde
obtención y timeout 5 s; no es cotización continua. EUR usa identidad. La campaña separa
pruebas con tasas fixture y consulta real del proveedor. Fallo live significa 503 controlado,
sin valor ficticio; registrar disponibilidad/fecha/response observed.

## 6. Requisitos, arquitectura y límites

La reconciliación FR01–FR11 está en
[`final-delivery-traceability.md`](../../docs/requirements/final-delivery-traceability.md),
complementada por requisitos funcionales y SPEC. Países ES/PT/FR/DE/IT/NL, plan `standard`;
validación oficial algorítmica únicamente España, genérica no oficial en los demás; no prueba
existencia del titular. Impuestos generales versionados simplificados; consumos storage/API
sin cargos. Preview sin escritura, guardar explícito y snapshots persistentes. Arquitectura,
modelo 0001–0004 y secuencias están en
[`solution-overview.md`](../../docs/architecture/solution-overview.md).

La matriz de entrega se actualizará tras la validación, clasificando pendientes con su
motivo. P-05, ausencia de auth, límites SQLite, seguridad de exposición y WCAG integral siguen
siendo límites conocidos; no se declara producción pública.

## 7. Desarrollo asistido por IA

Evidencias textuales versionadas: requisitos, ADR, SPEC, planes, informes, auditorías y PRs
humanos indexados en `ai-workspace/README.md`. TASK047F documenta decisión real de priorizar
Windows 10 después de detectar problemas específicos de Actions, sin ocultar la corrección
responsive fallida. No se reconstruyen conversaciones ni prompts. El propietario debe aportar
4–8 extractos/capturas auténticos de chats privados, redactados y aprobados, si desea
demostrar ese aspecto con evidencia directa.

## 8. Capturas propuestas

Selección máxima de ocho archivos existente en `%LOCALAPPDATA%\Temp\opencode\TASK046\screenshots`:
dashboard, alta/ficha ES, rechazo fiscal, búsqueda, preview 15 EUR sin persistencia, guardado
EUR, guardado USD con FX fixture y `TASK047A/after-320-valid.png` (fixture interceptada).
Inventario, nombres exactos y alt text en `TASK047-evidence-inventory.md`. El propietario debe
aprobar publicación por separado. No se incluyen imágenes en commits.

## 9. Commits, integridad y publicación

| Commit                                                                 | SHA                                        | Estado                             |
| ---------------------------------------------------------------------- | ------------------------------------------ | ---------------------------------- |
| `ci: retain manual quality checks and document validation scope`       | `afd51b2a482988821d1466bf770077fd264f1fbc` | Push ordinario verificado          |
| `docs: finalize Windows 10 setup and AI-assisted development evidence` | Pendiente                                  | Se registrará al publicar commit 2 |
| `docs: record final Windows delivery validation`                       | Pendiente                                  | Se registrará al publicar commit 3 |

`main` local/remota no se modifica. No se crea PR ni se hace merge. Hashes protegidos y
artefactos TASK047 pendientes se comprobarán en el cierre. DOCX/TASKS.zip privados, bases de
datos y capturas permanecen fuera de publicación.

## 10. Hallazgos de CI aplazados

- A47-01: overflow de 14 px en 320 px en Linux CI; primera corrección no resolvió. Pendiente.
- A47-02: Angular health check no pasó en Windows Actions; local Windows había arrancado.
  Pendiente.
- A47-03: Bash no validó propiedad del PID en stop/restart Linux. Pendiente.
- Links/run SHA/resultados completos se encuentran en `docs/guides/continuous-integration.md`.
  CI solo manual y no ejecutada por TASK047F.

## 11. Criterios CA01–CA36

Se completará una tabla individual en el cierre con estados CUMPLIDO, CUMPLIDO CON
OBSERVACIONES, PARCIAL, INCUMPLIDO o NO VERIFICADO y evidencia concreta. Los resultados de
CI multiplataforma se marcarán aplazados/pendientes, nunca cumplidos por la campaña Windows.

## 12. Autoevaluación

Pendiente de campaña y revisión del paquete. Se evaluarán planificación/diseño (35), criterio
técnico/QA (25), software (30) y README/ejecución local (10), explicando puntos concedidos y
deducciones. No es una nota oficial del propietario del reto.

## 13. Veredicto TASK047F

Pendiente. Emitir uno de los veredictos limitados a Windows 10 definidos en la instrucción
solo después de revisar la campaña desde el clon y reconciliar CA01–CA36.
