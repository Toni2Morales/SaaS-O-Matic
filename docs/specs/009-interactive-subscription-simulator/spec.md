# SPEC-009 — Simulador interactivo de suscripciones

| Campo | Valor |
| --- | --- |
| Estado | Implementada localmente y validada TASK043; revisión/publicación pendientes |
| Fecha | 2026-11-18 |
| Base | TASK042 en `feature/mvp-frontend`, HEAD `23cc43b486d20f7995a2cf29375e3f724f3c7c3f` |
| Contratos | OpenAPI generado desde FastAPI local y modelos existentes |
| Stack | Angular 22.2.6; se conservan dependencias y arquitectura aprobadas |

## 1. Objetivo y alcance

Completar el flujo comercial mensual de simulación dentro de la feature Angular
existente. El usuario configura consumo para un cliente recuperado desde FastAPI,
recibe una estimación reactiva no persistida y decide explícitamente guardarla. La API
es la autoridad exclusiva de validación definitiva, tarifas, impuestos, FX y persistencia.

Incluye la ruta existente `/customers/:customerId/simulations/new`, acceso desde ficha,
historial y acción del dashboard (previa selección de cliente), carga del contexto,
formulario accesible, preview, guardado, actualización del historial, explicación de
tramos y unificación cromática autorizada. No incluye cambios backend, nuevos endpoints,
dependencias, reglas de negocio, edición/eliminación de historial ni TASK044.

## 2. Contratos verificados

`GET /customers/{customer_id}` devuelve `CustomerResponse` con `id`, `legal_name`,
`country`, `plan` y demás datos ya definidos. Los identificadores se validan como UUID
antes de solicitar recursos. País fiscal y plan mostrados proceden de esta respuesta.

Ambos POST reciben exactamente `SimulationCreateRequest` (extras prohibidos):

```json
{
  "customer_id": "<uuid>",
  "user_count": 15,
  "storage_gb": 250,
  "api_calls_per_month": 100000,
  "display_currency": "EUR"
}
```

`POST /simulations/preview` responde 200 con `SimulationPreviewResponse`, no incluye
`id`/`created_at` y no persiste. `POST /simulations` responde 201 con
`SimulationResponse` persistida. Errores documentados incluyen 404, 422, 500 y 503
Problem Details; 503 indica indisponibilidad de conversión. La lectura del historial es
`GET /customers/{customer_id}/simulations` paginada. No se añade contrato ni se llama a
Frankfurter desde el navegador.

Campos de entrada: enteros estrictos `user_count` 0..1.000.000, `storage_gb`
0..1.000.000, `api_calls_per_month` 0..1.000.000.000; moneda EUR/USD/GBP, EUR inicial.
Valores iniciales UX (no regla comercial): 15, 0, 0 y EUR.

## 3. Flujos y estados

1. Abrir ruta con UUID válido; cargar cliente. UUID inválido no genera petición; 404,
   carga y error de transporte se distinguen y no permiten calcular ni guardar.
2. Tras cliente válido, mostrar razón social, país y plan y activar formulario.
3. Con formulario válido, solicitar preview inicial y después de cambios. El estado
   anterior, si se conserva, se etiqueta inequívocamente desactualizado.
4. Seleccionar EUR/USD/GBP genera preview. Si FX devuelve 503 se conserva formulario,
   se presenta error y reintento manual; EUR puede seleccionarse sin cambiar moneda
   automáticamente.
5. Guardar requiere preview exitosa correspondiente exactamente a los parámetros
   actuales, formulario estable y ausencia de peticiones/guardados concurrentes.
6. Tras 201, la respuesta persistida reemplaza la preview como resultado definitivo;
   actualizar la vista de historial del cliente y enlazar a ficha/historial. No hay
   confirmación optimista ni reintento automático. Un fallo de transporte al guardar
   advierte que pudo persistirse y aconseja comprobar historial.

Estados explícitos: cargando cliente, cliente inexistente/UUID inválido/error de carga,
formulario inválido, preparando preview, calculando, disponible, preview obsoleta,
error de cálculo/FX, guardando, guardado y error de guardado.

## 4. Formulario y slider

Reactive Forms estrictamente tipados; los controles numéricos permiten representar
transitoriamente texto vacío/no numérico y validan requerido, entero, finito y límites
sin redondeo ni truncamiento silencioso. Mensajes en español enlazados mediante
`aria-describedby` y `aria-invalid`. No se envían previews en estado inválido.

El slider cubre 0..1.000, paso 1, sincronizado bidireccionalmente con entrada manual.
Si la entrada manual excede 1.000, se conserva sin cambio en el formulario y el slider
se deshabilita temporalmente con explicación accesible; mover el slider explícitamente
restablece el formulario al valor elegido. No se clampa ni se reescribe el valor manual
por una actualización programática del slider.

Almacenamiento se expresa en GB y llamadas son mensuales. En este MVP ambos son datos
informativos sin coste adicional según la respuesta; la UI no les asigna precio.

## 5. Arquitectura y concurrencia

Conservar `core/shared/features`, standalone, Signals, RxJS, API central `/api`, proxy,
HttpClient y servicios de acceso a datos por feature. El cliente y el historial se
reutilizan desde TASK042. Separar cliente de simulaciones, formulario, presentación de
resultado y helpers cuando reduzca acoplamiento; sin store global.

El flujo de preview parte de cambios válidos del formulario y un disparador explícito
de reintento, aplica debounce de 250 ms, deduplica solicitudes consecutivas por
parámetros, usa `switchMap` para cancelar la anterior y un contador/generación de
solicitud para rechazar cualquier respuesta tardía. La invalidez se procesa antes del
debounce: cancela pendiente/en curso e invalida inmediatamente el resultado guardable.
La destrucción de la vista cancela todas las suscripciones. Guardado congela controles,
captura la misma petición que la preview vigente y bloquea doble envío.

No se deriva precio, impuesto, tipo de cambio ni importe convertido en TypeScript. La
presentación de tramos puede calcular solo cantidades no monetarias: hasta 10, 11–50 y
51+; las tarifas unitarias aprobadas (10/8/5 EUR) y cantidades actuales por banda se
presentan como explicación. Este recuento entero no monetario no calcula subtotal, que
procede siempre del backend.

## 6. Precisión y presentación económica

Importes y tipos de cambio permanecen como cadenas decimales del contrato. Reutilizar
el formateador exacto existente, con agrupación española y código/símbolo inequívoco;
conservar la cadena original. Mostrar los importes EUR, país fiscal, tasa e impuesto
devueltos, total convertido y moneda solicitada. Fecha de referencia/recuperación,
fuente y tasa se muestran solo cuando el backend las proporciona, con detalle técnico
secundario desplegable. Las tasas no se describen como mercado en directo: provienen del
proveedor y política de caché del backend. La estimación no es factura ni asesoramiento
fiscal.

## 7. Diseño, accesibilidad y responsive

En escritorio: dos columnas configuración/resultado; en móvil, una columna sin
desbordamiento desde 320 px. Destacar total mensual. Unificar primario Material con
tokens existentes y APIs públicas de tematización, conservando shell y estética; no
rediseñar páginas ajenas. Controles operables por teclado, foco visible, labels y
errores asociados, estados con anuncios no intrusivos y errores/éxitos anunciados.
Revisar foco programático de títulos al navegar sin interferir con teclado. Contraste y
dependencia exclusiva del color se verifican; no se afirma certificación WCAG AA.

## 8. Pruebas y aceptación

Vitest: límites, valores UX, slider/manual >1.000, moneda, invalidez inmediata, debounce,
duplicados, cancelación/desorden, datos decimales string, errores 404/422/503, EUR y
reintento, guardado vigente, bloqueo doble, divergencia preview/201, destrucción.
Playwright: ruta y accesos, formularios, moneda, FX, guardado e historial, teclado y
responsive; separar pruebas interceptadas de integración real. Validar Angular real con
FastAPI y SQLite temporal, clientes sintéticos, preview sin persistencia, guardado y
recarga; FX externo es comprobación puntual separada y no suite determinista.

Criterios: sustituir placeholder; cliente real; valores/límites exactos; preview
reactiva cancelable sin persistencia; respuesta obsoleta nunca visible como actual;
FastAPI única autoridad económica; EUR/USD/GBP y errores; guardado explícito seguro;
historial persistido; diseño, accesibilidad, documentación y regresiones verificables.

## 9. Riesgos y límites

- La respuesta de guardado puede diferir de preview por recálculo/tipo FX: la respuesta
  201 prevalece y cualquier diferencia se comunica.
- POST sin respuesta de red puede haberse persistido; no se presume idempotencia.
- Dependencia externa FX puede producir 503; EUR continúa disponible.
- El slider no representa valores >1.000, por lo que se deshabilita mientras el campo
  manual esté fuera de rango; el campo y el cálculo permanecen íntegros.
- Las limitaciones de red, navegador, herramienta o servicio externo se documentan como
  pendientes, nunca como criterios superados.
