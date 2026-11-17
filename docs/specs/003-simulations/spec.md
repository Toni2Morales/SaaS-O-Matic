# Especificación 003 - Simulaciones de costes

| Campo | Valor |
| --- | --- |
| ID | SPEC-003 |
| Título | Simulaciones de costes y reutilización del motor de precios |
| Estado | **Ocho identificadores SIM-P aprobados (nueve decisiones conceptuales, porque SIM-P09 cubre API y UI); nueve decisiones diferidas; contrato HTTP implementado localmente en TASK032; pendiente de auditoría independiente y publicación.** |
| Fecha | 2026-11-17 |
| Rama | `feature/simulations` |
| Base | `origin/main` en `9cd553fff035de640e12a5eb5530f0791ed7b9e7` (PR #4 fusionado) |
| Alcance | Primer incremento: crear y persistir una simulación de coste de usuarios asociada a un cliente registrado |
| Implementación | TASK032 implementó localmente el primer incremento. Suite completa: 240 pruebas superadas. Sin commit, push, PR ni merge |

## 1. Decisiones aprobadas y correspondencia de identificadores

### 1.1. Decisiones aprobadas

Hay **ocho identificadores SIM-P únicos aprobados** y **nueve decisiones conceptuales aprobadas**, porque SIM-P09 cubre dos niveles distintos: API y UI.

| Identificador | Decisión aprobada |
| --- | --- |
| SIM-P01 | Las simulaciones se persisten. El historial futuro deberá poder recuperar los importes originales. |
| SIM-P02 | Cada simulación está vinculada a un cliente previamente registrado. |
| SIM-P08 / Q-08 | Los importes HTTP se devuelven como cadenas decimales exactas. El cálculo interno usa `Decimal`. |
| SIM-P09 / Q-12 (API) | La API acepta entre 1 y 1.000.000 de usuarios, ambos inclusive. Sin coerciones. |
| SIM-P09 / Q-12 (UI) | La futura UI usará un slider de 1 a 1.000 usuarios y una entrada manual de hasta 1.000.000. No se implementa ahora. |
| SIM-P12 | Un UUID válido de cliente inexistente devuelve `404` con `application/problem+json`; no se persiste nada. Un UUID malformado es `422`. |
| SIM-P13 | El importe se almacena en SQLite como texto decimal canónico y se reconstruye como `Decimal`. |
| SIM-P15 | La ruta es `POST /simulations`, sin prefijo `/api/v1`. |
| SIM-P17 | El primer incremento calcula exclusivamente el coste progresivo de usuarios en EUR. |

La instrucción TASK030 usó `SIM-P03` para la representación monetaria y `SIM-P04` para el alcance inicial. Para no renumerar silenciosamente, SPEC-003 conserva la numeración original:

- La representación monetaria es **SIM-P08 / Q-08**.
- El alcance inicial es **SIM-P17**.
- **SIM-P03** sigue siendo la decisión pendiente sobre el plan.
- **SIM-P04** sigue siendo la decisión pendiente sobre Q-15.

### 1.2. Decisiones diferidas

Hay **nueve decisiones diferidas**:

| Identificador | Decisión diferida |
| --- | --- |
| SIM-P03 | Plan como contexto de simulación. |
| SIM-P04 / Q-15 | Almacenamiento y llamadas API. |
| SIM-P05 / Q-16 | Semántica del importe base. |
| SIM-P06 / Q-05 | Impuestos. |
| SIM-P07 / Q-06, Q-07, Q-17 | Divisas y tipos de cambio. |
| SIM-P10 / Q-09 | Inmutabilidad y edición. |
| SIM-P11 | Endpoints de lectura. |
| SIM-P14 | Impuesto histórico. |
| SIM-P16 | Idempotencia. |

La implementación del primer incremento se autorizó expresamente en TASK032 y se materializó de forma local. Las decisiones diferidas de esta sección no autorizan código adicional ni se resuelven por inferencia.

## 2. Fuentes

- [Requisitos funcionales](../../requirements/functional-requirements.md), especialmente FR-03, FR-04, FR-05, FR-06, FR-08, FR-09, FR-10, FR-11, CON-03, CON-04, CON-06, CON-07, CON-08, ASM-01 a ASM-07, Q-05, Q-06, Q-07, Q-08, Q-09, Q-12, Q-15, Q-16 y Q-17.
- [ADR 0001 - Stack tecnológico](../../adr/0001-technology-stack.md): Python 3.13, FastAPI, Pydantic v2, SQLAlchemy 2, SQLite, Alembic y EUR.
- [ADR 0002 - Arquitectura](../../adr/0002-architecture.md): monolito modular, capas, puertos y composition root.
- [Especificación 001 - Alta de clientes](../001-customer-registration/spec.md): contrato de cliente, D-02 y convenciones de persistencia y error.
- [Especificación 002 - Precios progresivos](../002-progressive-pricing/spec.md): motor aprobado y decisiones Q-02, PP-Q-01, Q-08 y Q-12.
- [Plan técnico 002](../002-progressive-pricing/plan.md) y [tareas 002](../002-progressive-pricing/tasks.md): implementación y pruebas del dominio `pricing`.
- [Proceso de desarrollo asistido por IA](../../process/ai-assisted-development.md).
- [AGENTS.md](../../../AGENTS.md).
- [TASK029 - Preparación de simulaciones](../../../ai-workspace/01-tasks/TASK029-simulations-preparation.md).
- [TASK030 - Cierre de decisiones y contrato](../../../ai-workspace/01-tasks/TASK030-simulations-decisions-and-contract.md).
- [TASK031 - Cierre definitivo de decisiones bloqueantes](../../../ai-workspace/01-tasks/TASK031-simulations-final-decisions.md).
- [Índice de trazabilidad](../../../ai-workspace/README.md).

## 3. Contexto y objetivo

SaaS-O-Matic ya dispone de:

- Registro de clientes mediante `POST /customers`.
- Persistencia de clientes en SQLite con SQLAlchemy y Alembic.
- Catálogo MVP con el único plan `standard` (D-02).
- Motor de precios progresivos en `saas_o_matic.domain.pricing`.
- Cálculo exacto del subtotal de usuarios en EUR con `Decimal`.
- Respuestas de error `application/problem+json` para clientes.

El primer incremento de simulaciones debe crear una simulación persistida, asociada a un cliente registrado, con el número de usuarios y el subtotal de usuarios en EUR. Debe reutilizar el motor existente y no duplicar sus tramos ni sus validaciones.

## 4. Alcance del primer incremento

### 4.1. Incluido

- `POST /simulations`.
- `customer_id` obligatorio y existente.
- `user_count` entero estricto, entre 1 y 1.000.000, ambos inclusive.
- Cálculo con `calculate_user_subtotal`.
- Persistencia de identificador UUID, cliente, número de usuarios, subtotal de usuarios en EUR y fecha de creación.
- Respuesta `201 Created` con el contrato aprobado.
- Errores `422`, `404` y `500` con `application/problem+json`.
- Pruebas futuras de caso de uso, repositorio, contrato HTTP y arquitectura.

### 4.2. Excluido del primer incremento

No se incluye en el cálculo ni en el contrato inicial:

- coste de almacenamiento;
- coste de llamadas a la API;
- impuestos;
- descuentos;
- conversiones de divisas;
- periodicidad de facturación;
- nuevos planes;
- tarifas comerciales adicionales;
- endpoints de lectura, edición o borrado;
- dashboard, Angular o controles gráficos;
- autenticación, autorización o multitenancy;
- idempotencia.

Estos elementos no se consideran cancelados. Permanecen como requisitos futuros o decisiones pendientes. No se usan importes ficticios de cero para representar conceptos no definidos.

### 4.3. Consecuencia sobre requisitos generales

El primer incremento no satisface por sí solo FR-04, FR-06, FR-10 ni FR-11 completos. La aceptación parcial se registra en la sección 12. Tampoco implementa FR-08 ni FR-09, que dependen de lectura, historial y frontend.

## 5. Requisitos y decisiones de partida

### 5.1. Reglas aprobadas

| Referencia | Decisión |
| --- | --- |
| Q-02 | Mínimo 1 usuario; cero se rechaza. |
| PP-Q-01 | Solo enteros positivos estrictos; se rechazan cero, negativos, no enteros y `bool`, sin coerciones. |
| Q-08 | Cálculo exacto con `Decimal` en EUR, sin `float` ni redondeo de negocio. La representación HTTP aprobada es cadena decimal exacta. |
| Q-12 | Sin máximo comercial en el dominio. La API fija un máximo técnico de 1.000.000; la UI usará slider de 1 a 1.000 y entrada manual de hasta 1.000.000. |
| D-02 | Único plan `standard`; el plan es obligatorio en el cliente, no modifica los tramos y no añade precios o prestaciones. |
| CON-03 | EUR es la divisa base. |
| CON-04 | Almacenamiento y llamadas API se registran y muestran, pero no generan cargos. |
| CON-06 | La aplicación estima costes; no es un sistema de cobro. |
| CON-07 | Autenticación, autorización, multitenancy, Stripe, PDF y correo quedan fuera de alcance. |

### 5.2. Estado de requisitos

| Requisito | Estado en el primer incremento |
| --- | --- |
| FR-03 | Alineado: persistencia y cliente obligatorio aprobados en SIM-P01 y SIM-P02. |
| FR-04 | Parcial y aceptado: solo se registra el número de usuarios; almacenamiento y llamadas quedan para una fase posterior tras Q-15. |
| FR-05 | Satisfecho mediante el motor existente. |
| FR-06 | Diferido y aceptado: no se calculan impuestos hasta Q-05/Q-16. |
| FR-08 | Diferido: la persistencia habilita el futuro historial, pero no se implementa endpoint de lectura. |
| FR-09 | Fuera del backend inicial: el simulador, el slider y la entrada manual pertenecen al frontend. |
| FR-10 | Diferido y aceptado: no se implementan divisas ni proveedor de tipos. |
| FR-11 | Parcial y aceptado: se conserva el subtotal de usuarios en EUR, pero no se define como importe base ni se persisten divisa/tasa. Q-16 y Q-17 siguen pendientes. |

## 6. Contrato HTTP aprobado

### 6.1. Endpoint

```text
POST /simulations
```

Sin prefijo `/api/v1`. Se mantienen las convenciones actuales hasta que exista una estrategia global de versionado. Esta decisión no impide introducir versionado en el futuro.

### 6.2. Entrada

| Campo | Tipo | Obligatoriedad | Validación |
| --- | --- | --- | --- |
| `customer_id` | UUID | Obligatorio (SIM-P02). | UUID válido y cliente existente. |
| `user_count` | Entero estricto | Obligatorio. | Entre 1 y 1.000.000, ambos inclusive; rechazar `bool`, `float`, cadena, cero, negativos y valores superiores. Sin coerciones. |

No se incluyen `plan`, `storage`, `api_calls`, `display_currency`, impuestos, descuentos ni otros campos comerciales no aprobados. No hay modo efímero ni híbrido: SIM-P01 aprobó persistencia.

Ejemplo:

```json
{
  "customer_id": "00000000-0000-0000-0000-000000000000",
  "user_count": 100
}
```

### 6.3. Salida

| Campo | Tipo | Contenido |
| --- | --- | --- |
| `id` | UUID | Identificador generado por el servidor. |
| `customer_id` | UUID | Cliente asociado. |
| `user_count` | Entero | Cantidad validada. |
| `user_subtotal_eur` | Cadena decimal | Subtotal de usuarios en EUR. |
| `created_at` | Fecha/hora ISO 8601 UTC | Momento de creación. |

No se incluye `base_amount_eur`, porque Q-16 no ha definido una magnitud base distinta. No se incluye `plan`, `storage`, `api_calls`, `display_currency`, `exchange_rate`, `rate_date` ni `rate_source`.

Ejemplo:

```json
{
  "id": "00000000-0000-0000-0000-000000000001",
  "customer_id": "00000000-0000-0000-0000-000000000000",
  "user_count": 100,
  "user_subtotal_eur": "670.00",
  "created_at": "2026-11-16T16:00:00Z"
}
```

El identificador de cliente es UUID porque es el tipo real de `customers.id` y de `CustomerResponse`.

### 6.4. Representación monetaria

La representación aprobada es una cadena decimal exacta:

- Punto como separador decimal.
- Sin separador de miles.
- Sin notación científica.
- EUR implícito en el nombre `user_subtotal_eur`.
- Dos decimales para los importes del alcance actual: `10.00`, `108.00`, `425.00`, `670.00`, `5000170.00`.
- Sin `float`.
- Sin redondeo comercial.

La representación con dos decimales es exacta para las tarifas actuales. Si una funcionalidad futura introduce importes con mayor precisión, deberá definirse su política monetaria antes de implementarla. No se redondeará silenciosamente.

Advertencia: ordenar importes almacenados como texto no equivale necesariamente a ordenarlos por su valor numérico. El primer incremento no implementa consultas monetarias, agregaciones ni ordenación histórica.

### 6.5. Fecha de creación

`created_at` se genera en UTC con `datetime.now(UTC)` y se serializa como fecha ISO 8601 con zona UTC. Pydantic v2, usado por la API actual, serializa un `datetime` consciente de UTC con sufijo `Z`. La persistencia SQLite puede devolver un valor sin zona; el mapeador futuro debe restaurar UTC como ya hace el mapeador de clientes.

### 6.6. Códigos HTTP

| Situación | Respuesta |
| --- | --- |
| Simulación persistida creada | `201 Created`. |
| Cuerpo o `user_count` inválido | `422 Unprocessable Content` con `application/problem+json`. |
| UUID malformado | `422 Unprocessable Content`. |
| Cliente válido inexistente | `404 Not Found` con `application/problem+json`. |
| Error interno | `500 Internal Server Error` con `application/problem+json`. |

No se introducen nuevos códigos, rutas o formatos sin justificación. Los errores no exponen detalles internos de infraestructura.

### 6.7. `Location` y endpoint de lectura

La API de clientes devuelve `201` sin cabecera `Location` y no existe un endpoint de consulta de cliente. Para simulaciones, `Location: /simulations/{id}` solo sería correcto si se aprueba y existe `GET /simulations/{id}`. El primer incremento no incluye lectura y **no emite `Location`**.

La ruta de lectura, su forma (`/simulations/{id}` o `/customers/{customer_id}/simulations`) y su autorización siguen pendientes (SIM-P11).

### 6.8. Cliente inexistente

- UUID mal formado: `422` por validación de forma.
- UUID válido no registrado: `404` con `application/problem+json`.
- La comprobación se realiza antes de persistir.
- No se crea ni persiste ninguna simulación.

TASK032 añadió un error de aplicación para cliente no encontrado y manejadores `404`/`422` de simulación. El título de validación se selecciona por ruta: «Datos de simulación no válidos» para `/simulations` y «Datos de cliente no válidos» para el resto, sin romper el contrato existente de clientes.

## 7. Arquitectura del primer incremento

### 7.1. Capas

| Capa | Componente | Responsabilidad |
| --- | --- | --- |
| Dominio | `domain/simulations/entities.py` | Entidad `Simulation` con los datos persistidos. |
| Dominio | `domain/simulations/ports.py` | Puerto `SimulationRepository`. |
| Aplicación | `application/simulations/use_cases.py` | Orquestar validación, cliente, cálculo y persistencia. |
| Aplicación | `application/simulations/dto.py` | Comando y resultado. |
| Aplicación | `application/simulations/errors.py` | Errores estables de simulación. |
| Infraestructura | `infrastructure/simulations/` | Modelo SQLAlchemy, mapeadores y repositorio. |
| Presentación | `presentation/simulations/` | Esquemas, router y dependencias HTTP. |
| Bootstrap | `bootstrap/simulations.py` | Composición con la sesión y los repositorios. |

El dominio de simulación no importa FastAPI, Pydantic, SQLAlchemy ni capas exteriores. La presentación no importa dominio.

### 7.2. Flujo del caso de uso

1. La presentación valida la forma del cuerpo y crea `CreateSimulationCommand`.
2. La aplicación valida el rango de `user_count` admitido por el incremento.
3. La aplicación llama a `calculate_user_subtotal(user_count)`.
4. Si el motor lanza `InvalidUserCount`, se traduce a un error de aplicación y la presentación devuelve `422`.
5. La aplicación comprueba `customer_id` mediante `CustomerRepository.exists_by_id`.
6. Si el cliente no existe, se lanza el error de aplicación y la presentación devuelve `404`.
7. La aplicación construye `Simulation` con `uuid4()` y `datetime.now(UTC)`.
8. El repositorio persiste y confirma la transacción.
9. La presentación devuelve `201` con el subtotal formateado como cadena decimal.

El orden propuesto valida primero la forma y el rango, después el cliente y finalmente persiste. El orden exacto puede ajustarse en la implementación sin cambiar los códigos aprobados.

### 7.3. Reutilización del motor

La aplicación importará:

```python
from saas_o_matic.domain.pricing.services import calculate_user_subtotal
```

No se copian tramos, precios, validaciones ni el algoritmo acumulativo. No se pasa el plan al motor. No se usan `float` ni redondeos nuevos. **No se modifica el dominio pricing.**

### 7.4. Cambio mínimo en clientes

El puerto actual `CustomerRepository` solo expone `exists_by_tax_id` y `add`. Para el primer incremento se recomienda añadir:

```python
def exists_by_id(self, customer_id: UUID) -> bool:
    """Comprueba si existe un cliente por su identificador."""
```

Ventajas:

- Evita cargar la entidad completa.
- Es suficiente porque el plan no se usa en el cálculo.
- Mantiene la dependencia de la aplicación hacia un puerto de dominio.
- Es compatible con los puertos, repositorios y dobles de prueba existentes.

`get_by_id` quedaría justificado si una fase futura necesita el plan u otros datos del cliente. No se modifica ninguna interfaz en TASK031.

### 7.5. Errores y transacciones

- `InvalidUserCount` del dominio se traduce a `InvalidSimulationData` de aplicación.
- La inexistencia de cliente se traduce a `CustomerNotFound` de aplicación.
- La presentación registra manejadores para ambos errores y mantiene `ProblemDetails`.
- El repositorio de simulación confirma la transacción, siguiendo el patrón de clientes.
- La sesión por petición se comparte entre el repositorio de clientes y el de simulaciones en el composition root.
- Ante cualquier error no se deja una simulación parcial.

## 8. Persistencia y modelo conceptual

### 8.1. Tabla `simulations`

| Columna | Tipo | Restricciones | Observaciones |
| --- | --- | --- | --- |
| `id` | UUID | Clave primaria, no nula. | Generado con `uuid4()`. |
| `customer_id` | UUID | No nulo; clave foránea a `customers.id`. | Cliente obligatorio. |
| `user_count` | Entero | No nulo; `>= 1` y `<= 1000000`. | Límite técnico del incremento; no es máximo comercial. |
| `user_subtotal_eur` | Texto decimal | No nulo. | Cadena canónica exacta; no se usa para aritmética SQL. |
| `created_at` | Fecha/hora UTC | No nulo. | Restaurar UTC al leer si SQLite devuelve naive. |

No se añaden `plan`, `storage`, `api_calls`, impuestos, divisa, tasa, `base_amount_eur`, versión de tarifa ni campos de edición. No se define política de recálculo: el importe persistido es el valor histórico calculado en el momento de la creación.

### 8.2. Integridad y transacciones

SQLite no aplica claves foráneas por defecto. La implementación de TASK032:

- Declara la clave foránea en el modelo y en la migración `0002_create_simulations`.
- Activa `PRAGMA foreign_keys=ON` mediante un listener de SQLAlchemy en cada conexión del motor SQLite.
- Prueba que no se puede persistir una simulación con un cliente inexistente.
- Confirma la transacción solo después de persistir la simulación.
- No deja registros parciales ante errores.
- No define borrado en cascada, edición ni versionado de tarifas.

La migración incluye `upgrade` y `downgrade`, y se prueba en ambos sentidos sobre bases SQLite temporales.

### 8.3. Almacenamiento exacto de importes en SQLite

| Alternativa | Valoración |
| --- | --- |
| Texto decimal canónico | **Aprobado.** Exacto, independiente de la afinidad de SQLite, coincide con la representación HTTP y no requiere aritmética SQL. |
| Entero de unidades menores | Exacto y compacto, pero presupone escala 2 y una regla de conversión. |
| `Numeric` de SQLAlchemy | Semántica monetaria, pero SQLite no tiene decimal nativo; exige probar el viaje de ida y vuelta. |
| `float` | Prohibido. |

La columna será de tipo texto. El valor se reconstruye con `Decimal` al leer. Las pruebas obligatorias deben cubrir `Decimal → SQLite → Decimal → HTTP` para los importes de aceptación.

### 8.4. Importe histórico y metadatos de tarifa

El subtotal persistido permite conservar la estimación original aunque cambie el código. No se añade una versión de la tabla de precios porque:

- El primer incremento usa una única tabla aprobada.
- No se requiere recalcular simulaciones históricas.
- No hay un requisito de auditoría que exija reconstruir el cálculo.

Si en el futuro se modifican los tramos o se exige reconstruir el cálculo, se necesitará una decisión adicional sobre versionado o snapshot. No se implementa ahora.

## 9. Capas de validación

| Capa | Responsabilidad |
| --- | --- |
| Dominio `pricing` | Mínimo 1; entero positivo estricto; rechazo de `bool`, no enteros y negativos; sin máximo comercial. No se modifica. |
| Aplicación | Validación defensiva del rango 1..1.000.000; comprobación de cliente; cálculo; persistencia; sin efectos ante error. |
| Presentación | UUID válido; entero estricto; rango 1..1.000.000; `422` para entradas inválidas; `application/problem+json`. |
| Persistencia | `CHECK` de `user_count` entre 1 y 1.000.000; FK; transacción; sin registros parciales. |
| UI futura | Slider de 1 a 1.000; entrada manual de hasta 1.000.000. No se implementa en este incremento. |

La validación de Pydantic no sustituye al dominio: el caso de uso sigue llamando a `calculate_user_subtotal`, que rechaza `bool`, no enteros y valores menores que 1.

## 10. Validaciones del contrato

| Caso | Tratamiento |
| --- | --- |
| `customer_id` ausente | `422`; es obligatorio. |
| `customer_id` mal formado | `422`. |
| `customer_id` válido inexistente | `404` con `problem+json`; no se persiste. |
| `user_count` ausente | `422`. |
| `user_count` = 0 | `422`; Q-02. |
| `user_count` negativo | `422`; PP-Q-01. |
| `user_count` = 1.000.001 | `422`; límite técnico de API. |
| `user_count` extremadamente grande | `422`; no se calcula ni persiste. |
| `user_count` decimal, cadena o `bool` | `422` sin coerción; PP-Q-01. |
| `user_count` nulo | `422`. |
| `plan` en la entrada | Se ignora conforme a la política existente de campos adicionales; no se usa en el cálculo ni se persiste. |
| `storage` / `api_calls` | Se ignoran; no se persisten; Q-15 sigue diferido. |
| Importe monetario | `Decimal` interno; salida como cadena exacta; sin `float` ni redondeo nuevo. |
| Error de validación | `application/problem+json` con `ProblemDetails`. |

## 11. Plan de pruebas de aceptación

TASK032 implementó y ejecutó estas pruebas. La suite completa quedó en 240 pruebas superadas, sin fallos ni omisiones:

### 11.1. Precios obligatorios

| Usuarios | Subtotal EUR |
| ---: | ---: |
| 1 | `10.00` |
| 10 | `100.00` |
| 11 | `108.00` |
| 50 | `420.00` |
| 51 | `425.00` |
| 100 | `670.00` |
| 1000000 | `5000170.00` |

Verificación independiente del algoritmo:

- 1–10: `10 × 10,00 = 100,00`.
- 11–50: `40 × 8,00 = 320,00`.
- 51–1.000.000: `999.950 × 5,00 = 4.999.750,00`.
- Total: `100,00 + 320,00 + 4.999.750,00 = 5.000.170,00`.

### 11.2. Límites y entradas inválidas

- 0 usuarios.
- Usuarios negativos.
- 1.000.001 usuarios.
- Cantidades extremadamente grandes.
- Decimales, incluidos valores como `10.0`.
- Cadenas numéricas.
- Booleanos.
- Valores nulos.
- Campos obligatorios ausentes.
- UUID malformado.
- UUID válido de cliente inexistente.

### 11.3. HTTP

- Creación correcta con `201`.
- Contrato de respuesta aprobado.
- Importes serializados como cadenas.
- Timestamp UTC.
- `422` para entradas inválidas.
- `404` para cliente inexistente.
- Formato `application/problem+json`.

### 11.4. Persistencia

- Simulación correctamente almacenada.
- Identificador único.
- Relación con cliente existente.
- Claves foráneas efectivamente aplicadas.
- Exactitud monetaria de ida y vuelta.
- Persistencia del máximo técnico autorizado.
- Ausencia de simulaciones ante errores.
- Migración y reversión.

### 11.5. Regresión y arquitectura

- Pruebas existentes de clientes.
- Pruebas existentes de pricing.
- Separación de capas.
- Ausencia de duplicación comercial.
- Ausencia de máximo comercial introducido en pricing.

## 12. Trazabilidad y aceptación parcial

### 12.1. Aceptación expresa del primer incremento

El propietario acepta que el primer incremento no satisfaga completamente estos requisitos:

| Requisito | Alcance del primer incremento |
| --- | --- |
| FR-04 | Solo número de usuarios; almacenamiento y llamadas API pendientes. |
| FR-06 | Sin cálculo de impuestos. |
| FR-10 | Sin conversión de divisas. |
| FR-11 | Persistencia del subtotal EUR; otros importes y metadatos pendientes. |

Esta aceptación no cancela requisitos, no modifica sus objetivos finales, no declara completado todo el MVP y no autoriza a inventar datos o importes cero para conceptos pendientes. Es aceptación del primer incremento, no cumplimiento completo del requisito.

### 12.2. Matriz de requisitos y preguntas

| Referencia | Intención original | Estado actual | Relación con el primer incremento | Conflicto o brecha | Acción | ¿Requiere aprobación? |
| --- | --- | --- | --- | --- | --- | --- |
| FR-03 | Crear y persistir simulaciones asociadas a un cliente. | Alineado por SIM-P01/SIM-P02. | Sí: se persiste y se exige cliente. | Ninguno. | Implementar persistencia y asociación. | Decisión ya aprobada. |
| FR-04 | Registrar usuarios, almacenamiento y llamadas API; unidades en Q-15. | Parcial aceptado. | Solo usuarios. | No se registran almacenamiento ni llamadas. | Diferir a una fase posterior; no inventar unidades. | Aceptación parcial registrada; Q-15 sigue abierta. |
| FR-06 | Incluir impuesto según país. | Diferido y aceptado. | No. | No se calcula impuesto. | Diferir tras Q-05/Q-16. | Aceptación parcial registrada. |
| FR-08 | Detalle del cliente con historial. | Pendiente. | La persistencia lo habilita, pero no hay lectura. | No hay endpoint de historial. | Diferir SIM-P11. | Sí, en una fase posterior. |
| FR-10 | Conversiones de divisa con API pública. | Diferido y aceptado. | No. | No se implementa conversión. | Diferir Q-06/Q-07. | Aceptación parcial registrada. |
| FR-11 | Persistir importe base, divisa, tasa, fecha y fuente. | Parcial aceptado. | Se guarda el subtotal de usuarios, no el importe base ni metadatos de conversión. | Q-16/Q-17 abiertas; no se define importe base. | Mantener `user_subtotal_eur` separado; diferir FR-11 completo. | Aceptación parcial registrada. |
| Q-05 | Fuente y vigencia de impuestos. | Pendiente. | No. | Bloquea FR-06. | Diferir. | Sí. |
| Q-06 | Proveedor de tipos de cambio. | Pendiente. | No. | Bloquea FR-10. | Diferir. | Sí. |
| Q-07 | Divisas soportadas. | Pendiente. | No. | Bloquea FR-10. | Diferir. | Sí. |
| Q-08 | Cálculo exacto y formato de salida. | Resuelta para HTTP: cadena decimal exacta. | Sí: salida `user_subtotal_eur` como cadena. | Ninguna en el alcance actual. | Probar exactitud y no usar `float`. | Decisión aprobada. |
| Q-09 | Historial inmutable o editable. | Pendiente. | No hay edición. | No se define política futura. | Diferir; no implementar `PATCH`/`PUT`/`DELETE`. | Sí. |
| Q-12 | Máximo de usuarios en UI/API. | Resuelta para API y UI de este incremento. | API 1..1.000.000; UI slider 1..1.000 y manual hasta 1.000.000. | El dominio sigue sin máximo comercial. | Implementar el límite solo en API/aplicación/persistencia. | Decisión aprobada. |
| Q-15 | Unidades de almacenamiento y llamadas. | Pendiente. | No se incluyen. | FR-04 parcial. | Diferir. | Sí. |
| Q-16 | Magnitud del importe base. | Pendiente. | No se usa `base_amount_eur`. | FR-11 parcial. | Mantener subtotal separado; decidir antes de impuestos/divisas. | Sí. |
| Q-17 | Obligatoriedad de fecha/fuente de tasa. | Pendiente. | No aplica sin divisas. | FR-11 parcial. | Diferir. | Sí. |

### 12.3. Matriz de decisiones SIM-P

| ID | Contenido | Estado | Relación con el primer incremento | Acción | ¿Bloquea? |
| --- | --- | --- | --- | --- | --- |
| SIM-P01 | Persistencia. | Aprobada. | Núcleo. | Implementar repositorio y migración. | No. |
| SIM-P02 | Relación con cliente. | Aprobada. | Núcleo. | Implementar comprobación y FK. | No. |
| SIM-P03 | Plan en el contrato. | Diferida. | Se omite. | Revisar si se necesita como contexto. | No. |
| SIM-P04 | Q-15: almacenamiento y API. | Diferida. | No se incluyen. | Diferir. | No. |
| SIM-P05 | Q-16: importe base. | Diferida. | Se guarda solo subtotal. | Diferir. | No. |
| SIM-P06 | Q-05: impuesto. | Diferida. | No se calcula. | Diferir. | No. |
| SIM-P07 | Q-06/Q-07/Q-17: divisas. | Diferida. | No se incluyen. | Diferir. | No. |
| SIM-P08 | Q-08: formato monetario. | Aprobada. | Salida `user_subtotal_eur`. | Implementar serialización exacta. | No. |
| SIM-P09 | Q-12: límites API/UI. | Aprobada. | API 1..1.000.000; UI 1..1.000 y manual hasta 1.000.000. | Implementar solo API/aplicación/persistencia; no pricing. | No. |
| SIM-P10 | Q-09: inmutabilidad/edición. | Diferida. | No hay edición. | Diferir. | No. |
| SIM-P11 | Endpoints de lectura. | Diferida. | No se implementan. | Diferir. | No. |
| SIM-P12 | Cliente inexistente. | Aprobada. | `404` con `problem+json`; UUID malformado `422`. | Implementar error y manejador. | No. |
| SIM-P13 | Decimal en SQLite. | Aprobada. | Texto decimal canónico. | Implementar y probar ida y vuelta. | No. |
| SIM-P14 | Impuesto histórico. | Diferida. | No aplica sin impuestos. | Diferir. | No. |
| SIM-P15 | Prefijo `/api/v1`. | Aprobada. | Ruta `/simulations` sin prefijo. | Mantener convención actual. | No. |
| SIM-P16 | Idempotencia. | Diferida. | Cada `POST` crea un registro. | Documentar riesgo de duplicados. | No. |
| SIM-P17 | Alcance inicial. | Aprobada. | Solo usuarios. | Implementar solo usuarios y documentar brechas. | No. |

## 13. Decisiones diferidas

| ID | Pregunta | Tratamiento | ¿Bloquea el primer incremento? |
| --- | --- | --- | --- |
| SIM-P03 | ¿Se incluye el plan como contexto? | Omitirlo mientras no afecte al cálculo. | No. |
| SIM-P04 / Q-15 | Unidades de almacenamiento y API. | Diferir; no inventar unidades ni cargos. | No. |
| SIM-P05 / Q-16 | Magnitud del importe base. | Mantener `user_subtotal_eur` separado. | No. |
| SIM-P06 / Q-05 | Fuente y vigencia del impuesto. | Diferir. | No. |
| SIM-P07 / Q-06, Q-07, Q-17 | Divisas y metadatos de tasa. | Diferir. | No. |
| SIM-P10 / Q-09 | Inmutabilidad o edición. | No exponer edición; decidir antes del historial. | No. |
| SIM-P11 | Rutas de lectura y `Location`. | No emitir `Location` hasta que exista lectura. | No. |
| SIM-P14 | Reconstrucción del impuesto histórico. | Diferir; no añadir campos sin requisito. | No. |
| SIM-P16 | Idempotencia. | Documentar que los reintentos pueden duplicar. | No. |

Estas decisiones quedan diferidas, no canceladas. No se introducen edición, borrado, endpoints de lectura, dashboard, autenticación, autorización, multitenancy ni reglas de idempotencia inventadas.

## 14. Actualizaciones documentales globales pendientes

No se modifican los requisitos generales en TASK031. Quedan registradas para una tarea posterior:

- Q-08: actualizar la pregunta global para reflejar que la serialización HTTP ya está resuelta por SPEC-003/TASK031.
- Q-12: actualizar la pregunta global para reflejar el máximo de API de 1.000.000 y los rangos de UI, manteniendo el dominio sin máximo comercial.
- FR-04, FR-06, FR-10 y FR-11: registrar la aceptación parcial del primer incremento sin declarar los requisitos completados.
- FR-08 y FR-09: mantener su estado futuro; no se implementan en este incremento.
- Q-15, Q-16 y Q-17: mantener abiertas.
- Q-09 y SIM-P16: mantener abiertas.

## 15. Riesgos

| Riesgo | Impacto | Mitigación |
| --- | --- | --- |
| FR-04, FR-06, FR-10 y FR-11 no se satisfacen completos. | El primer incremento es una entrega parcial. | Aceptación expresa registrada; planificar fases posteriores. |
| Ordenar texto monetario como si fuera número. | Resultados incorrectos. | No implementar ordenación/agregación; documentar la advertencia. |
| SQLite no aplica FK por defecto. | Simulaciones huérfanas. | Activar `PRAGMA foreign_keys` y probar. |
| Manejadores de error acoplados a clientes. | `422` con título incorrecto o `404` no problem+json. | Añadir manejadores de simulación y pruebas de regresión. |
| Sin idempotencia. | Reintentos crean duplicados. | Documentar el riesgo; decidir SIM-P16 en una fase posterior. |
| Sin endpoint de lectura. | No se puede consultar lo persistido desde la API. | Aprobar SIM-P11 en una fase posterior. |
| Máximo técnico de 1.000.000. | Entradas grandes pueden consumir recursos. | Validar antes de calcular; probar el límite y valores superiores. |
| Sin CI. | La validación depende de ejecución local. | Mantener checklist y registrar resultados reales. |
| Requisitos generales no actualizados. | Divergencia documental. | Registro en sección 14; actualización posterior autorizada. |

## 16. Criterios de aceptación

1. `POST /simulations` persiste una simulación con `id`, `customer_id`, `user_count`, `user_subtotal_eur` y `created_at`.
2. El caso de uso reutiliza `calculate_user_subtotal` y no duplica tramos.
3. Los siete ejemplos devuelven `10.00`, `100.00`, `108.00`, `420.00`, `425.00`, `670.00` y `5000170.00`.
4. `user_count` solo acepta enteros estrictos entre 1 y 1.000.000.
5. El cliente debe existir; un UUID válido inexistente devuelve `404`.
6. La respuesta monetaria es una cadena decimal exacta; no se usa `float`.
7. `created_at` es UTC y se serializa en ISO 8601.
8. Los errores usan `application/problem+json`.
9. La arquitectura respeta ADR 0002 y no introduce `presentation → domain`.
10. La migración, el repositorio y la recuperación exacta están probados.
11. Las suites existentes siguen pasando.
12. No se implementan impuestos, divisas, almacenamiento, API, plan ni cargos sin decisión expresa.

TASK032 considera satisfechos los doce criterios en el alcance local. La auditoría independiente y la publicación siguen pendientes.

## 17. Estado de implementación TASK032

### 17.1. Artefactos implementados

- Dominio: `domain/simulations/entities.py` contiene `Simulation`, las invariantes básicas y `format_eur_amount`; `domain/simulations/ports.py` define `SimulationRepository`.
- Aplicación: `application/simulations/` contiene DTOs, errores, el límite técnico y `CreateSimulation`.
- Infraestructura: `infrastructure/simulations/` contiene `SimulationModel`, los mapeadores y `SqlAlchemySimulationRepository`.
- Presentación: `presentation/simulations/` contiene esquemas, router y dependencia HTTP.
- Composición: `bootstrap/simulations.py` y el registro en `bootstrap/main.py`.
- Migración: `backend/migrations/versions/0002_create_simulations.py`.
- Pruebas: `test_simulation_use_case.py`, `test_simulation_repository.py`, `test_simulation_api.py` y `test_simulation_schemas.py`.

### 17.2. Contrato y persistencia

- `POST /simulations` devuelve `201` con `id`, `customer_id`, `user_count`, `user_subtotal_eur` y `created_at`.
- `user_count` es un entero estricto entre 1 y 1.000.000.
- `user_subtotal_eur` se serializa como cadena decimal exacta; se almacena como `TEXT` canónico y se reconstruye con `Decimal`.
- Un UUID malformado devuelve `422`; un UUID válido de cliente inexistente devuelve `404`; un fallo inesperado devuelve `500`. Todos usan `application/problem+json`.
- No se emite `Location`.
- La tabla `simulations` incluye FK a `customers.id`, `CHECK` del rango y `NOT NULL`. `PRAGMA foreign_keys=ON` se aplica en cada conexión del motor.
- El repositorio confirma la transacción; ante cualquier error durante el alta o la confirmación hace rollback y propaga la excepción.
- La migración se probó con upgrade, downgrade a `0001_create_customers`, conservación de clientes, downgrade a `base` y nuevo upgrade.

### 17.3. Resultados reales

- Suite completa: **240 pruebas superadas, 0 fallidas, 0 omitidas**.
- Pruebas nuevas de simulación: **72** (21 de caso de uso, 5 de repositorio, 24 de API y 22 de esquemas). Se añadió además una prueba de `exists_by_id` en clientes.
- Los siete subtotales se verificaron: `10.00`, `100.00`, `108.00`, `420.00`, `425.00`, `670.00` y `5000170.00`.
- Ruff check, Ruff format --check, mypy y `pip check` finalizaron sin errores.
- Ejemplo real obtenido con 100 usuarios: petición `{"customer_id": "<uuid>", "user_count": 100}` y respuesta `201` con `user_subtotal_eur: "670.00"`, sin `Location` y con `created_at` terminado en `Z`.

### 17.4. Límites del incremento

Siguen diferidos SIM-P03, SIM-P04/Q-15, SIM-P05/Q-16, SIM-P06/Q-05, SIM-P07/Q-06/Q-07/Q-17, SIM-P10/Q-09, SIM-P11, SIM-P14 y SIM-P16. No hay historial accesible por API, edición, borrado, idempotencia, impuestos, divisas, almacenamiento, llamadas API, autenticación, multitenancy ni CI. FR-04, FR-06, FR-10 y FR-11 siguen parcialmente satisfechos.

## 18. Referencias

- [Requisitos funcionales](../../requirements/functional-requirements.md)
- [ADR 0001 - Stack tecnológico](../../adr/0001-technology-stack.md)
- [ADR 0002 - Arquitectura](../../adr/0002-architecture.md)
- [Especificación 001 - Alta de clientes](../001-customer-registration/spec.md)
- [Especificación 002 - Precios progresivos](../002-progressive-pricing/spec.md)
- [Plan técnico 002](../002-progressive-pricing/plan.md)
- [Tareas 002](../002-progressive-pricing/tasks.md)
- [TASK024 - Preparación del motor de precios](../../../ai-workspace/01-tasks/TASK024-progressive-pricing-preparation.md)
- [TASK025 - Implementación del motor de precios](../../../ai-workspace/01-tasks/TASK025-progressive-pricing-implementation.md)
- [TASK027 - Correcciones del motor de precios](../../../ai-workspace/01-tasks/TASK027-progressive-pricing-audit-fixes.md)
- [TASK029 - Preparación de simulaciones](../../../ai-workspace/01-tasks/TASK029-simulations-preparation.md)
- [TASK030 - Cierre de decisiones y contrato](../../../ai-workspace/01-tasks/TASK030-simulations-decisions-and-contract.md)
- [TASK031 - Cierre definitivo de decisiones bloqueantes](../../../ai-workspace/01-tasks/TASK031-simulations-final-decisions.md)
- [TASK032 - Implementación del primer incremento](../../../ai-workspace/01-tasks/TASK032-simulations-implementation.md)
- [Plan técnico 003](plan.md)
- [Tareas 003](tasks.md)
- [Índice de trazabilidad](../../../ai-workspace/README.md)
