# Backend de SaaS-O-Matic

Scaffold inicial del backend con Python 3.13, FastAPI y una estructura de monolito modular. Esta fase no incluye lógica de negocio, modelos de datos ni acceso real a base de datos.

## Requisitos

- Python 3.13.
- PowerShell en Windows para los comandos de activación documentados.
- Git para el control de versiones.

## Crear y activar el entorno virtual

Desde la raíz del repositorio:

```powershell
cd backend
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

A partir de este punto, todos los comandos se ejecutan desde `backend/`. Si ya estás en ese directorio, omite `cd backend`.

Si PowerShell bloquea la activación por la política de ejecución, se puede habilitar temporalmente solo para la sesión actual:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

El entorno virtual está excluido de Git mediante la regla `.venv` del `.gitignore` raíz. No se debe versionar su contenido.

Antes de instalar dependencias, comprobar que el intérprete activo pertenece al entorno virtual:

```powershell
python -c "import sys; print(sys.executable); print(sys.prefix)"
```

Ambas rutas deben apuntar a `backend\.venv`.

## Instalar dependencias

Desde `backend/` y con el entorno activado:

```powershell
python -m pip install -e ".[dev]" -c requirements.lock
python -m pip check
```

- Las dependencias directas están fijadas con versiones exactas en `pyproject.toml`.
- `requirements.lock` contiene las versiones resueltas de las dependencias transitivas y se aplica con `-c` como **restricciones**, no como un lock estricto.
- La estrategia actual reduce la variación de versiones, pero no garantiza por sí sola un conjunto cerrado de paquetes ni la integridad de los artefactos.
- No se deben instalar paquetes fuera de `.venv` ni usar instalaciones globales.

### Verificar las dependencias instaladas

El siguiente control compara las versiones instaladas con las fijadas en `requirements.lock`:

```powershell
$lock = Get-Content requirements.lock | Where-Object { $_ -and -not $_.StartsWith('#') } | Sort-Object
$installed = python -m pip freeze --exclude-editable | Sort-Object
$diff = Compare-Object -ReferenceObject $lock -DifferenceObject $installed
if ($diff) {
    $diff
    throw 'Las dependencias instaladas no coinciden con requirements.lock.'
}
'Dependencias instaladas: coinciden con requirements.lock.'
```

Este control detecta desviaciones después de instalar, pero no impide que pip resuelva un conjunto distinto ni cubre la build isolation.

Las dependencias necesarias para construir e instalar el proyecto se pueden consultar con:

```powershell
python -c "import tomllib; from pathlib import Path; print(tomllib.loads(Path('pyproject.toml').read_text(encoding='utf-8'))['build-system']['requires'])"
```

La salida esperada es `['setuptools==84.2.1']`. Esa dependencia se instala en el entorno aislado de build y **no forma parte de `requirements.lock`**; por tanto, la estrategia actual no la bloquea desde el lock.

### Alcance y límites de la estrategia actual

- `-c requirements.lock` aplica restricciones; pip puede incorporar paquetes no listados si aparecen nuevas dependencias.
- La build isolation no está cubierta por el lock.
- No se usan hashes de artefactos.
- La versión de `pip` no está fijada.
- El control anterior detecta desviaciones, pero no garantiza por sí solo una reinstalación idéntica.

Estrategias más estrictas, no adoptadas en esta tarea:

- Instalar primero `python -m pip install -r requirements.lock` y después `python -m pip install -e . --no-deps`: reduce el margen de resolución, pero sigue sin hashes y sin cubrir la build isolation.
- Generar un lock con hashes mediante una herramienta como `pip-compile --generate-hashes` o equivalente: mejora la integridad de los artefactos, pero añade herramientas y un flujo de mantenimiento; requeriría aprobación del propietario.

## Ejecutar la aplicación

```powershell
python -m uvicorn saas_o_matic.bootstrap.main:app --reload
```

La aplicación expone:

- `GET /health`: comprobación de infraestructura; devuelve `{"status": "ok"}`.
- `GET /openapi.json`: esquema OpenAPI generado por FastAPI.

Ejemplo de comprobación en PowerShell:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
Invoke-RestMethod http://127.0.0.1:8000/openapi.json
```

## Pruebas y calidad

```powershell
python -m pytest
python -m ruff check .
python -m ruff format --check .
python -m mypy .
```

Las pruebas cubren el endpoint `/health`, la disponibilidad de `/openapi.json` y las reglas de dependencia de las capas.

## Estructura

```text
backend/
├── .venv/                  # Entorno virtual local; no versionado
├── pyproject.toml
├── requirements.lock
├── README.md
├── src/
│   └── saas_o_matic/
│       ├── __init__.py
│       ├── domain/         # Python puro; sin FastAPI, Pydantic ni SQLAlchemy
│       ├── application/    # Casos de uso; depende de domain
│       ├── infrastructure/ # Adaptadores; implementa puertos de domain
│       ├── presentation/   # Routers y esquemas HTTP; depende de application
│       └── bootstrap/      # Composition root provisional
└── tests/
```

### Reglas de dependencia

```text
presentation  →  application  →  domain
                                     ↑
                          infrastructure
```

- `domain` no importa ninguna otra capa ni frameworks.
- `application` solo puede depender de `domain`.
- `infrastructure` solo puede depender de `domain`.
- `presentation` solo puede depender de `application`.
- Ninguna capa depende de `infrastructure` ni de `bootstrap`.
- `bootstrap` puede depender de todas las capas porque actúa como composition root.

La prueba `tests/test_architecture.py` analiza estáticamente imports absolutos y relativos resolubles. No garantiza imports dinámicos (`importlib.import_module`, `__import__`, etc.), que quedan fuera del alcance del análisis estático.

La ubicación definitiva del composition root sigue pendiente. `bootstrap/` es una propuesta provisional, no una decisión arquitectónica cerrada. No se ha implementado todavía ninguna funcionalidad de negocio.

## Dependencias del scaffold

| Dependencia | Versión | Uso |
| --- | --- | --- |
| FastAPI | 0.163.1 | Framework HTTP y generación de OpenAPI. |
| Pydantic | 2.14.3 | Validación y serialización de esquemas. |
| SQLAlchemy | 2.1.8 | Base para la persistencia futura; no se usa aún. |
| Alembic | 1.20.1 | Base para migraciones futuras; no se usa aún. |
| Uvicorn | 0.54.0 | Servidor ASGI para ejecutar la aplicación. |
| Pytest | 9.2.0 | Pruebas automatizadas. |
| HTTPX | 0.28.1 | Cliente usado por las pruebas de la API. |
| Ruff | 0.17.5 | Lint y formato. |
| mypy | 2.4.1 | Comprobación estática de tipos. |

## Alcance de esta fase

Incluido:

- Entorno virtual aislado.
- Estructura de paquetes y capas.
- Aplicación FastAPI mínima.
- Endpoint de infraestructura `/health`.
- Esquema OpenAPI.
- Pruebas y configuración de calidad.

Excluido:

- Lógica de negocio.
- Modelos, migraciones y acceso a base de datos.
- Autenticación, autorización y multi-tenancy.
- Funcionalidades de clientes, simulaciones, impuestos o divisas.
