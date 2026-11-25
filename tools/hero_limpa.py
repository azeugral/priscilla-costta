"""Tira o texto do post 081_1 com LaMa (mantém a foto original com o fundo). Saída: _ref/hero-limpa.png"""
import numpy as np, cv2, onnxruntime as ort
from pathlib import Path
S = Path(__file__).resolve().parents[1]; R = S.parent / '_ref'
sess = ort.InferenceSession(r'C:/Users/dslru/Documents/L R G Z/Ferramentas/ferramentas/lama/lama_fp32.onnx')
img = cv2.imread(str(R / 'ig' / '081_DK-mvc2v-U2_1.jpg')); H, W = img.shape[:2]
g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(np.float32)
bgl = cv2.GaussianBlur(g, (0, 0), 25)
dark = (bgl - g) > 14
m = np.zeros((H, W), np.uint8)
xl = int(W * .545)
m[:, :xl][dark[:, :xl]] = 255
hy0, hy1 = int(H * .035), int(H * .09)
m[hy0:hy1, :int(W * .97)][dark[hy0:hy1, :int(W * .97)]] = 255
m[hy0:hy1, int(W*.02):int(W*.97)][np.abs(g[hy0:hy1, int(W*.02):int(W*.97)] - bgl[hy0:hy1, int(W*.02):int(W*.97)]) > 8] = 255
# botão "Arraste para o lado" inteiro
ys, xs = np.where(m[int(H*.6):int(H*.72), :xl] > 0)
m = cv2.dilate(m, np.ones((13, 13), np.uint8))
cv2.imwrite(str(R / '_mask.png'), m)
def tile(img, m, x0, y0, side):
    ci = img[y0:y0+side, x0:x0+side]; cm = m[y0:y0+side, x0:x0+side]
    if cm.max() == 0: return img
    a = cv2.resize(ci, (512, 512), interpolation=cv2.INTER_AREA)[..., ::-1].astype(np.float32) / 255
    b = (cv2.resize(cm, (512, 512), interpolation=cv2.INTER_NEAREST) > 127).astype(np.float32)
    a = a * (1 - b[..., None])
    out = sess.run(None, {'image': a.transpose(2, 0, 1)[None], 'mask': b[None, None]})[0][0].transpose(1, 2, 0)
    if out.max() <= 1.5: out = out * 255
    out = cv2.resize(np.clip(out, 0, 255).astype(np.uint8)[..., ::-1], (side, side), interpolation=cv2.INTER_CUBIC)
    f = cv2.GaussianBlur(cm, (0, 0), 3).astype(np.float32)[..., None] / 255
    r = img.copy(); r[y0:y0+side, x0:x0+side] = (out * f + ci * (1 - f)).astype(np.uint8); return r
side = 780
for y0 in list(range(0, H - side, 450)) + [H - side]:
    img = tile(img, m, 0, y0, side)
img = tile(img, m, W - side, 0, side)
cv2.imwrite(str(R / 'hero-limpa.png'), img)
print(W, H)
