# Backend de SaaS-O-Matic

## Estado vigente TASK041 (base frontend)

TASK039 auditó el backend acumulado con dictamen **APTA CON OBSERVACIONES** y sin
hallazgos bloqueantes. TASK039B corrige la trazabilidad, el README, `.env.example`,
la configuración de SQLite y la validación defensiva de tasas FX. El runtime y
Alembic comparten ahora la resolución de `DATABASE_URL`; la base predeterminada
sigue siendo `backend/var/saas_o_matic.sqlite3`. Las tasas externas fuera de los
límites técnicos se rechazan antes de la caché y producen `503
application/problem+json`. La suite backend tiene 579 pruebas. El backend se integró
en `main` mediante PR #6 (merge `23cc43b486d20f7995a2cf29375e3f724f3c7c3f`).
TASK042 implementa localmente dashboard y gestión de clientes Angular e integra el
flujo navegador–FastAPI–SQLite temporal. El simulador, el E2E completo del MVP,
seguridad de despliegue y CI continúan pendientes; no se modificó el backend.

## Delta TASK038 (conservado)

GET /customers: search opcional (máximo255 tras recortar), limit20 por defecto
(1..100) y offset0 no negativo. Retorna {items,total,limit,offset}, incluyendo
created_at de cliente. Búsqueda parcial OR por legal_name/tax_id, Unicode casefold,
%/_/barra inversa literales; sin quitar acentos ni normalizar NFC. Orden nombre
casefold e id ASC, colación binaria no lingüística. Filtrado/COUNT/página en SQLite,
sin cargar tablas completas en aplicación. Se registra UDF por conexión, sin migración.

GET /customers/{customer_id}: mismo CustomerResponse de creación, sin historial
embebido. UUID inválido422; cliente desconocido404. GET /customers/{customer_id}/simulations:
página de snapshots ordenada created_at/id DESC; verifica cliente primero. Campos
históricos desconocidos (incluida divisa y total con impuesto) NULL, no cero ni EUR
inventado. No consulta Frankfurter ni catálogo fiscal actual; no edición/borrado.

POST /simulations/preview: mismo cuerpo estricto de creación; 200 con todos los
datos de cálculo de SPEC-005, sin id ni created_at de registro. Sí incluye la fecha
de obtención FX, que no es fecha de persistencia. CalculateSimulation/MonthlyEstimator
y caché compartidos con guardado; sin INSERT/UPDATE/DELETE. 404/422/503/500 problem+json;
EUR sigue sin proveedor. No Location ni cotización bloqueada: una referencia distinta
al guardar puede cambiar resultado. Guardar implica recalcular y POST /simulations explícito.

Ejemplos (sustituir UUID por cliente existente):

```text
GET /customers?search=%C3%89cole&limit=20&offset=0
GET /customers/560e1a4d-49f2-4bf7-a3e5-fb53ac4d14ec
GET /customers/560e1a4d-49f2-4bf7-a3e5-fb53ac4d14ec/simulations
POST /simulations/preview
```

```json
{"customer_id":"560e1a4d-49f2-4bf7-a3e5-fb53ac4d14ec","user_count":15,"storage_gb":250,"api_calls_per_month":100000}
```

Para ES/EUR el cálculo da subtotal140.00, IVA29.40, total/convertido169.40, tasa1,
source identity y fecha de referencia NULL; todas las cantidades son cadenas exactas.
Historial sin registros: {items:[],total:0,limit:20,offset:0}. Los contratos definitivos,
OpenAPI y guía Angular (debounce/cancelación/respuestas obsoletas/guardado) están en
[SPEC-006](../docs/specs/006-customer-queries-and-preview/spec.md).

Validación TASK038: 538 pruebas (+127), sin Internet en la suite, sin migraciones
ni dependencias nuevas. Previews repetidos probados con DML denegado por SQLite y
sin aumentar historial. Limitación: LIKE/UDF puede escanear tablas y offset no es
snapshot estable ante escrituras concurrentes.

Validación TASK039B: 579 pruebas (+41 sobre 538), Ruff, formato, mypy y `pip check`
correctos; 35 pines del lock sin cambios. Se añadieron pruebas de resolución
SQLite compartida, base temporal alternativa, aislamiento de la base predeterminada,
tasas FX patológicas, recuperación de caché, `503` en preview/guardado, ausencia de
filas parciales y corrupción controlada del historial. Sin publicación.

## Impuestos y divisas (TASK037, conservados)

POST /simulations mantiene sus cuatro campos obligatorios y añade display_currency
opcional (EUR predeterminado; EUR/USD/GBP). Respuesta incorpora IVA general por
país del cliente, total EUR y conversión HALF_UP; dinero y tasas como cadenas exactas.
Metadatos fiscales: país, tasa, fuente, versión, ámbito, consulta y vigencia conocida.
Metadatos FX: tasa, referencia, obtención UTC y fuente; EUR identity/1/fecha referencia NULL.
Proveedor Frankfurter v2 único; urllib estándar, sin nuevas dependencias. Caché por
proceso/par de 24h desde éxito, timeout5s; no expirados ni fallback ficticio. 503
problem+json sin tasa válida; EUR no consulta red. Referencias no son mercado continuo.
Sin transacción de escritura durante la espera externa; lectura inicial se finaliza.

Límites técnicos FX: la tasa externa debe ser finita, positiva, estar entre
`0.000001` y `1000000` y tener como máximo 32 dígitos significativos. Son límites
de plausibilidad, no comerciales: EUR/USD y EUR/GBP se mueven alrededor de 0,8–1,2.
El límite de respuesta externa sigue siendo 64 KiB. Una tasa fuera de rango se
rechaza antes de la caché y se traduce al `503` externo existente; no se redondea
silenciosamente, no se cachea y no se convierte en un `500`. Los snapshots
históricos fuera de esos límites se consideran datos corruptos y siguen la política
controlada de A39-05.

Migración 0004 añade calculation_snapshot TEXT (JSON versionado con dinero/tasas
en cadenas). Históricos quedan NULL, sin recalcular; nuevas simulaciones completas.
Downgrade bloquea antes de DDL si existen snapshots. Revisiones previas intactas.
Catálogo único configurable por inyección en infrastructure/tax_catalog.py; fuentes
contrastadas 2026-11-17. No actualizar tasas sin verificar y versionar. Estimación
general simplificada, sin reducidos, exenciones, B2B, inversión ni regiones especiales.
La caché se pierde al reiniciar y no se comparte entre procesos; timeout de socket
no constituye garantía de latencia total. No se impone edad máxima de referencia
adicional al TTL de obtención (festivos/fines de semana).

Contrato y fuentes: [SPEC-005](../docs/specs/005-taxes-and-currency-conversion/spec.md).
Las exclusiones fiscales/FX inferiores corresponden al estado anterior TASK036.

Validación TASK037: 411 pruebas (+71 sobre 340), Ruff, formato, mypy y pip check
correctos; lock 35 pines sin cambios. Smoke real 201 para EUR/USD/GBP en base temporal;
ninguna prueba automatizada requiere Internet. Sin staging ni publicación.

Backend Python 3.13/FastAPI, monolito modular. Alta para ES/PT/FR/DE/IT/NL,
plan único `standard`, simulaciones mensuales persistidas desde cero usuarios,
impuestos generales, conversión FX, lecturas, historial y preview. TASK036–039B
se integraron mediante PR #6. TASK041/042 implementan localmente la base y gestión
frontend de clientes; P-01 se resolvió en ADR 0003 y P-05 sigue pendiente.

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

El runtime y Alembic comparten la resolución de `DATABASE_URL`. Si no se define,
ambos usan `backend/var/saas_o_matic.sqlite3`; las rutas SQLite relativas se
interpretan desde `backend/`, no desde el directorio de trabajo actual. Solo se
admite SQLite de fichero: se rechazan otros motores, `:memory:` y parámetros de
consulta. El backend **no carga automáticamente** un archivo `.env`; exporta la
variable en el proceso que arranca Uvicorn o Alembic. La plantilla
[`.env.example`](../.env.example) documenta la variable y no contiene secretos.

La aplicación expone:

- `GET /health`: comprobación de infraestructura; devuelve `{"status": "ok"}`.
- `GET /openapi.json`: esquema OpenAPI generado por FastAPI.
- `POST /customers`: alta de un cliente.
- `POST /simulations`: simulación mensual con consumos informativos sin cargos.
- `GET /customers`: listado/búsqueda paginados.
- `GET /customers/{customer_id}`: detalle.
- `GET /customers/{customer_id}/simulations`: historial inmutable paginado.
- `POST /simulations/preview`: cálculo sin escritura.

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

Países exactos: ES/PT/FR/DE/IT/NL. España conserva DNI/NIF/NIE/CIF algorítmico.
Los demás países usan validación genérica, no fiscal oficial: 1..64 caracteres
después de recortar/colapsar espacios y pasar a mayúsculas; conservar puntuación,
rechazar controles Unicode Cc/Cf/Cs antes de normalizar. Unicidad `(country, tax_id)`.
Clientes conservan su política de campos adicionales (no se aplica forbid aquí).

### Contrato de simulaciones (ruptura TASK036)

```json
{"customer_id":"c58669e3-4bcb-49ca-b2c3-7f6eb17cb506","user_count":15,"storage_gb":250,"api_calls_per_month":100000}
```

UUID ilustrativo: sustituir por un cliente registrado. Los cuatro campos son
obligatorios. Enteros estrictos: usuarios y GB 0..1.000.000; llamadas 0..1.000.000.000.
No enviar billing_period: el servidor fija `monthly`. Campos desconocidos, ausentes,
nulos, booleanos, cadenas o decimales producen 422 `application/problem+json`.
Las peticiones antiguas sin consumos dejan de ser compatibles.

Respuesta 201: id, customer_id, user_count, storage_gb, api_calls_per_month,
billing_period, user_subtotal_eur (cadena de dos decimales) y created_at UTC/Z.
15 usuarios producen `140.00`; cero `0.00`. Sin cargos por GB/llamadas; sí se
calculan IVA general, total EUR y, con `display_currency` USD/GBP, conversión y
snapshot FX. Cliente inexistente: 404; tasa externa no válida: 503; error
inesperado: 500; sin Location.

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

Las pruebas cubren `/health`, OpenAPI, reglas de dependencia, validación de
DNI/NIF, NIE y CIF/NIF, catálogo de plan `standard`, esquemas Pydantic,
normalización y límites de `legal_name`, precios progresivos, persistencia SQLite
temporal, migraciones y ciclos `downgrade`/`upgrade`, impuestos, Frankfurter con
transporte simulado, caché/errores, consultas, historial inmutable, preview sin
escrituras, errores `application/problem+json`, resolución SQLite compartida y
tasas FX patológicas. La suite no depende de Internet.

TASK036: 340 pruebas superadas frente al baseline real de 240; cubren además seis
países, identificadores genéricos, cero, contrato estricto de consumos, traps Decimal,
SQL físico TEXT, sesión nueva/UTC y upgrade poblado con downgrade protegido.
Ruff, formato, mypy y pip check correctos; 35 pines verificados, sin dependencias nuevas.

TASK039B: 579 pruebas superadas (+41 sobre 538), Ruff, formato, mypy y `pip check`
correctos; 35 pines sin cambios y sin dependencias nuevas. Incluye base SQLite
alternativa migrada y usada por el runtime, comprobación de que la base
predeterminada no cambia, límites FX, recuperación de caché, `503` en preview y
guardado, ausencia de filas parciales y corrupción controlada del historial.

## Estructura

```text
backend/
├── .venv/                  # Entorno virtual local; no versionado
├── alembic.ini
├── migrations/             # Revisiones 0001–0004
├── pyproject.toml
├── requirements.lock
├── README.md
├── src/
│   └── saas_o_matic/
│       ├── __init__.py
│       ├── domain/         # Python puro; sin FastAPI, Pydantic ni SQLAlchemy
│       │   ├── customers/  # Entidad, objetos de valor, errores y puerto
│       │   ├── pricing/    # Tramos progresivos
│       │   └── simulations/# Cálculo fiscal/FX, snapshots y entidad
│       ├── application/    # Casos de uso; depende de domain
│       │   ├── customers/  # Catálogos, DTOs, errores y CreateCustomer
│       │   └── simulations/# Estimador, cálculo, consultas y casos de uso
│       ├── infrastructure/ # Adaptadores; implementa puertos de domain
│       │   ├── database.py # Motor, sesiones y resolución SQLite compartida
│       │   ├── customers/  # Modelo, mapeador y repositorio SQLAlchemy
│       │   ├── simulations/# Modelo, mapeador, repositorio y snapshots
│       │   ├── frankfurter.py
│       │   └── tax_catalog.py
│       ├── presentation/   # Routers y esquemas HTTP; depende de application
│       │   ├── problems.py
│       │   ├── customers/  # Router, dependencias y esquemas Pydantic
│       │   └── simulations/# Router, dependencias y esquemas Pydantic
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

La configuración está en `alembic.ini` y `migrations/`. El runtime y Alembic
comparten `resolve_database_url` en `infrastructure/database.py`:

- prioridad: `DATABASE_URL` del proceso, URL configurada por Alembic y ruta
  predeterminada `backend/var/saas_o_matic.sqlite3`;
- las rutas SQLite relativas se resuelven desde `backend/`;
- solo se admite SQLite de fichero; otros motores, `:memory:` y parámetros de
  consulta se rechazan con `ValueError`;
- no se carga ningún `.env` automáticamente ni se abren conexiones al importar;
- el runtime crea el motor de forma perezosa, así que importar la aplicación no
  crea el directorio ni el fichero.

Los ficheros SQLite están excluidos por `.gitignore`. Las pruebas usan bases
temporales creadas con Alembic; no se usa `create_all()` como sustituto de la
migración. La prueba `tests/test_database_config.py` demuestra que una base
alternativa recibe la migración y las escrituras del runtime, y que la base
predeterminada no cambia.

Revisiones:

- `0001_create_customers` crea `customers` con UUID compatible con SQLite,
  campos funcionales no nulos, unicidad `(country, tax_id)` y `created_at` UTC.
- `0002_create_simulations` incorpora simulaciones.
- `0003_international_simulations` amplía tax_id, usuarios desde cero y consumos
  NULL históricos; asigna monthly sin alterar importes ni fechas. Conserva
  unicidad compuesta y verifica FK después del batch. El downgrade falla antes
  del DDL si hay datos incompatibles.
- `0004_add_simulation_taxes_and_fx` añade `calculation_snapshot` TEXT nullable
  con JSON versionado. Los históricos quedan NULL sin backfill; las nuevas
  simulaciones guardan el snapshot completo. El downgrade bloquea antes del DDL
  si existen snapshots.

Comandos de comprobación:

```powershell
python -m alembic heads
python -m alembic upgrade head
python -m alembic current
```

Para no tocar una base de desarrollo, se puede usar una ruta temporal:

```powershell
$db = Join-Path $env:TEMP 'saas-o-matic-task039b.sqlite3'
$env:DATABASE_URL = "sqlite:///$($db.Replace('\', '/'))"
python -m alembic upgrade head
python -m uvicorn saas_o_matic.bootstrap.main:app --reload
```

Ambos procesos leen la misma `DATABASE_URL`; si se omite, ambos usan la base
predeterminada del backend.

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
- Aplicación FastAPI con `/health`, `/openapi.json`, alta/listado/detalle de
  clientes, alta de simulaciones, historial y previsualización.
- Dominio fiscal de clientes: DNI/NIF, NIE y CIF/NIF; validación genérica no
  oficial para el resto.
- Catálogo MVP con el único plan `standard`.
- Precios progresivos, impuestos generales de seis países y conversión
  EUR/USD/GBP con snapshot histórico.
- Modelos SQLAlchemy, repositorios y migraciones Alembic 0001–0004.
- Esquemas Pydantic y errores `application/problem+json`.
- Pruebas y configuración de calidad.

Excluido:

- Edición o eliminación de clientes y simulaciones.
- Planes adicionales, precios de planes y prestaciones asociadas.
- Autenticación, autorización, multi-tenancy, CORS y límites globales.
- Facturación real, proveedores FX alternativos y fuentes fiscales configurables.
- Frontend Angular, CI y despliegue.

## Limitaciones

- SQLite limita la concurrencia y no reproduce producción; el DDL de las
  migraciones 0003/0004 no es transaccional y una interrupción podría dejar un
  estado parcial. Se recomienda copia de seguridad y prueba en copia antes de
  migrar datos reales (A39-13).
- La estructura global por capas puede no ser la frontera modular definitiva.
  `CalculateSimulation` usa el puerto completo de clientes aunque solo necesita
  leer el país; no se explota actualmente (A39-08).
- El lock de dependencias no es estricto ni usa hashes.
- No hay CI configurada.
- No hay autenticación, autorización, multi-tenancy, CORS ni límites globales de
  cuerpo o tasa. El backend no debe exponerse con datos reales antes de resolver
  esos controles (A39-12).
- La caché FX es por proceso, se pierde al reiniciar y serializa las consultas
  externas con un lock global; no se comparte entre workers (A39-14/A39-15).
- La búsqueda usa `LIKE`/UDF y puede escanear tablas; el `offset` no es un
  snapshot estable ante escrituras concurrentes (A39-11).
- La prueba de arquitectura solo analiza imports estáticos; no cubre
  `importlib.import_module`, `__import__` ni cargas dinámicas (A39-10).
- Un snapshot histórico corrupto produce un `500 application/problem+json`
  controlado, sin ocultar filas, inventar importes ni reparar datos. La
  corrupción no es alcanzable por la API; no hay logging estructurado de la fila
  afectada (A39-05/A39-07).
- Los clientes ignoran campos desconocidos por Q-26; las simulaciones los
  rechazan. La asimetría está aprobada y documentada (A39-09).
- No consta una revisión independiente humana de TASK020 ni de las tareas
  posteriores; TASK039/TASK039B son revisiones metodológicas del mismo agente.
