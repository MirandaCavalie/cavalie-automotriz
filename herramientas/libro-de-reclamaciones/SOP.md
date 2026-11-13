# SOP: Libro de Reclamaciones virtual de Cavalié Automotriz

## Qué hace
Permite que un cliente registre un reclamo o una queja desde la web del taller. Al enviarlo, recibe en su correo una copia de su Hoja de Reclamación con número y fecha. El taller recibe la misma copia y todas las hojas quedan guardadas en una hoja de cálculo de Google, donde se anota la respuesta.

## Por qué se construyó así (build/buy/kill)
**Construir, con herramientas gratuitas (Google Forms + Apps Script).**
- El taller necesita un Libro de Reclamaciones virtual porque tiene web. Lo exigen el Código de Protección y Defensa del Consumidor y su reglamento (D.S. 011-2011-PCM y modificatorias).
- El volumen esperado es muy bajo, de unos pocos reclamos al año, así que no se justifica pagar una suscripción mensual.
- Google Forms ya cubre el formulario y el guardado. El script agrega lo que Forms no hace solo: número correlativo y copia inmediata al consumidor.
- **Comprar** un servicio especializado sigue siendo la alternativa si el abogado o contador no aprueba esta versión, o si el taller prefiere no mantener nada.

## Cómo correrlo
**Paso 0 (obligatorio):** que el abogado o contador del taller revise los textos y campos de `Codigo.gs` y de `fuente/paginas/libro-de-reclamaciones.html`. Sin esa aprobación no se publica.

**Paso 1: crear el formulario (una sola vez)**
1. Entrar a https://script.google.com con la cuenta **cavalieautomotriz@gmail.com**. Debe ser esa cuenta, porque los correos salen desde ahí.
2. Clic en **Nuevo proyecto**. Ponerle de nombre "Libro de Reclamaciones".
3. Borrar el contenido de `Código.gs` y pegar todo el contenido de `herramientas/libro-de-reclamaciones/Codigo.gs`.
4. Guardar (ícono de disquete).
5. En el menú de funciones de arriba, elegir **crearLibro** y clic en **Ejecutar**.
6. Google pedirá permisos para Formularios, Hojas de cálculo, enviar correos y ejecutar al enviar. Aceptarlos con la misma cuenta. Si aparece "Google no verificó esta app": **Configuración avanzada → Ir a Libro de Reclamaciones**. Es normal, porque es un script propio.
7. Abrir **Registro de ejecución**. Aparecen 3 enlaces:
   - **Formulario para el público**: termina en `/viewform`.
   - **Editar formulario**: guardarlo solo para el taller.
   - **Hoja de respuestas**.

**Paso 2: conectar la web**
1. Abrir `fuente/paginas/libro-de-reclamaciones.html`.
2. Reemplazar `#URL-DEL-FORMULARIO` por la URL que termina en `/viewform`.
3. Opcional: quitar los `<!-- -->` del `<iframe>` y reemplazar `URL-DEL-FORMULARIO` por esa misma URL. Así el formulario se ve dentro de la página.
4. Borrar la línea del aviso amarillo `[Falta crear el formulario…]`.
5. Ejecutar `python3 herramientas/armar.py`, revisar en local, hacer commit y push. Vercel lo publica solo.

**Paso 3: prueba**
Enviar una hoja de prueba con un correo propio. Comprobar tres cosas:
- que llegue el correo con "N.° 000001-…";
- que la hoja de cálculo tenga la fila y el número;
- que el correo del taller reciba la copia.

Después, borrar la fila de prueba. Para que la primera hoja real sea la 000001, ir a **Configuración del proyecto → Propiedades del script** y volver a poner `correlativo` en `0`.

## Entradas y salidas
- **Entrada:** el formulario de Google que llena el consumidor. Pide:
  - nombre, tipo y número de documento, domicilio, teléfono y correo;
  - si es menor de edad, y en ese caso los datos de su padre, madre o apoderado;
  - bien contratado (servicio o producto), monto y descripción;
  - tipo (reclamo o queja), detalle, pedido y la declaración de veracidad.
- **Salidas:**
  1. Una fila en la hoja "Libro de Reclamaciones – respuestas", con las columnas **N.° de hoja**, **Respuesta del proveedor** y **Fecha de respuesta**.
  2. Un correo HTML con la Hoja de Reclamación completa. Va al consumidor, con copia a cavalieautomotriz@gmail.com, e incluye los datos del proveedor (razón social, RUC y domicilio), el número, la fecha y el plazo de respuesta.

## Casos límite conocidos
- **El consumidor escribe mal su correo:** no le llega la copia, pero la hoja queda guardada y el taller recibe su copia. El taller debe contactarlo por teléfono.
- **Dos envíos al mismo tiempo:** el script usa un bloqueo para que no se repita el número correlativo.
- **Cambio de año:** el número sigue corriendo (000045-2027). Si el abogado pide reiniciar la numeración cada año, se pone `correlativo` en `0` el 1 de enero.
- **Límite de correos de Google:** unos 100 por día en cuentas gratuitas, de sobra para este uso.
- **Spam o envíos falsos:** Google Forms no tiene captcha. Si llegan envíos basura, se marcan en la hoja como "No válido". No se borran filas.
- **Pendiente:** no está automatizado el aviso cuando se acercan los 15 días hábiles sin respuesta. Por ahora la revisión es manual (ver abajo).

## Umbral de aprobación humana
**Todo reclamo o queja lo atiende una persona.** No hay respuesta automática; el sistema solo registra y envía la copia.
- Quien revise el correo del taller debe responder cada hoja **en un plazo máximo de 15 días hábiles**, por correo al consumidor.
- Después debe anotar la respuesta y la fecha en las columnas "Respuesta del proveedor" y "Fecha de respuesta".
- Recomendado: revisar la hoja de respuestas **cada lunes**.

## Mantenimiento
- **Conservación:** no borrar filas ni la hoja de cálculo. La norma pide guardar las hojas **al menos 2 años**.
- **Cambia la razón social, el RUC, el domicilio o el correo:** actualizar `PROVEEDOR` en el script (en script.google.com) y la página `fuente/paginas/libro-de-reclamaciones.html`.
- **Cambia la norma** (plazos o campos de INDECOPI): actualizar `PLAZO_DIAS_HABILES` y los textos. Lo revisa el abogado o contador.
- **Qué lo rompería:**
  - que se cambie o se cierre la cuenta cavalieautomotriz@gmail.com;
  - que alguien edite los títulos de las preguntas en el formulario, porque el script las lee por su título;
  - que se borre el disparador "alEnviar", que se puede revisar en script.google.com → Activadores.
- **Responsable:** Miranda, para la parte técnica, y la administración del taller, para responder los reclamos.
