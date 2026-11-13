# ADR 0001 — Stack tecnológico

| Campo | Valor |
| --- | --- |
| Estado de la decisión | Aceptado en el alcance aprobado por el propietario, con elementos provisionales |
| Estado del documento | Pendiente de revisión del propietario técnico |
| Fecha | 2026-11-12 |
| Decisores | Propietario del repositorio |
| Autoría | Elaborado por OpenCode + DeepSeek (asistencia de IA) bajo la dirección del propietario |
| Revisión | Pendiente del propietario técnico |

## Contexto

SaaS-O-Matic es una herramienta interna para que un equipo comercial simule y estime suscripciones SaaS corporativas. El proyecto nace como evaluación técnica y debe demostrar buenas prácticas de ingeniería: separación de responsabilidades, tipado, pruebas automatizadas, documentación de API y un proceso de desarrollo trazable.

La propuesta inicial del propietario era Node.js/TypeScript con React. Antes de implementar nada, el propietario decidió cambiar el backend a Python y el frontend a Angular (ver [`architectural-evolution.md`](../../ai-workspace/00-project-context/architectural-evolution.md)).

## Decisión

### Backend

| Elemento | Elección | Motivo |
| --- | --- | --- |
| Lenguaje | Python 3.13 | Requisito del propietario para demostrar competencia en Python; versión estable con soporte amplio de librerías. |
| Framework HTTP | FastAPI | Tipado, inyección de dependencias ligera y OpenAPI generado a partir del código. |
| Validación y serialización | Pydantic v2 | Integración nativa con FastAPI, validación declarativa y buen rendimiento. |
| Persistencia | SQLAlchemy 2 + SQLite | ORM maduro con tipado moderno; SQLite elimina infraestructura externa en esta fase. |
| Migraciones | Alembic | Estándar del ecosistema SQLAlchemy; versiona el esquema. |
| Pruebas | Pytest + HTTPX | Ecosistema estándar; HTTPX permite probar ASGI sin servidor real. |
| Calidad | Ruff + mypy | Un solo linter/formateador rápido y comprobación estática de tipos. |

### Frontend

| Elemento | Elección | Motivo |
| --- | --- | --- |
| Framework | Angular | Elección explícita del propietario frente a React. |
| Lenguaje | TypeScript | Tipado estático y contrato explícito con la API. |
| Componentes | Standalone components | Modelo actual de Angular; menos `NgModule`. |
| Estado | Signals (+ RxJS donde aporte valor) | Estado reactivo simple y explícito. |
| Formularios | Reactive Forms | Validación tipada y control programático. |
| Navegación | Angular Router | Estándar del framework, con carga diferida por funcionalidad. |
| HTTP | HttpClient | Cliente oficial con interceptores. |
| Pruebas | Vitest | Runner propuesto. Angular ha incorporado soporte para Vitest en versiones recientes, pero la compatibilidad con la versión que se elija **no está verificada** y sigue pendiente (P-01). |

### Transversal

- Contrato de API documentado con **OpenAPI**.
- Divisa base **EUR**.
- Documentación y mensajes de interfaz en **español**; código e identificadores en **inglés**.

## Alternativas consideradas

| Alternativa | Valoración | Motivo del descarte |
| --- | --- | --- |
| Node.js + TypeScript + React (propuesta inicial) | Viable técnicamente | El propietario pidió expresamente demostrar Python en el backend y usar Angular en el frontend. |
| Django + Django REST Framework | Maduro, con admin y ORM incluidos | Menos explícito en tipado y OpenAPI; el propietario prefirió FastAPI. |
| Flask | Minimalista y flexible | Requiere más decisiones manuales (validación, OpenAPI, DI) para el mismo resultado. |
| PostgreSQL | Mejor paridad con producción y concurrencia real | Añade infraestructura; el alcance actual acepta SQLite. Reevaluar si el proyecto crece. |
| Vue / Svelte | Curva de entrada menor | El propietario eligió Angular. |

## Consecuencias

### Positivas

- Backend tipado de extremo a extremo y contrato OpenAPI generado sin esfuerzo extra.
- Dominio en Python puro, fácil de probar sin base de datos ni framework.
- Un único repositorio con dos aplicaciones y documentación compartida.
- Herramientas de calidad consolidadas y ampliamente documentadas.

### Negativas

- Dos ecosistemas y dos toolchains que mantener (Python y Node).
- SQLite limita concurrencia de escritura y no replica el comportamiento de una base de datos de producción.
- mypy estricto con SQLAlchemy 2 y Pydantic v2 requiere configuración específica de plugins.
- Vitest en Angular depende de la versión; si no hay compatibilidad, habría que revisar la decisión de testing.

## Decisiones pendientes de validación

| ID | Decisión pendiente | Responsable |
| --- | --- | --- |
| P-01 | Versión concreta de Angular y confirmación de Vitest como runner. | Propietario |
| P-02 | Fijar Python 3.13 en el proyecto; el entorno local tiene 3.15 instalado. | Propietario |
| P-03 | Proveedor público de tipos de cambio. | Propietario |
| P-04 | Fuente autoritativa de tipos impositivos. | Propietario |
| P-05 | Estrategia de despliegue y si SQLite es aceptable fuera de desarrollo. | Propietario |

Ninguna de estas decisiones se ha resuelto por inferencia en esta fase.
