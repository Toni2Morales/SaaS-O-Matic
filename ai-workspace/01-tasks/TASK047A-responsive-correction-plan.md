# TASK047A — Diagnóstico y corrección del simulador responsive

## Estado inicial

- Repositorio `Toni2Morales/SaaS-O-Matic`; rama autorizada `docs/final-delivery`.
- HEAD y `origin/docs/final-delivery`: `181afaf61174df2d9e7e817f27f6a7c79f5cf139`.
- `origin/main`: `99c0ebac984c70521c4e3c94226b35c15303f572`; `main` local:
  `8371f9f608ce6e06984cc501d8240e1b7edf34d5`.
- Índice vacío. Cambios pendientes observados antes de TASK047A: `README.md`,
  `ai-workspace/README.md`, y untracked `ai-workspace/01-tasks/TASK047-evidence-inventory.md`,
  `ai-workspace/01-tasks/TASK047-final-delivery-report.md`, `docs/guides/demo.md`.
- `Prueba Devs con IA.docx` aparece untracked; no se abre, lee, copia, publica ni incorpora al
  manifiesto. El hash de los otros documentos de TASK047 y README queda en el manifiesto
  complementario para comparar después de la tarea.
- No se observaron cambios staged.

## Hallazgo A47-01

Run Quality `44556931530`, commit `181afaf…`, Linux GitHub runner. Las mismas dos pruebas
responsive fallaron en Chromium, Firefox y WebKit:

1. `e2e/simulator.spec.ts:347` — body `scrollWidth <= innerWidth`.
2. `e2e/task045b-audit.spec.ts:251` — document/body no exceden viewport.

En 320 px, document `scrollWidth=334`, `clientWidth=320`. El DOM diagnóstico del segundo caso
registra `.panel`/`.columns` dentro de 280 px, formulario de 246 px, y `FORM.scrollWidth=297`.
El formulario contiene `.field-heading` como fila flex con los textos “Control deslizante” y
“Entrada manual: 0–1.000.000”. La hipótesis principal es que el tamaño mínimo intrínseco de
los dos ítems flex mantiene una sola fila más ancha que el formulario y empuja el documento.
Se confirmará con una reproducción/localización del elemento y una corrección de layout
acotada; no usar `overflow-x:hidden` ni ocultar información.

## Alcance y protecciones

Modificar solo CSS inline del componente del simulador o markup estrictamente necesario y
añadir regresión responsive solo si las pruebas existentes no bastan. No tocar backend,
contratos, economía, dependencias, Quick Start, workflows ni tests existentes (excepto una
prueba nueva añadida). Preservar todos los documentos de TASK047 y no usar/eliminar la base
QA local. No trabajar en otra rama, no PR/merge.

## Estrategia

1. Consultar logs completos/artefactos del run y registrar nombres exactos; artifacts de error
   no aparecen publicados por el workflow, así que no se presumirá disponibilidad.
2. Revisar simulador y estilos de layout. Reproducir la ruta y ancho de 320 px con Chromium,
   Firefox, WebKit local cuando sea viable. Si Windows no reproduce, apoyarse en mediciones CI
   observadas y declarar diferencias/limitaciones; no instalar WSL/Docker/runtime adicional.
3. Inspeccionar anchos, flex/grid y tamaño mínimo de `.field-heading` y descendientes en
   formulario. Confirmar causa raíz con mediciones before/after.
4. Corrección localizada que permita distribuir/partir los dos rótulos a ancho pequeño,
   preservando textos y controles. No cambiar breakpoints globales ni tamaño de viewport.
5. Ejecutar prueba responsive existente en los tres browsers y widths existentes; validar
   matriz adicional 320/375/390/768/1024/1440, importes, slider, error y axe según scripts.
6. Ejecutar typecheck, lint, format, Vitest, build, Playwright, backend checks y audits npm
   según alcance/autorización. Repetir integración real temporal si viable.
7. Capturas reales quedan fuera del repo y sin publicación.
8. Revisar hashes protegidos, cambios TASK047 pendientes y diffs. Un commit/push autorizado
   solamente si las comprobaciones locales exigibles pasan y el cambio está fundamentado.
   Nueva Quality real determina si A47-01 puede declararse resuelto.

## Criterios de aceptación

- No hay overflow horizontal en viewport 320 px, incluyendo las dos aserciones originales y
  Chromium/Firefox/WebKit.
- Textos, cifras y controles son visibles/legibles; slider, validación y resumen móvil siguen
  operativos; no hay regresiones desktop ni de pricing/FX/persistencia.
- Los tests originales permanecen, sin skips/retries/relajación.
- Todo el estado previo pendiente queda byte a byte preservado.
- Verificación CI se comunica con run ID/URL y SHA reales; una ejecución pendiente no es PASS.
- A47-02 y A47-03 quedan abiertos; no se reanuda TASK047 ni se inicia TASK047B.

## Riesgos

- El entorno Windows puede no reproducir métricas Linux; CI es criterio decisivo.
- Las capturas/artefactos de run pueden haber expirado o no haberse subido.
- Material Angular Material slider/outline puede tener overflow interno, pero solo debe
  cambiarse si la geometría evidencia que causa scroll del documento.
- Calidad del código no implica aprobación final del proyecto; Quick Start permanece aparte.
