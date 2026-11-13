# Evolución arquitectónica

| Campo | Valor |
| --- | --- |
| Fecha | 2026-11-12 |
| Estado | Registro histórico de decisiones |
| Autoridad | Propietario del repositorio |

Este documento resume la evolución de las decisiones técnicas de SaaS-O-Matic. **No reconstruye conversaciones literales ni inventa iteraciones**: recoge únicamente decisiones que el propietario comunicó y que quedaron reflejadas en el repositorio.

---

## 1. Punto de partida: Node.js/TypeScript + React

La propuesta inicial del proyecto planteaba:

- Backend en **Node.js con TypeScript**.
- Frontend en **React con TypeScript**.
- Un único lenguaje para ambas capas.

Era una opción coherente para una aplicación pequeña: un solo ecosistema, un solo gestor de paquetes y reutilización de tipos entre cliente y servidor.

**No llegó a implementarse.** No existen commits, código, dependencias ni pruebas de esa propuesta en el repositorio.

## 2. Cambio de decisión

Antes de escribir código, el propietario cambió el rumbo por dos motivos explícitos:

| Cambio | Motivo declarado por el propietario |
| --- | --- |
| Backend: Node.js/TypeScript → **Python 3.13 + FastAPI** | Demostrar competencia en Python como parte de la evaluación técnica. |
| Frontend: React → **Angular + TypeScript** | Preferencia explícita del propietario por Angular. |

El cambio no se produjo por un problema técnico detectado en la propuesta anterior, sino por los objetivos personales y profesionales del propietario. Se documenta como decisión consciente, no como corrección de un error.

## 3. Cronología de fases

| Fase | Estado | Resultado |
| --- | --- | --- |
| 1. Repositorio inicial | Completada | `README.md`, `.gitignore` y `LICENSE` (MIT). Un único commit creado desde la interfaz web de GitHub. |
| 2. Evaluación del repositorio | Completada | Inspección de estructura, Git, `.gitignore` y entorno; identificación de riesgos y huecos. |
| 3. Fundamento documental (esta rama) | En revisión | Requisitos, ADRs, proceso de trabajo, contexto de IA y configuración compartida. Sin código. |
| 4. Scaffold de backend | No iniciada | Pendiente de aprobación. |
| 5. Scaffold de frontend | No iniciada | Pendiente de aprobación. |
| 6. Funcionalidades | No iniciadas | Pendiente de especificación y aprobación. |

## 4. Consecuencias del cambio

### Ventajas

- El backend en Python permite demostrar tipado, pruebas y diseño de dominio con un lenguaje distinto al del frontend.
- FastAPI genera OpenAPI a partir del código, lo que encaja con el requisito de contrato documentado.
- Angular aporta una estructura opinada (Router, HttpClient, formularios reactivos) útil para una aplicación con varias pantallas.

### Costes asumidos

- Dos toolchains (Python y Node) y dos ecosistemas de pruebas.
- Duplicación conceptual de tipos entre backend y frontend; no hay tipos compartidos automáticos.
- Mayor superficie de configuración inicial.
- SQLite como base de datos de desarrollo, con limitaciones de concurrencia.

## 5. Estado actual del repositorio

En la fecha de este documento:

- No hay código de aplicación.
- No hay dependencias instaladas.
- No hay migraciones ni modelos de datos.
- No hay workflows de CI.
- Existe documentación de requisitos, arquitectura y proceso, pendiente de aprobación.

## 6. Decisiones todavía abiertas

Decisiones arquitectónicas y técnicas pendientes:

| ID | Decisión | Referencia |
| --- | --- | --- |
| P-01 | Versión de Angular y compatibilidad de Vitest | ADR 0001 |
| P-02 | Fijación de Python 3.13 frente al 3.15 local | ADR 0001 |
| P-03 | Proveedor de tipos de cambio | ADR 0001 |
| P-04 | Fuente autoritativa de tipos impositivos | ADR 0001 |
| P-05 | Estrategia de despliegue y papel de SQLite | ADR 0001 |
| P-06 | Fronteras definitivas de los módulos | ADR 0002 |
| P-07 | Límites transaccionales por caso de uso | ADR 0002 |
| P-09 | Política de errores de API (`application/problem+json`) | ADR 0002 |

Las preguntas de negocio Q-01 a Q-17 no se reproducen aquí para evitar duplicidad y deriva: su fuente única es [`docs/requirements/functional-requirements.md`](../../docs/requirements/functional-requirements.md), sección 5. No se mezclan ambos espacios de identificadores en una misma tabla.

El registro de tareas, evidencias y auditorías se mantiene en [`ai-workspace/README.md`](../README.md).

## 7. Lecciones registradas

- Documentar la decisión antes de implementar evitó construir sobre una base que iba a cambiar.
- El cambio de stack no invalida el análisis previo: la evaluación del repositorio y del `.gitignore` sigue siendo válida.
- La ausencia de requisitos detallados (impuestos, precios de almacenamiento y API) es el mayor riesgo del proyecto, no la elección de tecnologías.
