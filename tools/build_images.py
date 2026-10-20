#!/usr/bin/env python3
"""Builds every optimized image used by the site.

Sources live in _src/ (gitignored: stock originals, video frames) and in
source-photos/ + img/original/ (committed). Output goes to img/real/,
img/stock/, img/ba/ and img/brand/ as AVIF + WebP at several widths.

Run:  python3 tools/build_images.py
"""
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "_src"
OUT = ROOT / "img"
manifest = {}


def load(path):
    im = Image.open(path)
    im = ImageOps.exif_transpose(im)
    return im.convert("RGB")


def crop_ratio(im, ratio, fx=0.5, fy=0.5):
    """Crop to width/height ratio, focal point fx/fy (0..1)."""
    w, h = im.size
    if w / h > ratio:
        nw = round(h * ratio)
        x = round((w - nw) * fx)
        return im.crop((x, 0, x + nw, h))
    nh = round(w / ratio)
    y = round((h - nh) * fy)
    return im.crop((0, y, w, y + nh))


def emit(im, group, name, widths, q_webp=72, q_avif=55):
    d = OUT / group
    d.mkdir(parents=True, exist_ok=True)
    w0, h0 = im.size
    done = []
    for w in widths:
        if w > w0:
            w = w0
        if w in done:
            continue
        done.append(w)
        h = round(h0 * w / w0)
        r = im.resize((w, h), Image.LANCZOS)
        r.save(d / f"{name}-{w}.webp", "WEBP", quality=q_webp, method=6)
        r.save(d / f"{name}-{w}.avif", "AVIF", quality=q_avif, speed=5)
    manifest[f"{group}/{name}"] = {"w": done, "ratio": [w0, h0]}
    kb = sum((d / f"{name}-{w}.webp").stat().st_size for w in done) // 1024
    print(f"{group}/{name:28s} {w0}x{h0} -> {done}  ({kb} KB webp total)")


# ---------- real company photos ----------
SP = ROOT / "source-photos"
emit(load(SP / "equipe-tshirt.webp"), "real", "equipe-tshirt", [1360, 960, 640])
emit(load(SP / "solaire-toit-vegetal.webp"), "real", "solaire-toit-vegetal", [574, 420])
emit(load(SP / "vitres-vxv-barbers.webp"), "real", "vitres-vxv-barbers", [574, 420])

# frames from the company's own videos (old site: "interventions réalisées par Viva Service24")
O = SRC / "orig"
for n in ["solaire-brosse", "solaire-toit", "vitrine-1", "vitrine-2", "vitrine-3"]:
    emit(load(O / f"{n}-poster.jpg"), "real", f"poster-{n}", [576, 400])

# ---------- before / after ----------
F = SRC / "frames"
after = load(F / "w_15.1.jpg")
before = Image.open(F / "wb.png").convert("RGB")  # w_9.6 warped onto w_15.1 (4-point homography)
box = (12, 0, 452, 330)  # sign + upper glass, same box on both
from PIL import ImageFilter
sharp = ImageFilter.UnsharpMask(radius=1.6, percent=70, threshold=2)
emit(before.crop(box).resize((660, 495), Image.LANCZOS).filter(sharp), "ba", "vitrine-avant", [660])
emit(after.crop(box).resize((660, 495), Image.LANCZOS).filter(sharp), "ba", "vitrine-apres", [660])

S = SRC / "stock"
k_dirty = load(S / "cuisiniere-sale.jpg").crop((40, 330, 1160, 1170))
k_clean = load(S / "cuisiniere-propre.jpg").crop((250, 0, 1750, 1124))
emit(k_dirty.resize((1500, 1125), Image.LANCZOS), "ba", "cuisine-avant", [1200, 800])
emit(k_clean.resize((1500, 1125)), "ba", "cuisine-apres", [1200, 800])
b_dirty = load(S / "p10473680.jpg").crop((0, 1000, 2000, 2500))
b_clean = load(S / "p7664072.jpg").crop((0, 900, 2000, 2400))
emit(b_dirty, "ba", "sdb-avant", [1200, 800])
emit(b_clean, "ba", "sdb-apres", [1200, 800])

# ---------- stock (service illustrations) ----------
stock = {
    # name: (file, ratio, fx, fy, widths)
    "appart-vide": ("appart-vide.jpg", 3 / 2, 0.5, 0.5, [1600, 1200, 800]),
    "appart-vide-2": ("appart-vide-2.jpg", 4 / 3, 0.5, 0.5, [1200, 800]),
    "four-grille": ("four-grille.jpg", 4 / 5, 0.5, 0.45, [900, 600]),
    "douche": ("douche.jpg", 4 / 5, 0.5, 0.42, [900, 600]),
    "sdb-vapeur": ("sdb-vapeur.jpg", 4 / 3, 0.6, 0.5, [1200, 800]),
    "evier": ("evier-2.jpg", 4 / 3, 0.5, 0.5, [1200, 800]),
    "vitre-raclette": ("vitre-raclette.jpg", 4 / 5, 0.5, 0.55, [900, 600]),
    "vitre-chiffon": ("vitre-chiffon.jpg", 4 / 5, 0.5, 0.45, [900, 600]),
    "bureau": ("bureau.jpg", 4 / 3, 0.62, 0.5, [1600, 1200, 800]),
    "escalier": ("escalier.jpg", 4 / 5, 0.5, 0.55, [900, 600]),
    "chantier": ("chantier.jpg", 3 / 2, 0.5, 0.5, [1600, 1200, 800]),
    "immeuble": ("immeuble.jpg", 3 / 2, 0.3, 0.5, [1600, 1200, 800]),
    "haie": ("haie.jpg", 4 / 3, 0.5, 0.5, [1200, 800]),
    "tags": ("tags.jpg", 4 / 3, 0.5, 0.5, [1200, 800]),
    "tags-karcher": ("tags-karcher.jpg", 4 / 3, 0.62, 0.5, [1200, 800]),
    "lausanne": ("lausanne-ouchy.jpg", 16 / 9, 0.5, 0.55, [1800, 1200, 800]),
}
for name, (f, ratio, fx, fy, widths) in stock.items():
    emit(crop_ratio(load(S / f), ratio, fx, fy), "stock", name, widths)

# hero backgrounds of the landing pages (sit under a navy overlay)
heroes = {
    "hero-vitres": ("vitre-raclette.jpg", 0.5, 0.62),
    "hero-solaire": ("solaire-toit.jpg", 0.5, 0.6),
    "hero-chantier": ("chantier.jpg", 0.5, 0.5),
    "hero-immeuble": ("immeuble.jpg", 0.3, 0.5),
}
for name, (f, fx, fy) in heroes.items():
    emit(crop_ratio(load(S / f), 16 / 9, fx, fy), "stock", name, [1600, 1000, 640], q_webp=64, q_avif=46)

OR = ROOT / "img" / "original"

# hero poster (frame of the hero video)
hp = load(SRC / "hero-poster.jpg")
emit(hp, "stock", "hero-poster", [1600, 1280, 768], q_webp=66, q_avif=48)

# ---------- brand ----------
B = OUT / "brand"
B.mkdir(exist_ok=True)
for n in ["logo", "logo-white"]:
    im = Image.open(OR / f"{n}.png").convert("RGBA")
    im.save(B / f"{n}.webp", "WEBP", quality=90, method=6)
    im.resize((221, 120), Image.LANCZOS).save(B / f"{n}-221.png", optimize=True)
    im.save(B / f"{n}.png", optimize=True)

(ROOT / "tools" / "images.json").write_text(json.dumps(manifest, indent=1))
print("manifest written")
