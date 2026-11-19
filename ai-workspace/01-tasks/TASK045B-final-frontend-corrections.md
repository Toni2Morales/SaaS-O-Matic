# TASK045B — Informe final de correcciones del frontend

| Campo       | Resultado                                                                     |
| ----------- | ----------------------------------------------------------------------------- |
| Rama / HEAD | `feature/mvp-frontend`, `8cd664262ed908e101b19a7de715560e344105ca`            |
| Veredicto   | **Correcciones implementadas y validadas localmente; no publicadas.**         |
| Alcance     | A45-01/02, regresiones de accesibilidad/responsive, QA e integración aislada. |
| Git         | Sin staging, commit, push, PR, merge ni cambio de refs. Índice vacío.         |

## 1. Resumen

- A45-01: `--color-text-muted` cambió a `#5e6b82`; ratios calculados en DOM real:
  5,015:1 sobre `#f5f7fa` y 5,383:1 sobre blanco. Se quitó la opacidad global que
  reducía el contraste del resumen obsoleto.
- A45-02: el `role=status` deja de anunciar preparación/cálculo cuando hay error terminal;
  el alert de error se conserva, el resultado previo se identifica como obsoleto y el
  guardado queda bloqueado. Retry y selección EUR siguen disponibles.
- Axe añadió y ayudó a corregir tres problemas colaterales confirmados: nombres accesibles
  discordantes en enlaces, thumb de `mat-slider` sin nombre propio y contraste de texto en
  preview obsoleta. Skip-link quedó enfocable con teclado en WebKit.
- La matriz nueva descubrió overflow de tarjeta a 768 px (`scrollWidth` 904); el breakpoint
  de `CustomerCard` subió a 980 px. La matriz de 5 rutas × 5 anchos pasa en los tres motores.
- Sin cambios en backend, API, reglas de negocio, catálogo ni datos del propietario.

## 2. Archivos permanentes

Modificados:

- `README.md`, `frontend/README.md`, `ai-workspace/README.md`.
- `docs/specs/010-frontend-refinement-and-e2e/spec.md` y `tasks.md`.
- `frontend/angular.json`, `frontend/package.json`, `frontend/package-lock.json`,
  `frontend/playwright.config.ts`.
- `frontend/e2e/customer-management.spec.ts`, `navigation.spec.ts`, `simulator.spec.ts`.
- `frontend/src/app/core/layout/app-shell.html`.
- `frontend/src/app/features/simulations/simulation-page.ts`.
- `frontend/src/app/shared/components/customer-card.ts`, `frontend/src/styles.scss`.

Nuevos:

- Este informe y `TASK045B-frontend-corrections-plan.md`.
- `frontend/e2e/task045b-audit.spec.ts` y `task045b-real-integration.spec.ts`.
- `frontend/src/app/features/simulations/simulation-page.spec.ts`.

`TASK045B-initial-hashes.json` conserva el manifiesto inicial. Los artefactos TASK045 ya
presentes se dejaron intactos. `Prueba Devs con IA.docx` no se abrió ni modificó.

## 3. Criterios y trazabilidad CA01–CA50

CA01–CA45 son los criterios de la auditoría anterior; su evaluación base permanece en
[`TASK045-independent-frontend-audit.md`, §O](TASK045-independent-frontend-audit.md#o-criterios-de-aceptación-ca01ca45).
TASK045B no altera retrospectivamente esas conclusiones. Los cierres aplicables a esta
corrección y cinco criterios de cierre añadidos al completar el trabajo son:

| Criterio                        | Resultado TASK045B                          | Evidencia                                                                                                                                                          |
| ------------------------------- | ------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| CA26 / A45-02                   | CERRADO                                     | Vitest y E2E: 503 terminal, sin status pendiente, preview stale y save bloqueado; retry recupera.                                                                  |
| CA29 / V44-07                   | CERRADO                                     | E2E: error 1.000.001 asociado, `aria-invalid`, sin preview/bandas/save.                                                                                            |
| CA30 / responsive               | CERRADO con matriz ampliada                 | 5 rutas × 5 anchos en Chromium/Firefox/WebKit; overflow a 768 px corregido.                                                                                        |
| CA31 / accesibilidad            | CERRADO con límites                         | Axe Chromium sin violaciones en nueve estados; no equivale a revisión con AT ni certificación WCAG.                                                                |
| CA32 / navegadores              | CERRADO funcional                           | E2E funcionales Chromium, Firefox y WebKit; axe limitado a Chromium.                                                                                               |
| CA34 / dependencias             | CERRADO                                     | Solo axe-playwright 4.14.0 y coverage-v8 5.1.1; instalaciones `--ignore-scripts`; scripts nativos siguen bloqueados.                                               |
| CA35 / instalación limpia       | CERRADO                                     | `npm ci --ignore-scripts` en copia aislada; calidad, pruebas, build, E2E y audit.                                                                                  |
| CA36 / cobertura                | CERRADO con cobertura desigual              | Summary V8 reproducible; módulos y porcentajes anotados abajo, sin umbral inventado.                                                                               |
| CA40 / pruebas                  | CERRADO con incidencia de runner registrada | Backend 579/579; Vitest 40/40; E2E limpio 79 PASS/20 skips. Corrida sobre árbol habitual falló por pérdida del servidor de desarrollo.                             |
| CA41 / hallazgos A45            | CERRADO                                     | A45-01/02 corregidos y regresiones añadidas.                                                                                                                       |
| CA42 / integración              | CERRADO                                     | UI–FastAPI–SQLite temporal, altas/duplicado/búsqueda, preview no persistente, EUR/USD/GBP, reload e historial tras reinicio; FX fixture separado de consulta real. |
| CA43 / hashes                   | CERRADO con deltas autorizados              | 263/263 archivos tracked del preflight presentes; 16 difieren y corresponden exclusivamente a los archivos versionados modificados en esta tarea.                  |
| CA44 / restricciones Git        | CERRADO                                     | HEAD sin cambios, índice vacío; sin operaciones Git de escritura/publicación.                                                                                      |
| CA45 / entrega                  | CERRADO con pendiente operativo temporal    | Informe y evidencia disponibles; una SQLite temporal quedó bloqueada por proceso ajeno/no verificado y se preservó.                                                |
| CA46 / A45-01                   | CERRADO                                     | 4,434:1 baseline; 5,015:1 lienzo y 5,383:1 blanco después del cambio.                                                                                              |
| CA47 / estados FX               | CERRADO                                     | Error inicial/posterior, stale, retry y conversión EUR probados; estado pendiente ausente durante error.                                                           |
| CA48 / axe y accesibilidad      | CERRADO con limitación                      | Nueve estados representativos en Chromium, cero violaciones; Firefox tuvo crash al inyectar axe en una ejecución, no se suprimieron reglas.                        |
| CA49 / matriz responsive        | CERRADO                                     | Rutas `/`, listado, alta, ficha y simulador en 320/390/768/1024/1440 px, tres motores.                                                                             |
| CA50 / integración/persistencia | CERRADO                                     | Tres snapshots de divisa, preview sin escritura, historial tras reload y verificación UI tras reiniciar backend temporal.                                          |

## 4. Validación ejecutada y resultados reales

### Frontend

- `npm run typecheck`: PASS.
- `npm run lint`: PASS.
- `npm run format:check`: PASS para frontend. Prettier comprobado además sobre READMEs,
  plan y SPEC-010: PASS.
- `npm test`: **40/40**, 12 archivos.
- `npm run test:coverage`: **40/40**; statements 86,20 % (1350/1566), branches 81,86 %
  (492/601), functions 67,19 % (127/189), lines 86,84 % (964/1110).
- `npm run build`: PASS; bundle inicial 395,13 kB raw, estimación de transferencia
  99,01 kB.
- `npm ls --depth=0`: PASS. `npm audit` y `npm audit --omit=dev`: 0 vulnerabilidades.
- Copia limpia con lock actual e instalación `npm ci --ignore-scripts`: typecheck, lint,
  formato, Vitest, coverage, build y auditorías PASS. E2E limpio: **79 PASS/20 skips
  opt-in de 99**, en Chromium/Firefox/WebKit. Los skips son escenarios que necesitan
  capturas/servicios externos y el axe no-Chromium, no fallos.
- `npm run e2e` en el árbol de trabajo tuvo otra ejecución con 30 PASS y luego 49 errores
  de conexión (`NS_ERROR_CONNECTION_REFUSED` / “Could not connect to server”) cuando el
  servidor temporal desapareció al cambiar de engine. No se cuenta como PASS. La ejecución
  limpia aislada, con servidor/proxy propio, terminó con 79/20 PASS/skips.

### Backend y verificación integrada

- Sin modificar backend: Ruff check PASS; Ruff format **90 archivos** PASS; mypy **88
  archivos** PASS; pip check PASS; Pytest **579/579** PASS.
- Integración real de navegador **1/1** PASS en Chromium con backend FastAPI, migraciones
  0001–0004 y SQLite nueva. Incluyó alta ES inválida/válida, duplicado, búsquedas, preview
  sin escritura, POST 201 y snapshots EUR/USD/GBP, importes y tasas, límites, alta PT,
  historial y reload. Una llamada PATCH no mutadora confirmó historial sin alteración.
- FX de integración fue determinista por inyección externa mediante el seam/builder existente
  de `MonthlyEstimator`; USD `1.0998`, GBP `0.83348`, referencia fixture `2026-11-18`.
  Consulta Frankfurter real, separada y puntual: USD `1.0981` y GBP `0.83385`, referencia
  `2026-11-19`. No presentar fixtures como cotizaciones reales.
- El test post-reinicio del backend recuperó tres snapshots de la misma SQLite en UI y tras
  reload. Este test se ejecutó en la base temporal de integración anterior; la corrida final
  de integración volvió a pasar separadamente.
- Capturas sintéticas y reales se conservaron fuera del repositorio en
  `%LOCALAPPDATA%\Temp\opencode\TASK045B\screenshots`.

## 5. Desviaciones, riesgos y recursos temporales

- Axe se ejecuta en Chromium. Firefox tuvo fallos/crash al inyectar axe en una ejecución
  multipágina; las pruebas funcionales y responsive sí pasan en Firefox y WebKit.
- El runner E2E del árbol habitual mostró caída del servidor de desarrollo; el resultado
  verificado del conjunto completo procede de la copia limpia aislada. Repetir si se
  requiere validar el modo de servidor del árbol habitual bajo otra carga.
- La auditoría axe no certifica WCAG AA; no hubo lector de pantalla ni auditoría humana.
  Zoom/reflow de 400 % no se validó como prueba específica.
- El listener de 127.0.0.1:8000 permaneció intacto. Una SQLite temporal
  `integration.sqlite3` no pudo eliminarse porque el sistema informó que estaba abierta por
  otro proceso. Se preservó y no se investigó ni detuvo el proceso que podría poseerla.
  La base `final-integration.sqlite3`, el servicio propio 8008 y la copia de instalación
  limpia sí se retiraron. Las capturas quedan disponibles externamente.
- No se afirma preparación para producción pública: P-05, autenticación/autorización,
  despliegue, CI y WCAG integral permanecen fuera de alcance.

## 6. Estado final

- Rama `feature/mvp-frontend`; HEAD conserva `8cd664262ed908e101b19a7de715560e344105ca`.
- `git diff --check`: PASS; índice vacío; cambios sin publicar.
- 263/263 archivos tracked del manifiesto inicial están presentes; 16 cambios esperados
  corresponden a archivos modificados autorizados. Los nuevos archivos enumerados arriba
  son artefactos permanentes TASK045B.
- El DOCX privado sigue sin abrirse ni modificarse. No se inició TASK045BP, TASK046 ni
  TASK047.
