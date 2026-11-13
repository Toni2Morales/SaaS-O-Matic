# TASK004 — Corrección de hallazgos de la revisión documental

| Campo | Valor |
| --- | --- |
| ID | TASK004 |
| Título | Corrección de hallazgos de la revisión documental |
| Estado | Parcial; instrucción original disponible; informe original no disponible |
| Fecha | No documentada en la instrucción |
| Participantes | Propietario (decisiones y aprobación) / OpenCode + DeepSeek (autoría material indicada por la instrucción) / ChatGPT (sin escritura en el repositorio) |
| Autorización Git | Ninguna; la instrucción prohíbe `git add`, commit, push, PR y merge |

## 1. Objetivo y alcance

Aplicar las correcciones justificadas de la revisión documental TASK003, manteniendo el alcance estrictamente documental. La instrucción identificaba tres hallazgos mayores y varios menores, y pedía no resolver por cuenta propia las decisiones de negocio pendientes.

## 2. Instrucciones y fuentes

| Tipo de fuente | Referencia | Estado |
| --- | --- | --- |
| Instrucción original | `TASK004.md`, en `TASKS.zip` facilitado por el propietario | Disponible; el ZIP no se incorpora al repositorio |
| Resumen verificable | `docs/assessment/001-repository-assessment.md:128-140` y los documentos actuales | Parcial |
| Informe del agente | No disponible | No documentado |

## 3. Herramientas y participantes

- Propietario: conserva las decisiones de negocio y la aprobación final.
- OpenCode + DeepSeek: la instrucción indica que la elaboración material corresponde a OpenCode/DeepSeek; no consta informe original.
- ChatGPT: no se le atribuye la redacción material de los ADRs.
- Herramientas: Git, edición de Markdown y comprobaciones no destructivas.

## 4. Plan y decisiones

La instrucción pedía corregir:

1. **MAJ-1:** reproducibilidad de conversiones y contradicción con P-08; persistir importe base, divisa, tasa, fecha y fuente cuando estén disponibles.
2. **MAJ-2:** dirección de dependencias entre capas; `presentation` no importa `domain`; sin ciclos.
3. **MAJ-3:** autoría honesta de los ADRs y separación entre decisión, documento y aprobación.
4. **Menores:** ASM-02/Q-02, ASM-03/Q-03, estados documentales, fase 3 de evolución, separación P/Q, comentarios de `.gitignore`, patrones `env/`/`ENV/`, `.editorconfig`, Vitest, duplicación documental, Q-13/Q-14, `.env.example`, prefijos de rama, unidades de FR-04, `docs/specs/` y criterios de aceptación.

Restricciones: no implementar código, no añadir dependencias o scaffolding, no configurar CI/CD, no crear migraciones/modelos/endpoints, no hacer `git add`, commits, push, PR ni merge, no modificar `LICENSE` y no inventar decisiones de negocio.

## 5. Archivos afectados

Según la instrucción y el assessment:

- `docs/adr/0002-architecture.md`
- `docs/adr/0001-technology-stack.md`
- `docs/requirements/functional-requirements.md`
- `docs/process/ai-assisted-development.md`
- `README.md`
- `AGENTS.md`
- `.gitignore`
- `.editorconfig`
- `.env.example`
- Nota sobre `docs/specs/`

## 6. Validaciones ejecutadas

| Comprobación | Resultado | Evidencia |
| --- | --- | --- |
| Archivo original localizado y leído íntegramente en TASK012 | Sí | `TASK004.md` (TASKS.zip) |
| Correcciones reflejadas en los documentos actuales | Parcial | `docs/assessment/001-repository-assessment.md:130-140` |
| Informe de ejecución original | No disponible | No consta |
| Pruebas de aplicación | No ejecutadas | No existe código de aplicación |

## 7. Hallazgos y correcciones

Resumen verificable en `docs/assessment/001-repository-assessment.md:130-140`:

1. ADR 0002: se eliminó la contradicción entre FR-11 y P-08 y se aclaró que `presentation` no importa `domain`.
2. ADR 0001 y ADR 0002: se corrigió la autoría y se separó el estado de la decisión del estado del documento.
3. Requisitos: ASM-02 y ASM-03 quedaron como supuestos provisionales; se añadieron Q-13, Q-14 y Q-15; se precisaron FR-04 y FR-11.
4. Proceso, README y AGENTS: se alinearon los prefijos de rama y se redujo la duplicación.
5. `.gitignore`: se retiraron comentarios heredados y el patrón redundante `ENV/`.
6. `.editorconfig`: el límite de 100 se ajustó a 88 de forma provisional.
7. `.env.example`: se marcó como plantilla provisional.
8. Vitest: se retiró la afirmación de sustitución universal de Karma y se mantuvo la verificación pendiente.
9. `docs/specs/`: se indicó que todavía no existe y se creará en una tarea posterior.

## 8. Autorizaciones Git

Ninguna. La instrucción prohíbe `git add`, commit, push, PR y merge. No consta autorización para publicar cambios.

## 9. Resultado y decisiones pendientes

- Resultado: correcciones aplicadas según el assessment; no consta informe original de TASK004.
- Decisiones pendientes: conservar las preguntas de negocio abiertas y aprobar la base documental.
- Riesgos: el resumen del assessment no sustituye el informe completo de ejecución.

## 10. Referencias

- `TASK004.md` (TASKS.zip; fuente original facilitada por el propietario)
- [TASK003-independent-review.md](TASK003-independent-review.md)
- [TASK003-audit.md](../02-audits/TASK003-audit.md)
- `docs/assessment/001-repository-assessment.md:128-140`
- `docs/adr/0001-technology-stack.md`
- `docs/adr/0002-architecture.md`
