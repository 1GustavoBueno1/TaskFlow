# Mídia da landing (Higgsfield)

Estes arquivos são **opcionais** — a landing roda sem eles (fallback em gradiente/cor).
Só são usados na página pública `/` (index.html). O dashboard fica limpo, sem vídeo pesado.

Coloque os arquivos aqui com **exatamente** estes nomes:

| Slot                         | Arquivo            | Se faltar (fallback)                    |
|------------------------------|--------------------|-----------------------------------------|
| Vídeo do hero (mudo, ~6–10s) | `hero-loop.mp4`    | Gradiente animado CSS (`.lp-hero-bg`)   |
| Poster do hero               | `hero-poster.jpg`  | Cor sólida / gradiente da paleta        |
| Fundo da seção "metas"       | `section-1.jpg`    | Gradiente do `.lp-feature`              |

Recomendações:
- Vídeo: 1920×1080, H.264/MP4, **mudo**, loop curto, < ~4 MB (peso importa no LCP).
- Imagens: 1920×1080 ou maior, JPG/WEBP otimizado.
- Como são servidos pelo Flask static, ficam em `/static/media/<arquivo>`
  (o template usa `url_for('static', filename='media/...')`).
