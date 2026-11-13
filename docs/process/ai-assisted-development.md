# Proceso de desarrollo asistido por IA

| Campo | Valor |
| --- | --- |
| Versión | 0.4 (revisión TASK010) |
| Fecha | 2026-11-13 |
| Estado | Propuesto — pendiente de aprobación; utilizado provisionalmente como referencia de trabajo |

## 1. Principio general

La IA acelera el trabajo, pero **no decide**. Las decisiones de producto, alcance y arquitectura corresponden al propietario del repositorio. Todo cambio llega a `main` mediante revisión humana explícita.

## 2. Roles

| Rol | Quién | Responsabilidad |
| --- | --- | --- |
| Asesoría, instrucciones y revisión independiente | ChatGPT | Analiza requisitos, propone arquitectura, redacta instrucciones y revisa resultados **fuera del repositorio**. No materializa documentos ni código en el repositorio ni aprueba su propio trabajo. |
| Implementación y materialización | OpenCode + DeepSeek | Implementa las tareas aprobadas y materializa en el repositorio las especificaciones, planes, documentos, código e informes. Registra evidencias y proceso en `ai-workspace/`. Puede ejecutar `git add`, `git commit`, `git push` y crear pull requests cuando la tarea incluya expresamente esa operación y el propietario la autorice. No fusiona pull requests. |
| Propietario y responsable técnico | Desarrollador humano | Define el alcance, decide las cuestiones funcionales y técnicas pendientes, autoriza expresamente las operaciones Git que formen parte de la tarea, revisa los cambios y resultados y conserva la decisión final sobre la integración. Ejecuta personalmente el merge. Última palabra en cualquier conflicto. |

Un mismo agente no debe aprobar su propio trabajo como si fuera revisión independiente.

### 2.1 Autoría, materialización y revisión

- **Autoría intelectual o propuesta de contenido:** ChatGPT puede analizar, proponer arquitectura, redactar instrucciones y revisar resultados.
- **Materialización en el repositorio:** OpenCode + DeepSeek escribe los archivos y deja constancia de la autoría material.
- **Revisión independiente:** ChatGPT revisa las evidencias facilitadas. OpenCode + DeepSeek materializa el informe de revisión y registra la fuente; el informe no se presenta como validación automática ni como trabajo propio del implementador.
- **Aprobación:** el propietario decide la aceptación y autoriza las operaciones Git que procedan.

## 3. Flujo de trabajo

1. El propietario define el objetivo y aprueba las decisiones.
2. ChatGPT analiza, propone arquitectura, redacta instrucciones y revisa resultados fuera del repositorio.
3. OpenCode + DeepSeek implementa y materializa en el repositorio las especificaciones, planes, documentos, código e informes.
4. OpenCode + DeepSeek registra las evidencias y el proceso en `ai-workspace/`.
5. ChatGPT realiza una revisión independiente a partir de las evidencias facilitadas.
6. El propietario decide la aceptación y autoriza expresamente las operaciones Git que procedan.

```text
Requisitos → Especificación → Plan → Tareas → Aprobación humana
   → Implementación y materialización → Registro en ai-workspace
   → Revisión independiente → Pull Request → Merge humano
```

| Etapa | Artefacto | Responsable | Puerta de salida |
| --- | --- | --- | --- |
| 1. Requisitos | `docs/requirements/` | ChatGPT + propietario (contenido) / OpenCode + DeepSeek (materialización) | Requisitos y preguntas abiertas documentados |
| 2. Especificación | `docs/specs/NNN-<funcionalidad>/spec.md` (ubicación prevista; no existe todavía) | ChatGPT (contenido) / OpenCode + DeepSeek (materialización) | Comportamiento, datos y criterios de aceptación claros |
| 3. Plan | `docs/specs/NNN-<funcionalidad>/plan.md` (ubicación prevista; no existe todavía) | ChatGPT + OpenCode (contenido) / OpenCode + DeepSeek (materialización) | Enfoque técnico y ficheros afectados |
| 4. Tareas | `docs/specs/NNN-<funcionalidad>/tasks.md` (ubicación prevista; no existe todavía) | OpenCode + DeepSeek (contenido y materialización) | Tareas pequeñas y verificables |
| 5. Aprobación | Comentario o instrucción del propietario | Propietario | Autorización explícita para implementar |
| 6. Implementación | Código + pruebas + documentación | OpenCode/DeepSeek | Diff revisado localmente |
| 7. Registro | `ai-workspace/01-tasks/TASKxxx.md` | OpenCode/DeepSeek | Evidencias, validaciones y decisiones registradas |
| 8. Revisión | `ai-workspace/02-audits/TASKxxx-audit.md` o sección de revisión del registro de tarea | ChatGPT (contenido de revisión) / OpenCode + DeepSeek (materialización) | Observaciones resueltas o aceptadas |
| 9. Pull Request | Descripción del PR | OpenCode/DeepSeek (redacción y creación/publicación con autorización expresa) / Propietario (autorización y decisión final) | PR listo para revisión humana |
| 10. Merge | Fusión en `main` | Propietario | Aprobación explícita; nunca automática |

`docs/specs/` no se crea en esta fase. Las rutas indicadas son ubicaciones previstas para cuando se inicie la primera funcionalidad. Los informes de tarea y las auditorías se materializan en `ai-workspace/01-tasks/` y `ai-workspace/02-audits/`.

Ninguna etapa se salta. Si durante la implementación aparece una decisión no cubierta por la especificación, se detiene el trabajo y se vuelve a la etapa 2.

## 4. Ramas

| Prefijo | Uso | Ejemplo |
| --- | --- | --- |
| `docs/` | Documentación y fundamentos | `docs/project-foundation` |
| `feature/` | Funcionalidad nueva | `feature/customer-registration` |
| `fix/` | Corrección de errores | `fix/tax-rounding` |
| `test/` | Pruebas y fixtures | `test/pricing-boundaries` |
| `refactor/` | Reestructuración sin cambio de comportamiento | `refactor/pricing-module` |

Reglas:

- `main` es intocable durante el desarrollo; nunca se trabaja directamente sobre ella.
- Si una tarea parece requerir una escritura directa en `main`, el agente se detiene, explica el conflicto y no ejecuta esa escritura. La prohibición se mantiene; el cambio se canaliza mediante una rama y un pull request, o lo gestiona personalmente el propietario.
- Cada rama parte de `main` actualizada y contiene un propósito único.
- Los nombres van en minúsculas, con guiones y en inglés.
- No se usan prefijos distintos de los cinco anteriores; en particular, no se admiten `feat/` ni `chore/`.

## 5. Commits

Formato [Conventional Commits](https://www.conventionalcommits.org/):

```text
<tipo>(<ámbito opcional>): <descripción en imperativo>
```

Tipos admitidos: `feat`, `fix`, `docs`, `test`, `refactor`, `chore`, `build`, `ci`, `perf`.

Los tipos de commit son independientes de los prefijos de rama: `feat` y `chore` siguen siendo tipos válidos de Conventional Commits, pero no se usan como prefijo de rama.

Ejemplos:

```text
docs(adr): documentar el stack aprobado
feat(pricing): calcular tramos progresivos de usuarios
fix(tax): corregir redondeo del subtotal
test(pricing): cubrir los límites 10, 11, 50 y 51
```

Buenas prácticas:

- Un commit, un cambio lógico.
- Cuerpo del commit cuando haga falta explicar el *porqué*, no el *qué*.
- No mezclar refactorizaciones amplias con cambios funcionales.
- El propietario revisa el diff completo antes de autorizar un commit.

## 6. Revisión antes de push y PR

El propietario autoriza expresamente el push y la creación del pull request. Los agentes pueden ejecutar esas operaciones cuando la tarea las incluya y la autorización identifique la operación y la rama. Si la tarea no contempla commit, push o creación de PR, los agentes solo preparan los cambios locales y presentan la propuesta.

Checklist del propietario antes de autorizar un push:

1. Revisar `git status` y el diff completo.
2. Ejecutar las comprobaciones disponibles y anotar los resultados reales.
3. Verificar que no se incluyen secretos, bases de datos locales ni artefactos.
4. Confirmar que el alcance coincide con la tarea aprobada.

Checklist antes de autorizar la creación de un PR:

1. Confirmar que el cambio está listo para revisión humana.
2. Descripción con resumen, cambios, decisiones, comprobaciones y riesgos.
3. Rama publicada sin force-push.

Un cambio futuro de esta política requiere autorización explícita y específica del propietario.

## 7. Prohibiciones

- `git push --force` o `git push --force-with-lease` sobre cualquier rama.
- Que un agente ejecute `git add`, `git commit`, `git push` o cree pull requests sin autorización expresa para esa operación concreta. La autorización para implementar una tarea no habilita por sí sola a publicar cambios.
- `git reset --hard`, `git clean -fd` o cualquier otra operación destructiva que pueda eliminar, sobrescribir o descartar trabajo del repositorio. Esta prohibición es absoluta y no admite excepciones mediante autorización escrita. Si una operación destructiva parece necesaria, el agente debe detenerse y explicar el problema al propietario.
- Reescribir el historial de `main`.
- Que un agente fusione pull requests; el merge corresponde exclusivamente al propietario.
- Commitear secretos, `.env` reales, bases de datos locales o artefactos de build.
- Declarar pruebas superadas sin haberlas ejecutado.
- Inventar reglas de negocio, precios, impuestos o resultados.

## 8. Documentación de decisiones

- Toda decisión arquitectónica relevante se registra como ADR en `docs/adr/`.
- Las decisiones aún no validadas se marcan como **provisionales** o **pendientes de aprobación**.
- Los errores, correcciones y validaciones relevantes se documentan en `ai-workspace/01-tasks/TASKxxx.md`, sin reconstruir conversaciones ni historial ficticio.
- Las auditorías independientes se registran en `ai-workspace/02-audits/TASKxxx-audit.md`.
- El contexto de evolución del proyecto se mantiene en `ai-workspace/00-project-context/`.
- No se presenta un informe de OpenCode + DeepSeek como revisión independiente; la fuente de la revisión se identifica expresamente.

## 9. Honestidad del registro

- No se inventan iteraciones, discusiones ni resultados.
- Si una comprobación no se ejecutó, se indica expresamente.
- Si una decisión se tomó sin consenso, se refleja como pendiente.
- Los documentos describen el estado real del repositorio, no el deseado.
