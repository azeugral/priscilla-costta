"""Vetoriza a logo principal PC (_ref/logo-principal.png: dourado com contorno escuro).
Gera img/logo.svg (duas cores, fiel à original) e img/mono.svg (silhueta lisa para adornos)."""
from pathlib import Path
import numpy as np, potrace
from PIL import Image, ImageFilter
from scipy import ndimage
S = Path(__file__).resolve().parents[1]
im = Image.open(S.parent / '_ref' / 'logo-principal.png').convert('RGBA')
im = im.resize((im.width * 2, im.height * 2), Image.LANCZOS)
a = np.asarray(im).astype(float)
al = np.asarray(Image.fromarray(a[..., 3].astype('uint8')).filter(ImageFilter.GaussianBlur(1.5))).astype(float)
lum = np.asarray(Image.fromarray((a[..., :3] @ [.3, .59, .11]).astype('uint8')).filter(ImageFilter.GaussianBlur(1.5))).astype(float)
def limpa(m, mn=300):
    lab, n = ndimage.label(m); sz = ndimage.sum(m, lab, range(1, n + 1))
    return np.isin(lab, [i + 1 for i, s in enumerate(sz) if s > mn])
fora = limpa(al > 128)
ouro = limpa(fora & (lum > 120))
y, x = np.where(fora); x0, y0 = x.min() - 4, y.min() - 4; w, h = x.max() - x0 + 5, y.max() - y0 + 5
def d(mask):
    pl = potrace.Bitmap(~mask).trace(turdsize=30, alphamax=1.0, opticurve=True, opttolerance=.2)
    out = []
    for c in pl:
        s = c.start_point; p = f'M{s.x-x0:.1f} {s.y-y0:.1f}'
        for seg in c.segments:
            if seg.is_corner: p += f'L{seg.c.x-x0:.1f} {seg.c.y-y0:.1f}L{seg.end_point.x-x0:.1f} {seg.end_point.y-y0:.1f}'
            else: p += f'C{seg.c1.x-x0:.1f} {seg.c1.y-y0:.1f} {seg.c2.x-x0:.1f} {seg.c2.y-y0:.1f} {seg.end_point.x-x0:.1f} {seg.end_point.y-y0:.1f}'
        out.append(p + 'Z')
    return ''.join(out)
df, do = d(fora), d(ouro)
vb = f'viewBox="0 0 {w} {h}"'
(S / 'img' / 'logo.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" {vb}><path fill="#2b2019" fill-rule="evenodd" d="{df}"/><path fill="#d6b986" fill-rule="evenodd" d="{do}"/></svg>', encoding='utf-8')
(S / 'img' / 'mono.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" {vb}><path fill="#b8935a" fill-rule="evenodd" d="{df}"/></svg>', encoding='utf-8')
print(w, h, len(df), len(do))
