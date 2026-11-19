# TASK047A — Informe técnico de corrección responsive

> **A47-01 NO RESUELTO.** La corrección publicada pasa las validaciones locales Windows, pero
> el run GitHub Actions del commit TASK047A volvió a reproducir el overflow. Se detuvo tras
> ese resultado; no se intentó otra solución.

## A. Resumen ejecutivo

- Hallazgo: overflow del simulador a viewport 320 px en Chromium/Firefox/WebKit.
- Base: `181afaf61174df2d9e7e817f27f6a7c79f5cf139`.
- Corrección localizada en CSS del componente del simulador, más ampliación de matriz
  responsive con 375 px.
- La suite Playwright Windows completa pasó (79 PASS/20 skips); checks frontend y backend
  locales pasaron. La nueva Quality CI en `54bd817b748f7769266a2d653353ffd4c8406775` volvió
  a fallar las seis aserciones responsive originales con documentWidth 334 px.

## B. Diagnóstico

Run original: [Quality #44556931530](https://github.com/Toni2Morales/SaaS-O-Matic/actions/runs/44556931530),
Linux runner, SHA base. Seis fallos eran dos aserciones existentes repetidas en tres browsers:

| Prueba                       | Aserción original                          |
| ---------------------------- | ------------------------------------------ |
| `simulator.spec.ts:347`      | `body.scrollWidth <= innerWidth`           |
| `task045b-audit.spec.ts:251` | document/body no superan ancho de viewport |

Ambas referían `/customers/<id>/simulations/new` a 320 px, `scrollWidth=334` frente a
`clientWidth=320`. El log diagnóstico observa `.panel` a 280 px, `FORM` a 246 px y
`FORM.scrollWidth=297` (form empieza en x=37; su contenido alcanza el borde documentado de
334 px). La regla de `.field-heading` era una fila flex con `justify-content:space-between`
sin wrap; sus textos «Control deslizante» y «Entrada manual: 0–1.000.000» son los
responsables más probables de exceder el ancho mínimo intrínseco en el runner Linux. La
intervención de permitir wrap es coherente con esa geometría. No se cuenta con DOM replay
que pruebe causalidad exclusiva del encabezado; Windows pasa la prueba original incluso
antes del cambio, por diferencia de métricas/maquetación entre entornos. La ejecución CI nueva
conservó `FORM.scrollWidth=297` y document width 334 a pesar del wrap; por ello `.field-heading`
no era la causa suficiente. El elemento real que expande el formulario/documento sigue sin
aislarse. No se seguirá diagnosticando ni se cambiarán otras reglas sin nueva autorización.

`MAT-SLIDER` mostraba scroll interno en el diagnóstico, pero la caja `x=45..291` seguía
dentro del viewport de 320 px; no se modificó. GitHub no subió artifacts y el endpoint de
artifacts del run no devolvió ninguno; no hubo captura “antes”. No se instaló WSL, Docker ni
software del sistema.

## C. Solución

En `frontend/src/app/features/simulations/simulation-page.ts` se añadió
`.field-heading { flex-wrap: wrap; }` dentro de `@media (max-width: 760px)`. Los rótulos y
controles permanecen visibles; el encabezado conserva una fila cuando cabe y puede ocupar
dos líneas en ancho estrecho. Esto conserva legibilidad, pero el nuevo CI demuestra que no
resuelve el overflow observado. No se ocultó ni recortó contenido, no se alteró el slider ni
se usó overflow para tapar el problema.

En `frontend/e2e/task045b-audit.spec.ts` se incorpora 375 px a la lista existente
`[320, 390, 768, 1024, 1440]` → `[320, 375, 390, 768, 1024, 1440]`. No se quitaron ni
relajaron casos/aserciones. Las pruebas ya existentes comprueban las cinco rutas responsive
y el simulador a 320 px, incluido slider de teclado y 15→16 usuarios; no se añadió prueba
duplicada.

## D. Validaciones locales

- Antes del CSS, las dos pruebas responsive originales pasaron en Windows/Chromium: 2/2;
  el defecto Linux no se reproduce en ese host.
- Después del cambio, las dos pruebas originales pasaron en Chromium, Firefox y WebKit:
  **6/6**.
- Playwright completo Windows: **79 PASS, 20 skips opt-in, 0 fallos** (99 tests). Los skips
  son opt-in preexistentes y no se cuentan como PASS. Dos mensajes no fatales de WebKit de
  importación dinámica ocurrieron durante la ejecución.
- La matriz responsive de TASK045B pasó en 320, **375**, 390, 768, 1024 y 1440 px para
  dashboard, clientes, alta, ficha e inicio de simulador en los tres browsers.
- Axe en Chromium: nueve estados ejecutados, cero violaciones detectadas. No es certificación
  integral WCAG.
- Typecheck, ESLint, Prettier, Vitest **40/40**, build, `npm audit` y
  `npm audit --omit=dev`: PASS; ambos audits notificaron cero vulnerabilidades.
- Cobertura V8 (cambio CSS/E2E, código de dominio sin cambios): statements **86,20 %**,
  branches **81,86 %**, functions **67,19 %**, lines **86,84 %**.
- Backend: Ruff, Ruff format, mypy, pip check y Pytest **579/579** PASS.

## E. Evidencias visuales

Capturas Chromium reales posteriores, generadas con cliente y respuestas API sintéticos
interceptados; importes calculados en fixture determinista, no son integración ni cotización
FX en vivo:

| Archivo                          |            Viewport | Escenario                                                           |
| -------------------------------- | ------------------: | ------------------------------------------------------------------- |
| `after-320-valid.png`            |  320×1859 full page | 15 usuarios, total 169,40 EUR                                       |
| `after-320-maximum-users.png`    |  320×1883 full page | 1.000.000 usuarios, total fixture 6.050.205,70 EUR; cifras visibles |
| `after-320-validation-error.png` |  320×1845 full page | 1.000.001 usuarios, error de validación visible                     |
| `after-390-valid.png`            |  390×1737 full page | 15 usuarios en viewport móvil                                       |
| `after-1440-valid.png`           | 1440×1122 full page | distribución desktop                                                |

Conservación externa: `%LOCALAPPDATA%\Temp\opencode\TASK047A\evidence-<run-id>\`.
Las imágenes no se incluyeron en Git. La captura previa no existe: no hubo artifact CI y
Windows no reprodujo el defecto antes de la corrección.

## F. Integración real temporal

El test existente `task045b-real-integration.spec.ts` pasó 1/1 con FastAPI, Angular y SQLite
nueva migrada 0001–0004. Post-reinicio backend/historial pasó 1/1 y se verificaron tres
snapshots. Se inyectaron tasas deterministas fixture USD 1.0998/GBP 0.83348; no se consultó
Frankfurter en vivo.

Ambas pruebas finalizaron PASS. El harness exterior devolvió exit code 1 después porque el
proceso padre del servidor ya había terminado cuando el cleanup intentó detenerlo; el
verificador confirmó luego 8000/4200 libres y eliminó únicamente el directorio temporal
propio. No se atribuye ese error de cleanup al producto ni se esconde en la evidencia.

## G. Integridad y privacidad

Manifiesto inicial TASK047A: 287 archivos tracked y cinco documentos preexistentes TASK047
hasheados por separado. En la comprobación previa a commit, los únicos hashes tracked
distintos eran `frontend/src/app/features/simulations/simulation-page.ts` y
`frontend/e2e/task045b-audit.spec.ts`; los cinco documentos pendientes conservaban sus
hashes. No hubo cambios en backend, dependencias, manifiestos/lockfiles, Quick Start, workflows
ni LICENSE. El test temporal de capturas se eliminó tras ejecutarse. DOCX privado no se abrió,
leyó ni incluyó.

## H. Publicación y nueva CI

Commit `54bd817b748f7769266a2d653353ffd4c8406775`, mensaje
`fix: resolve simulator overflow on narrow viewports`; push ordinario verificado a
`origin/docs/final-delivery`. `origin/main` y `main` local no cambiaron. No se creó PR ni hubo
merge. Este informe recibió los resultados post-push localmente; por la autorización de un
solo commit no se hizo un segundo commit/push. El README, ai-workspace README y artefactos
TASK047 existentes también permanecen locales sin publicar.

Runs asociados exactamente al SHA `54bd817b748f7769266a2d653353ffd4c8406775`:

- [Quality #44566635410](https://github.com/Toni2Morales/SaaS-O-Matic/actions/runs/44566635410):
  backend y frontend PASS; Playwright **FAIL**. Repitió los mismos seis fallos originales en
  la ruta del simulador a 320 px, Chromium/Firefox/WebKit. Persistió `scrollWidth=334`,
  `clientWidth=320` y `.field-heading` wrap no modificó `FORM.scrollWidth=297`. Suite: 73
  passed/20 skipped/6 failed. Job de integración se omitió al fallar el Playwright gate. Esto
  confirma que A47-01 sigue sin resolverse y refuta la hipótesis `.field-heading` como causa
  raíz suficiente.
- [Quick Start #44566635425](https://github.com/Toni2Morales/SaaS-O-Matic/actions/runs/44566635425):
  Ubuntu pasó start y smoke HTTP, pero parada/reinicio y limpieza fallaron porque PID 2677 no
  coincide con el comando registrado. Windows volvió a agotar el health-check Angular tras
  `npm ci`; el script limpió los procesos que inició. Logs de error/redirección no se
  incorporaron al log de Actions; causas restantes no determinadas. No se modificó el workflow
  ni scripts, fuera de alcance TASK047A.

Los resultados Quick Start se registran por trazabilidad; no se intentó corregir ese problema.
No se añadieron badges.

## I. A47-02/A47-03

Siguen pendientes, fuera de TASK047A y sin cambios. Los fallos previos de Quick Start no se
abordan aquí.

## J. Veredicto TASK047A

**A47-01 NO RESUELTO.** El run Quality #44566635410 reprodujo el mismo overflow de 14 px y
fallaron las seis pruebas originales. La corrección publicada no solucionó el defecto. La
siguiente diagnosis/corrección exige nueva autorización TASK047B; no se hicieron más cambios.

## K. Criterios de aceptación CA01–CA56 (estado final observado)

|  CA | Estado                     | Evidencia / observación                                                                                   |
| --: | -------------------------- | --------------------------------------------------------------------------------------------------------- |
|  01 | CUMPLIDO                   | Repositorio `Toni2Morales/SaaS-O-Matic` y remoto comprobados.                                             |
|  02 | CUMPLIDO                   | Rama actual `docs/final-delivery`.                                                                        |
|  03 | CUMPLIDO                   | HEAD inicial `181afaf61174df2d9e7e817f27f6a7c79f5cf139`.                                                  |
|  04 | CUMPLIDO                   | `origin/docs/final-delivery` coincide con HEAD inicial.                                                   |
|  05 | CUMPLIDO                   | `main` local/remota se mantuvieron intactas.                                                              |
|  06 | CUMPLIDO                   | Plan TASK047A redactado antes de editar frontend.                                                         |
|  07 | CUMPLIDO                   | Manifiesto SHA-256 incluye 287 tracked y 5 pendientes TASK047; DOCX excluido.                             |
|  08 | CUMPLIDO                   | Logs del run original y resultado Playwright #44556931530 consultados.                                    |
|  09 | CUMPLIDO                   | Identificadas dos pruebas, tres motores, viewport/assercciones y 6 fallos.                                |
|  10 | CUMPLIDO CON OBSERVACIONES | Windows original no reproduce; nueva versión se probó antes/después, CI Linux pendiente.                  |
|  11 | PARCIAL                    | DOM acota `FORM` desbordada; flex-wrap intentado no cambia el fallo CI; raíz aún no aislada.              |
|  12 | CUMPLIDO CON OBSERVACIONES | Reproducción inicial intentada; en Windows original pasó.                                                 |
|  13 | PARCIAL                    | La hipótesis `.field-heading` como causa fue refutada por la nueva CI; raíz pendiente.                    |
|  14 | CUMPLIDO                   | CSS limitado a `.field-heading` en media query móvil.                                                     |
|  15 | CUMPLIDO                   | No se oculta contenido ni se aplicó `overflow-x:hidden`/hacks.                                            |
|  16 | INCUMPLIDO                 | CI en commit publicado volvió a medir 334 > 320 px; local Windows pasa, no basta.                         |
|  17 | CUMPLIDO CON OBSERVACIONES | Chromium local responsive PASS; mismo caso CI Chromium volvió a fallar.                                   |
|  18 | CUMPLIDO CON OBSERVACIONES | Firefox local responsive PASS; mismo caso CI Firefox volvió a fallar.                                     |
|  19 | CUMPLIDO CON OBSERVACIONES | WebKit local responsive PASS; mismo caso CI WebKit volvió a fallar.                                       |
|  20 | CUMPLIDO CON OBSERVACIONES | Matriz 6 widths/5 rutas/3 motores local PASS; CI conserva overflow a 320 px.                              |
|  21 | CUMPLIDO                   | Suite Playwright completa mantiene desktop; screenshot 1440 px generado.                                  |
|  22 | CUMPLIDO                   | Slider de teclado y resumen móvil comprobados por test original; captura móvil.                           |
|  23 | CUMPLIDO                   | Captura/fixture de 1.000.000 usuarios muestra importes completos.                                         |
|  24 | CUMPLIDO                   | Test y captura de validación 1.000.001 visibles a 320 px.                                                 |
|  25 | CUMPLIDO                   | Axe nueve estados Chromium sin violaciones detectadas; no certifica WCAG integral.                        |
|  26 | CUMPLIDO                   | Sin cambios de pricing; tests previos e integración continúan pasando.                                    |
|  27 | CUMPLIDO                   | Sin cambios de impuestos; backend y resultados de referencia pasan.                                       |
|  28 | CUMPLIDO                   | Sin cambios de FX; integración emplea fixture, no proveedor live.                                         |
|  29 | CUMPLIDO                   | Preview/guardado/historial pasan suite e integración dedicada.                                            |
|  30 | CUMPLIDO                   | No se cambian ni borran pruebas existentes; matriz se amplía en +375 px.                                  |
|  31 | CUMPLIDO CON OBSERVACIONES | Test de overflow existente cubre defecto; se amplió matriz, no hay test causal dedicado.                  |
|  32 | CUMPLIDO                   | Vitest 40/40.                                                                                             |
|  33 | CUMPLIDO                   | Typecheck PASS.                                                                                           |
|  34 | CUMPLIDO                   | ESLint PASS.                                                                                              |
|  35 | CUMPLIDO                   | Prettier PASS.                                                                                            |
|  36 | CUMPLIDO                   | Build PASS.                                                                                               |
|  37 | INCUMPLIDO                 | Playwright CI volvió a fallar las seis aserciones responsive; Windows suite pasa.                         |
|  38 | CUMPLIDO CON OBSERVACIONES | Axe automatizado PASS; no certificación WCAG.                                                             |
|  39 | CUMPLIDO                   | Pytest 579/579, Ruff, mypy, format, pip check PASS; sin cambios backend.                                  |
|  40 | CUMPLIDO CON OBSERVACIONES | Dos tests integración PASS; harness de cleanup emitió error de proceso padre ya terminado, ports limpios. |
|  41 | CUMPLIDO                   | npm audits normal y producción: cero vulnerabilidades reportadas.                                         |
|  42 | CUMPLIDO CON OBSERVACIONES | Cinco PNG reales fuera del repo; “antes” no disponible y no se fabrica.                                   |
|  43 | CUMPLIDO                   | Package manifests/lockfiles intactos.                                                                     |
|  44 | CUMPLIDO                   | Backend/migraciones/dependencias Python intactos.                                                         |
|  45 | CUMPLIDO                   | Scripts Quick Start no cambiaron.                                                                         |
|  46 | CUMPLIDO                   | Workflows CI no cambiaron.                                                                                |
|  47 | CUMPLIDO                   | Informe TASK047A redactado.                                                                               |
|  48 | CUMPLIDO                   | Commit selectivo `54bd817b748f7769266a2d653353ffd4c8406775`.                                              |
|  49 | CUMPLIDO                   | Push ordinario verificado; remoto coincide con el commit.                                                 |
|  50 | CUMPLIDO                   | Quality #44566635410 terminó sobre el SHA exacto; resultado failure verificado.                           |
|  51 | INCUMPLIDO                 | Las seis fallas originales se reprodujeron otra vez en los tres motores.                                  |
|  52 | CUMPLIDO CON OBSERVACIONES | No hay fallos nuevos diferentes, pero la suite sigue fallando por el overflow no resuelto.                |
|  53 | CUMPLIDO                   | A47-02/A47-03 fuera de alcance y sin cambios.                                                             |
|  54 | CUMPLIDO                   | DOCX permanece untracked, no abierto/consultado/staged.                                                   |
|  55 | CUMPLIDO                   | No PR, merge ni cambios a main.                                                                           |
|  56 | CUMPLIDO                   | No se inició TASK047B ni se completó TASK047.                                                             |

Las observaciones reflejan diferencias entre Windows local y Linux CI. La ejecución remota es
decisiva: CA51 incumplido. Para continuar se requiere nueva autorización; no habrá otro commit
o push desde TASK047A.
