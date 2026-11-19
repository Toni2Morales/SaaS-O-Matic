# SPEC-010 — Refinamiento del frontend y verificación E2E

| Campo   | Valor                                                                             |
| ------- | --------------------------------------------------------------------------------- |
| Estado  | Implementada y validada localmente en TASK044; revisión del propietario pendiente |
| Fecha   | 2026-11-19                                                                        |
| Base    | TASK043P, `feature/mvp-frontend`, `84b087af352c1082880417ce10f7c2ede9b7108e`      |
| Stack   | Se conserva Angular 22.2.6 / TypeScript 6.0.3 y herramientas existentes           |
| Fuentes | Instrucción TASK044, TASK041–TASK043P, SPEC-007–009, contratos backend actuales   |

## 1. Objetivo y límites

Estabilizar y refinar los flujos de cliente y simulación existentes sin rediseño general,
ampliación comercial, cambio de contrato ni dependencia nueva. Investigar observaciones
V43 y UX-01–UX-10; distinguir problemas del producto de limitaciones de fixtures y
capturas. Mantener FastAPI como única autoridad para cálculos, impuestos, FX y snapshots.

Se permiten cambios frontend, pruebas y documentación vigente en los términos TASK044.
Código, pruebas, migraciones y dependencias del backend permanecen protegidos salvo que
se confirme un defecto backend; en ese caso se registra la causa y se solicita autorización
antes de modificarlo. No staging, commit, push, PR ni merge. TASK045 no se inicia.

## 2. Hallazgos e hipótesis de causa raíz

### V43-01 — Diferencia aparente entre 16 usuarios y el resultado guardado

**Observación, no defecto confirmado:** una captura interceptada muestra 16 usuarios y
resultados que corresponden a 15. Para ES, los valores de referencia son 15 → subtotal
140.00, IVA 29.40, total 169.40; 16 → 148.00, 31.08, 179.08.

Hipótesis a discriminar mediante evidencia:

1. Fixture visual interceptado devuelve un cálculo que no corresponde a sus parámetros.
2. La UI manda parámetros antiguos debido a sincronización/cancelación/orden de respuestas.
3. La UI muestra correctamente una preview obsoleta pero la captura no evidencia ese estado.
4. Respuesta POST o registro persistido del backend difiere de la petición actual.
5. Fallo en selección de resultado o estado después de guardar.

Antes de corregir, reproducir el caso con FastAPI y SQLite reales y observar petición
preview, petición create, respuesta 201, estado visual y registro del historial. Si sólo
el fixture es incorrecto, corregir el fixture y registrar expresamente que no se confirmó
defecto productivo. Probar UI real con 15 y 16 usuarios y consultar valores persistidos.

### V43-02 — Cabecera, foco y skip link

Hipótesis: sticky topbar en combinación con captura `fullPage` y scroll/foco producen
superposición; alternativa: navegación o foco real de la app activa el skip link o desplaza
la cabecera. Comparar viewport screenshot con full-page screenshot, registrar
`document.activeElement`, `scrollY`, estado `:focus` del skip link y posición de cabecera
antes/después de rutas y teclado. No eliminar skip link, outline ni navegación accesible.

### V43-03–V43-07 y UX anteriores

- V43-03: hacer visible la estimación en edición móvil, con estados explícitos y sin cubrir
  campos, teclado virtual, errores o acciones.
- V43-04: reforzar rango y referencias del slider, diferenciándolo del rango manual.
- V43-05: errores específicos por campo, asociados a labels; ocultar bandas cuando
  `user_count` sea inválido.
- V43-06: transiciones inequívocas entre preparando, calculando, actual, obsoleta, error,
  guardando y guardado. No permitir guardar con parámetros distintos de la preview vigente.
- V43-07 y UX-01–UX-10: refinamientos visuales/léxicos acotados, sin rediseño general,
  ni suprimir navegación, contenido o controles accesibles.

## 3. Reglas funcionales invariables

- usuarios enteros 0..1.000.000; slider 0..1.000 paso 1; manual no clampa valores;
  almacenamiento 0..1.000.000 GB; llamadas/mes 0..1.000.000.000.
- Display currency EUR/USD/GBP. No se introduce aritmética económica en Angular.
- Subtotales referencia 15 y 16 usuarios en ES permanecen como fixtures de prueba
  contrastados con respuestas backend reales; el producto presenta strings de API.
- Preview usa sólo `POST /simulations/preview`, debounce/cancelación y sin persistencia.
- Guardado explícito usa sólo `POST /simulations`, parámetros vigentes, sin retry
  automático ni supuesto de idempotencia.
- Backend, contratos, reglas fiscales y FX, datos históricos, dependencias y migraciones
  no se cambian como parte de una corrección frontend.

## 4. Estados y comportamiento accesible

La estimación móvil compacta (si se implementa) debe:

- mostrar importe sólo si la preview coincide con parámetros actuales y está vigente;
- comunicar preparación, cálculo, invalidez, error y guardado sin contenido contradictorio;
- incluir código/divisa y no esconder la estimación completa ni el botón de guardado;
- respetar `safe-area-inset`, zoom, reflow, teclado virtual y foco visible;
- evitar que `aria-live` anuncie continuamente cada actualización o el foco sea robado.

El skip link permanece accesible por teclado y visible al tener foco; las capturas pueden
ajustarse para no enfocar o mostrarlo inadvertidamente, pero no eliminarlo. El slider tiene
nombre, valor y límites accesibles, soporte de teclas y una pista visual suficiente sin
depender sólo del color. Los errores se asocian con `aria-describedby`.

No se declara WCAG 2.2 AA ni se instala axe. Se documentan las verificaciones manuales y
automatizadas efectivamente realizadas.

## 5. Estrategia de instalación y seguridad

- No modificar package manifests/lock, dependencias ni versiones.
- No ejecutar instalación en el `frontend/node_modules` operativo.
- En carpeta temporal aislada, copiar el manifiesto/lock actuales y ejecutar `npm ci
--ignore-scripts`; intentar typecheck/build/Vitest/lint/E2E con ese árbol limpio.
- No usar `npm ci` normal, `npm audit fix`, aprobaciones de allowlist ni permisos globales.
- Si el build falla por scripts omitidos, registrarlo sin reconstruir ni modificar el árbol
  normal y sin solicitar/ejecutar autorización implícita. No afirmar instalación limpia
  satisfactoria si no pasan las pruebas en el árbol aislado.
- npm audit es una señal del registry, no auditoría completa de CVE/SAST.

## 6. Cobertura de pruebas

Unitarias y E2E deterministas deben incluir los límites y transiciones de SPEC-009; además:

- V43-01: real 15/16, body preview/create, respuesta 201 e historial; fixtures 15/16
  coherentes con subtotales, impuestos y totales dados en §2.
- V43-02: foco y topbar comprobados en carga inicial, navegación, teclado y captura.
- V43-03/04/05: viewport, controles, error de campo, slider y bandas.
- V43-06: request tardía, formulario inválido en vuelo, retry FX y POST único.
- UX-01/04/06/07/08/09/10: títulos, iconos, enlaces, etiquetas, estado vacío, textos y
  contador responsive comprobados.
- Diseño: 320×568, 390×844, 768×1024, 1024×768, 1280×800, 1440×900, 1920×1080; zoom
  y document scroll width cuando el entorno lo permita.
- Integración real: SQLite temporal, migraciones 0001–0004, clientes sintéticos, flujos
  ES/PT, consumo, FX spot si disponible, exactitud de historial tras reload.

Las suites deterministas no dependen de Frankfurter. La integración FX externa se ejecuta
separada, con errores y valores reales informados sin sustituirlos por fixtures.

## 7. Aceptación y límites

La tarea se considera preparada localmente cuando los defectos reproducidos del alcance
están corregidos, las hipótesis no confirmadas están identificadas como tales, las suites
autorizadas pasan o sus fallos se registran, la integración real prueba 15/16 y el informe
TASK044 evalúa cada criterio. V43-01 se etiqueta «fixture incorrecto» sólo si el flujo real
del producto demuestra petición/respuesta/persistencia correctas; de otro modo, se informa
el defecto y se solicita autorización para backend si corresponde.

Siguen fuera de alcance autenticación, precios/impuestos nuevos, nuevas divisas/proveedores,
rediseño integral, nuevos servicios, despliegue, cambios backend sin autorización y cualquier
publicación Git. La auditoría independiente se realizará en tarea posterior.
