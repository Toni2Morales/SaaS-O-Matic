# TASK043 — Simulador interactivo y conversión multidivisa

| Campo | Valor |
| --- | --- |
| Fecha | 2026-11-18 |
| Estado | Implementada y validada localmente; no publicada; revisión del propietario pendiente |
| Rama / base | `feature/mvp-frontend`, base/HEAD inicial `23cc43b486d20f7995a2cf29375e3f724f3c7c3f` |
| Main local | `8371f9f608ce6e06984cc501d8240e1b7edf34d5` |
| Especificación | [SPEC-009](../../docs/specs/009-interactive-subscription-simulator/spec.md) |
| Plan / tareas | [plan](../../docs/specs/009-interactive-subscription-simulator/plan.md) · [tasks](../../docs/specs/009-interactive-subscription-simulator/tasks.md) |
| Manifiesto inicial | [TASK043-initial-hashes.json](TASK043-initial-hashes.json) |

## 1. Resumen ejecutivo

El placeholder de simulación se sustituyó por una experiencia Angular integrada con
cliente, parámetros de consumo, divisa, preview reactiva no persistente, guardado
explícito y acceso al historial. FastAPI conserva cálculo, validación definitiva,
impuestos, conversiones y persistencia. No se modificaron backend, migraciones,
dependencias ni lockfiles. TASK043 no está publicada y no se inició TASK044.

## 2. Git inicial/final y preservación

Inicial: rama `feature/mvp-frontend`, HEAD/origin/main
`23cc43b486d20f7995a2cf29375e3f724f3c7c3f`, `main` local
`8371f9f608ce6e06984cc501d8240e1b7edf34d5`; 81 candidatos acumulados (9 modificados,
72 nuevos), índice vacío. El DOCX original no se abrió ni se incluyó; SHA-256 inicial
capturado en el manifiesto. Final: mismas referencias, índice vacío, 89 candidatos
(9 modificados y 80 nuevos; excluido el DOCX), de los cuales 19 archivos candidatos
iniciales cambiaron de contenido y se agregaron 8 rutas TASK043. Los 162 archivos
protegidos coinciden con sus hashes iniciales; el DOCX mantiene su hash.

No se ejecutaron `git add`, commit, push, merge, rebase, reset, stash, clean, checkout,
creación de rama ni PR. No se modificaron registros históricos TASK001–TASK042.

## 3. Arquitectura y componentes

- `SimulationPageComponent`: carga de cliente, Reactive Form, estados, preview y guardado.
- `SimulationsApiService` delega al `ApiClient`; POST exactos a
  `/simulations/preview` y `/simulations` por base `/api` existente.
- Reutiliza `CustomersApiService`, modelos HTTP, formateadores exactos, router e historial.
- El historial del cliente incluye un acceso contextual de nueva simulación; dashboard
  dirige primero al listado para elegir el cliente.
- No se incorporó almacén global, dependencia, endpoint ni cálculo monetario cliente.
- Tramos informativos muestran tarifas unitarias y cantidades actuales por banda; el
  subtotal procede de FastAPI. La aritmética de banda es únicamente entera y no monetaria.

## 4. Cliente, entrada y precisión

UUID se valida antes del GET; se recuperan razón social, país y plan reales. Estados de
carga, no encontrado e incidencia de transporte no habilitan guardar. Defaults UX 15
usuarios/0 GB/0 llamadas/EUR. Límites enteros: usuarios y GB 0..1.000.000; llamadas
0..1.000.000.000. EUR/USD/GBP. El slider cubre 0..1.000 y, si la entrada manual excede
1.000, se desactiva con ayuda; no modifica ni limita el valor del formulario. Al moverlo
explícitamente se sincroniza el campo.

Campos inválidos no generan POST; los errores se asocian a labels. Tasas e importes se
mantienen como strings. La tasa fiscal fraccional se presenta como porcentaje mediante
transformación decimal por cadenas, no aritmética de punto flotante. No se recalculan
tarifas, impuestos ni conversiones en Angular.

## 5. Preview, guardado, errores e historial

Preview inicial y por cambios válidos, debounce 250 ms, `switchMap`, cancelación ante
cambios/invalidez y destrucción, deduplicación consecutiva y generación para descartar
resultados no vigentes. La previa puede verse marcada obsoleta y no se puede guardar.
503 conserva datos, explica indisponibilidad y ofrece reintento y selección manual de
EUR; no se cambia moneda automáticamente.

POST de creación usa los parámetros válidos actuales, no importes. Deshabilita formulario
y acción durante la operación, no reintenta ni presume idempotencia. HTTP 201 sustituye
la preview como resultado final y enlaza a ficha/historial. Un fallo de transporte
advierte de posible persistencia y recomienda consultar historial. La pantalla de
historial consulta el registro real al abrirse o recargarse; no hay inserción optimista.

Resultado muestra subtotal, impuesto, país/tasa del backend, total EUR, total convertido,
fuente/tasa/fechas disponibles en información secundaria y aviso comercial/fiscal.
Información FX no se describe como cotización de mercado en directo.

## 6. Diseño y accesibilidad

Layout dos columnas en escritorio y una columna en móvil, sin anchuras fijas. Angular
Material usa paleta primaria derivada mediante mapa Sass público y tokens de marca
existentes; no se usan selectores privados. La cabecera mantiene el foco programático
existente en navegación móvil; en escritorio se preserva el foco de entrada y el enlace
de salto al contenido tras verificar la regresión de teclado. No se afirma conformidad
WCAG AA. El slider responde a teclado y se revisaron mensajes, estado y foco visible.

## 7. Pruebas y resultados

- Baseline antes de cambios: TypeScript, ESLint, Prettier correctos; Vitest 35/35.
- TASK043: Vitest **37 pruebas en 11 archivos**.
- Playwright interceptado: **17 pasadas**, 2 condicionadas/omitidas (integración real y
  captura visual opt-in) en corrida completa; evidencia visual opt-in: **1 pasada**.
- Integración real Chromium–Angular proxy–FastAPI–SQLite aislado: **1 pasada**. Alembic
  aplicó 0001–0004; registro sintético ES, búsqueda/detalle, preview de referencia
  subtotal 140,00 EUR / impuesto 29,40 / total 169,40, dos previews intermedias sin
  persistencia, guardado explícito, consulta/reload del historial, caso de 0 usuarios y
  caso PT (172,20 EUR con 23% devuelto por backend).
- FX puntual real (fuera de suites deterministas): USD HTTP 200, tasa `1.0998`, total
  `186.31`; GBP HTTP 200, tasa `0.83348`, total `141.19`, referencia `2026-11-18`.
  Proveedor indicado por backend: Frankfurter. No son tipos en vivo garantizados.
- Capturas: 12/12; desktop principal e historial final proceden del recorrido real;
  otras 10 proceden de un navegador real con respuestas interceptadas deterministas.
- TypeScript, ESLint, Prettier, build de producción pasan; `npm audit` y
  `npm audit --omit=dev`: 0 vulnerabilidades cada uno. Pytest: 579/579. `git diff --check`,
  enlaces Markdown relativos modificados, escaneo dirigido de secretos/artefactos y
  hashes protegidos pasan. Índice vacío y refs esperadas. `npm ci` no se ejecutó para no
  ejecutar/aprobar cuatro scripts de instalación pendientes de autorización.

## 8. Capturas visuales

Carpeta temporal externa al repositorio (no versionada):
`%LOCALAPPDATA%\Temp\opencode\TASK043\screenshots\`.

Archivos requeridos: `TASK043-simulador-desktop.png`, `TASK043-simulador-mobile.png`,
`TASK043-simulador-usd.png`, `TASK043-simulador-gbp.png`,
`TASK043-simulador-cero-usuarios.png`, `TASK043-simulador-usuario-manual.png`,
`TASK043-simulador-validacion.png`, `TASK043-simulador-calculando.png`,
`TASK043-simulador-error-fx.png`, `TASK043-simulacion-guardada.png`,
`TASK043-historial-actualizado.png`, `TASK043-dashboard-tema-unificado.png`.
La página visual de Playwright usa API interceptada determinista, salvo que el informe
indique expresamente integración real para desktop e historial.

## 9. Archivos y límites

Se crean SPEC-009 (spec/plan/tasks), manifiesto, informe, servicio de simulación y E2E
simulator/visual. Se modifican 19 rutas iniciales: README, contexto/índice AI, roadmap,
requisitos y matriz; README frontend, E2E customer/navigation, ApiClient + test, modelos,
customer guidance, simulador, historial + test, formatter + test y tema SCSS. Inventario final:
89 candidatos (9 modificados y 80 nuevos, DOCX excluido). Los otros cambios acumulados de
TASK041/042 (incluidos `backend/README.md`, `.gitignore` y ADR 0001) se conservan byte a
byte frente al manifiesto inicial. Cambios no incluidos:
backend y pruebas/migraciones, package manifests/lock, LICENSE, DOCX, registros antiguos,
capturas y artefactos generados.

## 10. Evaluación de aceptación

| # | Criterio | Resultado |
|---:|---|---|
| 1 | SPEC-009 antes de código | Sí, orden comprobado |
| 2 | Placeholder sustituido | Sí |
| 3 | Cliente real desde backend | Sí |
| 4 | Slider 0–1.000 | Sí |
| 5 | Entrada manual hasta 1.000.000 | Sí; 1.500 y 1.000.000 aceptados, 1.000.001 rechazado |
| 6 | Límites de consumo | Sí, validadores frontend y API |
| 7 | Preview reactiva | Sí; integración real |
| 8 | No prevalece respuesta obsoleta | Sí; E2E retrasa y libera una respuesta antigua y verifica que no sustituye la actual |
| 9 | FastAPI autoridad de cálculo | Sí; cuerpo solo contiene parámetros |
| 10 | Explicación de tramos | Sí, tarifas unitarias y cantidades enteras por banda |
| 11 | Impuestos del resultado | Sí; ES/PT reales |
| 12 | EUR/USD/GBP | Sí; respuesta real puntual FX |
| 13 | Precisión como string | Sí; formateo sin cálculo monetario |
| 14 | Errores FX | Sí; 503 interceptado, retry/EUR |
| 15 | Preview no persiste | Sí; historial 0 tras cambios |
| 16 | Guardado explícito | Sí; POST 201 real |
| 17 | Bloqueo doble envío | Sí; E2E verifica controles bloqueados y un único POST |
| 18 | Historial tras guardar | Sí, consulta real y reload |
| 19 | Persistencia tras recarga | Sí |
| 20 | Responsive | Sí; 320, 390, 768, 1280 y 1440 px |
| 21 | Unificación cromática | Sí; token primario y paleta pública |
| 22 | Accesibilidad principal por teclado | Slider y navegación probados; auditoría formal pendiente |
| 23 | Suites anterior/nueva | Sí: Vitest 37/37; Playwright 17/17; Pytest 579/579. Pruebas opt-in se pasaron aparte |
| 24 | Integración FastAPI/SQLite | Sí, cliente ES/PT sintético |
| 25 | Evidencias visuales | Sí, 12 archivos; distinguir interceptadas/real |
| 26 | Sin cambios backend/dependencias | Sí; backend funcional/tests/migraciones y manifests/lock sin cambios TASK043 |
| 27 | Documentación/trazabilidad | Sí; SPEC, requisitos, matriz, roadmap, READMEs, contexto e informe |
| 28 | Índice vacío | Sí; diff index vacío y sin staging |
| 29 | Sin publicación | Sí |
| 30 | TASK044 no iniciado | Sí |

## 11. Pendientes y cierre

Pendientes: instalación reproducible `npm ci` por cuatro scripts de instalación no
autorizados, auditoría formal de accesibilidad, seguridad SAST/DAST, CI y despliegue.
Observaciones UX diferidas a TASK044 sin corregir ahora: UX-01 títulos duplicados,
UX-02 separación de ayuda en móvil, UX-03 paginación recortada, UX-04 separación iconos,
UX-05 cromática (unificada en el alcance autorizado), UX-06 enlaces a fichas, UX-07
buscador truncado, UX-08 iconos vacíos, UX-09 terminología técnica y UX-10 contador de
historial móvil. Se revisó el foco de títulos: se mantiene foco programático móvil y se
preserva el salto accesible/teclado en escritorio; no se amplió el cambio global del shell.
TASK044 queda sin iniciar; el propietario revisará técnica y visualmente TASK043 antes
de cualquier autorización posterior. TASK043 termina localmente y se detiene sin publicar.
