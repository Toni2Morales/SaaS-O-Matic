# TASK047 — Plan de entrega final, Quick Start e integración continua

| Campo           | Estado inicial                                                                    |
| --------------- | --------------------------------------------------------------------------------- |
| Repositorio     | `Toni2Morales/SaaS-O-Matic`, `origin`, visibilidad GitHub verificada: **PUBLIC**  |
| PR #7           | MERGED; URL comprobada; merge commit `99c0ebac984c70521c4e3c94226b35c15303f572`   |
| Rama de trabajo | `docs/final-delivery`, creada desde `origin/main` actualizado                     |
| HEAD inicial    | `99c0ebac984c70521c4e3c94226b35c15303f572`, igual a `origin/main`                 |
| `main` local    | `8371f9f608ce6e06984cc501d8240e1b7edf34d5`; no se modifica                        |
| Estado inicial  | Índice vacío; sin cambios tracked. DOCX original untracked, excluido y no abierto |
| Integridad      | [Manifiesto inicial SHA-256](TASK047-initial-hashes.json), 276 rutas tracked      |

## 1. Objetivos

Preparar una entrega evaluable sin cambiar comportamiento ni reglas del MVP: Quick Start
seguro en PowerShell/Bash; README y manuales exactos; diagramas reales; CI de calidad sin
deployment; SDD y trazabilidad; inventarios de evidencias auténticas; guía de demo; matriz
del reto y auditoría final; clon limpio y mediciones reales.

## 2. Alcance y restricciones

Permitidos: documentación, `start.ps1`, `start.sh` y workflows/configuración CI. No añadir
dependencias ni alterar código, pruebas, migraciones, reglas económicas, LICENSE o informes
históricos. No Docker/cloud/CD, PR/merge, tags/releases ni imágenes sin aprobación. No
publicar DOCX, copias, `TASKS.zip`, secretos, SQLite, entornos o resultados ficticios.
Commits/pushes ordinarios solo en `docs/final-delivery`, staging selectivo, de acuerdo con
los cinco hitos especificados por TASK047.

## 3. Inventario documental inicial

- Requisitos canónicos: `docs/requirements/functional-requirements.md` y
  `requirements-traceability.md`; restricciones y estados históricos se conservarán.
- Stack/arquitectura: ADR-0001/0002/0003; P-05 sigue pendiente.
- Especificaciones de negocio 001–006 y frontend 007–010; planes/tareas e informes de
  implementación/auditoría en `ai-workspace/`.
- READMEs raíz/backend/frontend describen estados pre-merge y requieren reconciliación;
  leerlos antes de editarlos.
- No existe `.github/workflows` a la fecha inicial; revisar configuraciones y comandos
  reales antes de diseñar CI.
- Diagramas deben reflejar el código y revisiones Alembic 0001–0004, no hipótesis.

## 4. Estrategia Quick Start

Verificar Python `>=3.13,<3.14`, Node `>=24.15,<25`, npm `>=11,<12` (workspace exige npm
11), Git y puertos 8000/4200. No instalar runtimes ni terminar procesos ajenos. Crear
`backend/.venv`; instalar solo en ese venv con constraints declarados; ejecutar Alembic
sin borrar BD; `npm ci --ignore-scripts`; levantar procesos loopback propios, health-check
backend y comprobar Angular. Ante puerto ocupado, abortar con instrucciones seguras. Al
fallar, limpiar solo procesos lanzados y cuya identidad se verifique. Documentar parada,
restart y persistencia. Validar Windows local y Linux en runner si portable; macOS queda
sin verificar si no hay ejecución real.

## 5. Estrategia CI

Backend: Python compatible, instalación aislada, pip check, Ruff check/format, mypy, pytest.
Frontend: Node compatible, npm ci sin scripts, typecheck, lint, Prettier, Vitest/cobertura,
build. Playwright multibrowser solo con acción oficial fijada por SHA completo verificado,
permisos mínimos, timeout y sin secretos; usar estrategia reproducible y valorar runner
Playwright oficial. Integración API/SQLite fixture determinista solo si se puede aislar sin
cambiar producción. No ejecutar proveedor FX real en checks requeridos. Scripts CI no
despliegan ni modifican branch protection.

## 6. Instalación, evidencias y revisión

Revisar lockfiles y comandos desde manifests/config; medir clon limpio temporal de la rama,
primera y segunda ejecución, persistencia, parada y flujo completo, sin tocar recursos
preexistentes. Reconciliar con resultados TASK046 históricos, sin sumar ejecuciones como
pruebas únicas. Seleccionar solo informes/artefactos auténticos ya versionados; identificar
capturas TASK043–046 en carpeta externa autorizada sin leer DOCX. No copiar ni publicar
imágenes hasta aprobación expresa; solicitar al propietario conversaciones/capturas que no
estén disponibles. Guía demo con tax ID sintético validado en código.

## 7. Publicaciones incrementales

1. `build: simplify local application startup` — scripts y documentación inmediata.
2. `docs: prepare final SaaS-O-Matic delivery documentation` — README, manuales, diagramas,
   pricing, matriz y limitaciones.
3. `ci: add automated backend and frontend quality checks` — workflows y evidencia de runs.
4. `docs: document AI-assisted development and demonstration workflow` — SDD, guía demo,
   inventarios textuales/visuales sin imágenes no aprobadas.
5. `docs: finalize delivery verification and quality report` — clon limpio, CI y auditoría.

Antes/después de cada hito: verificar estado y diff, hashes protegidos, privacidad, identidad
GitHub noreply, staging selectivo, diff staged íntegro/check; push normal y verificar ref
remota. Parar ante fallo funcional, cambio imprevisto de `origin/main`, problema de
seguridad, falta de propiedad de recurso o incompatibilidad que requiera cambiar alcance.

## 8. Riesgos

- `requirements.lock` aplica restricciones, no hashes ni lock estricto; build isolation no
  está totalmente reproducible. npm está fijado por lock; scripts se deshabilitan.
- Dos servidores y proxy requieren puertos libres; no detener el servicio preexistente 8000.
- La app y CI dependen de runtimes modernos; Playwright browser install puede requerir red.
- FX externo es de referencia y puede no estar disponible; EUR funciona sin proveedor.
- Estados de documentación base pueden quedar obsoletos tras merge; no reescribir informes
  históricos, añadir actualizaciones contextualizadas.
- Evidencias de interacción IA/capturas no disponibles para el agente requieren aportación/
  aprobación humana; no se reconstruyen retrospectivamente.

## 9. Criterios de aceptación

Evaluar CA01–CA77 individualmente según TASK047, con estados y evidencia. Bloqueos
funcionales, instalación no reproducible o seguridad grave impiden veredicto favorable.
No considerar cumplidos CI, plataformas, imágenes o interacción privada hasta ejecutar,
comprobar o recibir autorización/evidencia auténtica. El veredicto no equivale a preparación
para producción pública ni autorización de entrega externa.

## 10. Evidencia inicial de Quick Start Windows (TASK047)

- Intérpretes/runtime existentes: Python launcher 3.13.17, Node 24.22.0 y npm 11.19.1.
- Árbol de trabajo en Windows 11, PowerShell, ruta con espacios. Primera ejecución del
  script: Python editable install dentro de `backend/.venv`, pip check, Alembic 0001–0004,
  npm ci `--ignore-scripts` (416 paquetes, zero advisories), health HTTP backend/frontend.
- Smoke API: alta sintética, preview de 15 usuarios `169.40 EUR`, historial preview 0,
  save `169.40`, historial 1. Email sintético example.com; no se envió correo.
- Segunda ejecución tras `start.ps1 -Stop`: ambos servicios disponibles; cliente/simulacion
  continuaron en SQLite. Parada verificada dejó 8000/4200 libres; SQLite no se borró.
- Puerto 8000 ocupado por un listener de prueba propio: el script falló claramente y el
  listener permaneció activo hasta cerrarlo por su owner. No se tocaron procesos ajenos.
- No se midió tiempo instrumental de inicio en el árbol habitual; se medirá el clon limpio.
- Aplicar Alembic desde cero creó las tablas durante la primera ejecución. El smoke posterior
  dejó 1 cliente sintético y 1 simulación en `backend/var/saas_o_matic.sqlite3`, archivo
  ignorado que no se eliminará; el clon limpio temporal tendrá su propia base.
- Bash validado sintácticamente con `bash -n`; no se considera ejecución Linux/macOS. Runs
  efímeros de Actions quedan pendientes hasta publicar/verificar workflows.
