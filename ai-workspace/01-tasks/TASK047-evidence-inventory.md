# TASK047 — Inventario de evidencias del proceso y visuales

## Principio de autenticidad y publicación

Este inventario selecciona artefactos que constan en el repositorio y capturas reales
generadas por E2E. No reproduce la conversación de ChatGPT/OpenCode, no reconstruye prompts
literales, no atribuye modelos sin evidencia y no publica imágenes. Las 13 capturas TASK046
permanecen fuera del repositorio en el directorio temporal de la máquina del implementador.
El propietario debe aprobar por separado cualquier copia al repositorio público.

## Evidencias documentales auténticas disponibles

| ID     | Tarea/fase                              | Fuente original versionada                                                                                                                                  | Qué demuestra                                                                  | Resultado observado / límites                                                                              |
| ------ | --------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------- |
| EV-T01 | Requisitos iniciales y reconciliación   | `docs/requirements/functional-requirements.md`; `docs/requirements/requirements-traceability.md`                                                            | Requisitos, supuestos abiertos, reglas y separación de estados backend/E2E     | Artefactos de trabajo reales; no equivalen a transcripción de conversación. El DOCX fuente no está en Git. |
| EV-T02 | Decisiones de tecnología y arquitectura | `docs/adr/0001-technology-stack.md`, `0002-architecture.md`, `0003-angular-frontend-stack.md`; `ai-workspace/00-project-context/architectural-evolution.md` | Decisión humana de Python/FastAPI y Angular, modularidad, constraints          | ADRs conservan estado de revisión y detalles pendientes; no se presentan como acta literal.                |
| EV-T03 | Especificación antes del desarrollo     | `docs/specs/001-...` a `010-...` (`spec.md`, y planes/tasks cuando existen)                                                                                 | Reglas previas, criterios de aceptación y trazabilidad                         | Usar SPEC-002 pricing, SPEC-005 impuestos/FX, SPEC-008 clientes y SPEC-009 simulador como muestra.         |
| EV-T04 | Dirección y límites a IA                | `AGENTS.md`, `docs/process/ai-assisted-development.md`, `ai-workspace/00-project-context/ai-tools-and-roles.md`                                             | Roles, aprobación humana, límites de alcance y disciplina Git                  | La página de roles describe el proceso declarado; no prueba por sí misma cada interacción.                 |
| EV-T05 | Iteración de clientes y simulación      | `ai-workspace/01-tasks/TASK042-customer-management-frontend.md`, `TASK043-interactive-subscription-simulator.md`                                            | Implementación incremental, tests y evidencia descrita                         | Informes de agente, no auditoría independiente. Resultados verificables citados en cada informe.           |
| EV-T06 | Auditoría backend y remediación         | `TASK039-backend-independent-audit.md`, `TASK039B-backend-audit-remediation.md`, `TASK040-mvp-backend-publication.md`                                       | Hallazgos, decisiones de no corregir alcance extra, correcciones y publicación | Incluye A39-07/08 pendientes/aceptadas; no reescribirlos como cerrados.                                    |
| EV-T07 | Auditoría/correcciones frontend         | `TASK045-independent-frontend-audit.md`, `TASK045B-final-frontend-corrections.md`, `TASK045BP-final-frontend-corrections-publication.md`                    | Defectos detectados, contraste/FX, regresiones y QA                            | Informes de agente; se distinguen pruebas automatizadas de certificación WCAG.                             |
| EV-T08 | Revisión final de integración           | `TASK046-final-frontend-pull-request.md` y PR #7                                                                                                            | Corte completo 579 backend, 40 Vitest, Playwright 79/20 skips, integración 1/1 | Estado histórico real TASK046; no asumir que son ejecuciones TASK047/CI.                                   |
| EV-T09 | Aprobación/publicación humana           | PR #1–#7 y commits enlazados desde `ai-workspace/README.md`                                                                                                 | PR review/merges y frontera de responsabilidad                                 | PR #7 merge verificado: `99c0ebac984c70521c4e3c94226b35c15303f572`. No es evidencia de conversación.       |

Los documentos de planificación/implementación son evidencia de proceso y diseño. No se
etiquetan como prompts estructurados literales salvo que el artefacto contenga explícitamente
la instrucción original y su procedencia.

## Evidencias de interacción IA: disponibles y pendientes del propietario

El agente no accede a conversaciones privadas, sesiones ajenas, historial personal ni
archivos fuera de los proporcionados/autorizados. Las instrucciones TASK041–TASK047F y los
informes incluidos sirven para trazar el trabajo, pero no sustituyen capturas/transcripciones
de los chats.

**Pendiente de aportar/aprobar por el propietario:** entre 4 y 8 recortes auténticos (ChatGPT
y/o OpenCode) que muestren, si existen:

1. Priorización del alcance original y una pregunta abierta resuelta por humano.
2. ADR/arquitectura antes de scaffolding.
3. SPEC/plan/criterios antes de implementar una feature.
4. Prompt concreto de implementación (solo si se conserva literalmente).
5. Revisión de código generado y decisión/corrección humana.
6. Hallazgo de auditoría y respuesta con pruebas de regresión.
7. Control de pruebas y hallazgo residual aceptado, no ocultado.
8. Autorización explícita de commit/push/PR y decisión humana de merge.

Cada recorte debe indicar tarea/fecha/contexto, difuminar nombre/cuenta/rutas personales y
eliminar secretos, conversaciones ajenas, datos fiscales/personales, tokens y contenido del
DOCX. No recrear interfaz de chat ni redactar diálogo retrospectivo. Si no se conservan
esas interacciones, consignar **«no disponible; no se reconstruye»**.

## Inventario de capturas reales disponibles fuera de Git

Ubicación temporal observada: `%LOCALAPPDATA%\Temp\opencode\TASK046\screenshots`.
Las 13 PNG se generaron mediante Playwright integrado con FastAPI aislado y SQLite migrada
durante TASK046; datos sintéticos. El adaptador de tasas USD/GBP usó fixtures deterministas,
no Frankfurter en vivo. Los ficheros no se copiaron ni se añadieron al commit/PR; el dueño
debe aprobar cualquier publicación. Las imágenes revisadas visualmente no muestran
credenciales ni datos fiscales/personales reales. Todas tienen resolución 1280×720.

| Prioridad / archivo existente                     | Escenario y requisito                                        | Integración                          | Nombre propuesto tras aprobación       | Alt text propuesto                                                                        |
| ------------------------------------------------- | ------------------------------------------------------------ | ------------------------------------ | -------------------------------------- | ----------------------------------------------------------------------------------------- |
| 1 `real-dashboard.png`                            | Dashboard/panel, países/divisas y estado inicial (FR07/UX)   | API real, SQLite vacía sintética     | `dashboard.png`                        | «Panel comercial de SaaS-O-Matic con países y divisas admitidos.»                         |
| 2 `real-alta-es-ficha-historial-vacio.png`        | Alta española válida, ficha e historial vacío (FR01/02/08)   | API y SQLite                         | `customer-detail.png`                  | «Ficha de empresa sintética española y su historial vacío.»                               |
| 3 `real-fiscal-es-invalido.png`                   | Rechazo de CIF inválido (FR02)                               | respuesta API real                   | `customer-validation-error.png`        | «Formulario de cliente que muestra error para identificador fiscal inválido.»             |
| 4 `real-busqueda-nombre-taxid.png`                | Búsqueda por razón social e ID fiscal (FR07)                 | API real                             | `customer-search.png`                  | «Listado filtrado por nombre o identificador fiscal sintético.»                           |
| 5 `real-preview-15-eur-no-persistencia.png`       | Preview 15, 140 EUR + 21 %, historial no cambia (FR05/06/09) | API/SQLite; verificó historial vacío | `simulation-preview.png`               | «Preview EUR de 15 usuarios: subtotal 140, IVA 29,40 y total 169,40; datos informativos.» |
| 6 `real-simulacion-guardada-eur.png`              | Guardado explícito en EUR, snapshot/historial (FR03/11)      | API real                             | `simulation-saved-eur.png`             | «Confirmación de simulación guardada en EUR.»                                             |
| 7 `real-simulacion-guardada-usd.png`              | Guardado USD; conversión/snapshot (FR10/11)                  | API real + FX fixture sintético      | `simulation-saved-usd.png`             | «Simulación guardada mostrada en USD con subtotal y total original EUR.»                  |
| 8 `real-simulacion-guardada-gbp.png`              | Guardado GBP e historial (FR10/11)                           | API real + FX fixture sintético      | `simulation-saved-gbp.png`             | «Simulación guardada mostrada en GBP.»                                                    |
| 9 `real-historial-eur-usd-gbp-tras-reload.png`    | Persistencia de monedas e historial tras reload (FR03/11)    | SQLite real sintética                | `simulation-history.png`               | «Historial conservado tras recargar la aplicación, con importes EUR/USD/GBP.»             |
| 10 `real-alta-internacional-pt.png`               | Registro PT (FR01)                                           | API/SQLite real                      | `international-customer.png`           | «Ficha de cliente sintético de Portugal, validación genérica no oficial.»                 |
| — `real-historial-1.png` / `real-historial-2.png` | Snapshots de historial intermedios                           | API real                             | No seleccionadas; redundantes con 9    | «Historial paginado de simulaciones guardadas.»                                           |
| — `real-limites-maximos-no-guardado.png`          | Límite superior/manual y no guardar                          | API real                             | No seleccionada; caso técnico de borde | «Simulador con entradas máximas admitidas, sin guardar.»                                  |

TASK046 no tiene una captura de error FX. No afirmar que una captura TASK046 muestre ese
escenario; la prueba E2E TASK046 cubre dicho estado. Las imágenes de esta sección son archivo
histórico y alternativas; la propuesta de ocho imágenes TASK047F generadas desde el clon está
en la sección siguiente. Cada fixture/API interceptada se identifica y nunca se presenta como
integración real.

### TASK047A — capturas adicionales locales

Ubicación externa original registrada en el informe TASK047A:
`%LOCALAPPDATA%\Temp\opencode\TASK047A\evidence-9c5ca903d4d84904acf77ea0e73904e0`.
Se comprobaron los archivos durante TASK047F; son capturas Chromium del simulador con API
fixture interceptada y datos sintéticos, no integración real ni tipos de cambio vivos:

| Archivo                          | Viewport  | Escenario                                 | Limitación                              |
| -------------------------------- | --------- | ----------------------------------------- | --------------------------------------- |
| `after-320-valid.png`            | 320×1859  | 15 usuarios, 169,40 EUR fixture           | Windows local; no demuestra CI resuelto |
| `after-320-maximum-users.png`    | 320×1883  | 1.000.000 usuarios, cifra fixture visible | UI interceptada; no backend live        |
| `after-320-validation-error.png` | 320×1845  | Validación de 1.000.001                   | UI interceptada                         |
| `after-390-valid.png`            | 390×1737  | 15 usuarios                               | UI interceptada                         |
| `after-1440-valid.png`           | 1440×1122 | Distribución desktop                      | UI interceptada                         |

No se generó ni fabricó una captura “antes”: la reproducción Windows pre-corrección no falló
y el run original no publicó artifact visual.

### TASK047F — propuesta final de ocho capturas de la campaña limpia

Ubicación fuera de Git: `%LOCALAPPDATA%\Temp\opencode\TASK047F\evidence-fafca9b7cef44d02b0c41ce9d9cd6636`.
Capturas Playwright Chromium en Windows 10 desde el clon limpio SHA
`8bdaf377454e8d943de01e2df46f502534eb76fb`. La UI y el backend accedieron a la SQLite del
clon con datos sintéticos. Divisa USD utilizó Frankfurter live fechado; no fixture. El
propietario debe revisar y autorizar cualquier publicación.

| Archivo                                            | Resolución | Estado                                                  | Alt text propuesto                                                         |
| -------------------------------------------------- | ---------: | ------------------------------------------------------- | -------------------------------------------------------------------------- |
| `dashboard-windows10.png`                          |  1440×1240 | Panel con dos clientes sintéticos                       | «Panel comercial con clientes sintéticos del clon Windows 10.»             |
| `international-customer-pt-windows10.png`          |  1280×1030 | Alta/ficha Portugal real                                | «Ficha de cliente sintético portugués con validación genérica no oficial.» |
| `customer-history-windows10.png`                   |  1440×1017 | Historial con simulación EUR guardada                   | «Ficha sintética e historial persistido tras guardado real.»               |
| `fiscal-validation-windows10.png`                  |  1440×1013 | CIF/NIF español inválido, error mostrado                | «Formulario que rechaza un identificador fiscal español inválido.»         |
| `simulator-preview-15-eur-windows10.png`           |  1440×1122 | Preview real, 15 usuarios, 250 GB, 100.000 llamadas/mes | «Preview 15 usuarios: subtotal 140, IVA 29,40, total 169,40 EUR.»          |
| `simulation-saved-eur-windows10.png`               |  1440×1122 | Confirmación de guardado real en EUR                    | «Simulación guardada explícitamente en EUR.»                               |
| `simulator-preview-usd-live-settled-windows10.png` |  1440×1122 | USD live: 1.0984, referencia 2026-11-19                 | «Estimación USD con total EUR original y tasa de referencia fechada.»      |
| `simulator-mobile-390-windows10.png`               |   390×1737 | Simulador móvil real, EUR                               | «Simulador responsive en viewport móvil de 390 px.»                        |

También se capturó `simulator-preview-gbp-live-settled-windows10.png` (0.83392/2026-11-19); es
evidencia adicional no incluida en el grupo de ocho. Los fallidos intentos de captura tomada
antes de que finalizara la preview no se proponen; solo se seleccionan archivos con estado
estable. No se publicaron imágenes en TASK047F.

### TASK047F — capturas de la campaña Windows 10

Ubicación externa: `%LOCALAPPDATA%\Temp\opencode\TASK047F\evidence-fafca9b7cef44d02b0c41ce9d9cd6636`.
Las respuestas de la UI se sirvieron desde el FastAPI y SQLite recién creados en el clon limpio;
los clientes son sintéticos. USD/GBP indicados como live provienen de la API real Frankfurter
vía backend, no de un fixture. No se copiaron al repositorio.

| Archivo                                            |  Viewport | Estado y tipo de integración                                              | Alt text propuesto                                                                |
| -------------------------------------------------- | --------: | ------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| `dashboard-windows10.png`                          | 1440×1240 | Dashboard, API/SQLite reales                                              | «Panel comercial de SaaS-O-Matic con datos sintéticos del clon Windows 10.»       |
| `international-customer-pt-windows10.png`          | 1280×1030 | Alta y ficha PT; validación genérica real, no fiscal oficial              | «Ficha de cliente sintético portugués; el identificador usa validación genérica.» |
| `customer-history-windows10.png`                   | 1440×1017 | Ficha e historial de simulación EUR real                                  | «Cliente sintético y simulación EUR guardada visible en historial.»               |
| `fiscal-validation-windows10.png`                  | 1440×1013 | CIF ES inválido rechazado por UI/API real                                 | «Formulario muestra error para un identificador fiscal español inválido.»         |
| `simulator-preview-15-eur-windows10.png`           | 1440×1122 | Preview API real, 15 usuarios, 250 GB, 100.000 calls; historial no cambia | «Preview mensual 15 usuarios: subtotal 140, IVA 29,40, total 169,40 EUR.»         |
| `simulation-saved-eur-windows10.png`               | 1440×1122 | Guardado explícito FastAPI/SQLite                                         | «Confirmación de simulación EUR guardada en SQLite sintética.»                    |
| `simulator-preview-usd-live-settled-windows10.png` | 1440×1122 | USD live Frankfurter vía FastAPI; reference fechada 2026-11-19            | «Total presentado en USD y total original EUR; tasa live fechada.»                |
| `simulator-mobile-390-windows10.png`               |  390×1737 | Simulador con backend/SQLite real                                         | «Simulador responsive en móvil 390 px, estimación EUR visible.»                   |

Una captura de GBP live también existe como `simulator-preview-gbp-live-settled-windows10.png`
en el mismo directorio, pero no integra la propuesta de ocho. Las capturas son candidatas;
el propietario debe aprobar nombres/selección/publicación por separado. No acreditan
compatibilidad Windows 11 ni resuelven el overflow de Linux CI A47-01.

## Catálogo externo adicional TASK042–TASK045B

Se encontró un árbol externo `Temp/opencode/TASK043`–`TASK045B`; se inspeccionaron
metadatos y muestras visuales. No se copió ningún PNG. Los bytes/resoluciones se conservan
en su ubicación temporal. Los nombres no certifican que cada imagen siga siendo el mejor
estado final; comparar contra los candidatos TASK046 antes de aprobación.

| Origen / integración                                                                                                                          | Archivos encontrados                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | Resoluciones y uso                                                                                                                                                                          |
| --------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TASK042, capturas sintéticas (el informe declara UI real y fixtures vacíos)                                                                   | El informe TASK042 enumera `TASK042-dashboard-desktop.png`, `TASK042-listado-desktop.png`, `TASK042-registro-desktop.png`, `TASK042-ficha-historial-desktop.png`, `TASK042-listado-mobile.png`, `TASK042-registro-mobile.png`, `TASK042-ficha-historial-mobile.png`, `TASK042-menu-mobile.png`, `TASK042-error-dashboard.png`, `TASK042-conflicto-formulario.png`, `TASK042-listado-vacio-desktop.png`, `TASK042-busqueda-sin-coincidencias.png`, `TASK042-validacion-formulario.png`.                                                                                                                                                                                                                                             | No se halló `TASK042/screenshots` bajo el directorio temporal TASK047; resolución/bytes y archivos no verificables. Fuente de nombres: informe TASK042, no se asume que siguen disponibles. |
| TASK043, 12 PNG; 2 estados señalados por el informe como recorrido real (desktop e historial), 10 como respuestas interceptadas deterministas | `TASK043-dashboard-tema-unificado.png`, `TASK043-historial-actualizado.png`, `TASK043-simulacion-guardada.png`, `TASK043-simulador-calculando.png`, `TASK043-simulador-cero-usuarios.png`, `TASK043-simulador-desktop.png`, `TASK043-simulador-error-fx.png`, `TASK043-simulador-gbp.png`, `TASK043-simulador-mobile.png`, `TASK043-simulador-usd.png`, `TASK043-simulador-usuario-manual.png`, `TASK043-simulador-validacion.png`.                                                                                                                                                                                                                                                                                                | Desktop 1280–1440 px, capturas largas ~994–1176 px; móvil 390×1660. FX error fixture; los tipos USD/GBP del informe son observaciones puntuales, no cotización actual.                      |
| TASK044, 21 PNG: 13 con FastAPI+SQLite real sintética y 8 con fixture/API interceptada                                                        | `TASK044-clientes-desktop.png`, `TASK044-clientes-mobile.png`, `TASK044-dashboard-desktop.png`, `TASK044-dashboard-mobile.png`, `TASK044-ficha-historial-desktop.png`, `TASK044-ficha-historial-mobile.png`, `TASK044-foco-teclado.png`, `TASK044-historial-persistido.png`, `TASK044-menu-mobile.png`, `TASK044-registro-desktop.png`, `TASK044-registro-mobile.png`, `TASK044-simulacion-guardada.png`, `TASK044-simulador-15-usuarios.png`, `TASK044-simulador-16-usuarios.png`, `TASK044-simulador-desktop.png`, `TASK044-simulador-error-fx.png`, `TASK044-simulador-gbp.png`, `TASK044-simulador-mobile-resumen.png`, `TASK044-simulador-mobile.png`, `TASK044-simulador-usd.png`, `TASK044-simulador-validacion.png`.       | Desktop 1280×720, 1440×900/1000; móvil 390×844. Las capturas de error FX/divisa en grupo fixture deben etiquetarse como tales.                                                              |
| TASK045, capturas fixture de la matriz TASK044 + una evidencia A45-02                                                                         | Carpeta `fixture-screenshots`: mismos 21 nombres TASK044 listados arriba; `screenshots/fx-error-status-conflict.png`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | Las 21 son Chromium con APIs interceptadas (no prueban persistencia); A45-02 390×844, 503 interceptado. No elegir como evidencia “integración real”.                                        |
| TASK045B, 29 PNG: 15 Chromium con fixtures y 14 capturas del test integrado/SQLite                                                            | Fixture: `chromium-alta-selector-movil-abierto-fixture.png`, `chromium-alta-selectores-cerrados-fixture.png`, `chromium-clientes-fixture.png`, `chromium-dashboard-contraste-fixture.png`, `chromium-error-fx-con-preview-obsoleta-fixture.png`, `chromium-error-fx-primera-referencia-fixture.png`, `chromium-ficha-historial-vacio-fixture.png`, `chromium-historial-tras-reload-fixture.png`, `chromium-menu-movil-abierto-estable-fixture.png`, `chromium-recuperacion-eur-fixture.png`, `chromium-simulacion-guardada-fixture.png`, `chromium-simulador-15-desktop-fixture.png`, `chromium-simulador-16-desktop-fixture.png`, `chromium-simulador-16-movil-fixture.png`, `chromium-simulador-validacion-1000001-fixture.png`. | 1440×900 desktop y 390×844 móvil; los estados de error/contraste son fixture, no proveedor real.                                                                                            |
| TASK045B, integración real navegador/API/SQLite                                                                                               | `real-alta-es-ficha-historial-vacio.png`, `real-alta-internacional-pt.png`, `real-busqueda-nombre-taxid.png`, `real-dashboard.png`, `real-fiscal-es-invalido.png`, `real-historial-1.png`, `real-historial-2.png`, `real-historial-eur-usd-gbp-tras-reload.png`, `real-historial-tras-reinicio-backend.png`, `real-limites-maximos-no-guardado.png`, `real-preview-15-eur-no-persistencia.png`, `real-simulacion-guardada-eur.png`, `real-simulacion-guardada-gbp.png`, `real-simulacion-guardada-usd.png`.                                                                                                                                                                                                                        | Todas 1280×720. ES/PT e integración API/SQLite real sintética; FX USD/GBP usa fixtures deterministas excepto el smoke spot separado que describe el informe.                                |

Las capturas TASK045B reales tienen equivalentes TASK046 actualizados en su mayoría. La
selección preferente sigue siendo TASK046 por fecha/estado final, no porque las capturas
anteriores sean falsas. El informe TASK042 declara 13 PNG pero no se localizaron en el
directorio externo al inspeccionarlo; no se publican ni se finge haberlos revisado.

### Solicitud de aprobación de publicación visual

Antes de copiarlas a `docs/images/` o añadirlas al README, el propietario debe aprobar los
nombres/selección de la tabla TASK047F y autorizar expresamente su publicación en el repo
público. TASK047/TASK047F no publican ninguna imagen.
