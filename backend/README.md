# Backend de SaaS-O-Matic

Backend con Python 3.13, FastAPI y una estructura de monolito modular. Incluye el alta de clientes de extremo a extremo: dominio fiscal, catálogo MVP con el único plan `standard`, caso de uso, persistencia SQLAlchemy, migración Alembic, endpoint `POST /customers` y pruebas de API.

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
- `POST /customers`: alta de un cliente.

Ejemplo de alta:

```powershell
$body = @{
    legal_name = 'Empresa Ejemplo S.L.'
    tax_id = 'B12345674'
    email = 'contacto@ejemplo.es'
    country = 'ES'
    plan = 'standard'
} | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/customers -ContentType 'application/json' -Body $body
```

`B12345674` es un identificador ficticio de prueba, sintáctica y algorítmicamente válido.

`legal_name` se recorta: se eliminan los espacios iniciales y finales, se conservan los interiores y debe contener entre 1 y 255 caracteres después del recorte. La respuesta y la base de datos contienen el valor normalizado.

La respuesta correcta es `201 Created` con `id`, `legal_name`, `tax_id`, `email`, `country`, `plan` y `created_at` en UTC. No se envía cabecera `Location`. Los errores controlados usan `application/problem+json`:

- `422` para datos inválidos, campos ausentes, razón social vacía o fuera del rango 1–255, país o plan no admitidos y JSON malformado.
- `409` para un identificador fiscal duplicado en el mismo país.
- `500` para un error interno no controlado, sin detalles internos.

## Pruebas y calidad

```powershell
python -m pytest
python -m ruff check .
python -m ruff format --check .
python -m mypy .
python -m pip check
```

Las pruebas cubren `/health`, OpenAPI, reglas de dependencia, validación de DNI/NIF, NIE y CIF/NIF, catálogo de plan `standard`, esquemas Pydantic, normalización y límites de `legal_name`, caso de uso, persistencia SQLite temporal, migración Alembic, ciclo `downgrade`/`upgrade`, errores `application/problem+json` y la API `POST /customers`.

## Estructura

```text
backend/
├── .venv/                  # Entorno virtual local; no versionado
├── alembic.ini
├── migrations/             # Configuración Alembic y revisión 0001_create_customers
├── pyproject.toml
├── requirements.lock
├── README.md
├── src/
│   └── saas_o_matic/
│       ├── __init__.py
│       ├── domain/         # Python puro; sin FastAPI, Pydantic ni SQLAlchemy
│       │   └── customers/  # Entidad, objetos de valor, errores y puerto
│       ├── application/    # Casos de uso; depende de domain
│       │   └── customers/  # Catálogos, DTOs, errores y CreateCustomer
│       ├── infrastructure/ # Adaptadores; implementa puertos de domain
│       │   ├── database.py
│       │   └── customers/  # Modelo, mapeador y repositorio SQLAlchemy
│       ├── presentation/   # Routers y esquemas HTTP; depende de application
│       │   ├── problems.py
│       │   └── customers/  # Router, dependencias y esquemas Pydantic
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

La ubicación definitiva del composition root sigue pendiente. `bootstrap/` es una propuesta provisional, no una decisión arquitectónica cerrada. `bootstrap/main.py` construye la fábrica de sesiones de forma perezosa y sustituye la dependencia del caso de uso de clientes para abrir una sesión por petición.

## Alembic y base de datos

La configuración está en `alembic.ini` y `migrations/`. La revisión `0001_create_customers` crea la tabla `customers` con:

- UUID compatible con SQLite.
- `legal_name`, `tax_id`, `email`, `country`, `plan` y `created_at` no nulos.
- Restricción única `(country, tax_id)`.
- `created_at` en UTC.

La URL por defecto es `sqlite:///./var/saas_o_matic.sqlite3` y puede sustituirse con `DATABASE_URL`. Los ficheros SQLite están excluidos por `.gitignore`. Las pruebas usan bases temporales creadas con Alembic; no se usa `create_all()` como sustituto de la migración.

Comandos de comprobación:

```powershell
python -m alembic heads
python -m alembic upgrade head
python -m alembic current
python -m alembic downgrade base
python -m alembic upgrade head
```

Para no tocar una base de desarrollo, se puede usar una ruta temporal:

```powershell
$db = Join-Path $env:TEMP 'saas-o-matic-task020.sqlite3'
$env:DATABASE_URL = "sqlite:///$($db.Replace('\', '/'))"
python -m alembic upgrade head
```

## Dependencias

| Dependencia | Versión | Uso |
| --- | --- | --- |
| FastAPI | 0.163.1 | Framework HTTP y generación de OpenAPI. |
| Pydantic | 2.14.3 | Validación y serialización de esquemas. |
| email-validator | 2.4.0 | Validación sintáctica de `EmailStr`. |
| SQLAlchemy | 2.1.8 | Modelo y repositorio de clientes. |
| Alembic | 1.20.1 | Migración de la tabla `customers`. |
| Uvicorn | 0.54.0 | Servidor ASGI para ejecutar la aplicación. |
| Pytest | 9.2.0 | Pruebas automatizadas. |
| HTTPX | 0.28.1 | Cliente usado por las pruebas de la API. |
| Ruff | 0.17.5 | Lint y formato. |
| mypy | 2.4.1 | Comprobación estática de tipos. |

TASK020 no añade dependencias ni modifica `pyproject.toml` ni `requirements.lock`.

## Alcance de esta fase

Incluido:

- Entorno virtual aislado.
- Estructura de paquetes y capas.
- Aplicación FastAPI con `/health`, `/openapi.json` y `POST /customers`.
- Dominio fiscal de clientes: DNI/NIF, NIE y CIF/NIF.
- Catálogo MVP con el único plan `standard`.
- Caso de uso de alta operativo.
- Modelo SQLAlchemy, repositorio y migración Alembic.
- Esquemas Pydantic y errores `application/problem+json`.
- Pruebas y configuración de calidad.

Excluido:

- Endpoints de listado, detalle, edición o eliminación.
- Planes adicionales, precios de planes y prestaciones asociadas.
- Autenticación, autorización y multi-tenancy.
- Simulaciones, impuestos y divisas.
- Frontend.

## Limitaciones

- SQLite limita la concurrencia y no reproduce producción.
- La estructura global por capas puede no ser la frontera modular definitiva.
- El lock de dependencias no es estricto ni usa hashes.
- No hay CI configurada.
- No consta una revisión independiente humana de TASK020.
