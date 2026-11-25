"""Logo do rodapé: _ref/logo-original.png com a borda escurecida (7%) e margem preta de 30%, usada com mix-blend-mode:screen."""
import numpy as np
from pathlib import Path
from PIL import Image
S = Path(__file__).resolve().parents[1]
lg = np.asarray(Image.open(S.parent / '_ref' / 'logo-original.png').convert('RGB')).astype(float); h, w = lg.shape[:2]
y, x = np.mgrid[0:h, 0:w]; d = np.minimum.reduce([x, w - 1 - x, y, h - 1 - y]).astype(float)
v = np.clip(d / (.07 * min(w, h)), 0, 1); v = v * v * (3 - 2 * v)
cv = Image.new('RGB', (int(w * 1.3), int(h * 1.3))); cv.paste(Image.fromarray((lg * v[..., None]).astype(np.uint8)), ((cv.width - w) // 2, (cv.height - h) // 2))
cv.resize((1600, int(cv.height * 1600 / cv.width)), Image.LANCZOS).save(S / 'img' / 'logo.webp', quality=88, method=6)
