# Guía de instalación y desarrollo local

## Quick Start

Prerrequisitos instalados por el evaluador: Git, Python 3.13 (`>=3.13,<3.14`), Node.js
24 (`>=24.15,<25`) y npm 11 (`>=11,<12`). Se requiere Internet para descargar dependencias
y para obtener conversiones USD/GBP de Frankfurter. No se instalan runtimes automáticamente
ni se necesitan privilegios de administrador.

### Windows — probado en Windows 11 / PowerShell

```powershell
git clone https://github.com/Toni2Morales/SaaS-O-Matic.git
cd SaaS-O-Matic
.\start.ps1
```

Abrir `http://127.0.0.1:4200`. Swagger: `http://127.0.0.1:8000/docs`; health: `/health`.
Para detener solo los procesos propios verificados, ejecutar en otra terminal desde la carpeta principal del repositorio:

```powershell
.\start.ps1 -Stop
```

Para volver a iniciar, ejecutar `.\start.ps1` desde la carpeta principal del repositorio.

La base por defecto se crea en `backend/var/saas_o_matic.sqlite3`, solo si Alembic necesita
crear/migrar el esquema; detener o reiniciar los servicios no elimina la base ni sus filas.
No se insertan datos de demostración automáticamente.

### Linux: previsto; run de GitHub Actions pendiente. macOS no probado

```bash
git clone https://github.com/Toni2Morales/SaaS-O-Matic.git
cd SaaS-O-Matic
bash start.sh
```

URLs iguales. Detención segura, desde otra terminal en el repositorio:

```bash
bash start.sh --stop
```

Los scripts usan loopback únicamente. Los puertos configurados son 8000 (FastAPI) y 4200
(Angular); si uno está ocupado, se informa y se aborta. No se mata el proceso que lo ocupa ni
se cambia permanentemente la configuración. Libere el puerto de forma consciente o detenga
el servicio que le pertenece antes de reintentar. El workflow pretende validar los scripts
en runners efímeros, incluyendo flujo HTTP, parada, reinicio y persistencia; hasta que el run
termine, no se declara verificado.

### Qué hace el arranque

1. Comprueba versiones/prerrequisitos y puertos antes de iniciar procesos.
2. Crea `backend/.venv` si falta; exige Python 3.13 también en el venv existente.
3. Instala el paquete backend dentro de ese venv con `requirements.lock` como constraints,
   ejecuta `pip check` y aplica `alembic upgrade head`.
4. Ejecuta `npm ci --ignore-scripts` en `frontend/`; es intencionalmente reproducible y
   puede descargar/rehacer `node_modules` en cada invocación. No ejecuta scripts npm de
   terceros ni instala dependencias globales.
5. Inicia Uvicorn/Angular en loopback y espera health HTTP y página frontend.
6. Muestra URLs, ubicación de logs y comando de parada.

Si falla un paso crítico, el script no anuncia el arranque como exitoso. Limpia únicamente
los procesos que inició y cuya identidad se puede verificar. No borra SQLite. Los logs
temporales de procesos se almacenan fuera del repositorio bajo `%LOCALAPPDATA%\SaaS-O-Matic\run`
en Windows o `${XDG_RUNTIME_DIR:-${TMPDIR:-/tmp}}/saas-o-matic-<uid>` en Bash.

## Instalación manual

### Backend (PowerShell)

```powershell
git clone https://github.com/Toni2Morales/SaaS-O-Matic.git
cd SaaS-O-Matic\backend
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]" -c requirements.lock
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -m alembic upgrade head
.\.venv\Scripts\python.exe -m uvicorn saas_o_matic.bootstrap.main:app --host 127.0.0.1 --port 8000
```

No se requiere activar el entorno. El manifiesto exige Python `>=3.13,<3.14`; toda
instalación de Python se realiza dentro de `.venv`. `requirements.lock` es un archivo de
constraints (no un lock con hashes); la build isolation y versión de pip no están fijadas.
No exporte `DATABASE_URL` para el arranque normal: runtime y Alembic usan la misma
configuración, por defecto `backend/var/saas_o_matic.sqlite3`. Solo se admite SQLite de
archivo. El backend no carga `.env` automáticamente.

Comprobar `GET http://127.0.0.1:8000/health`, OpenAPI en `/openapi.json` y Swagger en
`/docs`. En otra terminal detener Uvicorn con `Ctrl+C`.

Pruebas y calidad desde `backend/` con el venv:

```powershell
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m ruff format --check .
.\.venv\Scripts\python.exe -m mypy .
.\.venv\Scripts\python.exe -m pip check
```

### Backend manual (Linux/macOS; secuencia prevista, probar la plataforma antes de declararla verificada)

```bash
git clone https://github.com/Toni2Morales/SaaS-O-Matic.git
cd SaaS-O-Matic/backend
python3.13 -m venv .venv
.venv/bin/python -m pip install -e '.[dev]' -c requirements.lock
.venv/bin/python -m pip check
.venv/bin/python -m alembic upgrade head
.venv/bin/python -m uvicorn saas_o_matic.bootstrap.main:app --host 127.0.0.1 --port 8000
```

Use `.venv/bin/python -m ...` para ejecutar pruebas/calidad. `python3.13` debe ser el
intérprete del sistema compatible ya instalado.

### Frontend

En otra terminal:

```powershell
cd SaaS-O-Matic\frontend
npm ci --ignore-scripts
npm start
```

`npm start` usa el script del manifest y el proxy `src/proxy.conf.json`: Angular sirve
`127.0.0.1:4200`, `/api/*` se reenvía a FastAPI `127.0.0.1:8000` y se elimina el prefijo
artificial `/api`. La API real no tiene ese prefijo. Angular no consulta directamente
Frankfurter. Para detener, `Ctrl+C` en la terminal de cada servidor.

Comprobaciones desde `frontend/`:

```powershell
npm run typecheck
npm run lint
npm run format:check
npm test
npm run test:coverage
npm run build
npm run e2e
```

Playwright solo es necesario para QA. Instalar browsers oficiales cuando se ejecute E2E:

```powershell
npx playwright install chromium firefox webkit
```

La aplicación normal no necesita ni instala browsers Playwright.

Para Linux/macOS, desde una terminal del clon:

```bash
cd SaaS-O-Matic/frontend
npm ci --ignore-scripts
npm start
```

Comandos de calidad equivalentes: los `npm run ...` anteriores son multiplataforma.

## Solución de problemas

- **Python ausente/incompatible:** instale manualmente una versión 3.13 compatible desde
  la fuente oficial; los scripts no instalan runtimes. `py -0p` (Windows) permite ver
  intérpretes registrados. Un `.venv` existente de otra versión no se borra ni reemplaza.
- **Node/npm incompatibles:** revise `node --version`, `npm --version` y `frontend/.nvmrc`;
  el proyecto no instala herramientas globales.
- **Puertos ocupados:** scripts abortan sin terminar procesos; compruebe la propiedad y
  libere 8000/4200 manualmente. No fuerce la parada de procesos no identificados.
- **Migraciones:** el log informa de Alembic. Si la base es importante, haga una copia
  antes de actualizar; las migraciones 0003/0004 tienen operaciones SQLite no transaccionales
  y downgrades que pueden bloquear por pérdida de datos.
- **Backend/proxy no disponible:** compruebe `/health`, que Uvicorn escucha en loopback
  8000 y que `frontend/src/proxy.conf.json` apunta al mismo puerto; no cambie el proxy de
  producción (P-05 sigue pendiente).
- **Error FX/HTTP 503:** proveedor de referencia sin tasa válida o disponible; pruebe EUR
  (identidad, sin acceso de red). Reintente más tarde; no use tasas ficticias como fallback.
- **npm ci falla:** revise conectividad y versión npm 11; la instalación usa
  `--ignore-scripts` por diseño. No use `npm audit fix`, `--force` ni scripts globales.
- **Browser Playwright ausente:** instale los browsers oficiales indicados para QA; no es
  requisito para ejecutar el MVP.
- **Restricción de PowerShell:** ejecute el script firmado por el repositorio desde la
  terminal local según la política de la organización. No cambie la política global ni
  use `Set-ExecutionPolicy -Scope CurrentUser/LocalMachine`.

Quick Start es solo evaluación local. No resuelve autenticación, autorización, CORS,
multi-tenancy, hosting, proxy productivo ni la decisión P-05; no exponga estos servicios a
Internet o a la red local.
