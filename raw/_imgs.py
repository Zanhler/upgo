# fotos reais do Instagram e do Maps -> img/*.webp; tira o texto queimado das 2 fotos do tecido
import os, cv2, numpy as np
from PIL import Image, ImageOps
R = os.path.dirname(os.path.abspath(__file__)); H = R + "/hi/"; M = R + "/maps/"; V = R + "/video/"; O = R + "/../img/"
def limpa(arq, caixa, saida):
    im = cv2.imread(H + arq); x0, y0, x1, y1 = caixa; g = im[y0:y1, x0:x1]
    hsv = cv2.cvtColor(g, cv2.COLOR_BGR2HSV)
    txt = ((hsv[..., 2] > 120) & (hsv[..., 1] < 70)) | ((hsv[..., 0] > 100) & (hsv[..., 0] < 125) & (hsv[..., 1] > 120) & (hsv[..., 2] > 110))
    m = np.zeros(im.shape[:2], np.uint8); m[y0:y1, x0:x1] = txt.astype(np.uint8) * 255
    m = cv2.dilate(m, np.ones((15, 15), np.uint8))
    out = cv2.inpaint(im, m, 9, cv2.INPAINT_TELEA)
    Image.fromarray(cv2.cvtColor(out, cv2.COLOR_BGR2RGB)).save(O + saida, quality=84); return out
limpa("DfVBRclodb9_1.jpg", (55, 280, 505, 530), "tecido-ponte.webp")
limpa("DfVBRclodb9_0.jpg", (25, 690, 470, 980), "tecido-invertida.webp")
pares = {H+"DfCJrakkSTi_0.jpg":"arco-dupla", H+"DfCJrakkSTi_1.jpg":"arco", H+"Dez7OriuxNl_0.jpg":"invertida-cadillac", H+"De1pm49RUIG_0.jpg":"turma-barrel",
         M+"f_00.jpg":"estudio", M+"f_01.jpg":"bola-cadillac", M+"f_04.jpg":"parada-parede", M+"f_05.jpg":"barrel-alongamento", M+"f_06.jpg":"barrel", M+"f_08.jpg":"cadillac", M+"f_09.jpg":"reformer", M+"f_10.jpg":"tecido-aluna", M+"f_11.jpg":"invertida-parede"}
for f, n in pares.items():
    im = ImageOps.exif_transpose(Image.open(f)).convert("RGB"); im.thumbnail((1400, 1400)); im.save(O + n + ".webp", quality=82); print(n, im.size)
# capas dos reels e cópia dos vídeos
nomes = {"Dej_1z9xC5z":"desafios","De_492HRib_":"reformer","DfZ1rtKuXjj":"bola","DeNTygVOdkJ":"temos-desafio","DfF2319OWDh":"turma","DeZYz_0RAz5":"hollywood"}
for k, n in nomes.items():
    c = cv2.VideoCapture(V + k + ".mp4"); t = int(c.get(7)); c.set(1, int(t * .5)); ok, f = c.read()
    Image.fromarray(cv2.cvtColor(f, cv2.COLOR_BGR2RGB)).save(O + "reel-" + n + ".webp", quality=78)
    open(R + "/../video/" + n + ".mp4", "wb").write(open(V + k + ".mp4", "rb").read())
# frames para escolha: turma no tapete e instrutora observando
c = cv2.VideoCapture(V + "DfF2319OWDh.mp4"); c.set(1, int(c.get(7) * .12)); ok, f = c.read(); Image.fromarray(cv2.cvtColor(f, cv2.COLOR_BGR2RGB)).save(O + "turma-tapete.webp", quality=82)
c = cv2.VideoCapture(V + "DeZYz_0RAz5.mp4"); c.set(1, int(c.get(7) * .6)); ok, f = c.read(); h = f.shape[0]; Image.fromarray(cv2.cvtColor(f[int(h*.17):], cv2.COLOR_BGR2RGB)).save(O + "instrutora.webp", quality=82)
d = Image.open(H + "DePJPkbx491_0.jpg"); W, Hh = d.size; d.crop((int(W*.42), int(Hh*.30), W, int(Hh*.78))).save(R + "/_mandala_crop.jpg", quality=85); print(d.size)
