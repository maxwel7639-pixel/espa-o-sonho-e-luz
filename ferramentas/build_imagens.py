"""
Reprocessa os assets do site a partir dos originais do zip.

As fontes são pequenas (fotos de ~525x350, recortes da grade do Instagram de ~200px).
Ampliar não inventa detalhe — então o ganho real de qualidade vem de:

  1. ampliar UMA vez só, com LANCZOS, até no máximo o que a fonte aguenta
     (em vez de ampliar aqui e deixar o browser ampliar de novo por cima);
  2. suavizar de leve o ruído de bloco ANTES de ampliar, quando a fonte é
     um recorte de screenshot já comprimido — senão o LANCZOS amplia o artefato;
  3. devolver acutância com máscara de nitidez DEPOIS de ampliar;
  4. gravar em 4:4:4 (sem subamostragem de cor), porque as fotos têm parede
     verde, sofá vermelho e dourado — bordas coloridas que o 4:2:0 borra;
  5. gerar WebP ao lado do JPEG, para poder subir a qualidade sem subir o peso.

Uso:  python build_imagens.py <pasta-de-saida>
"""
import os
import sys
from PIL import Image, ImageFilter

FONTE = "espa+ºo sonho e luz/"
WA = "WhatsApp Image 2026-08-24 at 15.55.45.jpeg"

# nome de saída -> (arquivo fonte, recorte ou None, largura alvo, fonte_comprimida)
# A largura alvo é ~2x o maior tamanho de exibição medido no layout, limitada
# pelo que a fonte suporta sem virar mingau.
MANIFESTO = {
    # --- recortes da grade do Instagram (fontes minúsculas e já comprimidas) ---
    "circulo-pes":      ("imagem-19.png", (1124, 545, 1316, 776), 620, True),
    "grupo-01":         ("imagem-19.png", (712, 530, 912, 776), 640, True),
    "grupo-02":         ("imagem-18.png", (927, 385, 1127, 624), 620, True),
    "grupo-03":         ("imagem-18.png", (1328, 656, 1528, 888), 620, True),
    "grupo-04":         ("imagem-18.png", (520, 656, 720, 888), 620, True),

    # --- fotos do espaço ---
    "sala-constelacao": ("imagem-04.png", None, 912, False),
    "sala-vivencia":    ("imagem-03.png", None, 762, False),
    "sala-massagem":    ("imagem-06.png", None, 762, False),
    "recepcao":         ("imagem-08.png", None, 1260, False),
    "sala-lilas":       ("imagem-07.png", None, 762, False),
    "maca-lotus":       ("imagem-05.png", None, 1118, False),
    "mara-ritual":      ("imagem-02.png", None, 1030, False),
    # recortado na caixa do círculo já embutido na foto — o CSS fecha em
    # border-radius:50% e descarta os cantos escuros que vieram colados
    "mara-retrato":     (WA, (76, 18, 734, 676), 840, False),

    # --- fundos dos cards de terapia (recortados acima do texto e do logo) ---
    "t-sistemica":      ("imagem-11.png", (30, 248, 468, 424), 1050, False),
    "t-reflexologia":   ("imagem-10.png", (224, 240, 442, 396), 700, False),
    "t-fitoterapia":    ("imagem-14.png", (60, 250, 450, 368), 1000, False),
}


def preparar(im, alvo_w, comprimida):
    escala = alvo_w / im.width

    # Fonte comprimida ampliada mais que ~1.6x: o LANCZOS realça o quadriculado
    # do JPEG junto com o detalhe. Um borrão mínimo antes derruba o artefato
    # sem comer a estrutura da imagem.
    if comprimida and escala > 1.6:
        im = im.filter(ImageFilter.GaussianBlur(0.4))

    if escala != 1:
        im = im.resize((alvo_w, round(im.height * escala)), Image.LANCZOS)

    # Quanto mais se ampliou, mais acutância se perdeu — devolve na medida.
    if escala <= 1.05:
        forca = 55
    elif escala <= 1.8:
        forca = 95
    elif escala <= 2.6:
        forca = 130
    else:
        forca = 155
    return im.filter(ImageFilter.UnsharpMask(radius=1.1, percent=forca, threshold=3))


def gravar(im, destino_sem_ext):
    jpg = destino_sem_ext + ".jpg"
    webp = destino_sem_ext + ".webp"
    # subsampling=0 => 4:4:4, sem borrar bordas coloridas
    im.save(jpg, quality=93, subsampling=0, optimize=True, progressive=True)
    im.save(webp, quality=86, method=6)
    return os.path.getsize(jpg), os.path.getsize(webp)


def main():
    saida = sys.argv[1].rstrip("/\\") + os.sep
    total_j = total_w = 0
    print(f"{'arquivo':<20}{'fonte':>11}{'saida':>12}{'escala':>8}{'jpg':>9}{'webp':>9}")
    for nome, (arq, corte, alvo, comp) in MANIFESTO.items():
        caminho = arq if arq == WA else FONTE + arq
        im = Image.open(caminho).convert("RGB")
        if corte:
            im = im.crop(corte)
        orig = im.size
        im = preparar(im, alvo, comp)
        j, w = gravar(im, saida + nome)
        total_j += j
        total_w += w
        print(f"{nome:<20}{f'{orig[0]}x{orig[1]}':>11}{f'{im.width}x{im.height}':>12}"
              f"{alvo / orig[0]:>7.1f}x{j // 1024:>8}K{w // 1024:>8}K")
    print(f"{'TOTAL':<20}{'':>11}{'':>12}{'':>8}{total_j // 1024:>8}K{total_w // 1024:>8}K")


if __name__ == "__main__":
    main()
