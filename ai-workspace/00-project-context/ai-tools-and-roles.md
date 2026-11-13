# Herramientas y roles de IA

| Campo | Valor |
| --- | --- |
| Fecha | 2026-11-13 |
| Estado | Propuesto — pendiente de aprobación; utilizado provisionalmente como referencia de trabajo |
| Revisión | TASK010 (2026-11-13) |
| Ámbito | Sesiones de desarrollo asistido por IA en este repositorio |

## 1. Entorno de trabajo

| Elemento | Valor |
| --- | --- |
| Sistema operativo | Windows |
| Shell | PowerShell |
| Control de versiones | Git |
| Plataforma remota | GitHub (`Toni2Morales/SaaS-O-Matic`) |
| Gestión de GitHub | GitHub CLI (`gh`), autenticado por el propietario |
| Entorno de codificación | OpenCode |
| Modelo de implementación | DeepSeek v4.1 Flash Free |
| Asesor de arquitectura y revisión | ChatGPT |

Las versiones de herramientas y modelos pueden cambiar. Cuando cambien, se actualizará este documento; no se asumirán capacidades no verificadas.

## 2. Reparto de responsabilidades

### 2.1 Propietario (desarrollador humano)

- Define el producto, el alcance y las prioridades.
- Responde a las preguntas abiertas de negocio y decide las cuestiones funcionales y técnicas pendientes.
- Aprueba especificaciones, planes y cambios de arquitectura.
- Autoriza expresamente las operaciones Git que formen parte de una tarea y revisa los cambios y resultados.
- Conserva la decisión final sobre la integración y ejecuta personalmente el merge de los pull requests.
- Revisa el trabajo y tiene la última palabra.

### 2.2 ChatGPT — asesoría, instrucciones y revisión independiente

- Analiza requisitos y detecta ambigüedades.
- Propone arquitectura y alternativas con sus contrapartidas.
- Redacta instrucciones, especificaciones y planes **fuera del repositorio**.
- Revisa resultados y evidencias de forma independiente.
- **No** materializa documentos ni código en el repositorio ni aprueba su propio trabajo.

### 2.3 OpenCode + DeepSeek — implementación y materialización

- Ejecuta tareas previamente especificadas y aprobadas.
- Materializa en el repositorio las especificaciones, planes, documentos, código, pruebas e informes dentro del alcance acordado.
- Registra las evidencias y el proceso en `ai-workspace/01-tasks/` y `ai-workspace/02-audits/`.
- Prepara cambios locales, revisa el diff y ejecuta las comprobaciones disponibles.
- Puede ejecutar `git add`, `git commit`, `git push` y crear pull requests cuando la tarea incluya expresamente esa operación y el propietario la autorice. La autorización debe identificar la operación y los cambios o la rama afectados.
- La autorización para implementar una tarea no implica autorización para publicar cambios. Si la tarea no contempla expresamente commit, push o creación de PR, solo prepara los cambios y presenta el resultado.
- Redacta descripciones y resúmenes de PR.
- **No** fusiona pull requests; el merge corresponde exclusivamente al propietario.
- **No** ejecuta operaciones destructivas como `git push --force`, `git push --force-with-lease`, `git reset --hard`, `git clean -fd` o cualquier otra que pueda eliminar, sobrescribir o descartar trabajo. Esta prohibición es absoluta y no admite excepciones por autorización escrita. Si considera que una operación destructiva es necesaria, se detiene y consulta al propietario.
- **No** cambia la arquitectura, el stack ni el alcance por iniciativa propia.

### 2.4 Autoría, materialización y revisión

- **Autoría intelectual o propuesta de contenido:** ChatGPT puede analizar, proponer arquitectura, redactar instrucciones y revisar resultados.
- **Materialización en el repositorio:** OpenCode + DeepSeek escribe los archivos y deja constancia de la autoría material.
- **Revisión independiente:** ChatGPT revisa las evidencias facilitadas. OpenCode + DeepSeek materializa el informe de revisión y registra la fuente; el informe no se presenta como validación automática ni como trabajo propio del implementador.
- **Aprobación:** el propietario decide la aceptación y autoriza las operaciones Git que procedan.

### 2.5 Flujo de entrega

1. El propietario define el objetivo y aprueba las decisiones.
2. ChatGPT analiza, propone arquitectura, redacta instrucciones y revisa resultados fuera del repositorio.
3. OpenCode + DeepSeek implementa y materializa en el repositorio las especificaciones, planes, documentos, código e informes.
4. OpenCode + DeepSeek registra las evidencias y el proceso en `ai-workspace/`.
5. ChatGPT realiza una revisión independiente a partir de las evidencias facilitadas.
6. El propietario decide la aceptación y autoriza expresamente las operaciones Git que procedan.

## 3. Artefactos de contexto

| Ruta | Contenido |
| --- | --- |
| `AGENTS.md` | Reglas operativas para agentes de IA. |
| `docs/requirements/` | Requisitos, restricciones, supuestos y preguntas abiertas. |
| `docs/adr/` | Decisiones de arquitectura y stack, con su estado. |
| `docs/process/` | Flujo de trabajo, ramas, commits y prohibiciones. |
| `docs/assessment/` | Evaluaciones del repositorio. |
| `docs/specs/` | Especificaciones por funcionalidad (se creará al iniciar la primera funcionalidad; todavía no existe). |
| `ai-workspace/README.md` | Índice de tareas, auditorías y reglas de trazabilidad. |
| `ai-workspace/00-project-context/` | Evolución del proyecto y contexto de herramientas. |
| `ai-workspace/01-tasks/` | Registros de tareas, instrucciones, evidencias, validaciones y decisiones. |
| `ai-workspace/02-audits/` | Auditorías independientes, hallazgos y correcciones. |

Una sesión de IA debe leer estos artefactos antes de proponer cambios. El contexto no se transmite por memoria del modelo, sino por documentos versionados.

### 3.1 Ubicación y materialización de artefactos

| Artefacto | Ubicación prevista | Materializa |
| --- | --- | --- |
| `spec.md` | `docs/specs/NNN-<funcionalidad>/spec.md` | OpenCode + DeepSeek |
| `plan.md` | `docs/specs/NNN-<funcionalidad>/plan.md` | OpenCode + DeepSeek |
| `tasks.md` | `docs/specs/NNN-<funcionalidad>/tasks.md` | OpenCode + DeepSeek |
| Informe de tarea | `ai-workspace/01-tasks/TASKxxx.md` | OpenCode + DeepSeek |
| Auditoría | `ai-workspace/02-audits/TASKxxx-audit.md` | OpenCode + DeepSeek |

`docs/specs/` no se crea en esta fase: las rutas son ubicaciones previstas para cuando se inicie la primera funcionalidad. La autoría intelectual o propuesta de contenido puede ser de ChatGPT; la materialización en el repositorio corresponde a OpenCode + DeepSeek.

## 4. Reglas de colaboración

1. **Una tarea, un objetivo.** No se mezclan funcionalidades ni refactorizaciones no solicitadas.
2. **Especificar antes de implementar.** Sin especificación aprobada no se escribe código de producto.
3. **No inventar.** Precios, impuestos, divisas y reglas fiscales provienen del propietario.
4. **Reportar con honestidad.** Los resultados de pruebas se copian de la ejecución real, incluidos los fallos.
5. **Parar ante la duda.** Es preferible una pregunta a una decisión silenciosa.
6. **Revisión humana y autorización expresa.** Los agentes pueden ejecutar `git add`, `git commit`, `git push` y crear pull requests solo con autorización expresa para esa operación. La autorización para implementar no implica autorización para publicar. El merge corresponde exclusivamente al propietario.

## 5. Registro de intervenciones

Cada intervención debe dejar constancia de:

- Qué se pidió y qué se hizo.
- Qué ficheros cambiaron.
- Qué decisiones se tomaron y por qué.
- Qué comprobaciones se ejecutaron y con qué resultado.
- Qué quedó pendiente o requiere aprobación.

Este registro vive en `ai-workspace/01-tasks/TASKxxx.md`; las auditorías independientes se registran en `ai-workspace/02-audits/TASKxxx-audit.md`. Cuando la decisión es estructural, se registra además en un ADR. No se reconstruyen conversaciones ni se atribuyen afirmaciones que no estén documentadas.

## 6. Limitaciones conocidas

- El modelo de implementación puede no conocer cambios recientes del ecosistema; las versiones se verifican en el repositorio y en la documentación oficial.
- El agente no tiene acceso a decisiones que solo existen en la cabeza del propietario: deben estar escritas.
- Las comprobaciones automáticas no sustituyen la revisión de negocio ni la revisión de seguridad.
- El entorno local puede diferir del de integración; las diferencias se documentan.
