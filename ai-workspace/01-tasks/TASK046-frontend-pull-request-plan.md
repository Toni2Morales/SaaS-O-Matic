# TASK046 — Final frontend Pull Request

| Campo              | Resultado inicial                                                                                   |
| ------------------ | --------------------------------------------------------------------------------------------------- |
| Objetivo           | Revisar y preparar la PR final `feature/mvp-frontend` → `main`; no hacer merge.                     |
| Autorización       | PR expresamente autorizada; un commit documental y push a la rama autorizados.                      |
| Repositorio        | `Toni2Morales/SaaS-O-Matic`, `origin` verificado.                                                   |
| Rama               | `feature/mvp-frontend`.                                                                             |
| HEAD / rama remota | `b1367923f251cde79305b028b514daf03478b62c` (iguales).                                               |
| Base PR esperada   | `origin/main` `23cc43b486d20f7995a2cf29375e3f724f3c7c3f`.                                           |
| Integridad         | [Manifiesto SHA-256 inicial](TASK046-initial-hashes.json), solo rutas tracked anteriores a TASK046. |
| Estado             | Plan previo a revisión; PR y commit documental no creados todavía.                                  |

## 1. Alcance y restricciones

Revisar el diff acumulado desde `main`, trazabilidad, pruebas, seguridad y límites operativos;
materializar el informe TASK046; publicar únicamente la documentación del informe con el
commit autorizado; crear una PR ordinaria dirigida a `main`. No cambiar código, API,
dependencias, manifiestos, lockfiles, migraciones ni reglas de negocio. No hacer merge,
activar auto-merge, iniciar TASK047 ni exponer una aplicación.

`Prueba Devs con IA.docx` permanece sin abrir, leer, modificar, calcular hash ni publicar.
Se conserva fuera del manifiesto inicial por ser un untracked privado. El puerto 8000 y la
SQLite bloqueada de tareas anteriores no se utilizarán ni se tocarán.

## 2. Estado inicial comprobado

Tras `git fetch origin`:

- Rama actual: `feature/mvp-frontend`.
- HEAD y `origin/feature/mvp-frontend`: `b1367923f251cde79305b028b514daf03478b62c`.
- `main` local: `8371f9f608ce6e06984cc501d8240e1b7edf34d5`.
- `origin/main`: `23cc43b486d20f7995a2cf29375e3f724f3c7c3f`.
- `merge-base(main, feature/mvp-frontend)`: `8371f9f608ce6e06984cc501d8240e1b7edf34d5`.
- Últimos commits frontend: `b136792 fix: finalize frontend accessibility and simulation reliability`,
  `8cd6642 feat: refine frontend UX accessibility and end-to-end integration`,
  `84b087a feat: implement SaaS-O-Matic MVP frontend`.
- Índice vacío, sin diferencias tracked; el único untracked de usuario es el DOCX privado.
- `gh pr list --head feature/mvp-frontend --state open`: lista vacía; no hay PR abierta duplicada.
- Identidad Git preconfigurada: `Antonio Morales` con correo GitHub noreply autorizado.
- El diff acumulado contiene una actualización histórica de `backend/README.md` que
  describe TASK039B/PR #6/TASK041–042. Es documentación, no código backend, contrato,
  pruebas, migraciones ni comportamiento.

## 3. Estrategia de revisión

1. Revisar los commits acumulados desde el merge-base de main, no solo HEAD.
2. Revisar requisitos/SPEC, TASK041–TASK045BP, informe de TASK044P y manifiesto/hash.
3. Verificar arquitectura Angular y que FastAPI conserva la autoridad económica.
4. Mapear flujos funcionales/pricing/divisas a pruebas; no inventar reglas o resultados.
5. Ejecutar pruebas actuales por stack; repetir E2E solo en copia limpia aislada con
   `npm ci --ignore-scripts` para mitigar la caída del servidor documentada.
6. No reejecutar integración sobre servicios/SQLite de propiedad no verificada. Registrar
   integración real TASK045B como evidencia histórica aceptada por el propietario.
7. Revisar privacidad, licencias, paths, dependencias, datos de fixtures y recursos locales.
8. Materializar el informe previo a publicación; añadir un único commit documental aprobado,
   push ordinario de rama y crear una PR sin auto-merge.
9. Verificar por GitHub la ref publicada, base, diff, PR, checklists y ausencia de merge.

## 4. Comprobaciones previstas

Backend: Pytest, Ruff check/format, mypy, pip check usando solo `backend/.venv`.

Frontend: typecheck, ESLint, Prettier, Vitest/cobertura, build, Playwright, axe,
responsive, npm audit y audit de producción. Instalación reproducible solo en copia temporal
con `npm ci --ignore-scripts`; no activar scripts ni actualizar browser/dependencias.

Integración y revisión visual: reutilizar como evidencia los resultados aceptados de
TASK045B; no utilizar el puerto 8000, datos reales ni la SQLite bloqueada. Capturas se
mantienen fuera de Git. No afirmar WCAG AA ni preparación de producción.

## 5. Riesgos y decisiones de parada

- Se documentó una caída del servidor E2E del árbol habitual; se usará el procedimiento
  limpio aislado que terminó con 79 PASS/20 skips y warnings WebKit no fatales.
- Integración real de datos sintéticos quedó validada históricamente en TASK045B. Un proceso
  ajeno/no identificado conserva una SQLite temporal; no se abrirá ni eliminará.
- Axe es automatización parcial de Chromium; no sustituye prueba humana/AT ni certifica WCAG.
- FX es referencia fechada con caché, no cotización continua; producción requiere hosting,
  proxy/API y autenticación/autorización aún fuera de alcance.
- Si aparece defecto crítico/alto, secreto, cambio fuera de alcance, divergencia de ramas,
  prueba material fallida o recurso de propiedad incierta, detener antes de PR y reportar.
- Merge solo humano. El proceso termina después de crear/verificar la PR y entregar informe.

## 6. Criterios de aceptación

Se evaluarán CA01–CA45 individualmente según la instrucción TASK046. Estados válidos:
CUMPLIDO, PARCIAL, INCUMPLIDO y NO APLICABLE, con evidencia. Resultados históricos se
marcarán como tales, no como ejecuciones TASK046. La decisión final APTA/PARCIAL/NO APTA
para merge manual dependerá de la revisión y no implica preparación para producción.
