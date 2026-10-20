# Assets: real vs stock

## Real company material (shown as real on the site)
| File | What it shows | Source |
|---|---|---|
| source-photos/equipe-tshirt.webp → img/real/equipe-tshirt-* | Back of a team member, Viva Service24 t-shirt, on a solar roof | provided by the client |
| source-photos/solaire-toit-vegetal.webp → img/real/solaire-toit-vegetal-* | Team member cleaning solar panels on a green roof, pure-water pole | provided by the client |
| source-photos/vitres-vxv-barbers.webp → img/real/vitres-vxv-barbers-* | Cleaning the shop windows of vXv Barber's, Crissier (client who left a 5★ review) | provided by the client |
| video/real-*.mp4 + img/real/poster-* | 5 short videos: vXv Barber's windows (3), solar panels (2) | vivaservice24.ch, whose legal page states they show real interventions |
| img/ba/vitrine-avant / -apres | Before/after of the vXv Barber's window | two frames of video vitrine-1 (9.6 s and 15.1 s), aligned with a 4-point perspective transform and cropped. Nothing painted or retouched |
| img/brand/logo*.png | Logo | vivaservice24.ch |

## Original site images (img/original/)
All downloaded from vivaservice24.ch. logo.png and logo-white.png are the real logo. All photos are Unsplash stock (their own legal page says so): bail, chantier, conciergerie, entretien, jardin (American-looking, rejected), lausanne, solaire-card, speciaux, tags, vitres. hero-solaire-mobile.webp looks like a generated illustration: rejected.

## Stock (illustration only, never presented as their work)
Listed with source and author in CREDITS.md. The kitchen and bathroom before/after pairs are two different stock photos each, labelled "Photos d'illustration" on the page.

All stock was opened and checked by eye before use. Rejected: images with third-party branding (an "everdrop" bottle), American suburbs, posed models, derelict/abandoned bathrooms.

## Pipeline
`python3 tools/build_images.py` → AVIF + WebP, 2–3 widths each, used through `<picture>` with `srcset`/`sizes`, explicit width/height, lazy loading except the hero. Videos re-encoded with ffmpeg: hero 10 s, H.264 1.0 MB + WebM 0.46 MB (plus a 768 px version), real clips 0.2–1.4 MB.
