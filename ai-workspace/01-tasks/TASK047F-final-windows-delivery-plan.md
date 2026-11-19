# TASK047F — Plan de entrega local para Windows 10

## Decisión y contexto

El propietario prioriza la entrega evaluable y la ejecución reproducible en Windows 10. La
compatibilidad multiplataforma y los defectos observados solo en GitHub Actions quedan
aplazados expresamente; no se intentarán arreglar ni ejecutar workflows durante esta tarea.
TASK047F sustituye para la entrega actual las actuaciones pendientes TASK047, TASK047A2,
TASK047B y TASK047C. A47-01/02/03 siguen registrados como pendientes, no se cierran por esta
decisión.
La rama autorizada es `docs/final-delivery`; no crear otra rama, PR ni merge.

## Estado inicial y protección

- Repositorio público `Toni2Morales/SaaS-O-Matic`, remoto HTTPS.
- Rama `docs/final-delivery`; HEAD y `origin/docs/final-delivery`:
  `54bd817b748f7769266a2d653353ffd4c8406775`.
- `origin/main`: `99c0ebac984c70521c4e3c94226b35c15303f572`; `main` local:
  `8371f9f608ce6e06984cc501d8240e1b7edf34d5`.
- Índice inicialmente vacío. README raíz, README de ai-workspace e informe TASK047A están
  modificados; documentos TASK047 (informe e inventario) y guía demo están sin seguimiento.
  El manifiesto TASK047A enumera hashes de cinco documentos TASK047 y el manifiesto TASK047
  previo documenta el corte anterior.
- `Prueba Devs con IA.docx` permanece privado y sin seguimiento: no abrir, leer, hashear,
  copiar ni publicar. `TASKS.zip`, bases de datos y capturas no se incorporan.
- `TASK047F-initial-hashes.json` registra los 290 archivos tracked actuales, los documentos
  locales pendientes permitidos y las rutas funcionales/protegidas. Se compararán antes de
  publicar cada incremento. Solo documentación y triggers YAML pueden cambiar.

## Entorno de referencia observado

La inspección real encuentra Windows 10 Pro 22H2, build 19045, x64, Windows PowerShell 5.1.
Es el host disponible autorizado por la nueva instrucción TASK047F. No afirmar Windows 11 ni
compatibilidad completa con Linux, macOS o Windows Server.

Runtimes: Git 2.56.0.windows.2; Python 3.13.17 disponible mediante `py -3.13` (el `python`
global predeterminado es 3.15, fuera del rango del proyecto); pip 26.2.2; Node 24.22.0/npm
11.19.1. `backend/.venv` Python 3.13.17, SQLite runtime 3.50.4, FastAPI 0.163.1, Pydantic
2.14.3, SQLAlchemy 2.1.8, Alembic 1.20.1, pytest 9.2.0, Ruff 0.17.5, mypy 2.4.1.
Angular/CLI 22.2.6, TypeScript 6.0.3, RxJS 7.8.2, Vitest 5.1.1, Playwright 1.65.1.
Los browsers gestionados por Playwright están instalados; Edge y Chrome también están
presentes. Sus versiones se comprueban por metadatos del ejecutable, pero la matriz E2E se
ejecutará con Chromium/Firefox/WebKit Playwright. Esta sección es inventario, no todavía la
campaña de prueba final.

## Alcance de cambios

1. Crear planificación y manifiesto antes de modificar contenido de entrega.
2. Commit 1: cambiar únicamente `push`/`pull_request` por `workflow_dispatch` en los dos
   workflows, documentar el aplazamiento/hallazgos y quitar badges engañosos si existieran.
3. Commit 2: finalizar README, guía Windows 10/manual, matriz FR01–FR11, ai-workspace,
   documentación arquitectónica existente, guía demo e inventario auténtico de evidencias.
   No duplicar diagramas ya creados ni reescribir informes históricos como resultados nuevos.
4. Tras push del commit 2, clonar GitHub explícitamente `docs/final-delivery` en una carpeta
   temporal propia fuera del repo. Ejecutar una única campaña desde ese clon: Quick Start
   literal, health/UI/Swagger, integridad API y DB, stop/restart/persistencia, puerto ocupado,
   smoke funcional y test suite/calidad una sola vez. DB y dependencias propias del clon.
5. Probar FX fixture sin atribuirle tipo real y hacer una petición separada a Frankfurter
   live; si falla, probar/documentar 503/EUR con cobertura existente, no inventar datos.
6. Commit 3: informe final con resultados observados, hashes, veredicto y CA01–CA36. Los
   resultados post-push quedan en este commit; no se ejecutan Actions manualmente.

## Verificación funcional objetivo

Comprobar Dashboard, alta ES válida/inválida, alta internacional genérica, búsqueda nombre/
tax ID, ficha e historial; preview/guardado/reload; slider/manual; consumos informativos; EUR,
USD, GBP con FX real separado; errores; responsive. Valores ES: 15 usuarios subtotal 140,00,
IVA 29,40, total 169,40 EUR; 16 usuarios subtotal 148,00, IVA 31,08, total 179,08 EUR. Preview
no crea historial; guardado explícito sí. La validación algorítmica no acredita titularidad.

## Integridad, privacidad y parada

No cambiar backend/frontend funcional, pruebas, scripts, migraciones, paquetes/manifests/
lockfiles ni LICENSE. No modificar refs `main`. Staging explícito por commit y límites de
publicación de la tarea. No matar servicios ajenos ni eliminar datos existentes. Si un
bloqueo funcional aparece en Windows 10, documentar evidencia y detenerse; no corregirlo bajo
esta tarea. No publicar imágenes sin aprobación ni conversaciones no aportadas por el dueño.

## Criterios de salida

- README permite ejecutar tras instalar runtimes; describe instalación automática/manual,
  URLs, persistencia, puertos, Internet, seguridad y límites.
- Windows 10 clon limpio real desde rama remota; resultados/timing reproducibles y reportados.
- Requisitos FR01–FR11 y entregables originales contrastados; estados parciales honestos.
- Workflows únicamente manuales, comprobaciones intactas y no ejecutadas por dispatch.
- Hallazgos A47-01/02/03 permanecen abiertos/aplazados por decisión del propietario.
- Hasta tres commits/pushes ordinarios con mensajes aprobados, remote verificado tras cada uno.
- Sin PR/merge; sin cambios `main`; árbol de trabajo previo de TASK047 preservado.

## Riesgos

- Windows objetivo indicado y entorno real coinciden en Windows 10 Pro; aun así no representa
  todas las revisiones/ediciones de Windows ni sustituye la aprobación del propietario.
- CI falla en responsive Linux y scripts de Quick Start; se conserva como infraestructura
  futura, manual y no bloqueante para el veredicto local definido por el dueño.
- Frankfurter es proveedor externo; disponibilidad/rates cambian. No se usarán como fixtures.
- Conversaciones de IA privadas faltan y no se pueden reconstruir. Capturas requieren
  aprobación, por lo que se entregan nombres/rutas existentes sin publicar imágenes.
- `requirements.lock` es constraints sin hashes; pip build isolation no está totalmente
  fijada. npm usa package-lock y `npm ci --ignore-scripts`.
