# PLAN-004 — Plan técnico

Implementado localmente. Baseline 240; cierre 340 pruebas, Ruff/formato/mypy/pip
check correctos. Evidencias y limitaciones en el [registro TASK036](../../../ai-workspace/01-tasks/TASK036-international-customers-and-simulations.md).

1. Verificar Git, hashes TASK035 y baseline antes del código.
2. Extender CountryCode; añadir GenericTaxId y selector por país. Adaptar entidad,
   puerto, caso de uso y mapeador con unión de tipos; conservar SpanishTaxId.
3. Admitir cero en pricing y simulaciones; aislar contexto del formateador.
4. DTO de creación con consumos obligatorios; entidad admite NULL histórico.
   Límites técnicos en aplicación y HTTP; servidor fija periodo. Validar antes
   de comprobar cliente y calcular. No importar dominio desde presentación.
5. Modelo ORM y migración batch 0003 con preflight de downgrade y comprobación FK.
   La unicidad compuesta ya existe: conservarla, no crear otra redundante.
6. Adaptar regresión solo por contratos aprobados, añadir tests de internacionalización,
   estrictos, SQL físico, migración poblada, traps y arquitectura.
7. Ejecutar Pytest/Ruff/formato/mypy/pip check y verificar 35 pines sin instalaciones.
8. Actualizar documentación vigente y registrar evidencias TASK036, sin publicar.

Rechazar downgrade con consumos conocidos evita perder información incluso cuando
el esquema antiguo podría almacenar usuarios positivos. No modificar datos para
sortear esta protección. H-06 conserva FK y rollback; no hay borrado público.
