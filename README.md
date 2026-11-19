# SaaS-O-Matic

**SaaS-O-Matic** es una aplicación local para que un equipo comercial registre clientes y
estime suscripciones SaaS corporativas. Incluye dashboard, búsqueda, ficha e historial de
clientes, y un simulador mensual de usuarios, almacenamiento y llamadas API. FastAPI calcula
precios, impuestos y conversiones, y guarda snapshots en SQLite; Angular ofrece la interfaz.
Es un MVP de evaluación, no un sistema de facturación ni un servicio preparado para producción
pública.

## Entorno de referencia y prerrequisitos

Entorno local de referencia de esta entrega: **Windows 10 Pro, versión 22H2 (build 19045),
x64, Windows PowerShell 5.1**. La verificación final se registra en
[`TASK047F`](ai-workspace/01-tasks/TASK047F-final-windows-delivery-report.md). No se afirma
compatibilidad certificada con Windows 11, Linux, macOS ni Windows Server.

Instala previamente:

- [Git for Windows](https://git-scm.com/download/win).
- [Python 3.13 para Windows](https://www.python.org/downloads/windows/), versión `>=3.13,<3.14`.
  Comprueba `py -3.13 --version`. El script prefiere el Python Launcher `py` y no instalará
  Python por ti.
- [Node.js 24](https://nodejs.org/en/download), versión `>=24.15,<25`, que incluye npm.
  Se requiere npm `>=11,<12`; comprobado con `node --version` y `npm --version`.
- Internet para descargar dependencias en la primera instalación y para las referencias FX
  USD/GBP. EUR funciona sin el proveedor externo.

Versiones observadas durante la validación: Git 2.56.0.windows.2, Python 3.13.17, pip 26.2.2,
Node.js 24.22.0, npm 11.19.1, Angular/CLI 22.2.6 y TypeScript 6.0.3. FastAPI 0.163.1 y
SQLite 3.50.4 (runtime de Python) se ejecutan en el entorno virtual del backend. Los rangos
compatibles están definidos por los manifests; las versiones locales son un corte probado,
no límites mínimos adicionales. Angular CLI, Playwright y SQLite no requieren instalación
global separada.

## Quick Start (Windows PowerShell)

Una vez instalados los prerrequisitos, desde una terminal PowerShell:

```powershell
git clone https://github.com/Toni2Morales/SaaS-O-Matic.git
cd SaaS-O-Matic
.\start.ps1
```

Abrir:

- Aplicación Angular: <http://127.0.0.1:4200>
- Swagger UI: <http://127.0.0.1:8000/docs>
- Health FastAPI: <http://127.0.0.1:8000/health>
- OpenAPI JSON: <http://127.0.0.1:8000/openapi.json>

El primer arranque crea `backend/.venv` con el Python 3.13 ya instalado, instala el backend
en ese entorno y comprueba `pip check`; aplica las migraciones Alembic hasta la revisión
actual; ejecuta `npm ci --ignore-scripts` en `frontend/`; luego inicia FastAPI y Angular
escuchando solo en loopback y espera ambos health checks. Los runtimes no se instalan
automáticamente. Los arranques posteriores vuelven a validar/instalar el backend y ejecutar
Alembic idempotente y `npm ci --ignore-scripts` conforme al lockfile. npm no ejecuta scripts
de instalación de terceros. No hay inserción automática de clientes de demo.

Para detener los procesos registrados por esta copia, abrir otra terminal en la raíz y usar:

```powershell
.\start.ps1 -Stop
```

Reiniciar ejecutando de nuevo:

```powershell
.\start.ps1
```

La base predeterminada está en `backend/var/saas_o_matic.sqlite3`; detener o reiniciar no borra los
datos. Haz una copia externa antes de migrar datos que quieras conservar. Los puertos son
8000 (FastAPI) y 4200 (Angular). Si uno está ocupado, el script aborta sin detener ni alterar
el listener existente. Revisa la propiedad del proceso por tu cuenta antes de liberarlo.
Logs/registro de procesos se guardan bajo `%LOCALAPPDATA%\SaaS-O-Matic\run`.

La guía detallada incluye primera/segunda ejecución, instalación manual, solución de
problemas y límites: [desarrollo local](docs/guides/local-development.md).

## Funcionalidades y alcance

- Clientes de ES/PT/FR/DE/IT/NL y un solo plan `standard`; identificadores españoles DNI/NIF,
  NIE y CIF/NIF validados algorítmicamente. Fuera de España la validación es genérica y no
  equivale a comprobación fiscal oficial. Ningún algoritmo prueba la existencia o titularidad.
- Dashboard, búsqueda por razón social/identificador fiscal, ficha e historial paginado.
- Simulador mensual con slider y entrada manual; preview no persistente y guardado explícito.
- Precio progresivo acumulativo por usuario: primeros 10 a 10 EUR, usuarios 11–50 a 8 EUR,
  resto a 5 EUR. Para España, 15 usuarios: subtotal 140,00, IVA general 29,40, total 169,40
  EUR; 16 usuarios: subtotal 148,00, IVA 31,08, total 179,08 EUR.
- Impuestos generales simplificados versionados; no son asesoramiento fiscal y no representan
  regímenes especiales, reducciones ni todas las circunstancias de una operación.
- EUR base y conversión de presentación EUR/USD/GBP. Frankfurter v2 se consume **desde el
  backend** y devuelve tasas de referencia fechadas, no cotizaciones continuas de mercado.
  Caché por proceso de 24 h desde obtención y timeout de 5 s; si falla no se inventa una tasa
  y la API informa error 503. EUR usa identidad y no requiere Internet.
- Almacenamiento GB y llamadas mensuales se registran como información: no generan cargos.
- Las simulaciones guardadas son históricas; no se recalculan con catálogos/tipos actuales.

Más detalle: [pricing, impuestos y FX](docs/guides/pricing-and-limits.md) y
[trazabilidad FR01–FR11](docs/requirements/final-delivery-traceability.md).

## Arquitectura y desarrollo

Monolito modular: navegador Angular → proxy de desarrollo → API REST FastAPI/OpenAPI → casos
de uso/dominio → adaptadores SQLAlchemy/SQLite y cliente Frankfurter. El backend es autoridad
de cálculos y persistencia; el navegador no consulta Frankfurter. Arquitectura, modelo de
datos, organización y secuencias existentes se describen en
[`solution-overview.md`](docs/architecture/solution-overview.md). Especificaciones y ADR se
indexan desde [requisitos](docs/requirements/functional-requirements.md) y
[`ai-workspace`](ai-workspace/README.md).

## Calidad local y estado CI

La aceptación de esta entrega se basa en la campaña local reproducible desde un clon limpio
Windows 10 descrita en el [informe TASK047F](ai-workspace/01-tasks/TASK047F-final-windows-delivery-report.md).
No se confunden resultados Windows con GitHub Actions. Los workflows `Quality` y `Quick Start`
se conservan como controles futuros, ahora manuales; no se ejecutaron en TASK047F. No se
publican badges que sugieran un estado verde.

Históricamente, [Quality #44556931530](https://github.com/Toni2Morales/SaaS-O-Matic/actions/runs/44556931530)
falló seis comprobaciones de overflow a 320 px en Chromium/Firefox/WebKit. La corrección
publicada en `54bd817` no resolvió el caso: [Quality #44566635410](https://github.com/Toni2Morales/SaaS-O-Matic/actions/runs/44566635410)
volvió a fallar los mismos seis tests y midió 334 px. El arranque Angular no pasó health en
Windows Actions; Bash no verificó el PID al detener/reiniciar en Ubuntu:
[Quick Start #44556931645](https://github.com/Toni2Morales/SaaS-O-Matic/actions/runs/44556931645)
y [#44566635425](https://github.com/Toni2Morales/SaaS-O-Matic/actions/runs/44566635425).
A47-01/02/03 siguen **pendientes y aplazados por decisión expresa del propietario**; no se
presentan como corregidos. La ausencia de CI verde no es por sí sola incumplimiento del reto,
pero no valida otros sistemas operativos.

## Desarrollo asistido por IA

El proceso versionado enlaza requisitos → ADR/SPEC → plan/tareas → aprobación humana →
implementación iterativa → pruebas/auditoría/correcciones → publicación y revisión humana.
Los registros y artefactos auténticos disponibles están en
[`ai-workspace/README.md`](ai-workspace/README.md) y el
[inventario de evidencias](ai-workspace/01-tasks/TASK047-evidence-inventory.md). No se
reconstruyen conversaciones ni prompts literales no conservados. El propietario debe aportar
4–8 extractos/capturas auténticos si desea demostrar interacciones privadas; eliminar nombres,
rutas personales, secretos y datos fiscales antes de compartirlos.

## Guía de demostración y capturas

Guion sintético de 5–10 minutos: [docs/guides/demo.md](docs/guides/demo.md). Se propone una
selección de 8 capturas existentes; archivos y descripciones están en el inventario. Todas
permanecen fuera del repositorio hasta aprobación humana. Las capturas TASK047A adicionales
son del navegador Chromium local con API fixture interceptada (no integración/FX real) y
tampoco se publican.

## Limitaciones

MVP local sin autenticación/autorización, multi-tenancy, facturación, cobro ni aprovisionamiento.
SQLite tiene límites de concurrencia. Solo se valida fiscalmente por algoritmo España; el
catálogo de impuestos simplifica el caso general. Frankfurter puede no estar disponible. No
hay proxy productivo ni decisión de hosting/despliegue (P-05); no exponer a Internet ni usar
datos reales de clientes. Responsive y axe son verificaciones automatizadas parciales; no hay
certificación integral WCAG. No se declara aptitud para producción pública ni compatibilidad
universal.

## Instalación manual

Ver [guía local](docs/guides/local-development.md): backend `.venv` Python 3.13, instalación
`pip install -e ".[dev]" -c requirements.lock`, `pip check`, Alembic; frontend
`npm ci --ignore-scripts` y `npm start`. Playwright se instala solo si se van a ejecutar E2E.

## Licencia

Distribuido bajo licencia [MIT](LICENSE).
