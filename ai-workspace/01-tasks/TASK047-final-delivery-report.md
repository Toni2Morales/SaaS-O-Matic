# TASK047 — Informe de estado y bloqueo

> **Registro histórico/supersedido para el alcance de entrega actual.** TASK047F, por decisión
> expresa del propietario, sustituye los hitos pendientes por una entrega validada localmente
> en Windows 10. Este informe conserva los fallos CI originales; no editar sus resultados ni
> interpretarlo como el veredicto final TASK047F. Véase
> [`TASK047F-final-windows-delivery-report.md`](TASK047F-final-windows-delivery-report.md).

> **INFORME PARCIAL — TAREA DETENIDA POR FALLAS BLOQUEANTES DE VERIFICACIÓN.**
> No es un certificado de aceptación ni un cierre final. No se corrige código funcional ni
> se continúa a Hito 4/5 hasta decisión/autorización humana. Estado escrito localmente, aún
> no publicado en un commit posterior a Hito 3.

## A. Resumen ejecutivo y veredicto

Se verificaron el merge de PR #7, se crearon/publicaron Hitos 1–3 en `docs/final-delivery`,
se probó Quick Start y manuales desde un clon limpio Windows, y pasaron los checks backend/
frontend del clon y los jobs estáticos/units en GitHub Actions. La primera ejecución real de
CI detectó dos bloqueos:

1. El Playwright Linux de GitHub Actions falla seis tests de responsive (dos casos en cada
   motor Chromium/Firefox/WebKit) a 320 px. El documento llega a 334 px, overflow real
   reportado por las pruebas existentes. No se ha alterado app ni pruebas.
2. Quick Start Actions falló en Windows esperando Angular y en Bash al verificar propiedad
   del PID de Angular al detenerlo. El API/smoke inicial de Linux sí arrancó y pasó antes de
   la falla del paso de parada.

Debido al fallo de pruebas funcionales/responsive preexistentes, se aplica la condición de
parada TASK047. **Veredicto: NO APTA PARA REVISIÓN FINAL DE ENTREGA.** Hitos 4/5, puntuación
final y CA01–CA77 completos quedan detenidos. No hay PR/merge/release ni imágenes publicadas.

## B. Estado Git y PR #7

- PR #7: MERGED por el propietario; merge commit confirmado
  `99c0ebac984c70521c4e3c94226b35c15303f572`.
- Repositorio `Toni2Morales/SaaS-O-Matic`: PUBLIC, observado por `gh repo view`.
- Rama actual: `docs/final-delivery`; `main` local protegido
  `8371f9f608ce6e06984cc501d8240e1b7edf34d5`; `origin/main` permanece
  `99c0ebac984c70521c4e3c94226b35c15303f572`.
- Commits publicados por push normal a la rama de documentación:

| Commit                                     | Mensaje                                                   | Alcance                                                              |
| ------------------------------------------ | --------------------------------------------------------- | -------------------------------------------------------------------- |
| `b7341e3b69f8b7edb6888fb261af7fb84b302f7b` | `build: simplify local application startup`               | Quick Start PS/Bash, guía local, plan/manifiesto                     |
| `fdc7b2c6ff83bbe403a684c56e835de9926c76ef` | `fix: harden Quick Start process handling`                | Codificación Windows PS5/Bash `--stop` sin prerrequisito innecesario |
| `ed35772c26951f2c89c98b912532df9a19557148` | `docs: prepare final SaaS-O-Matic delivery documentation` | README, arquitectura, pricing, reconciliación                        |
| `181afaf61174df2d9e7e817f27f6a7c79f5cf139` | `ci: add automated backend and frontend quality checks`   | Workflows CI, guía CI, enlace del README                             |

Cada push fue ordinario; se verificó igualdad HEAD/remoto en cada hito y `origin/main` no
cambió. No se creó PR ni se efectuó merge. GitHub anunció un nuevo PR al publicar rama; no
se abrió. Hitos 4/5 solo tienen archivos de trabajo local/untracked, no commit ni push.

## C. Quick Start, clon limpio e instalación manual

Clon limpio de Windows/PowerShell 5.1, descargado de `docs/final-delivery` en el commit
`b7341e3b69f8b7edb6888fb261af7fb84b302f7b`; Python 3.13.17, Node 24.22.0/npm 11.19.1.
PowerShell se ejecutó desde ruta con espacios.

- Primera ejecución Quick Start: **75,51 s**; venv, instalación Python dentro del venv,
  `pip check`, Alembic 0001–0004, `npm ci --ignore-scripts` (416 paquetes), health API y
  Angular HTTP 200.
- Smoke API en DB nueva temporal: alta española sintética; preview 15 usuarios **169.40 EUR**
  no persistida (historial 0); guardado explícito y total **169.40 EUR**; historial 1.
- Parada propia, segunda ejecución: **52,33 s**; DB/cliente/snapshot se conservaron; API y
  UI respondieron y el segundo stop dejó 8000/4200 libres. Test adicional con el puerto
  8000 ocupado abortó sin detener el listener controlado por el test.
- Instalación manual en el clon: `pip install -e ".[dev]" -c requirements.lock`, pip check,
  Alembic, `npm ci --ignore-scripts`, API y `npm start`: health/HTTP 200. Durante limpieza
  de ese test manual el predicado del harness no reconoció de inmediato la ruta normalizada
  de `ng`; se inspeccionó la cadena de procesos, se verificó que pertenecía al clon TASK047
  y se detuvieron exclusivamente Node/command-wrapper de esa cadena. Puertos quedaron libres.
- El primer harness de integración temporal consultó history después de apagar API, generó
  un error de wrapper después de que las pruebas hubieran pasado; se repitió con el orden
  corregido. La repetición terminó en PASS 1/1 + 1/1, tres snapshots tras restart, fixtures
  USD `1.0998`/GBP `0.83348`. No se consultó Frankfurter real.
- macOS no ejecutado. Linux/Ubuntu: Quick Start de Actions pasó arranque y smoke HTTP, pero
  falló parada/reinicio segura descrita más abajo; por tanto no se declara Quick Start Linux
  aceptado.
- El clon era la revisión inicial de scripts (antes de la corrección Windows fdc7b2c y antes
  de Hitos 2/3); el informe final obligatorio debe repetirse contra el último SHA al reanudar.

## D. Documentación entregada en Hitos 1–2

README raíz (Quick Start, stack, QA histórico vs actual, limitaciones y links); READMEs
backend/frontend actualizados; guía manual; Mermaid contexto/capas/frontend/DB/secuencias;
modelo pricing/tax/FX; matriz FR01–FR11 y reconciliación de entregables. Enlaces revisados en
scope y Prettier. No se reescribieron informes históricos ni se modificó LICENSE.

## E. GitHub Actions — runs reales observados

### Quality #44556931530

URL: https://github.com/Toni2Morales/SaaS-O-Matic/actions/runs/44556931530
Commit: `181afaf61174df2d9e7e817f27f6a7c79f5cf139`.

- Backend: PASS en 50 s (pip install/check, Ruff, Ruff format, mypy, Pytest).
- Frontend: PASS en 38 s (npm ci, typecheck, lint, Prettier, Vitest cobertura, build, ambos
  audits).
- Playwright: **FAIL en 3m34s**; 73 passed, 20 skipped, 6 failed. Fallaron los tests
  existentes `simulator.spec.ts:347` y `task045b-audit.spec.ts:251` en Chromium, Firefox y
  WebKit. A 320 px el documento tenía `scrollWidth=334`, `clientWidth=320` en la ruta
  `/customers/.../simulations/new`; overflow de 14 px. El viewport principal y varios
  componentes eran 320 px; `MAT-SLIDER` y notch outline reportaron anchos mayores. No se
  atribuye a instalación/browser ausente: browsers oficiales se instalaron y los tests
  terminaron. Axe no llegó al caso opt-in Firefox/WebKit; el job global falló.
- GitHub anotó que las actions fijadas con runtime Node 20 se forzaron a Node 24 (warning de
  deprecación). No fue la causa de las fallas.

El overflow es un fallo funcional/layout bajo la matriz existente y bloquea CA44/67. La tarea
prohíbe modificar implementación/tests y ordena detenerse ante este tipo de fallo; no se
oculta, corrige ni rebaja su severidad.

### Quick Start #44556931645

URL: https://github.com/Toni2Morales/SaaS-O-Matic/actions/runs/44556931645
Commit: `181afaf61174df2d9e7e817f27f6a7c79f5cf139`.

- Ubuntu: servicios iniciaron y los casos HTTP sintéticos de alta/preview/save/historial
  pasaron; el paso `Stop and restart services (Linux)` falló porque PID `2630` no coincidió
  con la firma registrada. `Stop services safely (Linux)` volvió a fallar por la misma
  verificación. No se forzó ninguna parada remota; runner GitHub efímero terminó.
- Windows: `npm ci --ignore-scripts` instaló 416 paquetes sin vulnerabilidades notificadas;
  backend/migraciones arrancaron. El script agotó el health-check de Angular tras unos 40 s
  (`Angular no respondió`), por lo que no llegó al smoke HTTP. Su catch detuvo los PIDs propios
  1880/8400. `frontend.log`/`frontend.err.log` quedaron en el runner que expiró y no se
  incorporaron al log de workflow; la causa exacta sigue sin determinar.
- Los fallos demuestran que los checks Quick Start multiplataforma no están aceptados. No
  hubo procesos persistentes del runner, pero no se han corregido estos fallos.

## F. Calidad en el clon limpio Windows

- Backend: **579/579 Pytest**; Ruff, Ruff format (90), mypy (88), pip check PASS.
- Frontend: typecheck, ESLint, Prettier, build, `npm audit` y `--omit=dev` PASS; 0 advisories
  reportados. Vitest **40/40**.
- V8: statements **86,27 %**; branches **81,86 %**; functions **67,72 %**; lines **86,93 %**.
- Playwright Windows: **79 PASS/20 skips opt-in**, 99 casos; 0 fallos. Dos mensajes no fatales
  en WebKit `Importing a module script failed`. Axe: 9 estados Chromium sin violaciones
  detectadas; matriz responsive de la suite pasó en Windows en los viewports existentes.
- El run no se suma a TASK046; es una ejecución separada del clon Windows.
- Auditorías npm no son auditoría de seguridad absoluta. Axe no certifica WCAG.

## G. Integración real separada

Clon limpio Windows, FastAPI + Angular + SQLite recién migrada 0001–0004; adaptador de FX
determinista aplicado en el puerto de dependency injection existente. Playwright browser/API/
SQLite **1/1 PASS**, reinicio backend/history **1/1 PASS**, tres snapshots recuperados. Rates
fixture sintéticas (USD `1.0998`, GBP `0.83348`), no se presentan como cotizaciones live. El
directorio SQLite/fixture es temporal y propio; ports 8000/4200 cerrados.

## H. SDD, evidencias y privacidad

La reconciliación canónica y el inventario distinguen documentos auténticos versionados de
conversaciones privadas no disponibles. El propietario debe proporcionar/autorizar de cuatro
a ocho capturas o extractos reales de conversaciones IA; no se fabrican prompts/modelos.
Capturas funcionales TASK042–TASK046 se inventarían en fichero local; **ninguna imagen se
copió, publicó o enlazó**. Selección propuesta (9) pendiente de aprobación del propietario.
TASK042 screenshots listados en su informe no se hallaron en el directorio temporal buscado.

DOCX del reto privado no se abrió, hashó ni staged. LICENSE intacta. Manifiesto inicial tenía
276 tracked files; a la comprobación inicial al desarrollar se mantenían y los cambios
tracked estaban limitados a documentación; la revisión completa de hashes al cierre aún está
pendiente. No hay cambios de código funcional, pruebas existentes, dependencias ni migraciones.

## I. Autoevaluación (no oficial)

**No puntuada:** el gate de Playwright en tres browsers falló por responsive 320 px y el CI
Quick Start falló en Windows/Linux. Fijar puntuación antes de resolver los bloqueos produciría
una valoración engañosa. No es una nota oficial.

## J. Riesgos residuales y trabajo detenido

- **Bloqueante:** overflow UI medido en Linux runner en viewport 320 px; afecta pruebas
  existentes del simulador y responsive. Requiere que el propietario/arquitecto decida si se
  autoriza una tarea posterior de producto/corrección; TASK047 no lo cambia.
- **Bloqueante entrega:** Quick Start Actions no pasó ambos OS (Windows frontend health,
  Linux safe stop); logs Windows no disponibles tras finalizar runner.
- **Acciones obsoletas:** workflow emitió advertencia Node 20 forzado a 24; funcionamiento no
  falló por esto, pero mantenimiento de pins queda pendiente.
- **P-05**, autenticación/autorización, falta de facturación real, SQLite y límites fiscales/
  FX descritos en README y matriz siguen vigentes. No declarar producción.
- **Hitos 4/5 no realizados:** SDD/evidencias finales, guía demo publicada, badges, nueva
  verificación final desde el commit más reciente, autoevaluación y auditoría final.
- Este informe y ficheros locales de Hito 4 permanecen sin commit/push; solo están publicados
  los Hitos 1–3 y el commit de corrección Quick Start. `README.md` local se actualizó para
  reflejar los runs fallidos, pero no se hizo commit/push tras el bloqueo; el README público
  de la rama, al SHA de Hito 3, aún marca las ejecuciones como pendientes.

## K. Criterios de aceptación

Evaluación del estado detenido; no equivale al cierre TASK047. `CUMPLIDO CON OBSERVACIONES`
indica evidencia real con limitaciones documentadas.

|  CA | Estado                     | Evidencia / razón                                                                               |
| --: | -------------------------- | ----------------------------------------------------------------------------------------------- |
|  01 | CUMPLIDO                   | PR #7 MERGED y merge commit comprobado por `gh`.                                                |
|  02 | CUMPLIDO                   | `origin/main` actualizado al merge de PR #7.                                                    |
|  03 | CUMPLIDO                   | `docs/final-delivery` creada desde `origin/main`.                                               |
|  04 | CUMPLIDO                   | `main` local `8371f9f6…` no modificado.                                                         |
|  05 | CUMPLIDO                   | Plan TASK047 creado antes de implementar.                                                       |
|  06 | CUMPLIDO                   | Manifiesto SHA-256 de 276 rutas tracked originales.                                             |
|  07 | CUMPLIDO                   | `gh repo view` confirma repositorio PUBLIC.                                                     |
|  08 | CUMPLIDO CON OBSERVACIONES | `start.ps1` probado en Windows; Actions no consiguió health Angular en el runner.               |
|  09 | CUMPLIDO CON OBSERVACIONES | `start.sh` arrancó/smokeó en Ubuntu; stop no verificó la firma de PID.                          |
|  10 | CUMPLIDO                   | Versiones/prerrequisitos probados localmente en Windows y por scripts en runners.               |
|  11 | CUMPLIDO                   | `.venv` Python 3.13 probado en clon limpio; no sustituye venv incompatible.                     |
|  12 | CUMPLIDO                   | `pip install` confinado al venv; `npm ci --ignore-scripts` reproducible.                        |
|  13 | CUMPLIDO                   | Alembic 0001–0004 aplicadas en DB nueva temporal.                                               |
|  14 | CUMPLIDO                   | FastAPI health y endpoints disponibles en clone/API runner.                                     |
|  15 | CUMPLIDO CON OBSERVACIONES | UI HTTP 200 en Windows local/clon y Linux start; Windows Actions Angular sin health.            |
|  16 | CUMPLIDO CON OBSERVACIONES | Health checks detectan timeout; Windows runner falló y Linux startup sí respondió.              |
|  17 | CUMPLIDO                   | URLs frontend, Swagger y health comunicadas en ambos scripts/README.                            |
|  18 | CUMPLIDO CON OBSERVACIONES | Stop Windows propio verificado; Linux Actions bloqueó por firma PID.                            |
|  19 | CUMPLIDO CON OBSERVACIONES | Restart/persistencia Windows limpio PASS; Linux workflow no alcanzó restart.                    |
|  20 | CUMPLIDO CON OBSERVACIONES | SQLite limpia del clon preservó datos sintéticos; una fila QA quedó en DB local ignorada.       |
|  21 | CUMPLIDO CON OBSERVACIONES | PowerShell port ocupado abortó y preservó listener; Bash requiere revisar stop ownership.       |
|  22 | CUMPLIDO CON OBSERVACIONES | Windows probado; Linux Quick Start parcial/fallido; macOS no probado.                           |
|  23 | CUMPLIDO CON OBSERVACIONES | README profesional/Quick Start redactados; informe/artefactos Hito4–5 aún locales.              |
|  24 | CUMPLIDO                   | Quick Start al inicio del README y tres comandos por plataforma.                                |
|  25 | CUMPLIDO                   | Funcionalidades y límites reconciliados con requisitos y código.                                |
|  26 | CUMPLIDO                   | Versiones contrastadas con manifests, ADR y runtime.                                            |
|  27 | CUMPLIDO                   | Instalación manual backend, venv, migración y tests en clon.                                    |
|  28 | CUMPLIDO                   | `npm ci --ignore-scripts` y `npm start` manual con UI HTTP 200.                                 |
|  29 | CUMPLIDO                   | Endpoints Swagger/OpenAPI documentados.                                                         |
|  30 | CUMPLIDO                   | Puertos, dependencias, migraciones, FX, proxy y PowerShell tratados.                            |
|  31 | CUMPLIDO                   | Separa evaluación local de exposición/producción no validada.                                   |
|  32 | CUMPLIDO                   | Diagrama Mermaid de contexto creado.                                                            |
|  33 | CUMPLIDO                   | Diagrama de capas backend creado conforme ADR-0002 y composición real.                          |
|  34 | CUMPLIDO                   | Diagrama Angular Router/features/forms/signals/RxJS/HTTP creado.                                |
|  35 | CUMPLIDO                   | ER Mermaid inspeccionado contra modelos/migraciones, JSON snapshot como TEXT.                   |
|  36 | CUMPLIDO                   | Secuencia preview sin DML creada.                                                               |
|  37 | CUMPLIDO                   | Secuencia guardado/201/historial creada.                                                        |
|  38 | CUMPLIDO                   | Secuencia error FX/503/retry/EUR creada.                                                        |
|  39 | CUMPLIDO                   | Estructura de carpetas resumida/documentada.                                                    |
|  40 | CUMPLIDO                   | Formula acumulativa y diez importes de referencia incluidos.                                    |
|  41 | CUMPLIDO                   | Tasas seis países, FX, rounding/snapshots y limitaciones documentados.                          |
|  42 | CUMPLIDO                   | Backend CI real PASS (579 tests y análisis estático).                                           |
|  43 | CUMPLIDO                   | Frontend CI real PASS (unit, lint, typecheck, build, audits).                                   |
|  44 | INCUMPLIDO                 | Playwright CI falló seis responsive tests de 320 px en tres browsers; 334 px documentWidth.     |
|  45 | CUMPLIDO CON OBSERVACIONES | SHA pins, permisos y runner aislado; GitHub advierte runtime Node20 obsoleto.                   |
|  46 | CUMPLIDO CON OBSERVACIONES | Runs/URLs reales verificados, pero Quality/Quick Start concluyeron failure.                     |
|  47 | PARCIAL                    | Badges no añadidos; runs no están todos en estado exitoso.                                      |
|  48 | CUMPLIDO CON OBSERVACIONES | Índice SDD actualizado localmente; Hito4 no commit/push.                                        |
|  49 | CUMPLIDO CON OBSERVACIONES | SDD explicado con mapa de fases y evidencias; aún no publicado el update de índice.             |
|  50 | CUMPLIDO CON OBSERVACIONES | Documentos textuales auténticos seleccionados en inventario local.                              |
|  51 | PARCIAL                    | Conversaciones/capturas auténticas de ChatGPT/OpenCode deben aportarse por propietario.         |
|  52 | CUMPLIDO CON OBSERVACIONES | Capturas TASK043–046 catalogadas; carpeta TASK042 nombrada históricamente no localizada.        |
|  53 | CUMPLIDO                   | Selección reducida, requisitos demostrados, alt text y ubicación propuestos.                    |
|  54 | CUMPLIDO                   | Ninguna imagen/DOCX/secretos publicada; capturas sintéticas externas.                           |
|  55 | CUMPLIDO CON OBSERVACIONES | Guía de demo 5–10 min escrita; Hito4 no commit/push.                                            |
|  56 | CUMPLIDO CON OBSERVACIONES | Matriz FR01–FR11 y límites creada; hito actual test responsive fallido.                         |
|  57 | CUMPLIDO                   | Resumen original autorizado contrastado; privado DOCX no se abrió.                              |
|  58 | PARCIAL                    | Repo público/ai-workspace/diseño/calidad trazados; interacción privada pendiente.               |
|  59 | CUMPLIDO                   | Límites de MVP, FX, SQLite, auth y P-05 documentados.                                           |
|  60 | CUMPLIDO                   | A39-07/08, A39-11–15 y P-05 reconciliados sin corregirlos.                                      |
|  61 | CUMPLIDO CON OBSERVACIONES | Clon limpio de commit inicial de scripts efectuado; falta clonar SHA final posterior a docs/CI. |
|  62 | CUMPLIDO CON OBSERVACIONES | Quick Start literal Windows, persistencia y restart PASS; runner Linux stop falló.              |
|  63 | CUMPLIDO CON OBSERVACIONES | Backend/frontend manual comprobados en clon Windows; no se repitió en Linux/macOS.              |
|  64 | CUMPLIDO                   | Integración real API/Angular/SQLite determinista y post-restart 1/1 cada una.                   |
|  65 | CUMPLIDO                   | Backend Pytest 579/579 y static checks PASS en clon.                                            |
|  66 | CUMPLIDO CON OBSERVACIONES | Vitest/typecheck/lint/build PASS, pero Playwright multibrowser CI tuvo fallos.                  |
|  67 | INCUMPLIDO                 | Axe sin violaciones en Chromium; responsive 320 px falló en CI y no hay WCAG cert.              |
|  68 | CUMPLIDO CON OBSERVACIONES | Audits npm 0 advisories en clon y job; no son auditoría integral.                               |
|  69 | CUMPLIDO                   | Manifiesto/pruebas mostraron código, tests, manifests, migrations y LICENSE intactos.           |
|  70 | CUMPLIDO                   | Hitos 1–3 y pushes ordinarios verificados contra refs remotas.                                  |
|  71 | CUMPLIDO CON OBSERVACIONES | Enlaces de documentos Hito2 revisados; Hito4/5 locales no se publicaron.                        |
|  72 | INCUMPLIDO                 | Informe final está en estado parcial/bloqueado, no auditoría/cierre final.                      |
|  73 | NO VERIFICADO              | No se puntuó; los bloqueos invalidan una valoración de entrega.                                 |
|  74 | CUMPLIDO                   | `Prueba Devs con IA.docx` excluido; no se leyó ni hasheó.                                       |
|  75 | CUMPLIDO                   | `main` local/remota no se modificó; no se hizo merge.                                           |
|  76 | CUMPLIDO                   | Ninguna imagen pendiente de aprobación se publicó.                                              |
|  77 | CUMPLIDO                   | No se abrió PR, no merge, tag, release ni entrega externa.                                      |

Los criterios con estado distinto de `CUMPLIDO` quedan justificados por la limitación/fallo
indicado; Hitos 4–5 no se ejecutaron tras aplicar condición de parada.
