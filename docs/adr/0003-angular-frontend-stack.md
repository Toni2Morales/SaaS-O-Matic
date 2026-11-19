# ADR 0003 — Stack del frontend Angular

| Campo | Valor |
| --- | --- |
| Estado de decisión | Aceptado en TASK041 para el scaffold frontend |
| Estado de documento | Propuesto para revisión técnica del propietario |
| Fecha | 2026-11-18 |
| Decisor | Propietario (autorización TASK041); versión resuelta por compatibilidad oficial |
| Alcance | Herramientas frontend de desarrollo; no resuelve P-05 |

## Contexto

P-01 en ADR 0001 reservaba elegir una versión concreta de Angular y validar Vitest.
TASK041 aprueba Angular, TypeScript, standalone, Signals, RxJS, Reactive Forms,
Router, HttpClient y permite Material/CDK, SCSS, Vitest, Playwright y npm sujetos a
compatibilidad. El runtime local comprobado es Node v24.22.0/npm 11.19.1; no se
cambian globalmente.

## Decisión

| Componente | Versión fijada | Uso |
| --- | --- | --- |
| Node.js | local 24.22.0; `.nvmrc`/engine de proyecto v24 | runtime LTS compatible |
| npm | local 11.19.1; engine ≥11 | gestor/lockfile |
| Angular core/common/forms/router/platform-browser | 22.2.6 | framework |
| Angular CLI | 22.2.6 | herramienta local, sin instalación global |
| Angular build | 22.2.6 | aplicación y Vitest builder |
| Angular Material/CDK | 22.2.6 | componentes accesibles y layout |
| TypeScript | 6.0.3 | modo estricto |
| RxJS | 7.8.2 | flujos async/HTTP |
| Vitest | 5.1.1 | pruebas unitarias, peer-compatible |
| Playwright Test | 1.65.1 | smoke E2E Chromium |
| ESLint / `@eslint/js` | 10.15.0 / 10.0.1 | lint TypeScript y plantillas |
| angular-eslint | 22.8.0 | builder, reglas y esquemas Angular |
| typescript-eslint | 8.73.0 | parser/reglas compatibles con TS 6.0 |
| jsdom | 30.1.3 | entorno DOM de Vitest |
| Prettier | 3.8.1 | check de formato |
| SCSS | compilador del build Angular | estilos y tokens |

El scaffold no incluye SSR. Se usa `@angular/build:application` y su dev server
integrado; el proxy es configuración de desarrollo, no API pública nueva.

## Compatibilidad y fuentes

Consulta realizada 2026-11-18. `angular.dev/reference/versions` indica para Angular
22 Node `^22.22.3 || ^24.15.0 || ^26`, TypeScript `>=6.0 <6.1` y RxJS `^6.5.3 ||
^7.4.0`. Node 24 está en LTS según Node.js releases y la versión local satisface el
rango. Angular 22 figura Active support hasta 2027-06 y LTS hasta 2028-06 en
`angular.dev/reference/releases`. Angular Material/CDK 22.2.6 package metadata exige
CDK igual y permite Angular core/forms/common/platform-browser 22/23, RxJS 6/7.
Angular CLI/build 22.2.6 requieren Node en rango y build declara TypeScript 6.0 y
Vitest 4/5. Vitest 5.1.1 queda en ese peer range; Playwright Test 1.65.1 declara
Node ≥20 y su guía documenta Node 22/24/26 y Windows 11/Server 2019+. angular-eslint
22.8.0 acepta ESLint 9/10; typescript-eslint 8.73.0 acepta TypeScript `<6.1` y
ESLint 8/9/10. ESLint 10.15.0 y `@eslint/js` 10.0.1 cumplen sus peers.

Fuentes:

- https://angular.dev/reference/versions
- https://angular.dev/reference/releases
- https://angular.dev/tools/cli/setup-local
- https://angular.dev/tools/cli/build-system-migration
- https://angular.dev/guide/testing
- https://angular.dev/guide/testing/migrating-to-vitest
- https://angular.dev/tools/cli/serve
- https://angular.dev/guide/http/setup
- https://angular.dev/guide/routing
- https://angular.dev/guide/forms/reactive-forms
- https://angular.dev/best-practices/a11y
- https://nodejs.org/en/about/previous-releases
- https://playwright.dev/docs/intro
- https://material.angular.dev/
- npm registry package metadata for exact peerDependencies/versions (same date).

## Alternativas consideradas

- Angular 21 LTS: viable, pero elegir versión anterior no aporta ventaja al Node 24
  local y Angular 22 está en soporte activo; decisión en favor de 22.2.6 estable.
- Angular 22.3 latest Material: no seleccionar paquetes de versiones distintas antes
  de publicación coherente del core; al corte consultado las versiones verificadas
  core/CLI/build/Material/CDK son todas 22.2.6.
- Karma/Jasmine: rechazado porque CLI actual soporta Vitest por defecto en apps nuevas.
- Vitest 4: compatible, pero Vitest 5.1.1 también satisface el peer range del builder.
- Jest/NgRx/Tailwind/Bootstrap: no necesarios y ampliarían dependencias/arquitectura.
- CLI global: prohibida por tarea; usar ejecutable del workspace.

## Consecuencias

Reproducibilidad mediante versiones exactas y `package-lock.json`; parches sólo tras
revisión/upgrade. La compatibilidad oficial no garantiza ausencia de defectos; build,
tests, peer metadata y `npm audit` deben verificarse con ejecución real. P-05 sigue
pendiente: no se define hosting, URL productiva, SSR ni estrategia de despliegue.

## Actualización de P-01

P-01 queda **resuelta en alcance TASK041**: Angular 22.2.6 con TypeScript 6.0.3,
Vitest 5.1.1 y compatibilidad Node/RxJS conforme a documentación oficial. No resuelve
P-05 ni autoriza futuras features de UI.
