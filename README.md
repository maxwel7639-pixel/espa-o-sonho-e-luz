# Espaço Terapêutico Sonho e Luz

No ar: <https://espa-o-sonho-e-luz.vercel.app/>

Site institucional da **Mara Nunes** — Constelação Familiar, Terapia Sistêmica e terapias
integrativas. Canoas/RS, atendimento presencial e online.

HTML/CSS/JS estático, sem build e sem dependências. Basta servir a pasta.

## Rodar localmente

```bash
python -m http.server 8899
# abre http://127.0.0.1:8899
```

## Estrutura

```
index.html            página única
assets/css/style.css  paleta, layout e responsivo
assets/js/main.js     menu mobile, acordeão do FAQ e revelação no scroll
assets/img/           fotos reais do espaço, dos grupos e da Mara
```

## Decisões de design

**Paleta** extraída das peças reais do Instagram da Mara (`@espacosonhoeluz`), não escolhida
no olho: vinho `#5E2340`, roxo ameixa `#2E1226`, lilás `#B897B1` e dourado `#C9A063` como
acento. Os neutros quentes (`#F8F3ED`, `#EFE4DA`) vêm da luz das fotos do espaço.

**Tipografia**: Cormorant Garamond (títulos) + Public Sans (texto). Serifada de traço fino
para o tom espiritual, sem a frieza de uma grotesca genérica nos títulos.

**Estrutura**: capítulos numerados em vez do padrão hero → features → CTA. A página é lida
como uma matéria — número do capítulo, olho, capitular, pull-quote, ficha técnica do
encontro, trilha de passos, bento de terapias com foto real de fundo, mural de depoimentos e
mosaico do espaço.

## Conteúdo

Todo o conteúdo vem de material real: fotos do espaço, prints das avaliações do Google
(5,0 · 7 avaliações), depoimentos recebidos por WhatsApp/Facebook/Instagram e as artes de
divulgação do Instagram. Os textos de constelação foram escritos a partir das próprias
frases da Mara nos posts.

## Pontos a confirmar com a cliente

- **Telefone**: o site usa `5551984540487` (o que aparece no Google Maps e nas artes mais
  recentes). Alguns posts antigos trazem `(51) 98973-5015` — confirmar qual é o canal ativo.
- **Domínio**: no ar em <https://espa-o-sonho-e-luz.vercel.app/>. As tags `og:url`,
  `canonical`, `og:image` e o JSON-LD já apontam para esse endereço. Se um dia entrar um
  domínio próprio, é só trocar essas quatro URLs — sem isso a prévia do link no
  WhatsApp/Instagram não carrega a imagem.
