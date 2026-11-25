"""Hero com a foto original (081_1, lado direito) + fundo desfocado na cor do próprio fundo da foto."""
import subprocess, tempfile
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter
S = Path(__file__).resolve().parents[1]; R = S.parent / '_ref'
ESR = Path(r'C:/Users/dslru/Documents/L R G Z/Ferramentas/ferramentas/realesrgan')
im = Image.open(R / 'ig' / '081_DK-mvc2v-U2_1.jpg').convert('RGB'); W, H = im.size
# topo (faixa de texto do post) vem da versão limpa com LaMa (tools/hero_limpa.py), com emenda suave
lp = Image.open(R / 'hero-limpa.png').convert('RGB').resize((W, H))
g = np.zeros((H, W), np.float32); y1 = int(H * .105); g[:y1] = 1
g = np.asarray(Image.fromarray((g * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(H * .008))).astype(np.float32)[..., None] / 255
im = Image.fromarray((np.asarray(lp) * g + np.asarray(im) * (1 - g)).astype(np.uint8))
c = im.crop((int(W * .53), int(H * .03), W, H))
a = np.asarray(c).astype(float)
cor = np.median(a[:int(.25 * a.shape[0]), -int(.12 * a.shape[1]):].reshape(-1, 3), 0)
print('cor do fundo', '#%02x%02x%02x' % tuple(int(v) for v in cor), c.size)
with tempfile.TemporaryDirectory() as td:
    e, s = Path(td) / 'e.png', Path(td) / 's.png'; c.save(e)
    subprocess.run([str(ESR / 'realesrgan-ncnn-vulkan.exe'), '-i', str(e), '-o', str(s), '-n', 'realesrgan-x4plus', '-m', str(ESR / 'models')], check=True, capture_output=True)
    u = Image.open(s).convert('RGB')
u = u.resize((1200, int(u.height * 1200 / u.width)), Image.LANCZOS)
u.save(S / 'img' / 'hero-foto.webp', quality=86, method=6); print('foto', u.size)
