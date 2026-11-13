#!/usr/bin/env python3
"""Arma el sitio estático de Cavalié Automotriz.

Une fuente/plantilla.html (cabecera y pie compartidos) con cada página de
fuente/paginas/ y escribe el resultado en web/. También genera sitemap.xml.

Uso:
    python3 herramientas/armar.py              # vista previa (noindex en todas las páginas)
    python3 herramientas/armar.py --publicar   # versión final: quita el noindex

Solo usa la biblioteca estándar de Python.
"""
import json
import re
import sys
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
FUENTE = RAIZ / "fuente"
WEB = RAIZ / "web"
DOMINIO = "https://cavalieautomotriz.com"

# ruta pública -> datos de la página
PAGINAS = {
    "/": {
        "archivo": "inicio.html",
        "titulo": "Taller automotriz en Lima: GLP y gasolina | Cavalié Automotriz",
        "descripcion": "Taller automotriz y mecánico multimarca en Santa Beatriz, Lima, desde 1999. Mantenimiento de autos a GLP y gasolina. 4,8★ en Google. Cotiza por WhatsApp.",
        "portada": "hero-atencion",
        "faq": True,
        "sitio_web": True,
        "prioridad": "1.0",
    },
    "/mantenimiento-glp/": {
        "archivo": "mantenimiento-glp.html",
        "titulo": "Mantenimiento GLP en Lima: BRC y Landi Renzo | Cavalié Automotriz",
        "nombre": "Mantenimiento GLP",
        "descripcion": "Mantenimiento de GLP en Lima: filtros, reductor, inyectores, prueba de fugas y calibración con software. BRC, Landi Renzo y todas las marcas.",
        "faq": True,
        "servicio": "Mantenimiento de sistema GLP",
        "prioridad": "0.9",
    },
    "/mantenimiento-gasolina/": {
        "archivo": "mantenimiento-gasolina.html",
        "titulo": "Taller mecánico en Lima: mecánica general | Cavalié Automotriz",
        "nombre": "Mantenimiento gasolina",
        "descripcion": "Taller mecánico multimarca en Santa Beatriz, Lima: mantenimiento preventivo, mecánica general, electrónica, frenos, suspensión y motor. Desde 1999.",
        "servicio": "Mantenimiento de autos a gasolina y mecánica general",
        "prioridad": "0.9",
    },
    "/preguntas-frecuentes/": {
        "archivo": "preguntas-frecuentes.html",
        "titulo": "Preguntas frecuentes sobre GLP | Cavalié Automotriz",
        "nombre": "Preguntas frecuentes",
        "descripcion": "Cada cuánto hacer el mantenimiento GLP, cuánto se ahorra con gas, si pierde potencia, qué aceite usar y más. Respuestas del equipo de Cavalié Automotriz.",
        "faq": True,
        "prioridad": "0.8",
    },
    "/contacto/": {
        "archivo": "contacto.html",
        "titulo": "Contacto y cómo llegar | Cavalié Automotriz",
        "nombre": "Contacto",
        "descripcion": "Jr. José Gálvez 1469, Santa Beatriz, Lima. Lunes a viernes 8:15–17:50 y sábados 8:15–13:00. Cotiza por WhatsApp al 983 745 377.",
        "prioridad": "0.8",
    },
    "/politica-de-privacidad/": {
        "archivo": "politica-de-privacidad.html",
        "titulo": "Política de privacidad | Cavalié Automotriz",
        "nombre": "Política de privacidad",
        "descripcion": "Cómo Cavalié Automotriz trata los datos que nos envías por WhatsApp o por el formulario de cotización.",
        "prioridad": "0.3",
    },
    "/guias/": {
        "archivo": "guias/index.html",
        "titulo": "Guías para cuidar tu auto | Cavalié Automotriz",
        "nombre": "Guías",
        "descripcion": "Guías del taller Cavalié Automotriz sobre mantenimiento GLP, GLP o GNV, señales de falla y cómo elegir un taller mecánico de confianza en Lima.",
        "prioridad": "0.6",
    },
    "/guias/mantenimiento-glp-lima/": {
        "archivo": "guias/mantenimiento-glp-lima.html",
        "titulo": "Mantenimiento GLP en Lima: qué incluye, cada cuánto y precio",
        "titular": "Mantenimiento GLP en Lima: qué incluye, cada cuánto y cuánto cuesta",
        "nombre": "Mantenimiento GLP: guía",
        "descripcion": "Qué incluye un mantenimiento GLP completo, cada cuántos kilómetros se hace, señales de que toca y de qué depende el precio en Lima. Guía de Cavalié Automotriz.",
        "fecha": "2026-11-13",
        "prioridad": "0.7",
    },
    "/guias/senales-falla-glp/": {
        "archivo": "guias/senales-falla-glp.html",
        "titulo": "7 señales de falla del GLP en tu auto | Cavalié Automotriz",
        "titular": "7 señales de que tu auto a GLP necesita revisión",
        "nombre": "Señales de falla del GLP",
        "descripcion": "Tirones, se pasa solo a gasolina, olor a gas, más consumo o check engine: qué significa cada señal de falla del GLP y qué hacer. Guía de Cavalié Automotriz.",
        "fecha": "2026-11-13",
        "prioridad": "0.7",
    },
    "/guias/glp-o-gnv/": {
        "archivo": "guias/glp-o-gnv.html",
        "titulo": "GLP o GNV: cuál conviene en Lima | Cavalié Automotriz",
        "titular": "GLP o GNV: cuál conviene para tu auto en Lima",
        "nombre": "GLP o GNV",
        "descripcion": "GLP o GNV para tu auto en Lima: diferencias en ahorro, potencia, autonomía, espacio del tanque y desgaste del motor. Guía de Cavalié Automotriz.",
        "fecha": "2026-11-13",
        "prioridad": "0.7",
    },
    "/guias/como-elegir-taller-mecanico-lima/": {
        "archivo": "guias/como-elegir-taller-mecanico-lima.html",
        "titulo": "Cómo elegir un taller mecánico en Lima | Cavalié Automotriz",
        "titular": "Cómo elegir un taller mecánico de confianza en Lima: 8 cosas que debes pedir",
        "nombre": "Cómo elegir un taller mecánico",
        "descripcion": "8 cosas que debes pedir antes de dejar tu auto en un taller mecánico en Lima: diagnóstico, presupuesto, historial, reseñas y más. Guía de Cavalié Automotriz.",
        "fecha": "2026-11-13",
        "prioridad": "0.7",
    },
    "/libro-de-reclamaciones/": {
        "archivo": "libro-de-reclamaciones.html",
        "titulo": "Libro de Reclamaciones | Cavalié Automotriz",
        "nombre": "Libro de Reclamaciones",
        "descripcion": "Libro de Reclamaciones virtual de CARVALIE E.I.R.L. (Cavalié Automotriz), RUC 20503409021. Registra tu reclamo o queja.",
        "prioridad": "0.3",
    },
    "/404.html": {
        "archivo": "404.html",
        "titulo": "Página no encontrada | Cavalié Automotriz",
        "descripcion": "La página que buscas no existe. Cavalié Automotriz: mantenimiento GLP y gasolina en Santa Beatriz, Lima.",
        "sin_sitemap": True,
    },
}

NOINDEX = '  <meta name="robots" content="noindex, nofollow"><!-- VISTA PREVIA: quitar esta línea al publicar -->\n'


def ld(objeto):
    texto = json.dumps(objeto, ensure_ascii=False, indent=2)
    return '<script type="application/ld+json">\n' + texto + "\n  </script>"


def migas(ruta, titulo, padre=None):
    """Migas de pan: Inicio › (padre) › página. `padre` es (ruta, nombre), p. ej. las guías."""
    niveles = [("/", "Inicio")] + ([padre] if padre else []) + [(ruta, titulo)]
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i, "name": n, "item": DOMINIO + r}
            for i, (r, n) in enumerate(niveles, 1)
        ],
    }


GUIAS = ("/guias/", "Guías")
AUTOR = {"@type": "Person", "name": "Domingo Cavalié", "jobTitle": "Fundador de Cavalié Automotriz",
         "worksFor": {"@id": DOMINIO + "/#taller"}}


def articulo(ruta, p):
    """Schema Article para las guías, con Domingo Cavalié como autor."""
    return {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": p["titular"],
        "description": p["descripcion"],
        "author": AUTOR,
        "publisher": {"@id": DOMINIO + "/#taller"},
        "datePublished": p["fecha"],
        "dateModified": p["fecha"],
        "inLanguage": "es-PE",
        "image": DOMINIO + "/img/og-cavalie.jpg",
        "mainEntityOfPage": DOMINIO + ruta,
    }


def faq_desde_html(html):
    """Construye el schema FAQPage leyendo los <details> de la página."""
    import re
    preguntas = []
    for bloque in re.findall(r"<details>(.*?)</details>", html, re.S):
        p = re.search(r"<summary>(.*?)</summary>", bloque, re.S)
        r = re.findall(r"<p>(.*?)</p>", bloque, re.S)
        if p and r:
            limpiar = lambda s: re.sub(r"<[^>]+>", "", s).strip()
            preguntas.append({
                "@type": "Question",
                "name": limpiar(p.group(1)),
                "acceptedAnswer": {"@type": "Answer", "text": " ".join(limpiar(x) for x in r)},
            })
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": preguntas}


# Bloques de texto donde se evita la viuda (una palabra sola en la última línea)
# Primero títulos y párrafos; luego los contenedores (li, dd...) que no tengan títulos o párrafos adentro
_BLOQUES = re.compile(r"(<(h[1-3]|p|summary)\b[^>]*>)(.*?)(</\2>)", re.S)
_CONTENEDORES = re.compile(r"(<(li|dd|blockquote|figcaption)\b[^>]*>)(.*?)(</\2>)", re.S)


# Largo máximo (en letras) de las dos palabras unidas: más largo y desbordaría a 320 px
_MAX_UNION = {"h1": 14, "h2": 20, "h3": 22}


def sin_viudas(html):
    """Une las dos últimas palabras de cada bloque de texto con &nbsp;.

    Respaldo para navegadores sin `text-wrap: balance/pretty` (ver estilos.css).
    En los títulos solo se unen si juntas caben en un celular de 320 px (ver _MAX_UNION).
    """
    def unir(m):
        apertura, etiqueta, interior, cierre = m.groups()
        if re.search(r"<(h[1-6]|p|ul|ol)\b", interior):
            return m.group(0)
        partes = re.split(r"(<[^>]+>)", interior)
        for i in range(len(partes) - 1, -1, -1):
            texto = partes[i]
            if texto.startswith("<"):
                continue
            recortado = texto.rstrip()
            pos = recortado.rfind(" ")
            if pos == -1:
                if recortado:  # la última palabra está sola en este tramo; el espacio previo está antes de una etiqueta
                    break
                continue
            ultima = re.sub(r"<[^>]+>", "", "".join(partes[i + 1:])).strip()
            ultimas = (recortado[pos + 1:] + ultima)
            penultima = recortado[:pos].rsplit(" ", 1)[-1]
            if len(penultima) + len(ultimas) > _MAX_UNION.get(etiqueta, 40):
                break
            partes[i] = recortado[:pos] + "&nbsp;" + texto[pos + 1:]
            break
        return apertura + "".join(partes) + cierre
    return _CONTENEDORES.sub(unir, _BLOQUES.sub(unir, html))


def armar(publicar=False):
    plantilla = (FUENTE / "plantilla.html").read_text(encoding="utf-8")
    negocio = json.loads((FUENTE / "negocio.json").read_text(encoding="utf-8"))
    if publicar:
        plantilla = plantilla.replace(NOINDEX, "")

    for ruta, p in PAGINAS.items():
        contenido = (FUENTE / "paginas" / p["archivo"]).read_text(encoding="utf-8")
        esquemas = [negocio]
        if p.get("nombre"):
            esquemas.append(migas(ruta, p["nombre"], GUIAS if p.get("titular") else None))
        if p.get("titular"):
            esquemas.append(articulo(ruta, p))
        if p.get("sitio_web"):
            esquemas.append({"@context": "https://schema.org", "@type": "WebSite", "@id": DOMINIO + "/#sitio",
                             "name": "Cavalié Automotriz", "alternateName": "Cavalié: Taller Automotriz y Mecánico", "url": DOMINIO + "/",
                             "inLanguage": "es-PE", "publisher": {"@id": DOMINIO + "/#taller"}})
        if p.get("servicio"):
            esquemas.append({
                "@context": "https://schema.org",
                "@type": "Service",
                "name": p["servicio"],
                "serviceType": p["servicio"],
                "provider": {"@id": negocio["@id"]},
                "areaServed": {"@type": "City", "name": "Lima"},
                "url": DOMINIO + ruta,
            })
        if p.get("faq"):
            esquemas.append(faq_desde_html(contenido))

        precarga = ""
        if p.get("portada"):
            n = p["portada"]
            precarga = (f'\n  <link rel="preload" as="image" href="/img/{n}-1520.webp" '
                        f'imagesrcset="/img/{n}-800.webp 800w, /img/{n}-1520.webp 1520w" imagesizes="100vw">')

        html = (plantilla
                .replace("{{titulo}}", p["titulo"])
                .replace("{{descripcion}}", p["descripcion"])
                .replace("{{ruta}}", ruta)
                .replace("{{preload}}", precarga)
                .replace("{{schema}}", "\n  ".join(ld(e) for e in esquemas))
                .replace("{{contenido}}", contenido)
                .replace('  <link rel="canonical" href="https://cavalieautomotriz.com/404.html">\n', "")
                .replace("<body>", '<body class="inicio">' if ruta == "/" else "<body>", 1))
        # marcar la página actual en el menú
        html = html.replace(f'<a href="{ruta}">', f'<a href="{ruta}" aria-current="page">', 1) if ruta != "/" else html

        html = sin_viudas(html)

        if ruta.endswith(".html"):
            destino = WEB / ruta.strip("/")
        elif ruta == "/":
            destino = WEB / "index.html"
        else:
            destino = WEB / ruta.strip("/") / "index.html"
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(html, encoding="utf-8")
        print("ok", ruta)

    hoy = date.today().isoformat()
    urls = "\n".join(
        f"  <url><loc>{DOMINIO}{r}</loc><lastmod>{hoy}</lastmod><priority>{p['prioridad']}</priority></url>"
        for r, p in PAGINAS.items() if not p.get("sin_sitemap"))
    (WEB / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "\n</urlset>\n",
        encoding="utf-8")
    print("ok sitemap.xml", "(publicación)" if publicar else "(vista previa: noindex activo)")


if __name__ == "__main__":
    armar(publicar="--publicar" in sys.argv)
