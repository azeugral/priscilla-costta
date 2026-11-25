"""Foto do Quem é: _ref/sobre-escadaria.webp inteira (sem recorte), Real-ESRGAN x4 e reduzida a 1300 de largura."""
import subprocess, tempfile
from pathlib import Path
from PIL import Image
S = Path(__file__).resolve().parents[1]
ESR = Path(r'C:/Users/dslru/Documents/L R G Z/Ferramentas/ferramentas/realesrgan')
with tempfile.TemporaryDirectory() as t:
    e, s = Path(t) / 'e.png', Path(t) / 's.png'
    Image.open(S.parent / '_ref' / 'sobre-escadaria.webp').convert('RGB').save(e)
    subprocess.run([str(ESR / 'realesrgan-ncnn-vulkan.exe'), '-i', str(e), '-o', str(s), '-n', 'realesrgan-x4plus', '-m', str(ESR / 'models')], check=True, capture_output=True)
    im = Image.open(s).convert('RGB')
    im = im.resize((1300, round(1300 * im.height / im.width)), Image.LANCZOS)
    im.save(S / 'img' / 'sobre.webp', quality=86, method=6)
    print(im.size)
