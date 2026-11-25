"""Vetoriza a logo principal PC (_ref/logo-principal.png: dourado com contorno escuro).
Gera img/logo.svg (duas cores, fiel à original) e img/mono.svg (silhueta lisa para adornos)."""
from pathlib import Path
import numpy as np, potrace
from PIL import Image, ImageFilter
from scipy import ndimage
S = Path(__file__).resolve().parents[1]
im = Image.open(S.parent / '_ref' / 'logo-principal.png').convert('RGBA')
im = im.resize((im.width * 4, im.height * 4), Image.LANCZOS)
a = np.asarray(im).astype(float)
al = np.asarray(Image.fromarray(a[..., 3].astype('uint8')).filter(ImageFilter.GaussianBlur(6))).astype(float)
lum = np.asarray(Image.fromarray((a[..., :3] @ [.3, .59, .11]).astype('uint8')).filter(ImageFilter.GaussianBlur(5))).astype(float)
def limpa(m, mn=3000):
    lab, n = ndimage.label(m); sz = ndimage.sum(m, lab, range(1, n + 1))
    return np.isin(lab, [i + 1 for i, s in enumerate(sz) if s > mn])
fora = limpa(al > 128)
ouro = limpa(fora & (lum > 120))
y, x = np.where(fora); x0, y0 = x.min() - 4, y.min() - 4; w, h = x.max() - x0 + 5, y.max() - y0 + 5
def d(mask):
    pl = potrace.Bitmap(~mask).trace(turdsize=400, alphamax=1.2, opticurve=True, opttolerance=.6)
    out = []
    for c in pl:
        s = c.start_point; p = f'M{s.x-x0:.1f} {s.y-y0:.1f}'
        for seg in c.segments:
            if seg.is_corner: p += f'L{seg.c.x-x0:.1f} {seg.c.y-y0:.1f}L{seg.end_point.x-x0:.1f} {seg.end_point.y-y0:.1f}'
            else: p += f'C{seg.c1.x-x0:.1f} {seg.c1.y-y0:.1f} {seg.c2.x-x0:.1f} {seg.c2.y-y0:.1f} {seg.end_point.x-x0:.1f} {seg.end_point.y-y0:.1f}'
        out.append(p + 'Z')
    return ''.join(out)
df, do = d(fora), d(ouro)
vb = f'viewBox="0 0 {w/4:.1f} {h/4:.1f}"'
def esc(p):  # volta à escala da original (1/4), mantendo 2 casas
    import re
    return re.sub(r'-?\d+\.\d', lambda m: f'{float(m.group())/4:.2f}', p)
df, do = esc(df), esc(do)
svg = lambda cor: f'<svg xmlns="http://www.w3.org/2000/svg" {vb} shape-rendering="geometricPrecision"><path fill="{cor}" fill-rule="evenodd" d="{df}"/></svg>'
(S / 'img' / 'logo.svg').write_text(svg('#a9834b'), encoding='utf-8')
(S / 'img' / 'logo-cl.svg').write_text(svg('#d6b986'), encoding='utf-8')
(S / 'img' / 'mono.svg').write_text(svg('#b8935a'), encoding='utf-8')
(S / 'img' / 'logo-2c.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" {vb} shape-rendering="geometricPrecision"><path fill="#2b2019" fill-rule="evenodd" d="{df}"/><path fill="#d6b986" fill-rule="evenodd" d="{do}"/></svg>', encoding='utf-8')
print(w, h, len(df), len(do))
