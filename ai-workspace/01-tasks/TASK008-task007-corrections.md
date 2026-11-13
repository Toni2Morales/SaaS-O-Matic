# TASK008 — Corrección final de hallazgos TASK007

| Campo | Valor |
| --- | --- |
| ID | TASK008 |
| Título | Corrección final de hallazgos TASK007 |
| Estado | Parcial; instrucción original disponible; informe original no disponible |
| Fecha | No documentada en la instrucción |
| Participantes | Propietario (decisiones y aprobación) / implementador documental no identificado nominalmente / ChatGPT sin escritura en el repositorio |
| Autorización Git | La política general permite a OpenCode + DeepSeek `git add`, commit, push y PR con autorización expresa; TASK008 no autoriza ninguna publicación; merge reservado al propietario |

## 1. Objetivo y alcance

Corregir exclusivamente los hallazgos de TASK007, sin ampliar el alcance ni reescribir documentación que no necesitara cambios. La tarea era documental y de configuración; no debía crear código, scaffolding, dependencias, tests ni workflows.

## 2. Instrucciones y fuentes

| Tipo de fuente | Referencia | Estado |
| --- | --- | --- |
| Instrucción original | `TASK008.md`, en `TASKS.zip` facilitado por el propietario | Disponible; el ZIP no se incorpora al repositorio |
| Resumen verificable | `docs/assessment/001-repository-assessment.md:153-159` y los documentos actuales | Parcial |
| Informe del agente | No disponible | No documentado |

## 3. Herramientas y participantes

- Propietario: define el alcance, autoriza operaciones y conserva la decisión final sobre la integración.
- Implementador documental: rol definido por la instrucción; no se identifica nominalmente.
- ChatGPT: no se le atribuye escritura en el repositorio.
- OpenCode + DeepSeek: entorno de implementación del proyecto; no consta informe de ejecución de TASK008.
- Herramientas: Git, edición de Markdown y comprobaciones no destructivas.

## 4. Plan y decisiones

La instrucción pedía:

1. Documentar la política Git: el propietario decide y ejecuta el merge; OpenCode + DeepSeek pueden ejecutar `git add`, `git commit`, `git push` y crear PR solo con autorización expresa que identifique la operación y el alcance; la autorización para implementar no autoriza publicar.
2. Mantener la prohibición absoluta de `git push --force`, `git push --force-with-lease`, `git reset --hard`, `git clean -fd` y cualquier operación destructiva, sin excepciones por autorización escrita.
3. Corregir NUEVO-01 a NUEVO-06: política Git en AGENTS, proceso, roles y README; comandos destructivos; README incompleto; referencias a un PR inexistente; composition root provisional; descripción histórica de `dist/` y `coverage/`.
4. Añadir Q-17 sobre la obligatoriedad de fecha y fuente del tipo de cambio, sin cambiar FR-11.
5. No publicar cambios en TASK008 y dejar todo sin staged.

Restricciones: solo documentación y `.gitignore` si fuera imprescindible; no código, scaffolding, dependencias, tests, workflows, `LICENSE` ni `docs/specs/`; no resolver preguntas de negocio; no alterar ADR 0001 ni las decisiones arquitectónicas ya corregidas.

## 5. Archivos afectados

Según la instrucción y el assessment:

- `AGENTS.md`
- `docs/process/ai-assisted-development.md`
- `ai-workspace/00-project-context/ai-tools-and-roles.md`
- `README.md`
- `docs/adr/0002-architecture.md`
- `docs/requirements/functional-requirements.md`
- `docs/assessment/001-repository-assessment.md`
- `ai-workspace/00-project-context/architectural-evolution.md`

## 6. Validaciones ejecutadas

| Comprobación | Resultado | Evidencia |
| --- | --- | --- |
| Archivo original localizado y leído íntegramente en TASK012 | Sí | `TASK008.md` (TASKS.zip) |
| Correcciones reflejadas en los documentos actuales | Parcial | `docs/assessment/001-repository-assessment.md:155-159` |
| Informe de ejecución original | No disponible | No consta |
| Pruebas de aplicación | No ejecutadas | No existe código de aplicación |

## 7. Hallazgos y correcciones

Resumen verificable en `docs/assessment/001-repository-assessment.md:155-159`:

1. Proceso, AGENTS, contexto de roles y README: se revisó la política Git; el propietario define el alcance, autoriza operaciones Git y conserva la decisión final; los agentes pueden ejecutar `git add`, `git commit`, `git push` y crear PR con autorización expresa, pero nunca fusionan; las operaciones destructivas quedan prohibidas de forma absoluta.
2. ADR 0002: la ubicación definitiva del composition root se incluyó entre los detalles provisionales pendientes de concretar durante el scaffold.
3. Requisitos: se añadió Q-17 para la obligatoriedad de la fecha y la fuente del tipo de cambio, sin modificar FR-11.
4. Referencias: se sustituyeron las menciones que presuponían una revisión ya abierta por «esta rama» en el assessment y en el contexto de evolución.
5. Evaluación histórica: se aclaró que los patrones generales de `dist/` y `coverage/` fueron acotados posteriormente en TASK006.

Esta tarea es el punto de cambio de la política Git: antes, TASK006 y TASK007 reservaban la publicación al propietario; TASK008 introdujo la autorización expresa para que OpenCode + DeepSeek ejecutaran `git add`, `git commit`, `git push` y crearan PR. El merge siguió reservado al propietario y la prohibición de comandos destructivos se mantuvo absoluta.

## 8. Autorizaciones Git

La política general permite a OpenCode + DeepSeek `git add`, `git commit`, `git push` y creación de PR con autorización expresa. TASK008 **no autoriza** ninguna operación de publicación: no se autorizan `git add`, commit, push, PR ni merge. El merge corresponde exclusivamente al propietario y los comandos destructivos están prohibidos sin excepciones.

## 9. Resultado y decisiones pendientes

- Resultado: correcciones aplicadas según el assessment; no consta informe original de TASK008.
- Decisiones pendientes: aprobación del propietario y autorización separada de publicación.
- Riesgos: el resumen del assessment no sustituye el informe completo de ejecución.

## 10. Referencias

- `TASK008.md` (TASKS.zip; fuente original facilitada por el propietario)
- [TASK007-audit-task.md](TASK007-audit-task.md)
- [TASK007-audit.md](../02-audits/TASK007-audit.md)
- [TASK009-final-audit-task.md](TASK009-final-audit-task.md)
- `docs/assessment/001-repository-assessment.md:153-159`
- `docs/process/ai-assisted-development.md`
- `AGENTS.md`
