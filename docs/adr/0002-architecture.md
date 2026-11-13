# ADR 0002 — Arquitectura

| Campo | Valor |
| --- | --- |
| Estado de la decisión | Aceptado en cuanto al monolito modular; detalles provisionales (P-06, P-07, P-09 y ubicación definitiva del composition root) |
| Estado del documento | Pendiente de revisión del propietario técnico |
| Fecha | 2026-11-12 |
| Decisores | Propietario del repositorio |
| Autoría | Elaborado por OpenCode + DeepSeek (asistencia de IA) bajo la dirección del propietario |
| Revisión | Pendiente del propietario técnico |

## Contexto

El proyecto debe ser mantenible, testeable y comprensible por una sola persona con apoyo de IA. El alcance funcional gira en torno a clientes, simulaciones, cálculo de tramos, impuestos y conversión de divisas. No hay requisitos de alta disponibilidad, multi-tenancy ni integraciones de pago en esta fase.

Se necesita una estructura que:

- Aísle las reglas de negocio de FastAPI y de SQLAlchemy.
- Permita probar el cálculo de precios sin base de datos ni servidor.
- Escale por funcionalidad sin convertir el proyecto en microservicios.
- Deje explícito dónde vive cada responsabilidad.

## Decisión

**Monolito modular** con cuatro capas por módulo funcional y dependencias dirigidas hacia el dominio.

### Dependencias entre capas

```text
presentation  →  application  →  domain
                                     ↑
                          infrastructure
```

- `presentation` depende de `application`.
- `application` depende de `domain`.
- `infrastructure` depende de `domain` para implementar los puertos definidos allí.
- `domain` no depende de ninguna otra capa.
- Ninguna capa depende de `infrastructure`.
- No existen dependencias circulares.

### Capas

| Capa | Responsabilidad | Puede depender de |
| --- | --- | --- |
| `domain` | Entidades, objetos de valor, reglas de cálculo, errores de negocio y puertos (interfaces). Python puro. | Nada del proyecto salvo utilidades puras. |
| `application` | Casos de uso, orquestación, DTOs de entrada/salida y transacciones. | `domain` |
| `infrastructure` | Modelos SQLAlchemy, repositorios concretos, mapeadores y clientes externos. Implementa los puertos definidos en `domain`. | `domain` |
| `presentation` | Routers FastAPI, esquemas Pydantic, dependencias HTTP y traducción de resultados y errores de aplicación a respuestas HTTP. | `application` |

### Estructura por módulo

```text
modules/<module>/
├─ domain/          entities.py  value_objects.py  services.py  ports.py  errors.py
├─ application/     use_cases.py  dto.py
├─ infrastructure/  models.py  repositories.py  mappers.py
└─ presentation/    router.py  schemas.py
```

### Reglas de dependencia

1. `domain` no importa FastAPI, Pydantic ni SQLAlchemy.
2. Los casos de uso reciben puertos, nunca sesiones de base de datos.
3. Los modelos SQLAlchemy y los esquemas Pydantic son independientes; se mapean explícitamente.
4. Los errores de negocio se definen en `domain`. La capa `application` los traduce a errores de aplicación (por ejemplo, recurso no encontrado o validación fallida) y `presentation` convierte esos errores de aplicación en códigos HTTP. `presentation` **no importa `domain`**.
5. `presentation` no contiene reglas de negocio: solo valida la forma de la petición, invoca casos de uso y serializa la respuesta.
6. Ninguna capa importa `infrastructure`: las implementaciones concretas se inyectan desde el composition root.
7. `infrastructure` no depende de `application`; implementa los puertos definidos en `domain` y se conecta a los casos de uso a través de ellos.

### Composition root

La construcción y conexión de las implementaciones concretas se realiza en un **composition root** externo a las cuatro capas. Su responsabilidad es instanciar los adaptadores de `infrastructure` y los casos de uso de `application`, e inyectar los primeros en los segundos a través de los puertos de `domain`.

Como ubicación propuesta se usará el punto de entrada o módulo de bootstrap de `backend/`, fuera de `domain`, `application`, `infrastructure` y `presentation`. La ruta definitiva se concretará durante el scaffold y forma parte de los detalles provisionales de esta decisión. El composition root puede depender de las cuatro capas, pero ninguna capa depende de él.

### Módulos previstos

| Módulo | Contenido |
| --- | --- |
| `customers` | Cliente, identificador fiscal, país, plan y búsqueda. |
| `simulations` | Simulación, consumo declarado y persistencia del resultado. |
| `pricing` | Tramos de usuarios, cálculo del subtotal y redondeo. |
| `taxation` | Reglas de impuestos configurables por país. |
| `currencies` | Obtención de tipos de cambio, conversión reproducible y persistencia del importe base, la divisa, la tasa aplicada y la fecha y fuente del tipo. |

La lista es provisional: los límites definitivos se fijarán en la especificación de cada funcionalidad.

### Persistencia de conversiones

FR-11 exige guardar el importe base en EUR, la divisa de visualización, el tipo de cambio aplicado y la fecha y fuente del tipo cuando estén disponibles. Con esos datos la conversión es reconstruible, por lo que **no es necesario persistir adicionalmente el importe convertido**. Esta conclusión no introduce ninguna regla de negocio nueva: se limita a aplicar FR-11. La magnitud económica exacta que se convierte y persiste como importe base queda pendiente de Q-16.

## Alternativas consideradas

| Alternativa | Valoración | Motivo del descarte |
| --- | --- | --- |
| Monolito en capas único (`api/services/models`) | Más rápido de arrancar | Mezcla reglas de negocio con framework y dificulta las pruebas del cálculo. |
| Clean Architecture completa con casos de uso por operación y DTOs en todas las fronteras | Máximo aislamiento | Ceremonia excesiva para el tamaño actual; se adopta una versión pragmática. |
| Microservicios | Escalado independiente | Complejidad operativa innecesaria para una herramienta interna. |
| Serverless | Menos infraestructura | No aporta ventajas claras con SQLite y un frontend Angular. |
| DDD táctico completo (agregados, eventos, repositorios genéricos) | Rico para dominios complejos | El dominio es pequeño; se toman solo los conceptos que aportan valor. |

## Consecuencias

### Positivas

- El cálculo de tramos, impuestos y validaciones se prueba con pruebas unitarias rápidas y sin I/O.
- Sustituir SQLite por PostgreSQL afecta solo a `infrastructure`.
- Los routers quedan finos y el contrato OpenAPI se mantiene estable.
- Los módulos permiten incorporar funcionalidad sin tocar código ajeno.

### Negativas

- Más ficheros y mapeos explícitos que un monolito en capas.
- Riesgo de sobreingeniería si un módulo trivial se separa en cuatro capas sin necesidad.
- Requiere disciplina para que `domain` no acabe importando utilidades de framework.

## Decisiones pendientes

| ID | Decisión pendiente |
| --- | --- |
| P-06 | Confirmar la lista definitiva de módulos y sus fronteras. |
| P-07 | Definir los límites transaccionales por caso de uso. |
| P-09 | Confirmar la política de errores de API (`application/problem+json`). |
| — | Ubicación definitiva del composition root (detalle provisional sin identificador P). |

La antigua P-08 (persistencia de conversiones) se retiró: FR-11 ya exige los datos que hacen reconstruible la conversión, de modo que no hay una decisión adicional que tomar sobre la persistencia del importe convertido. La magnitud del importe base se decide en Q-16. Se conserva la numeración de P-09 para no romper referencias. La propuesta P-09 se documenta aquí como pendiente y no se ha implementado. La ubicación definitiva del composition root también queda pendiente de concretar durante el scaffold.
