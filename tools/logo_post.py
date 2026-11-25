"""Vetoriza o monograma PC e o nome a partir de _ref/logo-x4.png (dourado sobre café)."""
import sys; sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
import numpy as np, potrace
from PIL import Image, ImageFilter
S = Path(__file__).resolve().parents[1]
im = Image.open(S.parent / '_ref' / 'logo-x4.png').convert('RGB').filter(ImageFilter.GaussianBlur(1.2))
a = np.asarray(im).astype(float); lum = a @ [.3, .59, .11]
m = lum > 105
m[:, :int(.04 * m.shape[1])] = False  # tira a quina dourada da esquerda
from scipy import ndimage
lab, n = ndimage.label(m); sz = ndimage.sum(m, lab, range(1, n + 1))
m = np.isin(lab, [i + 1 for i, s in enumerate(sz) if s > 400])
def paths(mask, ox, oy):
    bm = potrace.Bitmap(~mask); pl = bm.trace(turdsize=20, alphamax=1.0, opticurve=True, opttolerance=.2)
    out = []
    for c in pl:
        s = c.start_point; d = f'M{s.x-ox:.1f} {s.y-oy:.1f}'
        for seg in c.segments:
            if seg.is_corner: d += f'L{seg.c.x-ox:.1f} {seg.c.y-oy:.1f}L{seg.end_point.x-ox:.1f} {seg.end_point.y-oy:.1f}'
            else: d += f'C{seg.c1.x-ox:.1f} {seg.c1.y-oy:.1f} {seg.c2.x-ox:.1f} {seg.c2.y-oy:.1f} {seg.end_point.x-ox:.1f} {seg.end_point.y-oy:.1f}'
        out.append(d + 'Z')
    return ''.join(out)
ys, xs = np.where(m); H = m.shape[0]
# monograma: tudo acima de 55% da altura
mono = m.copy(); mono[int(.55 * H):] = False
nome = m.copy(); nome[:int(.55 * H)] = False
for nm, mk in [("mono", mono)]:
    y, x = np.where(mk); x0, x1, y0, y1 = x.min(), x.max(), y.min(), y.max()
    d = paths(mk, x0 - 2, y0 - 2); w, h = x1 - x0 + 4, y1 - y0 + 4
    (S / 'img' / f'{nm}.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}"><path fill="#b8935a" fill-rule="evenodd" d="{d}"/></svg>', encoding='utf-8')
    print(nm, w, h, len(d))
