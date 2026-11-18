# Plan TASK041 — Fundamentos Angular

| Campo | Valor |
| --- | --- |
| Estado | Plan aprobado para implementación local TASK041 |
| Base | `23cc43b486d20f7995a2cf29375e3f724f3c7c3f` |
| Rama | `feature/mvp-frontend` |
| Especificación | [spec.md](spec.md) |

## 1. Secuencia (spec-first)

1. Verificar Git, branch y proteger SHA-256 de registros/históricos, lock backend,
   migraciones y LICENSE.
2. Leer requisitos, ADRs, SPEC-001–006, TASK035–040, reto original local sin
   modificar/publicar y OpenAPI/código del backend.
3. Consultar documentación/compatibilidad y seleccionar versiones; resolver P-01
   en ADR antes de generar el scaffold.
4. Materializar SPEC-007 (spec, plan, tasks), ADR 0003 y actualización de la decisión
   P-01. No generar frontend antes del paso 4.
5. Crear `frontend/` con CLI local pinneado, standalone, routing, strict TS, SCSS,
   Vitest y package-lock. Ejecutar `npm ci` tras establecer dependencias.
6. Instalar Material/CDK compatibles, configurar tema oficial y adaptar shell,
   navegación y páginas preparatorias con componentes reales.
7. Añadir contratos TypeScript a partir de OpenAPI, ApiClient y manejo de errores,
   proxy local `/api` → `127.0.0.1:8000` manteniendo URI original.
8. Configurar Playwright Chromium, smoke tests y scripts. Añadir exclusiones Git.
9. Ejecutar tests, build, lint/typecheck, Playwright, audit y pruebas backend.
10. Verificar integración proxy contra migración temporal, inspeccionar interfaz,
    revisar enlaces, secretos, hashes protegidos, diff y árbol sin staged.
11. Actualizar READMEs, requisitos/matriz/roadmap, ai-workspace, crear TASK041 y
    registrar resultados reales. No publicar ni comenzar TASK042.

## 2. Arquitectura y decisiones de implementación

- Estructura por `core`, `shared` y `features`; no crear carpetas vacías.
- Una app Angular, sin SSR ni server runtime: frontend estático de desarrollo; P-05
  producción queda pendiente.
- Build system Angular `application` oficial, dev-server usa Vite proxy oficial.
- Angular Material/CDK para shell/menu, controles; CSS propio para tokens/layout,
  sin Bootstrap/Tailwind. Sistema Material con SCSS theming API pública.
- Vistas en blanco explicativas, sin datos falsos, peticiones o botones inactivos.
- `ApiClient` añade `/api` central; con proxy se elimina sólo ese prefijo.
- `ProblemDetails` fiel al contrato: extensiones opcionales, no asumir extensiones.
- Las pruebas no miden cobertura porcentual ni llaman servicios externos.

## 3. Dependencias propuestas/resueltas

ADR 0003 recoge la selección exacta y compatibilidad. Todas se instalarán con
versiones exactas y npm lock; Angular CLI no será global. Si la instalación revela
un conflicto no cubierto por peer metadata, detener y revisar, no usar force/legacy.

## 4. Ficheros esperados

- `docs/specs/007-angular-frontend-foundation/{spec,plan,tasks}.md`.
- `docs/adr/0003-angular-frontend-stack.md`, ADR 0001 y documentos vigentes
  actualizados sólo en P-01/estado frontend.
- `frontend/` fuente/config/lock/tests/README.
- `.gitignore`, `README.md`, requisitos, matriz, roadmap, `ai-workspace/README.md`.
- `ai-workspace/01-tasks/TASK041-angular-frontend-foundation.md`.

No se esperan cambios en `backend/`, `LICENSE`, los documentos del reto ni registros
TASK035–TASK040.

## 5. Riesgos

- Versiones Angular con rangos Node/TS estrictos; evitar versiones preview.
- Material 3/theme API y componentes accesibles requieren validar contraste, no sólo
  seleccionar colores de marca.
- El proxy depende del dev server; no resolver por anticipado despliegue.
- Browser binary Playwright puede estar ausente o bloquearse por red; registrar
  instalación y resultado real.
- Perceptible responsive/a11y requiere navegador real; Chromium es baseline, no matriz
  completa de browsers/assistive tech.
- TypeScript duplica OpenAPI; contraste automatizado/manual y tarea posterior para
  generador si la deriva lo justifica.
