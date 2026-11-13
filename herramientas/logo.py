"""Genera web/img/logo-cavalie.svg y logo-cavalie-blanco.svg.

Tipografía: Jost (SIL OFL) o TeX Gyre Adventor (GUST Font License), en
assets-originales/fuentes/ (no se sube al repo). Las medidas salen del logo original
ampliado 8x: cada elemento se escala y se ubica en la misma caja que ocupa en el original.
Uso (requiere fonttools): python herramientas/logo.py adventor 0 0.8
(fuente, peso si es Jost, compresión horizontal)
Provisorio hasta tener el logo original en vector.
"""
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

import sys
from fontTools.varLib.instancer import instantiateVariableFont
FUENTE = sys.argv[1] if len(sys.argv) > 1 else 'adventor'
PESO = int(sys.argv[2]) if len(sys.argv) > 2 else 700
if FUENTE == 'jost':
    F = instantiateVariableFont(TTFont('assets-originales/fuentes/Jost-variable.ttf'), {'wght': PESO})
else:
    F = TTFont('assets-originales/fuentes/texgyreadventor-bold.otf')
GS, CMAP, HM = F.getGlyphSet(), F.getBestCmap(), F['hmtx']
BASE = 272                      # línea base en el original ampliado

def caja(ch):
    bp = BoundsPen(GS); GS[CMAP[ord(ch)]].draw(bp); return bp.bounds

K = float(sys.argv[3]) if len(sys.argv) > 3 else 0.8   # el logo original está comprimido en horizontal

def trazo(ch, x, sx, sy, base):
    pen = SVGPathPen(GS); GS[CMAP[ord(ch)]].draw(TransformPen(pen, (sx, 0, 0, -sy, x, base)))
    return pen.getCommands()

def linea(texto, x0, x1, sy, base):
    """Ubica el texto entre x0 y x1 (escala vertical sy, horizontal sy*K) repartiendo el espacio."""
    sx = sy * K
    anchos = [HM[CMAP[ord(c)]][0] * sx for c in texto]
    b0, b1 = caja(texto[0]), caja(texto[-1])
    natural = sum(anchos[:-1]) + b1[2] * sx - b0[0] * sx
    extra = (x1 - x0 - natural) / (len(texto) - 1)
    x = x0 - b0[0] * sx; d = []
    for c, w in zip(texto, anchos):
        d.append(trazo(c, x, sx, sy, base)); x += w + extra
    print(texto, 'espacio entre letras', round(extra, 1))
    return ''.join(d)

xh = F['OS/2'].sxHeight; cap = F['OS/2'].sCapHeight
# Medidas del original (PNG de 200 px) x8, origen en x=35: ver comentarios
# "C": caja x 16-224, y 24-288
cb = caja('C'); sy = 264 / (cb[3] - cb[1]); sx = 208 / (cb[2] - cb[0])
C = trazo('C', 16 - cb[0] * sx, sx, sy, 288 + cb[1] * sy)
# "avalie": altura x 180, de x 240 a 1016, línea base 284
resto = linea('avalie', 240, 1016, 180 / xh, 284)
# AUTOMOTRIZ: altura 80, de x 456 a 1016, línea base 376
auto = linea('AUTOMOTRIZ', 456, 1016, 80 / cap, 376)
# hoja en lugar de la tilde: caja x 952-1028, y 14-98
hoja = ('M956,96 C952,62 966,32 994,18 C1008,11 1018,12 1028,12 '
        'C1029,36 1022,62 1002,78 C990,88 974,94 956,96 Z')

VB = '8 4 1030 382'
def svg(cC, cR, cA, cH, defs=''):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{VB}" role="img" aria-label="Cavalié Automotriz">{defs}'
            f'<path fill="{cC}" d="{C}"/><path fill="{cR}" d="{resto}"/>'
            f'<path fill="{cA}" d="{auto}"/><path fill="{cH}" d="{hoja}"/></svg>')

g = ('<defs><linearGradient id="v" x1="0" y1="0" x2="0" y2="1">'
     '<stop offset="0" stop-color="#6BB138"/><stop offset="1" stop-color="#3E8E2C"/></linearGradient></defs>')
open('web/img/logo-cavalie.svg', 'w').write(svg('url(#v)', '#0E1A6E', '#0E1A6E', 'url(#v)', g))
open('web/img/logo-cavalie-blanco.svg', 'w').write(svg('#B9E07A', '#FFFFFF', '#FFFFFF', '#B9E07A'))
print('ok', 'xh', xh, 'cap', cap)
