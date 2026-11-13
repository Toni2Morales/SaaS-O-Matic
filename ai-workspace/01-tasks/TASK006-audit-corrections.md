# TASK006 — Corrección de hallazgos de la auditoría final

| Campo | Valor |
| --- | --- |
| ID | TASK006 |
| Título | Corrección de hallazgos de la auditoría final |
| Estado | Parcial; instrucción original disponible; informe original no disponible |
| Fecha | No documentada en la instrucción |
| Participantes | Propietario (decisiones y aprobación) / implementador documental no identificado nominalmente / ChatGPT sin escritura en el repositorio |
| Autorización Git | Ninguna; la instrucción prohíbe `git add`, commit, push, PR y merge; la política histórica reservaba la publicación al propietario |

## 1. Objetivo y alcance

Corregir los tres hallazgos bloqueantes de TASK005 y las observaciones menores que pudieran resolverse sin introducir decisiones de negocio ni alterar el alcance. La tarea era exclusivamente documental y de configuración del repositorio; no debía crear código, instalar dependencias ni iniciar el scaffold.

## 2. Instrucciones y fuentes

| Tipo de fuente | Referencia | Estado |
| --- | --- | --- |
| Instrucción original | `TASK006.md`, en `TASKS.zip` facilitado por el propietario | Disponible; el ZIP no se incorpora al repositorio |
| Resumen verificable | `docs/assessment/001-repository-assessment.md:144-149` | Parcial |
| Informe del agente | No disponible | No documentado |

## 3. Herramientas y participantes

- Propietario: define el alcance, las decisiones y la aprobación final.
- Implementador documental: rol definido por la instrucción; no se identifica nominalmente.
- ChatGPT: no se le atribuye escritura en el repositorio.
- OpenCode + DeepSeek: entorno de trabajo del proyecto; no consta informe de ejecución de TASK006.
- Herramientas: Git, edición de Markdown y comprobaciones no destructivas.

## 4. Plan y decisiones

La instrucción pedía:

1. Comprobar rama, HEAD `8371f9f608ce6e06984cc501d8240e1b7edf34d5`, estado de archivos, ausencia de staged y cambios ajenos.
2. **ALTO-01:** separar el diagrama de dependencias de la composición; `presentation → application → domain`, `infrastructure → domain`, composition root fuera de las cuatro capas.
3. **MEDIO-01:** ampliar las excepciones de fixtures de SQLite para `tests/` y `backend/tests/`, sin abrir excepciones generales.
4. **MEDIO-02:** documentar que el propietario ejecuta personalmente commits, push, PR y merge; los agentes no publican aunque la tarea esté autorizada.
5. **BAJO-02 a BAJO-08:** Q-11, `dist/`/`coverage/`, `env/`/`ENV/`, coherencia de AGENTS con ADR 0002, precisión/redondeo, magnitud convertida y preguntas abiertas.
6. Validar fixtures, patrones de `.gitignore`, enlaces, tablas, bloques, codificación, secretos, `LICENSE`, staged/commits y diff completo.

Restricciones: no crear código, dependencias o scaffolding; no crear `docs/specs/`; no modificar `LICENSE`; no cambiar de rama; no ejecutar `git add`, commit, push, PR, merge ni comandos destructivos; no ampliar el alcance.

## 5. Archivos afectados

Según la instrucción y el assessment:

- `docs/adr/0002-architecture.md`
- `.gitignore`
- `docs/requirements/functional-requirements.md`
- `AGENTS.md`
- `docs/process/ai-assisted-development.md`
- `docs/assessment/001-repository-assessment.md`

## 6. Validaciones ejecutadas

| Comprobación | Resultado | Evidencia |
| --- | --- | --- |
| Archivo original localizado y leído íntegramente en TASK012 | Sí | `TASK006.md` (TASKS.zip) |
| Correcciones reflejadas en los documentos actuales | Parcial | `docs/assessment/001-repository-assessment.md:146-149` |
| Informe de ejecución original | No disponible | No consta |
| Pruebas de aplicación | No ejecutadas | No existe código de aplicación |

## 7. Hallazgos y correcciones

Resumen verificable en `docs/assessment/001-repository-assessment.md:146-149`:

1. ADR 0002: se separó el diagrama de dependencias de la composición; `presentation` depende de `application`, `application` de `domain`, `infrastructure` solo de `domain`, y el composition root queda fuera de las cuatro capas.
2. `.gitignore`: las excepciones de fixtures cubren `tests/` en la raíz y dentro de `backend/`, y las extensiones `.db`, `.sqlite` y `.sqlite3`; `dist/` se ancló a la raíz y a `frontend/`; `coverage/` a `frontend/`; se restauró `ENV/`.
3. Requisitos: Q-11 se reformuló para distinguir la tasa por simulación de una caché histórica; Q-08 incluye la precisión decimal; se añadió Q-16; los dos decimales quedan como supuesto provisional.
4. AGENTS: se añadió Pydantic a las prohibiciones del dominio y un enlace a ADR 0002 como fuente principal.

La política Git de TASK006 reservaba commits, push, PR y merge al propietario. TASK008 introdujo posteriormente la autorización expresa para que OpenCode + DeepSeek pudieran ejecutar `git add`, `git commit`, `git push` y crear PR; el merge y la prohibición absoluta de comandos destructivos se mantuvieron.

## 8. Autorizaciones Git

Ninguna. La instrucción prohíbe `git add`, commit, push, PR y merge; además, la política histórica de TASK006 reservaba esas operaciones al propietario. No consta autorización para publicar cambios.

## 9. Resultado y decisiones pendientes

- Resultado: correcciones aplicadas según el assessment; no consta informe original de TASK006.
- Decisiones pendientes: conservar las preguntas de negocio abiertas y aprobar la base documental.
- Riesgos: el resumen del assessment no sustituye el informe completo de ejecución.

## 10. Referencias

- `TASK006.md` (TASKS.zip; fuente original facilitada por el propietario)
- [TASK005-pending.md](TASK005-pending.md)
- [TASK005-audit.md](../02-audits/TASK005-audit.md)
- [TASK007-audit-task.md](TASK007-audit-task.md)
- `docs/assessment/001-repository-assessment.md:144-149`
