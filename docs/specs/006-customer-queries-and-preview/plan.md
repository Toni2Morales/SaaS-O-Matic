# PLAN-006

1. Fetch/estado, inventario y huellas antes de editar; baseline411 y lock35.
2. Documentar contratos, Unicode, NULL históricos y cálculo compartido antes del código.
3. Añadir puertos de lectura segregados y consultas SQL paginadas sobre modelos actuales.
4. Registrar UDF casefold por conexión, patrón LIKE escapado y orden estable; sin migración.
5. Añadir casos de uso y DTO de consultas, detalle e historial.
6. Extraer CalculateSimulation para compartir validación/cliente/pricing/MonthlyEstimator;
   PreviewSimulation no recibe puerto de escritura; mantener creación compatible.
7. Esquemas de respuesta diferenciados: preview sin id/created_at y registro histórico
   con todos los datos desconocidos NULL. No importar dominio desde presentación.
8. Endpoints, problem details, dependencias y composición real de bootstrap.
9. Pruebas offline y SQL authorizer de solo lectura; OpenAPI y flujo completo.
10. Documentación vigente, evidencias y validaciones finales sin publicación.
