# TASK045B — Plan de correcciones y refuerzo del frontend

| Campo               | Valor                                                                                                                                       |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| Rama / HEAD inicial | `feature/mvp-frontend`, `8cd664262ed908e101b19a7de715560e344105ca`                                                                          |
| Estado              | Implementación/validación local finalizadas; sin staging ni operaciones Git de publicación                                                  |
| Manifiesto          | [TASK045B-initial-hashes.json](TASK045B-initial-hashes.json): 263 tracked y tres documentos TASK045 previos                                 |
| Alcance aprobado    | A45-01, A45-02, cierre V44-01/02/07; QA Playwright multibrowser/axe/cobertura; instalación limpia; integración real aislada y documentación |
| Restricciones       | Backend/API/reglas intactas; sin scripts npm; instalaciones solo `--ignore-scripts`; sin Git de escritura; no PR/commit/push                |

## Preflight y compatibilidad inicial (completado antes de producto)

- Rama `feature/mvp-frontend`, HEAD/remota `8cd664262ed908e101b19a7de715560e344105ca`;
  `origin/main` `23cc43b486d20f7995a2cf29375e3f724f3c7c3f`; main local
  `8371f9f608ce6e06984cc501d8240e1b7edf34d5`; índice vacío.
- Los 263 hashes de `TASK045-initial-hashes.json` coinciden con los bytes actuales. Solo
  existen los tres documentos TASK045 previos y el DOCX privado excluido como untracked.
- Runtime: Node 24.22.0/npm 11.19.1; Angular 22.2.6, TypeScript 6.0.3,
  Playwright 1.65.1, Vitest 5.1.1. `backend/.venv`: Python 3.13.17.
- Puertos 4200/4201/4202 y 8000/8006/8007 no están escuchando en este preflight. La ruta
  antigua SQLite TASK044 existe; no se abrió ni se tocó.
- Metadata publicada consultada, sin instalar paquetes ni ejecutar scripts: axe-playwright
  4.14.0 (MPL-2.0, peer playwright-core >=1, dependency axe-core ~4.14.0, Node >=22.12),
  coverage-v8 5.1.1 (MIT, peer Vitest exactamente 5.1.1, `@vitest/browser` opcional).
  Sus scripts solo se leyeron de metadata: axe paquete declara `prepare` que instala
  navegadores/build; coverage-v8 declara `dev` y `build`; ninguno se ejecutará y toda
  instalación se hará con `--ignore-scripts`. Angular unit-test builder soporta options
  `coverage`, `coverageInclude/Exclude/Reporters`, por lo que no hace falta nueva config
  global si el CLI permite reproducirla.

### Evidencia de implementación inicial

- Baseline A45-01/A45-02 reproducido por E2E Chromium (4,434:1 en lienzo y estado
  «Preparando una estimación actualizada…» después de 503). La regresión de V44-07
  también pasó: mensaje específico visible, aria-describedby/aria-invalid, bandas y save
  bloqueados y sin nueva preview.
- `@axe-core/playwright@4.14.0` y `@vitest/coverage-v8@5.1.1` se instalaron solo con
  `--ignore-scripts`, sin actualizar las versiones existentes. npm ls root correcto; npm
  audit completo y de producción reportaron cero vulnerabilidades en el corte.
- Playwright instaló sus browsers oficiales Firefox 159.0 y WebKit 27.2 (revisión Playwright
  1.65.1); no se instalaron componentes de sistema ni actualizó el paquete.
- E2E axe de Chromium recorrió dashboard, listado, formularios vacío/inválido, ficha,
  simulador vigente/inválido/FX error y menú móvil estable. Antes de corregir también
  encontró label-content-name-mismatch en marca/enlace, slider thumb sin label y contraste
  inferior dentro del resumen obsoleto; cambios mínimos incluidos en el alcance.
- A45-01 quedó con color muted `#5e6b82`: contraste medido 5,02:1 en lienzo `#f5f7fa` y
  5,38:1 en blanco. El resumen stale dejó de bajar la opacidad del texto. El campo slider
  thumb tiene su propio nombre/description; enlaces usan el texto visible y skip-link lleva
  `tabindex=0` para el primer Tab de WebKit.
- La matriz dedicada de 5 rutas × 5 anchos reprodujo overflow horizontal dashboard/tarjeta
  a 768 px (document scrollWidth 904 px); se ajustó el breakpoint responsive de la tarjeta
  y la repetición Chromium/Firefox/WebKit pasó. Hallazgo B45B-04, fuera de lista A45 pero
  dentro de la verificación responsive autorizada.
- axe 4.14.0 encontró y motivó arreglos de nombres accesibles discordantes, thumb unlabeled
  y contraste stale. Repetición Chromium axe: cero violaciones en nueve estados. El runner
  Firefox tuvo crash en axe durante una ejecución; axe se configura y verifica en Chromium,
  mientras E2E funcional responsive se ejecuta en los tres engines. No se desactivaron reglas.
- En una primera invocación de E2E hubo dos proyectos Firefox/WebKit duplicados en la
  configuración; se eliminó la duplicación. Firefox también tuvo un crash al inyectar axe
  en una página de simulador en el ciclo multiruta; por ahora axe se ejecuta solo en
  Chromium y los flujos E2E funcionales se ejecutan en los tres engines. Esa limitación se
  debe documentar; no se omiten reglas axe.

## Reproducción baseline registrada antes de corregir

- E2E de regresión nuevo en Chromium: A45-01 falló con foreground `rgb(100, 116, 139)`
  sobre fondo `rgb(245, 247, 250)`, ratio exacto 4.4341598:1.
- E2E de regresión nuevo en Chromium: A45-02 falló; tras 503, `.status` permanece
  «Preparando una estimación actualizada…», con alert de FX visible. El guardado queda
  deshabilitado.
- V44-07: nueva prueba Chromium PASS: mensaje visible, `aria-describedby` contiene
  `users-error`, `aria-invalid=true`, bandas ocultas, sin nueva preview, botón de guardar
  disabled y preview anterior marcada stale.
- El primer intento de prueba manual fuera del runner resolvió módulos desde la raíz y no
  arrancó navegador; el segundo comando interactivo fue interrumpido durante ejecución.
  No lo contamos como evidencia; la reproducción anterior en TASK045 y los E2E del runner
  local son la fuente reproducible.

## Avance de implementación/validación

- Correcciones de contraste, anuncio FX, stale opacity, label visible/accesible de enlaces,
  label del thumb y foco skip-link aplicadas mínimamente con regresiones.
- QA añadida: axe-playwright 4.14.0 y coverage-v8 5.1.1 con `--ignore-scripts`; configuración
  Angular genera summary de cobertura bajo `frontend/coverage` (ignorado).
- E2E multibrowser Chromium/Firefox/WebKit ejecuta correcciones, axe (Chromium), y una
  matriz responsive de cinco rutas/anchos. Axe detectó/remedió hallazgos concretos; no se
  deshabilitaron reglas. Evidencia final: [informe TASK045B](TASK045B-final-frontend-corrections.md).
- Se añadió harness ASGI temporal externo que sustituye solo el proveedor FX mediante el
  builder/puerto de estimación ya existente. No se ha editado `backend/` ni contrato.
- Durante la integración, 127.0.0.1:8000 se encontró ocupado por un listener no verificado;
  el backend de pruebas se cambió a 8008 y el proxy temporal Angular a 4201. No se detuvo
  el listener del 8000. El backend propio y la base final de integración se retiraron; una
  base temporal `integration.sqlite3` quedó bloqueada por otro proceso y se preservó.

## Cierre verificado

- Unitarias 40/40; coverage 86,20 % statements / 81,86 % branches / 67,19 % functions /
  86,84 % lines. Clean install/build/typecheck/lint/formato/audits PASS; Playwright limpio
  79 PASS/20 skips opt-in. La corrida del árbol habitual falló al perder el servidor de
  desarrollo y no se registra como PASS.
- Responsive 5×5 y funcionalidad pasan en Chromium/Firefox/WebKit; axe pasa en nueve
  estados Chromium. Integración real PASS y backend 579/579.
- La comprobación SHA-256 final encontró 263/263 tracked iniciales presentes y 16
  modificados, todos en el alcance autorizado. Índice vacío, `git diff --check` PASS; HEAD
  y refs sin cambios. Detalle en el informe final enlazado arriba.

## Objetivo y guardas

Resolver con cambios mínimos los dos defectos reproducidos en TASK045, completar las
comprobaciones pendientes y probar con dependencias exactas compatibles, sin extender el
MVP. FastAPI seguirá siendo autoridad económica. Los resultados de red/proveedor se
separarán de fixtures. No se abrirá ni alterará el DOCX privado. Capturas, coverage, DB,
logs y node_modules temporales quedarán fuera del control de versiones.

## Secuencia de trabajo

1. **Preflight/integridad:** comprobar rama, HEAD, refs, índice y los tres archivos
   TASK045 sin seguimiento; manifiesto de 263 tracked comprobado. Hacer copia de hashes
   de cualquier candidato de producto antes de tocarlo. Nunca restaurar/revertir por Git.
2. **Reproducción/base:** contrastar A45-01 con luminancia relativa y superficies reales;
   reproducir A45-02 en preview FX 503 y con estimate previo; registrar el estado de 1000001.
3. **Compatibilidad QA:** consultar metadata npm de versiones exactas de axe Playwright y
   coverage-v8 para Playwright 1.65.1 / Vitest 5.1.1; revisar peers, licencia, dependencias
   y scripts. No instalar/ejecutar scripts. Si aparece incompatibilidad o script requerido,
   detener esa incorporación y documentar.
4. **Cambios mínimos:** token muted/superficies de color; estado terminal FX accesible;
   tests focalizados; V44-07 si el defecto se reproduce; V44-01/02 únicamente si persiste
   tras estabilizar transiciones. V44-03/05/06 se aceptan sin cambios.
5. **QA autorizada:** añadir únicamente las dos devDependencies permitidas, pines exactos;
   npm install/ci siempre con `--ignore-scripts`. Mantener los cuatro scripts previos
   bloqueados. Añadir cobertura Vitest sin thresholds arbitrarios; documentar inclusiones y
   exclusions. Ejecutar axe en estados representativos y resolver hallazgos dentro de scope.
6. **Navegadores:** usar Playwright ya fijado; instalar solo binarios oficiales Chromium,
   Firefox y WebKit si están ausentes. No actualizar Playwright/Angular. Si se requieren
   dependencias del sistema no disponibles, no pedir elevación: documentar y dejar ese
   navegador sin verificar.
7. **Integración completa:** crear SQLite temporal TASK045B, migrar 0001–0004, backend en
   puerto libre propio, Angular con proxy temporal externo al repo. Hacer recorrido real
   UI–API–SQLite con datos sintéticos, preview sin escritura, EUR/USD/GBP, historial,
   reload y reinicio solo del backend propio. Proxy/UI sin intercepts durante la integración.
   FX determinista: sustituir solo el proveedor mediante seam de pruebas existente si es
   viable sin alterar contrato/código backend. Consulta Frankfurter real separada y puntual.
8. **Matriz visual:** viewports 320/390/768/1024/1440 en cinco rutas; estados válido,
   inválido, error, guardado y menú. Screenshots Chromium fuera del repo, con nombre,
   browser, viewport, estado y fixture/real. Compatibilidad funcional en tres engines.
9. **Instalación limpia/regresión:** copia aislada, `npm ci --ignore-scripts`; typecheck,
   lint, Prettier, Vitest/coverage, E2E, axe, build, audits. Backend con `.venv` solamente:
   Pytest, Ruff check/format, mypy, pip check. No corregir backend.
10. **Cierre:** documentar CA01–50, hallazgos/limitaciones y evidencias; rehash 263
    originales más los tres artefactos TASK045; `git diff --check`, formato, enlaces, refs,
    índice y status. Retirar solo DB/procesos/copia npm temporales propios; conservar PNG
    fuera del repo para el propietario. No iniciar TASK045BP.

## Archivos candidatos previstos (no autorización automática)

- A45-01: `frontend/src/styles.scss`, test de contraste nuevo junto a la utilería de test
  apropiada; `frontend/src/app/shared/utils/*` solo si una utilidad central justifica el
  cambio. Sin añadir librerías de producto.
- A45-02/V44-07: `frontend/src/app/features/simulations/simulation-page.ts` y su spec;
  E2E existente solo si necesita una regresión de comportamiento que no cubre unit test.
- QA: `frontend/package.json`, `frontend/package-lock.json`, `frontend/playwright.config.ts`
  y config Vitest/Angular existente únicamente donde sea imprescindible.
- Uso/instrucciones: `README.md`, `frontend/README.md`, SPEC-010 plan/tasks y evidencias
  autorizadas. No modificar registros históricos TASK001–TASK045.
- Nuevos permanentes: este plan, manifiesto inicial, informe final TASK045B; tests de
  regresión/código QA autorizados por esta tarea. Sin artifacts generados.

## Riesgos y reglas de parada

- Contraste: preferir margen superior a 4,5:1 sin degradar estados/material/foco.
- Estado FX: error terminal nunca se anuncia como pending; conservar inputs, stale tagging,
  retry manual y bloqueo de guardado obsoleto.
- Axe puede señalar contenido Material/landmarks fuera del scope; no suprimir reglas sin
  causa, no afirmar WCAG AA y pedir decisión ante hallazgo crítico/arquitectónico.
- Coverage puede identificar código no alcanzado; añadir pruebas útiles, no tests de líneas
  triviales ni exclusions para manipular porcentaje.
- npm install usa registry pero no sube código; verificar cada cambio de lock y no aprobar
  scripts. Si `--ignore-scripts` impide instalar las herramientas, parar esa parte.
- No tocar servicio/base preexistente puerto 8000 ni `real-integration.sqlite3` de TASK044.
- Desviación de base o cambios tracked no autorizados: detenerse antes de implementar y
  presentar evidencia al propietario.
- Cualquier defecto backend, cambio API, necesidad de privilegios del sistema o dependencia
  adicional fuera de dos paquetes autorizados: detenerse y pedir autorización.
