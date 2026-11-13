# AGENTS.md

Instrucciones para agentes de IA (OpenCode, DeepSeek u otros) que trabajen en este repositorio. El propietario del repositorio es la autoridad final: ninguna decisión de alcance o arquitectura se toma sin su aprobación explícita.

## 1. Antes de implementar

Lee, en este orden, la documentación relevante:

1. [`docs/requirements/functional-requirements.md`](docs/requirements/functional-requirements.md) — requisitos, restricciones, supuestos y preguntas abiertas.
2. [`docs/adr/0001-technology-stack.md`](docs/adr/0001-technology-stack.md) y [`docs/adr/0002-architecture.md`](docs/adr/0002-architecture.md) — decisiones técnicas aceptadas.
3. [`docs/process/ai-assisted-development.md`](docs/process/ai-assisted-development.md) — flujo de trabajo y reglas de Git.
4. [`ai-workspace/README.md`](ai-workspace/README.md) — índice de tareas y auditorías; y [`ai-workspace/00-project-context/`](ai-workspace/00-project-context/) — contexto de evolución y roles.
5. La especificación de la tarea en `docs/specs/` (se creará en una tarea posterior; todavía no existe).

### Roles y artefactos

- El propietario define el objetivo, aprueba las decisiones y autoriza las operaciones Git.
- ChatGPT analiza, propone arquitectura, redacta instrucciones y revisa resultados **fuera del repositorio**. No materializa documentos ni código en el repositorio.
- OpenCode + DeepSeek implementa y materializa en el repositorio las especificaciones, planes, documentos, código e informes, y registra las evidencias en `ai-workspace/`.
- `spec.md`, `plan.md` y `tasks.md` se ubicarán en `docs/specs/NNN-<funcionalidad>/` cuando se inicie la funcionalidad; no se crean en esta fase. Los informes de tarea y las auditorías se registran en `ai-workspace/01-tasks/` y `ai-workspace/02-audits/`.
- La revisión independiente se basa en las evidencias facilitadas y no se presenta como validación automática ni como trabajo del implementador.

Si la tarea no está especificada, contradice la documentación o requiere una decisión de negocio, **detente y pregunta**. No rellenes huecos con suposiciones.

## 2. Disciplina de alcance

- Implementa únicamente lo aprobado en la tarea y su especificación.
- No inventes precios, impuestos, tasas, divisas ni reglas de negocio. Los datos no definidos se registran como preguntas abiertas.
- No añadas dependencias, servicios o tecnologías sin justificar la necesidad y marcar la decisión como pendiente de aprobación.
- No amplíes el alcance de forma silenciosa: si detectas trabajo adicional necesario, descríbelo y espera aprobación.
- No refactorices código ajeno a la tarea sin justificarlo.

## 3. Convenciones técnicas

- Python 3.13 como versión de proyecto (aunque el entorno local pueda tener otra; no cambies la configuración del sistema).
- Código, nombres de ficheros y símbolos en inglés. Documentación, mensajes de interfaz y comentarios explicativos en español.
- Tipado explícito y compatible con mypy. Formato y lint con Ruff.
- El dominio no importa FastAPI, Pydantic ni SQLAlchemy. Las dependencias apuntan hacia dentro (presentación → aplicación → dominio). Fuente principal: [ADR 0002](docs/adr/0002-architecture.md).
- Los esquemas de API (Pydantic) no se reutilizan como modelos de persistencia (SQLAlchemy).
- Los importes monetarios se manejan con `Decimal` y EUR como divisa base; nunca con `float`.
- Toda funcionalidad nueva incluye pruebas proporcionales a su riesgo.
- No incluyas en los cambios ficheros generados, bases de datos locales ni secretos.

## 4. Git y GitHub

El propietario define el alcance de cada tarea, decide las cuestiones funcionales y técnicas pendientes, autoriza expresamente las operaciones Git que formen parte de la tarea, revisa los cambios y resultados y conserva la decisión final sobre la integración. El merge de los pull requests lo ejecuta personalmente el propietario.

- Nunca trabajes directamente sobre `main`.
- Prepara los cambios en local, revisa el diff completo y presenta el resultado.
- Puedes ejecutar `git add`, `git commit`, `git push` y crear pull requests **solo cuando la tarea incluya expresamente esa operación y el propietario la haya autorizado**. La autorización debe identificar la operación y los cambios o la rama afectados.
- La autorización para implementar una tarea no implica autorización para publicar cambios. Si la tarea no contempla expresamente commit, push o creación de PR, limítate a preparar los cambios y presentar el resultado.
- Puedes redactar descripciones y resúmenes de pull request.
- No fusiones pull requests: el merge corresponde exclusivamente al propietario.
- Prohibido `git push --force`, `git push --force-with-lease`, `git reset --hard`, `git clean -fd` y cualquier otra operación destructiva que pueda eliminar, sobrescribir o descartar trabajo del repositorio. Esta prohibición es absoluta y no admite excepciones mediante autorización escrita. Si consideras que una operación destructiva es necesaria, detente y explica el problema al propietario.
- No reescribas el historial existente.

Los prefijos de rama admitidos son `docs/`, `feature/`, `fix/`, `test/` y `refactor/`. El formato de commit es Conventional Commits. La fuente principal de ambas convenciones es el [proceso de desarrollo](docs/process/ai-assisted-development.md). Un cambio futuro de esta política requiere autorización explícita y específica del propietario.

## 5. Pruebas y validación

- Ejecuta las comprobaciones que existan en el repositorio (Ruff, mypy, Pytest, Vitest, build) antes de proponer un cambio.
- No afirmes que una comprobación pasa si no la has ejecutado.
- Reporta los resultados reales, incluidos los fallos y las comprobaciones no ejecutadas.
- Si una comprobación no puede ejecutarse por falta de dependencias, indícalo y no la sustituyas por una suposición.

## 6. Informe final

Cada intervención termina con un informe breve que incluya:

1. Resumen del trabajo realizado.
2. Ficheros creados, modificados o eliminados.
3. Decisiones tomadas y su justificación.
4. Comprobaciones ejecutadas y resultados reales.
5. Supuestos, dudas y riesgos pendientes.
6. Estado de la rama y del árbol de trabajo.

## 7. Cuándo detenerse

Detente y consulta al propietario si:

- La tarea exige una decisión de negocio no documentada.
- Es necesario cambiar la arquitectura, el stack o el modelo de datos aprobado.
- Aparecen conflictos con trabajo local del propietario.
- Si una tarea parece requerir una escritura directa en `main`, detente, explica el conflicto al propietario y no ejecutes esa escritura. La prohibición se mantiene; el cambio debe canalizarse mediante una rama y un pull request, o gestionarse personalmente por el propietario.
- Se requiere una operación destructiva: detente, explica el problema al propietario y no la ejecutes.
- La especificación es ambigua o incompleta.

## 8. Entorno

- El propietario trabaja en Windows con PowerShell, Git y GitHub CLI.
- Evita rutas absolutas específicas de una máquina en ficheros versionados.
- Respeta los finales de línea definidos en [`.gitattributes`](.gitattributes).
