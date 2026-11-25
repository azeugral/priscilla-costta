"""Prepara o material da prévia a partir de _ref/ig. Uso: python -I tools/prep.py (de dentro de site/)"""
import subprocess, tempfile, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter
sys.stdout.reconfigure(encoding='utf-8')
S = Path(__file__).resolve().parents[1]; R = S.parent / '_ref' / 'ig'; O = S / 'img'
ESR = Path(r'C:/Users/dslru/Documents/L R G Z/Ferramentas/ferramentas/realesrgan')

def up(im):
    with tempfile.TemporaryDirectory() as td:
        e, s = Path(td) / 'e.png', Path(td) / 's.png'; im.save(e)
        subprocess.run([str(ESR / 'realesrgan-ncnn-vulkan.exe'), '-i', str(e), '-o', str(s), '-n', 'realesrgan-x4plus', '-m', str(ESR / 'models')], check=True, capture_output=True)
        return Image.open(s).convert('RGB')

def crop45(im, cx=.5, cy=.5, w=None):
    W, H = im.size; r = 4 / 5
    if W / H > r: nw, nh = int(H * r), H
    else: nw, nh = W, int(W / r)
    x = int(min(max(cx * W - nw / 2, 0), W - nw)); y = int(min(max(cy * H - nh / 2, 0), H - nh))
    return im.crop((x, y, x + nw, y + nh))

def save(im, name, w):
    h = int(im.height * w / im.width); im.resize((w, h), Image.LANCZOS).save(O / name, quality=84, method=6)

# --- logo (084, dourado sobre café) ---
a = Image.open(R / '084_DHoHm-vvlig.jpg').convert('RGB').crop((850, 1300, 1270, 1545))
up(a).save(S.parent / '_ref' / 'logo-x4.png')

# --- retrato do hero (081_1, blazer branco), recorte BiRefNet ---
from rembg import remove, new_session
ses = new_session('birefnet-general-lite')
p = Image.open(R / '081_DK-mvc2v-U2_1.jpg').convert('RGB'); W, H = p.size
p = p.crop((int(W * .47), int(H * .06), W, H))
p4 = up(p); p4 = p4.resize((p4.width // 2, p4.height // 2), Image.LANCZOS)
cut = remove(p4, session=ses)
cut.save(S.parent / '_ref' / 'retrato-hero.png')
bb = cut.getchannel('A').point(lambda v: 255 if v > 20 else 0).getbbox(); cut = cut.crop(bb)
cut.thumbnail((1100, 1600), Image.LANCZOS); cut.save(O / 'retrato.webp', quality=88, method=6)
print('retrato', cut.size)

# --- hero (101_1 Lisboa, foto original no quadro) ---
s = Image.open(R / '101_CxnPXPoOh0G_1.jpg').convert('RGB'); save(crop45(s, .5, .45), 'hero-foto.webp', 1100)
# --- trajetória (4:5) ---
G = [('040_DWWqAqvlj4y_1', .5, .4, 'posse'), ('040_DWWqAqvlj4y_2', .5, .5, 'abmcj'), ('102_CxgNsXvpqMz_3', .5, .5, 'lisboa'),
     ('021_DbBCBh0Jy0t', .5, .5, 'livro'), ('018_DbrnWRFu7nq', .5, .5, 'homenagem'), ('059_DSVKO-Ejqvz_6', .5, .55, 'palco'),
     ('003_DgBtaQehYGR', .62, .5, 'evento'), ('014_DcjtksaCTcB_2', .55, .5, 'fiema'), ('041_DWPDmJVicTM', .5, .4, 'socias'), ('064_DQwoChTDA27', .5, .55, 'escritorio')]
for f, cx, cy, n in G:
    im = Image.open(R / f'{f}.jpg').convert('RGB'); c = crop45(im, cx, cy)
    if c.width < 900: c = up(c)
    save(c, f't-{n}.webp', 900)
print('ok')
