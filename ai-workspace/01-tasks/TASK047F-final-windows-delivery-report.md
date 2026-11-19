# TASK047F — Informe final de entrega para Windows 10

> **VEREDICTO: APTA PARA ENTREGA EN ENTORNO WINDOWS 10 CON OBSERVACIONES.** La campaña única
> desde el clon limpio de `docs/final-delivery` pasó en el host Windows 10 observado. Los
> fallos históricos A47-01/02/03 siguen sin resolver y se aplazan por decisión expresa del
> propietario; Actions no se ejecutó y no se afirma compatibilidad multiplataforma ni
> preparación para producción.

## 1. Resumen y decisión de alcance

TASK047F sustituye las actuaciones pendientes TASK047/TASK047A2/TASK047B/TASK047C para la
entrega actual. Se priorizó Quick Start local Windows 10, trazabilidad del reto y evidencia
reproducible. No se modificó código funcional, tests, scripts, dependencias, migraciones ni
LICENSE. Solo los triggers de dos workflows pasaron a ejecución manual; sus jobs no cambiaron.

El clon y la validación se realizaron desde GitHub en la rama de entrega y SHA
`8bdaf377454e8d943de01e2df46f502534eb76fb`. Resultado de suites locales, integración, pricing,
persistencia, FX live, responsive y axe: PASS según los detalles siguientes. La validación no
certifica todos los equipos/revisiones Windows 10 ni otros sistemas operativos.

## 2. Estado inicial y entorno exacto

Estado inicial de la tarea: `docs/final-delivery`, HEAD y remoto
`54bd817b748f7769266a2d653353ffd4c8406775`; `origin/main`
`99c0ebac984c70521c4e3c94226b35c15303f572`; `main` local
`8371f9f608ce6e06984cc501d8240e1b7edf34d5`; índice vacío. El repo fue verificado público.

Entorno real informado desde el host de campaña, sin publicar identidad del usuario/equipo:

| Herramienta                               | Versión observada                                                                               |
| ----------------------------------------- | ----------------------------------------------------------------------------------------------- |
| Windows                                   | Windows 10 Pro 22H2, build 19045, arquitectura x64                                              |
| PowerShell                                | Windows PowerShell 5.1.19041.6456, Desktop                                                      |
| Git                                       | 2.56.0.windows.2                                                                                |
| Python del proyecto                       | 3.13.17 seleccionado con `py -3.13`; el comando global `python` resuelve 3.15.0 y no se utiliza |
| pip en Python 3.13                        | 26.2.2                                                                                          |
| Node.js / npm                             | 24.22.0 / 11.19.1                                                                               |
| Angular / Angular CLI                     | 22.2.6 / 22.2.6                                                                                 |
| TypeScript / RxJS                         | 6.0.3 / 7.8.2                                                                                   |
| FastAPI / Pydantic / SQLAlchemy / Alembic | 0.163.1 / 2.14.3 / 2.1.8 / 1.20.1 (venv del clon)                                               |
| SQLite                                    | 3.50.4 (runtime `sqlite3` embebido en Python; no se requiere CLI aparte)                        |
| pytest / Ruff / mypy                      | 9.2.0 / 0.17.5 / 2.4.1                                                                          |
| Vitest / Playwright Test                  | 5.1.1 / 1.65.1                                                                                  |
| Edge / Chrome instalados                  | 157.0.4341.60 / 157.0.8103.79 (no son los navegadores de la matriz E2E)                         |
| Navegadores Playwright                    | Chromium 159.0.8154.6 / Firefox 159.0 / WebKit 27.2                                             |

Compatibilidad declarada por manifests/scripts: Python `>=3.13,<3.14`, Node `>=24.15,<25`,
npm `>=11,<12`. No se inventan mínimos de CPU/RAM/almacenamiento. Prerrequisitos oficiales:
[Git for Windows](https://git-scm.com/download/win), [Python para Windows](https://www.python.org/downloads/windows/)
y [Node.js](https://nodejs.org/en/download). Angular CLI, SQLite y Playwright browsers no son
requisitos globales del Quick Start. Solo se afirma validación local en el corte Windows 10
descrito; no Windows 11, Linux, macOS ni Windows Server.

## 3. Clon limpio y Quick Start

Comando ejecutado expresamente contra GitHub:

```powershell
git clone --branch docs/final-delivery --single-branch https://github.com/Toni2Morales/SaaS-O-Matic.git <directorio-temporal>
cd <directorio-temporal>
```

El SHA del clon fue `8bdaf377454e8d943de01e2df46f502534eb76fb`, rama
`docs/final-delivery`, working tree limpio antes de la campaña. Se ejecutó literalmente el
Quick Start del README desde PowerShell en la raíz del clon. No se usó el árbol de trabajo
habitual como única evidencia.

| Medición observada                          |                                                                                        Resultado |
| ------------------------------------------- | -----------------------------------------------------------------------------------------------: |
| Clon GitHub limpio                          |                                                                                           2,13 s |
| Primera ejecución `start.ps1`               |                                                                                          73,83 s |
| `npm ci --ignore-scripts` primera ejecución |                                        29 s; 416 paquetes, 0 vulnerabilidades reportadas por npm |
| Parada propia y verificada                  |                                            0,99 s; API/UI terminaron y 8000/4200 quedaron libres |
| Segunda ejecución `start.ps1`               |                                                                                          47,68 s |
| `npm ci --ignore-scripts` segunda ejecución |                                                                               31 s; 416 paquetes |
| Smoke HTTP/funcional directo                |                                                                                           0,61 s |
| Puertos ocupados                            | 8000 y 4200 probados por separado; ambos abortaron con exit 1 y preservaron el listener del test |

Primera ejecución: el script creó `backend/.venv` Python 3.13, instaló backend solo dentro del
venv, pasó `pip check`, migró Alembic 0001–0004 y ejecutó `npm ci --ignore-scripts`; inició
FastAPI/Angular en loopback. Health `/health`, Swagger `/docs` y UI `/` respondieron HTTP 200.
Segunda ejecución repitió instalación declarada por el script, reaplicó migraciones
idempotentemente y conservó filas de SQLite. Tras reinicio se encontraron las dos
simulaciones guardadas del cliente sintético y quedó verificado su historial. La base propia
del clon está en `backend/var/saas_o_matic.sqlite3`; no se borró ni reutilizó la base del árbol
habitual. El script no inserta clientes de demo. Logs quedan bajo `%LOCALAPPDATA%\SaaS-O-Matic\run`.

URLs: Angular `http://127.0.0.1:4200`, Swagger `http://127.0.0.1:8000/docs`, OpenAPI
`/openapi.json`, health `http://127.0.0.1:8000/health`. La instalación descarga npm/Python;
Internet es necesaria para paquetes y referencias FX USD/GBP. EUR usa identidad sin proveedor.

Un listener que ocupaba 8000 o 4200 era creado y propiedad del test en el mismo proceso de
validación; el script hijo rechazó el puerto y el PID verificado siguió escuchando. Los
listeners propios se cerraron después de la aserción; ambos puertos quedaron libres. Ningún
proceso ajeno fue parado.

## 4. Verificación funcional real

Campaña HTTP/browser en los servicios Angular, FastAPI y SQLite temporales del clon:

- Dashboard Angular HTTP 200.
- Registro ES con `B12345674` sintético, y PT con identificador genérico sintético; el alta PT
  se completó también desde la interfaz. Validación fiscal ES inválida `B12345670` mostró
  error en UI. Es validación algorítmica, no verificación de existencia/titular.
- Búsqueda en UI y endpoint por razón social y por `B12345674`; ficha e historial abrieron.
- Para 15 usuarios ES, almacenamiento 250 GB y 100.000 llamadas/mes: subtotal `140.00`,
  impuesto `29.40`, total `169.40` EUR. Para 16: `148.00`, `31.08`, `179.08` EUR.
- Slider de teclado 15→16 actualizó la estimación; entrada manual 15 también. Los consumos
  fueron utilizables e informativos, sin cargo.
- Preview 15 dejó el historial en 1 (sin incrementar); guardado explícito lo incrementó a 2.
  La UI volvió a cargar ficha/historial tras reload, y la segunda ejecución de FastAPI
  conservó ambos snapshots.
- Cambio de moneda real desde UI: USD mostró `186,07 US$`, tasa `1.0984`, fecha `2026-11-19`;
  GBP mostró `141,27 £`, tasa `0.83392`, fecha `2026-11-19`; fuente en ambas respuestas
  `frankfurter`. No son valores fixture ni precios continuos de mercado.
- UI móvil 390 px: viewport 390, document `scrollWidth=390`, body `scrollWidth=390`; desktop
  1440 px visualizado. La matriz automatizada cubrió cinco rutas y 320/375/390/768/1024/1440
  en Chromium, Firefox y WebKit.
- Estados de error FX/control, límites, validaciones, teclado, navegación y formularios también
  se cubrieron por los tests E2E existentes con fixtures. Esos casos son pruebas de UI y no
  sustituyen el smoke live de FX.

Una primera petición del harness usó `.test` y el validador rechazó correctamente ese email
reservado con HTTP 422 antes de crear cliente; se cambió el dato sintético a `example.com` y
el flujo pasó. Asimismo, una captura temprana se tomó antes de resolver un cambio de moneda
asíncrono y mostró estado anterior mientras la UI indicaba “Preparando”; no se selecciona
como evidencia. La comprobación estable esperó POST y respuesta completa y confirmó USD/GBP.
Son ajustes del procedimiento de prueba, no defectos del producto.

### Capturas reales generadas en el clon

Ocho candidatos, todos fuera de Git en `%LOCALAPPDATA%\Temp\opencode\TASK047F\evidence-<run-id>\`,
con datos sintéticos y Angular/FastAPI/SQLite real del clon:

| Archivo                                            | Escenario                   | Integración                                       |
| -------------------------------------------------- | --------------------------- | ------------------------------------------------- |
| `dashboard-windows10.png`                          | Panel comercial             | API/SQLite reales                                 |
| `international-customer-pt-windows10.png`          | Alta y ficha PT             | API/SQLite reales; validación genérica no oficial |
| `customer-history-windows10.png`                   | Ficha/historial de cliente  | API/SQLite reales                                 |
| `fiscal-validation-windows10.png`                  | Identificador ES inválido   | API real, error visible                           |
| `simulator-preview-15-eur-windows10.png`           | 15 usuarios, EUR y consumos | Preview real, historial no cambia                 |
| `simulation-saved-eur-windows10.png`               | Guardado EUR explícito      | API/SQLite reales                                 |
| `simulator-preview-usd-live-settled-windows10.png` | Conversión USD              | Frankfurter live, fecha/tasa arriba               |
| `simulator-mobile-390-windows10.png`               | Simulador a 390 px          | API/SQLite reales                                 |

También existen `customer-search-windows10.png`, `simulator-preview-gbp-live-settled-windows10.png`
y capturas de depuración de cambio de divisa pendiente; la última no es candidata y no debe
presentarse como estado GBP final. Se aprueba una propuesta de ocho, pero **ninguna imagen se
publicó**. El propietario debe revisar/autorizar cualquier inclusión. La selección propuesta
incluye alt text en `TASK047-evidence-inventory.md`.

## 5. Calidad local del clon

Una sola campaña posterior a `npm ci --ignore-scripts` y QA backend aislado en el venv del
clon:

| Comprobación                                | Resultado                                                             |
| ------------------------------------------- | --------------------------------------------------------------------- |
| Ruff                                        | PASS                                                                  |
| Ruff format check                           | PASS, 90 archivos                                                     |
| mypy                                        | PASS, 88 source files                                                 |
| pip check                                   | PASS, sin dependencias rotas                                          |
| Pytest                                      | PASS, 579/579                                                         |
| Typecheck                                   | PASS                                                                  |
| ESLint                                      | PASS                                                                  |
| Prettier check                              | PASS                                                                  |
| Vitest con cobertura                        | PASS, 40/40                                                           |
| Cobertura V8                                | statements 86,20%; branches 81,86%; functions 67,19%; lines 86,84%    |
| Build Angular                               | PASS; bundle inicial raw 395,13 kB                                    |
| `npm audit` / `npm audit --omit=dev`        | PASS; ambos informaron 0 vulnerabilidades en ese momento              |
| Playwright completo Chromium/Firefox/WebKit | PASS: 79 aprobados, 20 skips opt-in, 0 fallidos                       |
| Axe                                         | PASS: nueve estados en Chromium, cero violaciones detectadas          |
| Matriz responsive existente                 | PASS en 320/375/390/768/1024/1440, cinco rutas y tres engines Windows |

Los 20 skips son opt-in preexistentes del proyecto y no se cuentan como pruebas aprobadas.
La suite E2E mantiene todos sus engines y aserciones. Dos mensajes no fatales de WebKit
`Importing a module script failed` se imprimieron durante la ejecución, pero suite terminó
79/20/0. Axe no constituye certificación WCAG integral.

Tiempo frontend (typecheck, lint, Prettier, Vitest/cobertura, build, audits y E2E): 204,90 s.
Instalar dependencias de desarrollo Python en el venv existente del clon: 26,23 s; checks
backend total 92,66 s. La campaña QA backend no instaló Python globalmente. npm audit depende
del registry/advisories en la fecha de consulta.

## 6. FX, fixtures y limitaciones económicas

La consulta live anterior usó Frankfurter a través del backend, no una conexión del navegador.
Rates recibidas en la fecha indicada son referencias fechadas, no cotización continua. FX
live se hizo separadamente de tests que usan fixtures; los fixtures solo estabilizan
verificaciones y no se muestran como valores live. Si Frankfurter no está disponible, el
backend responde 503 sin tasa inventada y EUR sigue operativo.

Seis países, un plan `standard`, IVA general simplificado, sin cargos por almacenamiento ni
llamadas. Validación oficial algorítmica solo España; identidad del titular no comprobada.
No hay autenticación, autorización, multi-tenancy, facturación ni cobro. SQLite restringe
concurrencia; P-05/hosting, proxy productivo y preparación de exposición pública siguen
pendientes. Sin declaración de producción.

## 7. Requisitos originales FR01–FR11 y arquitectura

La matriz [FR01–FR11 y entregables](../../docs/requirements/final-delivery-traceability.md)
se mantiene junto a los requisitos canónicos; refleja límites y evidencia TASK047F. Resumen:

| FR   | Resultado en alcance local                    | Límites                                                         |
| ---- | --------------------------------------------- | --------------------------------------------------------------- |
| FR01 | Alta ES/PT, plan `standard`                   | Seis países; no verificación de identidad                       |
| FR02 | Error/aceptación algorítmica ES               | Otros países genérico no oficial                                |
| FR03 | Simulaciones guardadas e historial/reload     | Sin editar/borrar; SQLite local                                 |
| FR04 | Usuarios, GB y llamadas validadas/registradas | Sin cargos de GB/llamadas; límites técnicos                     |
| FR05 | Pricing acumulativo API; 15/16 exactos        | Mensual, solo usuarios                                          |
| FR06 | Impuestos generales de seis países            | Sin asesoramiento ni regímenes especiales                       |
| FR07 | Dashboard y búsqueda nombre/tax ID            | Paginación limitada                                             |
| FR08 | Ficha e historial                             | Históricos no recalculados                                      |
| FR09 | Slider/manual, preview, guardar explícito     | Preview puede diferir al cambiar FX                             |
| FR10 | EUR/USD/GBP; FX mediado por backend           | Frankfurter referencia fechada; disponibilidad externa          |
| FR11 | Snapshots persistidos exactos                 | Conversión histórica no se reconstruye si campos heredados NULL |

API REST, SQLite, Alembic, arquitectura general/backend/frontend, modelo de datos y secuencias
preview/save/503 ya están documentados en requisitos, ADR, SPEC y
[`solution-overview.md`](../../docs/architecture/solution-overview.md); no se duplicaron
diagramas. Se comprobó navegación de enlaces relativos de la documentación preparada.

## 8. Desarrollo asistido por IA y evidencias pendientes

Proceso verificable: requisitos → ADR/SPEC → plan/tasks → autorización humana → cambios
iterativos → tests/auditorías → correcciones → commits/pushes. TASK047/TASK047A registran
honestamente hallazgos CI y la corrección fallida; TASK047F registra la priorización Windows 10. Los commits y PR #1–#7 prueban publicaciones/supervisión humana documentada, no cada
prompt. El modelo identificado para esta sesión TASK047F fue GPT-6 Luna/OpenCode; no atribuir
esta tarea a DeepSeek. Las evidencias privadas de chat no están en el repo y se solicita al
propietario aporte/apruebe 4–8 extractos si desea evidencia directa. No se fabricaron diálogos.

Guía de demo 5–10 minutos: [`docs/guides/demo.md`](../../docs/guides/demo.md), sintéticos,
sin consultas FX inventadas.

## 9. Git, commits y pushes

| Commit                                                                 | SHA completo                               | Push                                         |
| ---------------------------------------------------------------------- | ------------------------------------------ | -------------------------------------------- |
| `ci: retain manual quality checks and document validation scope`       | `afd51b2a482988821d1466bf770077fd264f1fbc` | Ordinario, remoto verificado                 |
| `docs: finalize Windows 10 setup and AI-assisted development evidence` | `8bdaf377454e8d943de01e2df46f502534eb76fb` | Ordinario, clonado remoto directo verificado |
| `docs: record final Windows delivery validation`                       | `83e41479853821b4bd85a9fd1ca9218d238e9c8b` | Push ordinario verificado                    |

Los workflows actuales contienen solo `workflow_dispatch`; no se ejecutaron manualmente ni
automáticamente durante TASK047F. `main` local y `origin/main` quedaron intactas. En el corte
TASK047F no se creó PR ni se hizo merge; TASK048 registra la revisión y creación de la PR.

## 10. Integridad y privacidad

El manifiesto inicial TASK047F cubre 290 tracked, seis artefactos documentales pendientes y
166 rutas protegidas. Los 166 hashes backend/frontend funcional, tests, scripts, migraciones,
manifests/lockfiles y LICENSE permanecieron iguales. README/ai-workspace/evidencia/guía y el
informe TASK047A se preservaron/actualizaron solo dentro del alcance documental aprobado.
La DB del clon se mantuvo bajo el clon temporal; las imágenes son externas. `Prueba Devs con
IA.docx` no se abrió, leyó ni hasheó, no se añadió al Git y permanece en su estado local
previo; `TASKS.zip` no se consultó. No hay secretos ni rutas privadas en los documentos.

## 11. Hallazgos de GitHub Actions (pendientes/aplazados)

- **A47-01:** [Quality #44556931530](https://github.com/Toni2Morales/SaaS-O-Matic/actions/runs/44556931530)
  identificó seis fallos responsive a 320 px y 334 px en Linux. No se reprodujo en Windows
  local. La corrección inicial publicada en `54bd817` no resolvió el defecto:
  [Quality #44566635410](https://github.com/Toni2Morales/SaaS-O-Matic/actions/runs/44566635410)
  repitió las seis fallas. **Abierto, no corregido**.
- **A47-02:** Angular health no pasó en el runner Windows:
  [Quick Start #44556931645](https://github.com/Toni2Morales/SaaS-O-Matic/actions/runs/44556931645),
  y volvió a aparecer en [#44566635425](https://github.com/Toni2Morales/SaaS-O-Matic/actions/runs/44566635425).
  Start local Windows 10 pasó. **Aplazado**.
- **A47-03:** Bash no validó propiedad PID en el stop/restart Linux en ambos Quick Start
  históricos anteriores. **Aplazado**.

Por decisión expresa del propietario, los workflows se conservan solo como dispatch manual;
los jobs/aserciones no se modificaron. El objetivo del reto se evalúa localmente Windows 10.
Estos resultados no se etiquetan como resueltos ni como pass multiplataforma.

## 12. Autoevaluación no oficial

| Categoría                     | Puntuación | Razonamiento                                                                                                                                                           |
| ----------------------------- | ---------: | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Planificación y diseño (35)   |      32/35 | Requisitos, 10 SPEC, ADR, matriz y planes trazables; faltan conversaciones privadas y revisión externa humana.                                                         |
| Criterio técnico y QA (25)    |      20/25 | 579 backend, 40 Vitest, Playwright tres motores, axe, audits e integración real; se deducen puntos por A47-01/02/03 aplazados y no tener certificación WCAG/seguridad. |
| Software entregado (30)       |      26/30 | Flujos principales y persistencia pasan localmente; límites de MVP/fiscalidad/SQLite y overflow CI conocido no resuelto.                                               |
| README y ejecución local (10) |       9/10 | Quick Start limpio Windows 10 medido y manual documentado; no se ensayó instalación manual completa independiente ni se cubren otros OS.                               |
| **Total**                     | **87/100** | Autoevaluación del implementador; no nota del propietario/evaluador ni aprobación de producción.                                                                       |

## 13. Reconciliación de criterios originales TASK047 (CA01–CA77)

`C` = cumplido; `CO` = cumplido con observaciones; `P` = parcial; `I` = incumplido; `NV` = no
verificado; `D` = diferido expresamente. El detalle/evidencia histórica permanece en
[`TASK047-final-delivery-report.md`](TASK047-final-delivery-report.md); esta tabla actualiza el
resultado del alcance de entrega actual.

|  CA | Estado |  CA | Estado |  CA | Estado |  CA | Estado |  CA | Estado |
| --: | :----: | --: | :----: | --: | :----: | --: | :----: | --: | :----: |
|  01 |   C    |  17 |   C    |  33 |   C    |  49 |   C    |  65 |   C    |
|  02 |   C    |  18 |   C    |  34 |   C    |  50 |   C    |  66 |   CO   |
|  03 |   C    |  19 |   C    |  35 |   C    |  51 |   P    |  67 |   CO   |
|  04 |   C    |  20 |   C    |  36 |   C    |  52 |   CO   |  68 |   C    |
|  05 |   C    |  21 |   C    |  37 |   C    |  53 |   C    |  69 |   C    |
|  06 |   C    |  22 |   C    |  38 |   C    |  54 |   C    |  70 |   C    |
|  07 |   C    |  23 |   C    |  39 |   C    |  55 |   C    |  71 |   C    |
|  08 |   C    |  24 |   C    |  40 |   C    |  56 |   C    |  72 |   C    |
|  09 |   D    |  25 |   C    |  41 |   C    |  57 |   C    |  73 |   C    |
|  10 |   C    |  26 |   C    |  42 |   C    |  58 |   P    |  74 |   C    |
|  11 |   C    |  27 |   CO   |  43 |   CO   |  59 |   C    |  75 |   C    |
|  12 |   C    |  28 |   C    |  44 |   D    |  60 |   C    |  76 |   C    |
|  13 |   C    |  29 |   C    |  45 |   C    |  61 |   C    |  77 |   C    |
|  14 |   C    |  30 |   C    |  46 |   C    |  62 |   C    |     |        |
|  15 |   C    |  31 |   C    |  47 |   C    |  63 |   CO   |     |        |
|  16 |   C    |  32 |   C    |  48 |   C    |  64 |   C    |     |        |

CO/P/D tienen justificación concreta: CA09 y CA44 son CI multiplataforma aplazado con
fallos históricos; CA27 manual alternativo solo documentado; CA43 static frontend CI histórico
pass, pero A47 Playwright fail y runs actuales no repetidos; CA51/58 conversación privada
pendiente; CA63 se verificó el procedimiento Quick Start, no una instalación manual autónoma;
CA66/67 registran la observación CI A47 y el límite axe; no ocultan las fallas. Los criterios
de varias plataformas y CI satisfactoria se aplazan por decisión expresa y no se convierten
en “cumplidos”. La ausencia de CI verde no constituye por sí sola incumplimiento del reto
original.

## 14. Criterios prioritarios TASK047F (CA01–CA36)

|  CA | Estado | Evidencia / justificación                                                                                         |
| --: | ------ | ----------------------------------------------------------------------------------------------------------------- |
|  01 | C      | Rama, HEAD, remoto, main e índice comprobados al inicio/cierre.                                                   |
|  02 | C      | Se reutilizaron seis documentos locales previstos; no se destruyó ninguno.                                        |
|  03 | C      | Windows 10 Pro 22H2 build 19045 x64, PowerShell 5.1 documentados.                                                 |
|  04 | C      | Versiones runtime/librerías/navegadores anotadas y fuente identificada.                                           |
|  05 | C      | Rangos y descargas oficiales de Git, Python, Node/npm documentados; no hardware inventado.                        |
|  06 | C      | README arriba incluye Quick Start, funcionalidades, URLs, entorno y límites.                                      |
|  07 | C      | `start.ps1` probado de clon público limpio, primer arranque PASS.                                                 |
|  08 | C      | Clon directo GitHub con rama/SHA verificados.                                                                     |
|  09 | C      | FastAPI health/API 200; Pytest PASS.                                                                              |
|  10 | C      | Angular UI HTTP 200 y flujos Playwright reales/fixtures según identificación.                                     |
|  11 | C      | Stop propio verificado; puertos libres después.                                                                   |
|  12 | C      | Segundo start y dos simulaciones preservadas/releídas tras restart.                                               |
|  13 | CO     | Manual backend/frontend documentado; inicio observado vía Quick Start, no campaña manual separada.                |
|  14 | C      | Flujos cliente, fiscal, búsqueda, historial, simulator y divisas verificados localmente.                          |
|  15 | C      | Totales 15/16 exactos y validación fiscal observada.                                                              |
|  16 | C      | USD/GBP consultados live vía backend; referencias fechadas y límites documentados.                                |
|  17 | C      | Pytest 579/579, Ruff/formato/mypy/pip check PASS.                                                                 |
|  18 | C      | Typecheck/lint/Prettier/Vitest/build/audits PASS.                                                                 |
|  19 | CO     | Matriz 6 anchos/5 rutas/3 motores PASS en Windows; A47-01 continúa fallando Linux CI y está aplazado.             |
|  20 | CO     | Axe 9 estados Chromium sin violaciones; no es certificación WCAG.                                                 |
|  21 | C      | Angular/FastAPI/SQLite reales, preview, guardado, historial/reload; FX live separado.                             |
|  22 | C      | Arquitectura y secuencias existentes revisadas/enlazadas; no se duplican diagramas.                               |
|  23 | C      | Matriz FR01–FR11 y limitaciones reconciliadas.                                                                    |
|  24 | C      | Índice ai-workspace y archivos TASK047F actualizados con fuentes y estados históricos.                            |
|  25 | P      | Planes/informes/commits son evidencia auténtica; conversaciones privadas directas quedan a cargo del propietario. |
|  26 | C      | Demo 5–10 min documentada con datos sintéticos.                                                                   |
|  27 | CO     | Ocho capturas nuevas fuera del repo, seleccionadas y descritas; publicación requiere aprobación del propietario.  |
|  28 | C      | Workflows Quality/Quick Start conservados solo como `workflow_dispatch`; jobs intactos y no ejecutados.           |
|  29 | C      | Cuatro links/run y fallos A47-01/02/03 documentados como abiertos/aplazados.                                      |
|  30 | C      | 166 hashes protegidos backend/frontend/tests/scripts/migraciones/dependencias/LICENSE intactos.                   |
|  31 | C      | DOCX, TASKS.zip, DBs e imágenes privadas/no aprobadas no publicados.                                              |
|  32 | C      | `gh repo view` confirmó repositorio público.                                                                      |
|  33 | C      | Informe final, evidencias, matriz, CI y limitaciones incluidos.                                                   |
|  34 | C      | Autoevaluación ponderada justificada 87/100, no oficial.                                                          |
|  35 | C      | Tres commits/pushes ordinarios verificados, SHA/ref citados.                                                      |
|  36 | C      | No PR, merge ni modificación de `main`.                                                                           |

## 15. Veredicto

**APTA PARA ENTREGA EN ENTORNO WINDOWS 10 CON OBSERVACIONES.** La aplicación, instalación
limpia, integración y QA local pasan en el host documentado. El veredicto está limitado a
Windows 10 y el alcance MVP. A47-01/02/03 siguen abiertos por decisión del propietario; no hay
certificación multiplataforma, WCAG integral ni preparación para producción pública. Las
capturas y chats privados requieren aprobación/aporte humano; imágenes no se publican.
