# Cavalié Automotriz — sitio web

Sitio estático de [cavalieautomotriz.com](https://cavalieautomotriz.com): taller de mantenimiento GLP y gasolina en Santa Beatriz, Lima. Reemplaza al WordPress anterior y a cavalie.pe.

## Estructura

| Carpeta | Qué hay |
|---|---|
| `fuente/plantilla.html` | Cabecera, menú y pie compartidos por todas las páginas |
| `fuente/negocio.json` | Datos del negocio para Google y buscadores con IA (schema `AutoRepair`) |
| `fuente/paginas/` | El contenido de cada página |
| `herramientas/armar.py` | Une plantilla + páginas y escribe el sitio en `web/` (solo Python estándar) |
| `web/` | **El sitio listo para subir**: HTML, CSS, JS, imágenes, `.htaccess`, `sitemap.xml`, `robots.txt`, `llms.txt` |

## Editar y ver en local

```bash
python3 herramientas/armar.py
python3 -m http.server 4321 --directory web
```

Abrir http://localhost:4321. Los textos se editan en `fuente/` y luego se vuelve a correr `armar.py`. `web/css`, `web/js` y `web/img` se editan directamente.

## Publicar

Ver `PENDIENTES.md`. La vista previa lleva `noindex`; `python3 herramientas/armar.py --publicar` lo quita.

`.htaccess` contiene las redirecciones 301 de las URLs del sitio anterior, para conservar el SEO.
