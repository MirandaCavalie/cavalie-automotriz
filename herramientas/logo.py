"""Genera web/img/logo-cavalie.svg y logo-cavalie-blanco.svg vectorizando el logo original.

Fuente: foto de perfil de la página de Facebook del taller (719x719 px, el logo mide
~620 px de ancho), guardada en assets-originales/logo/logo-facebook-719.jpg (fuera del repo).
Cada color (azul, tres verdes de la C y la hoja) se separa, se suaviza y se vectoriza con potrace.
Uso (requiere pillow, numpy y potracer): python herramientas/logo.py
Si llega el logo original en vector, reemplaza a este.
"""
from PIL import Image, ImageFilter
import numpy as np
import potrace

ORIGEN = 'assets-originales/logo/logo-facebook-719.jpg'
CAJA = (40, 240, 680, 480)          # recorte alrededor del logo
S = 4                               # sobremuestreo antes de vectorizar

img = Image.open(ORIGEN).convert('RGB').crop(CAJA)
big = np.asarray(img.resize((img.width * S, img.height * S), Image.LANCZOS)).astype(float)
r, g, b = big[..., 0], big[..., 1], big[..., 2]
tinta = (r + g + b) < 560

# Colores de referencia medidos en el original
TONOS = {'verde_claro': (106, 176, 54), 'verde_medio': (66, 150, 40), 'verde_oscuro': (4, 116, 52), 'azul': (4, 28, 110)}
centros = np.array(list(TONOS.values()), float)
dist = ((big[..., None, :] - centros[None, None]) ** 2).sum(-1)
clase = np.argmin(dist, -1)

def suave(mask, rad=S * 0.9):
    m = Image.fromarray((mask * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(rad))
    return np.asarray(m) > 127

def trazar(mask):
    curvas = potrace.Bitmap(~mask).trace(turdsize=60 * S, alphamax=1.0, opticurve=True, opttolerance=0.25)
    d = []
    for c in curvas:
        p = c.start_point; d.append(f'M{p.x / S:.2f},{p.y / S:.2f}')
        for sg in c.segments:
            if sg.is_corner:
                d.append(f'L{sg.c.x / S:.2f},{sg.c.y / S:.2f}L{sg.end_point.x / S:.2f},{sg.end_point.y / S:.2f}')
            else:
                d.append(f'C{sg.c1.x / S:.2f},{sg.c1.y / S:.2f} {sg.c2.x / S:.2f},{sg.c2.y / S:.2f} '
                         f'{sg.end_point.x / S:.2f},{sg.end_point.y / S:.2f}')
        d.append('Z')
    return ''.join(d)

capas = {n: trazar(suave(tinta & (clase == i))) for i, n in enumerate(TONOS)}
ys, xs = np.where(tinta)
vb = f'{xs.min() / S - 4:.0f} {ys.min() / S - 4:.0f} {(xs.max() - xs.min()) / S + 8:.0f} {(ys.max() - ys.min()) / S + 8:.0f}'

def svg(colores):
    partes = ''.join(f'<path fill="{colores[n]}" d="{capas[n]}"/>' for n in TONOS)
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" role="img" aria-label="Cavalié Automotriz">{partes}</svg>'

open('web/img/logo-cavalie.svg', 'w').write(svg({'verde_claro': '#6AB036', 'verde_medio': '#429628',
                                                 'verde_oscuro': '#047434', 'azul': '#041C6E'}))
# Versión para fondos oscuros: verdes en lima de la marca, azul en blanco
open('web/img/logo-cavalie-blanco.svg', 'w').write(svg({'verde_claro': '#C8E68A', 'verde_medio': '#B9E07A',
                                                        'verde_oscuro': '#A6D468', 'azul': '#FFFFFF'}))
print('viewBox', vb, {n: len(d) for n, d in capas.items()})
