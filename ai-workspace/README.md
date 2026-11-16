# Trazabilidad del desarrollo asistido por IA

| Campo | Valor |
| --- | --- |
| Fecha de creación | 2026-11-13 |
| Estado | Registro preparado para revisión; limitaciones históricas documentadas |
| Ámbito | Colaboración entre el propietario, ChatGPT y OpenCode + DeepSeek |

## 1. Propósito

Este directorio conserva el rastro verificable del trabajo asistido por IA: qué se pidió, qué se hizo, quién participó, qué se validó, qué se corrigió y qué queda pendiente.

No sustituye a `docs/`. Los requisitos, ADRs, evaluaciones y proceso siguen siendo la fuente principal en `docs/`; aquí se registra el proceso y se enlaza a esos documentos para evitar duplicidad.

## 2. Estructura

```text
ai-workspace/
├── README.md
├── 00-project-context/
│   ├── architectural-evolution.md
│   └── ai-tools-and-roles.md
├── 01-tasks/
│   ├── _TEMPLATE.md
│   ├── TASK001-pending.md
│   ├── TASK002-pending.md
│   ├── TASK003-independent-review.md
│   ├── TASK004-review-corrections.md
│   ├── TASK005-pending.md
│   ├── TASK006-audit-corrections.md
│   ├── TASK007-audit-task.md
│   ├── TASK008-task007-corrections.md
│   ├── TASK009-final-audit-task.md
│   ├── TASK010-documentation-corrections.md
│   ├── TASK011-final-audit-task.md
│   ├── TASK012-original-task-sources.md
│   ├── TASK013-documentation-publication.md
│   ├── TASK014-backend-scaffold.md
│   ├── TASK015-backend-scaffold-audit.md
│   ├── TASK016-scaffold-corrections.md
│   ├── TASK017-backend-publication.md
│   ├── TASK018-customer-registration.md
│   ├── TASK019-customer-implementation.md
│   ├── TASK020-customer-registration-completion.md
│   └── TASK022-customer-validation-fix.md
└── 02-audits/
    ├── TASK003-audit.md
    ├── TASK005-audit.md
    ├── TASK007-audit.md
    ├── TASK009-audit.md
    ├── TASK011-audit.md
    └── TASK015-audit.md
```

### 2.1 Fuentes originales

En TASK012, el propietario facilitó un ZIP `TASKS.zip` con los diez archivos `TASK001.md`–`TASK010.md`. Los diez se comprobaron y se leyeron íntegramente antes de actualizar los registros. El ZIP no se incorpora al repositorio: los registros citan el nombre del archivo original y no copian su contenido completo.

`TASK011` y `TASK012` no forman parte de `TASKS.zip`. Su instrucción y su informe proceden de la sesión de OpenCode; se identifican así en los registros correspondientes.

`TASK013` y `TASK014` tampoco forman parte de `TASKS.zip`. Sus instrucciones proceden de la sesión de OpenCode. TASK013 registra la publicación y el merge del PR #1; TASK014 materializa el registro de TASK013 y el scaffold inicial del backend.

`TASK015` y `TASK016` tampoco forman parte de `TASKS.zip`. TASK015 registra la auditoría técnica del scaffold y TASK016 las correcciones posteriores.

`TASK017` registra la publicación del scaffold y el merge del PR #2 por el propietario. `TASK018` inicia la primera funcionalidad, documenta la especificación del alta de clientes y se detiene en el punto de control por decisiones funcionales pendientes. `TASK019` aplica las decisiones aprobadas e implementa la base técnica de clientes, manteniendo el endpoint y la migración bloqueados por el catálogo de planes. `TASK020` aprueba D-02, completa el catálogo `standard`, crea la migración Alembic y deja operativo `POST /customers` con pruebas de dominio, aplicación, infraestructura, migración y API. `TASK021` fue una auditoría en sesión, sin archivo de registro; sus hallazgos se trazan en `TASK022`. `TASK022` aplica D-15, corrige la validación de `legal_name` y añade pruebas de regresión.

## 3. Índice de tareas

| ID | Título | Estado | Registro | Auditoría | Fuente disponible |
| --- | --- | --- | --- | --- | --- |
| TASK001 | Initial Repository Assessment & Project Foundation | Parcial; instrucción original disponible; informe de ejecución no disponible | [TASK001-pending.md](01-tasks/TASK001-pending.md) | — | `TASK001.md` (TASKS.zip); informe de ejecución no disponible |
| TASK002 | Prepare PR #1: Project Foundation | Parcial; instrucción original disponible; informe de ejecución no disponible | [TASK002-pending.md](01-tasks/TASK002-pending.md) | — | `TASK002.md` (TASKS.zip); archivos actuales verificables |
| TASK003 | Independent Review Package for PR #1 | Parcial; instrucción original disponible; informe original no disponible | [TASK003-independent-review.md](01-tasks/TASK003-independent-review.md) | [TASK003-audit.md](02-audits/TASK003-audit.md) | `TASK003.md` (TASKS.zip); informe original no disponible |
| TASK004 | Corrección de hallazgos de la revisión documental | Parcial; instrucción original disponible; resumen en el assessment | [TASK004-review-corrections.md](01-tasks/TASK004-review-corrections.md) | — | `TASK004.md` (TASKS.zip); resumen en el assessment |
| TASK005 | Auditoría final independiente de la base documental | Parcial; instrucción original disponible; informe original no disponible | [TASK005-pending.md](01-tasks/TASK005-pending.md) | [TASK005-audit.md](02-audits/TASK005-audit.md) | `TASK005.md` (TASKS.zip); hallazgos referenciados por TASK006 |
| TASK006 | Corrección de hallazgos de la auditoría final | Parcial; instrucción original disponible; resumen en el assessment | [TASK006-audit-corrections.md](01-tasks/TASK006-audit-corrections.md) | — | `TASK006.md` (TASKS.zip); resumen en el assessment |
| TASK007 | Auditoría independiente de las correcciones TASK006 | Parcial; instrucción original disponible; informe original no disponible | [TASK007-audit-task.md](01-tasks/TASK007-audit-task.md) | [TASK007-audit.md](02-audits/TASK007-audit.md) | `TASK007.md` (TASKS.zip); veredicto referenciado por TASK008 |
| TASK008 | Corrección final de hallazgos TASK007 | Parcial; instrucción original disponible; resumen en el assessment | [TASK008-task007-corrections.md](01-tasks/TASK008-task007-corrections.md) | — | `TASK008.md` (TASKS.zip); resumen en el assessment |
| TASK009 | Auditoría final de documentación y trazabilidad en `ai-workspace/` | Completada; informe del agente | [TASK009-final-audit-task.md](01-tasks/TASK009-final-audit-task.md) | [TASK009-audit.md](02-audits/TASK009-audit.md) | `TASK009.md` (TASKS.zip); informe del agente |
| TASK010 | Corrección documental y trazabilidad del desarrollo asistido por IA | Completada; pendiente de revisión | [TASK010-documentation-corrections.md](01-tasks/TASK010-documentation-corrections.md) | — | `TASK010.md` (TASKS.zip); informe en el registro |
| TASK011 | Auditoría de aceptación y preparación del primer PR | Completada; informe del agente | [TASK011-final-audit-task.md](01-tasks/TASK011-final-audit-task.md) | [TASK011-audit.md](02-audits/TASK011-audit.md) | Instrucción y respuesta de la sesión; no está en TASKS.zip |
| TASK012 | Incorporación de TASK originales y cierre documental | Completada; pendiente de revisión | [TASK012-original-task-sources.md](01-tasks/TASK012-original-task-sources.md) | — | Instrucción de la sesión; TASKS.zip con `TASK001.md`–`TASK010.md` |
| TASK013 | Publicación de la base documental y del primer PR | Completada; PR #1 fusionado por el propietario | [TASK013-documentation-publication.md](01-tasks/TASK013-documentation-publication.md) | — | Instrucción de la sesión; PR #1 y commit de merge `50f8047` |
| TASK014 | Scaffold del backend y entorno virtual Python | Completada; publicada en PR #2 | [TASK014-backend-scaffold.md](01-tasks/TASK014-backend-scaffold.md) | — | Instrucción de la sesión; comprobaciones ejecutadas en el repositorio |
| TASK015 | Auditoría técnica del scaffold Python | Completada; informe del agente | [TASK015-backend-scaffold-audit.md](01-tasks/TASK015-backend-scaffold-audit.md) | [TASK015-audit.md](02-audits/TASK015-audit.md) | Instrucción de la sesión; comprobaciones ejecutadas en el repositorio |
| TASK016 | Correcciones finales del scaffold antes del PR #2 | Completada; publicada en PR #2 | [TASK016-scaffold-corrections.md](01-tasks/TASK016-scaffold-corrections.md) | — | Instrucción de la sesión; correcciones y comprobaciones en el repositorio |
| TASK017 | Publicación del scaffold mediante PR #2 | Completada; PR #2 fusionado por el propietario | [TASK017-backend-publication.md](01-tasks/TASK017-backend-publication.md) | — | Instrucción de la sesión; PR #2 y merge commit `be755a6` |
| TASK018 | Primera funcionalidad: alta de clientes | Parcial; bloqueada en el punto de control por decisiones funcionales pendientes | [TASK018-customer-registration.md](01-tasks/TASK018-customer-registration.md) | — | Instrucción de la sesión; especificación y comprobaciones en el repositorio |
| TASK019 | Implementación de clientes con decisiones aprobadas | Parcial; base técnica implementada; endpoint y migración bloqueados por D-02, completados en TASK020 | [TASK019-customer-implementation.md](01-tasks/TASK019-customer-implementation.md) | — | Instrucción de la sesión; código, pruebas y validaciones en el repositorio |
| TASK020 | Cierre del alta de clientes: plan `standard`, Alembic y `POST /customers` | Completada y validada localmente; cambios no publicados | [TASK020-customer-registration-completion.md](01-tasks/TASK020-customer-registration-completion.md) | — | Instrucción de la sesión; código, migración, pruebas y validaciones en el repositorio |
| TASK022 | Corrección de `legal_name` y pruebas de regresión | Completada y validada localmente; cambios no publicados | [TASK022-customer-validation-fix.md](01-tasks/TASK022-customer-validation-fix.md) | — | Instrucción de la sesión; código, pruebas y validaciones en el repositorio |

### 3.1 Publicaciones

| PR | Rama | Base | Estado | Merge commit | Registro |
| --- | --- | --- | --- | --- | --- |
| [#1](https://github.com/Toni2Morales/SaaS-O-Matic/pull/1) | `docs/project-foundation` | `main` | Fusionado por el propietario el 2026-11-13T16:50:46Z | `50f80470eafc9517a277b652252391880b4a491e` | [TASK013](01-tasks/TASK013-documentation-publication.md) |
| [#2](https://github.com/Toni2Morales/SaaS-O-Matic/pull/2) | `feature/backend-scaffold` | `main` | Fusionado por el propietario el 2026-11-15T16:10:42Z | `be755a68a52392fd562eb3901e317bc85b1ed8e9` | [TASK017](01-tasks/TASK017-backend-publication.md) |

Los merges del PR #1 y del PR #2 fueron ejecutados personalmente por el propietario. El agente no ejecutó merge ni force-push.

## 4. Índice de auditorías

| Auditoría | Estado | Fuente | Nota |
| --- | --- | --- | --- |
| [TASK003-audit.md](02-audits/TASK003-audit.md) | Parcial | `TASK003.md` (TASKS.zip) y `docs/assessment/001-repository-assessment.md` | El informe original no está disponible; `TASK004.md` referencia tres hallazgos mayores. |
| [TASK005-audit.md](02-audits/TASK005-audit.md) | Parcial | `TASK005.md` (TASKS.zip) y `TASK006.md` | El informe original no está disponible; TASK006 referencia tres hallazgos bloqueantes. |
| [TASK007-audit.md](02-audits/TASK007-audit.md) | Parcial | `TASK007.md` (TASKS.zip) y `TASK008.md` | El informe original no está disponible; TASK008 referencia el veredicto NO APTA. |
| [TASK009-audit.md](02-audits/TASK009-audit.md) | Informe del agente | `TASK009.md` (TASKS.zip) y respuesta de TASK009 en la sesión | No es una validación independiente. |
| [TASK011-audit.md](02-audits/TASK011-audit.md) | Informe del agente | Instrucción y respuesta de TASK011 en la sesión de OpenCode | No es una validación independiente; veredicto APTA CON OBSERVACIONES. |
| [TASK015-audit.md](02-audits/TASK015-audit.md) | Informe del agente | Instrucción y respuesta de TASK015 en la sesión de OpenCode | No es una validación independiente; veredicto APTA CON OBSERVACIONES; hallazgos M1, M2 y B1–B4. |

## 5. Reglas de reconstrucción histórica

1. Utilizar únicamente información verificable en el repositorio, los informes facilitados y las instrucciones originales disponibles.
2. Identificar las instrucciones originales `TASK001.md`–`TASK010.md` como fuentes facilitadas en `TASKS.zip`; el ZIP no se versiona.
3. No inventar prompts literales, conversaciones, planes, fechas, ejecuciones ni resultados.
4. Distinguir entre instrucción original disponible, resumen verificable, informe aportado por el agente, resultado comprobado directamente e información no documentada.
5. Cuando no exista fuente original, indicar **«No documentado; pendiente de aportar fuente»**.
6. Cuando la evidencia no permita afirmar una ausencia, usar **«no consta»** en lugar de afirmaciones categóricas.
7. No presentar un informe del agente como una validación independiente.
8. Enlazar a `docs/` en lugar de duplicar requisitos y ADRs completos.
9. No atribuir a ChatGPT acciones de escritura en el repositorio ni ejecuciones de comandos que no realizó.
10. Conservar la evolución histórica de la política Git: TASK001–TASK007 mantenían una política restrictiva en la que los agentes no publicaban y TASK005–TASK007 reservaban expresamente commits, push, PR y merge al propietario; TASK008 introdujo la autorización expresa para que OpenCode + DeepSeek ejecutaran `git add`, `git commit`, `git push` y crearan PR; el merge sigue reservado al propietario y los comandos destructivos están absolutamente prohibidos.

## 6. Clasificación de fuentes

| Tipo | Significado |
| --- | --- |
| Instrucción original disponible | Texto de la tarea facilitado en la sesión o en un archivo identificable, como `TASK001.md`–`TASK010.md` de `TASKS.zip`. |
| Resumen verificable | Síntesis de una fuente existente, con enlace al documento que la contiene. |
| Informe aportado por el agente | Resultado elaborado por OpenCode + DeepSeek; no equivale a revisión independiente. |
| Resultado comprobado directamente | Dato obtenido mediante una comprobación ejecutada en el repositorio. |
| No documentado; pendiente de aportar fuente | No hay evidencia disponible; no se reconstruye de memoria. |
| No consta | La evidencia disponible no permite afirmar ni negar el hecho. |

## 7. Cómo añadir una tarea

1. Copiar `01-tasks/_TEMPLATE.md` con el nombre `TASKxxx-<descripcion>.md`.
2. Registrar objetivo, alcance, instrucciones y fuentes.
3. Indicar participantes y autorizaciones Git expresas.
4. Anotar archivos afectados y validaciones realmente ejecutadas.
5. Enlazar ADRs, requisitos, especificaciones e informes relacionados.
6. Si hay auditoría, crear `02-audits/TASKxxx-audit.md` y enlazarla desde el índice.
7. Actualizar las tablas de este README.

## 8. Limitaciones actuales

- Las instrucciones originales `TASK001.md`–`TASK010.md` están disponibles en `TASKS.zip`, pero el ZIP no se incorpora al repositorio.
- No constan los informes originales de ejecución de TASK001, TASK002, TASK004, TASK006 ni TASK008. El assessment resume TASK004, TASK006 y TASK008; los archivos actuales permiten verificar parte de TASK002.
- No constan los informes originales de auditoría de TASK003, TASK005 ni TASK007. `TASK004.md` referencia los hallazgos de TASK003; `TASK006.md` referencia los hallazgos bloqueantes de TASK005; `TASK008.md` referencia el veredicto NO APTA de TASK007.
- TASK009, TASK010, TASK011, TASK012, TASK013, TASK014, TASK015, TASK016, TASK017, TASK018, TASK019, TASK020 y TASK022 disponen de registros o informes del agente, pero no consta una revisión independiente humana. TASK021 fue una auditoría en sesión sin archivo de registro.
- TASK011, TASK012, TASK013, TASK014, TASK015, TASK016, TASK017, TASK018, TASK019, TASK020 y TASK022 no forman parte de `TASKS.zip`; su origen es la sesión de OpenCode.
- `docs/specs/001-customer-registration/` contiene la especificación cerrada: D-01 a D-15 están aprobadas; D-02 se aprobó en TASK020 con el único plan `standard` y D-15 en TASK022 para `legal_name`; el endpoint y la migración están implementados y validados localmente.
- Existe un backend con dominio fiscal, caso de uso operativo, modelo SQLAlchemy, repositorio, migración Alembic y `POST /customers`. No hay frontend ni endpoints de listado, detalle, edición o eliminación.
- El entorno virtual `backend/.venv` es local y no se versiona. `TASKS.zip` permanece sin seguimiento y está excluido localmente mediante `.git/info/exclude`; esa regla no se versiona.
- La estrategia de dependencias usa restricciones de versión, no un lock estricto con hashes; la build isolation queda fuera de `requirements.lock`.
- La prueba de arquitectura es estática y no cubre imports dinámicos.
- El inventario de 29 rutas del informe de TASK011 corresponde al estado auditado en TASK011; TASK012 añade y modifica documentación y actualiza el inventario.
