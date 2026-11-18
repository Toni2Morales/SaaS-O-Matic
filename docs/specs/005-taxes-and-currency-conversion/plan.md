# PLAN-005

1. Inventario/hashes acumulados, fetch y baseline 340 antes del código.
2. Verificar fuentes y escribir SPEC-005 antes de implementar.
3. Objetos de dominio y cálculo exacto reutilizable; catálogo versionado en infraestructura.
4. Puerto estructural en aplicación; adaptador urllib con caché compartida e inyección de reloj/transporte.
5. Obtener país y cerrar lectura antes de red; calcular antes de persistir snapshot completo.
6. Ampliar DTO/HTTP (EUR predeterminado), errores 503 y OpenAPI.
7. Migración 0004 nullable TEXT, codec validado; históricos intactos y downgrade protegido.
8. Regresión y pruebas sintéticas; smoke externo separado; revisión documental/hashes/Git.

No nuevas dependencias. Infraestructura no importa aplicación; implementa el puerto
por compatibilidad estructural. Snapshot JSON TEXT con tasas/importes en cadenas,
no números JSON ni REAL. Pruebas SQL físicas deberán verificar esa propiedad.
