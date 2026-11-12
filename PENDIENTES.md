# Pendientes antes de publicar

En la vista previa, los datos por confirmar aparecen **resaltados en amarillo** (clase `pendiente`). Ninguno puede quedar al publicar.

## Datos que debe confirmar el taller
- [ ] Razón social y RUC (el registro de cavalie.pe menciona "CARVALIE E.I.R.L."; confirmar)
- [ ] Correo de contacto público
- [ ] Dirección exacta: Google Maps dice **Jr.** José Gálvez 1469; el sitio viejo dice **Av.** Usamos la de Maps
- [ ] ¿Sigue activo el fijo (01) 470-0652? Hoy no aparece en el sitio
- [ ] Condiciones y vigencia de la promoción del 50% (¿sobre la mano de obra o el total? ¿aplica a todos los autos?)
- [ ] Lista exacta de lo que incluye el mantenimiento GLP (`fuente/paginas/mantenimiento-glp.html`)
- [ ] Que el taller sigue autorizado por el MTC y que las certificaciones GLP siguen siendo con SGS
- [ ] Testimonios: son del sitio de 2013 (Víctor Arteaga Ferrando, Hernán Carranza, Federico Gálvez). Confirmar que se pueden usar, o reemplazarlos por reseñas recientes de Google
- [ ] Logo en alta resolución o vector (SVG/AI/PDF). El actual es un PNG de 200×50 de cavalie.pe
- [ ] Fotos recientes del taller (las del sitio son de 2013–2024)

## Legal y Google Ads
- [ ] Libro de Reclamaciones virtual (obligatorio en Perú; Indecopi). Hoy es un marcador en el pie
- [ ] Revisar la política de privacidad (`fuente/paginas/politica-de-privacidad.html`) con un asesor
- [ ] Revisar el estado de las cuentas de Google Ads y sus anuncios activos
- [ ] Configurar Google Tag Manager: el sitio ya envía el evento `whatsapp_click` a `dataLayer` en cada clic a WhatsApp; crear con ese evento la conversión de Ads y GA4
- [ ] Pausar o actualizar los anuncios que apuntan a las landings viejas (/lp/…) y a cavalie.pe antes de redirigirlos

## Servidor
- [ ] Tareas de seguridad y de espacio en disco del hosting: ver la auditoría local (`auditoria/AUDITORIA.md`, fuera del repo)

## Publicar
1. `python3 herramientas/armar.py --publicar` (quita el `noindex` de todas las páginas)
2. Verificar que no queda ningún `class="pendiente"`: `grep -r 'class="pendiente"' web/`
3. Seguir el plan de cambio del doc "Plan web Cavalié Automotriz": mover el WordPress a una carpeta de respaldo y subir `web/` a `public_html` (incluido `.htaccess`)
