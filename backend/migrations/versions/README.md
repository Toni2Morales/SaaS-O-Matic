# Migraciones de clientes

La revisión `0001_create_customers` crea la tabla `customers` con los cinco
campos funcionales obligatorios, `created_at` en UTC y la restricción única
`(country, tax_id)`.

El catálogo de planes aprobado para el MVP contiene únicamente `standard`. No se
crea una tabla de planes porque el catálogo es fijo y no aporta datos
adicionales en esta fase.
