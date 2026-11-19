# Guía de demostración técnica (5–10 minutos)

## Preparación previa

- En el entorno probado Windows 10, instalar los runtimes descritos en la
  [guía local](local-development.md) y ejecutar `start.ps1` desde la raíz del clon.
- Confirmar health API y abrir `http://127.0.0.1:4200`.
- Usar únicamente datos sintéticos. El identificador español `B12345674` está cubierto
  como válido por las pruebas existentes; `B12345670` se usa como ejemplo inválido en el
  E2E. Algoritmo fiscal solo valida control, no existencia del titular.
- Si `B12345674` ya existe en esa base local, abrir el cliente existente o usar un
  identificador sintético alternativo cuya validez esté comprobada con las pruebas del
  validador; no crear datos personales reales.
- USD/GBP requieren Internet/proveedor FX. Si no está disponible, mostrar el 503 controlado
  y cambiar a EUR; no inventar tipos ni sustituirlos por fixtures en la aplicación normal.

## Guion

| Tiempo     | Acción y explicación                                                                                                                                                                                                                                     |
| ---------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 0:00–0:45  | Mostrar `start.ps1`, las URLs y el propósito: estimar suscripciones SaaS para equipo comercial interno.                                                                                                                                                  |
| 0:45–1:45  | En alta ES registrar empresa sintética. Mostrar rechazo de `B12345670`, alta de `B12345674`; explicar validación algorítmica frente a existencia real. Opcional: cliente PT con código genérico `PT-AUDIT-045B` (no validación fiscal oficial).          |
| 1:45–2:30  | Buscar cliente por razón social y por ID fiscal, abrir ficha, indicar que historial es paginado e inmutable.                                                                                                                                             |
| 2:30–4:20  | Abrir simulador: usuarios 15, almacenamiento 250 GB y 100.000 llamadas/mes. Mostrar subtotal 140, IVA ES 29,40 y total 169,40 EUR. Explicar 10×10 + 5×8; storage/llamadas informativos, sin cargos. Cambiar a 16: subtotal 148, IVA 31,08, total 179,08. |
| 4:20–5:20  | Mostrar USD y GBP si proveedor accesible. FastAPI es quien consulta Frankfurter; la UI no se conecta directamente. Referencias fechadas, caché 24 h, no mercado continuo. Si 503, explicar y usar EUR.                                                   |
| 5:20–6:20  | Mostrar preview sin escritura (historial intacto), guardar explícitamente, ver historial; recargar para demostrar persistencia y snapshot original.                                                                                                      |
| 6:20–7:00  | Reducir viewport para mostrar responsive y navegación móvil.                                                                                                                                                                                             |
| 7:00–9:00  | Explicar modularidad, ADR/SPEC/plan/tasks, backend como autoridad de cálculos, snapshots y calidad local. Aclarar que Actions es manual y los hallazgos A47 están aplazados, no resueltos.                                                               |
| 9:00–10:00 | Cerrar con límites: sin auth/facturación, seis países/un plan, SQLite local, FX de referencia, accesibilidad no certificada, P-05/hosting no resuelto.                                                                                                   |

## Mensajes técnicos clave

- Preview llama el endpoint de cálculo sin escritura; guardar vuelve a calcular en el
  servidor y devuelve HTTP 201. Puede diferir de una preview previa si cambia la referencia.
- Los datos económicos históricos no se recalculan con las reglas/tasas actuales.
- La aplicación es una herramienta local/interna de evaluación; esta guía no implica que
  esté preparada para producción pública.
- Si la demo no tiene FX, EUR funciona por identidad y se puede mostrar el estado de error
  como comportamiento previsto; jamás presentar una tasa inventada como real.
