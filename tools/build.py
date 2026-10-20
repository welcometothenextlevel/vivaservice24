#!/usr/bin/env python3
"""Generates every HTML page of the Viva Service24 site, plus sitemap.xml and robots.txt.

The output is plain static HTML that works on its own (no build step is needed to run
the site). This script only exists so the shared parts (header, form, reviews, footer)
stay identical on every page. Edit the texts here, then run:

    python3 tools/build.py

All links are relative, so the site works in the GitHub Pages subfolder
(https://<user>.github.io/vivaservice24/) as well as on its own domain.
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE_URL = "https://welcometothenextlevel.github.io/vivaservice24/"  # change when the site moves to vivaservice24.ch
V = "7"  # cache-busting version for css/js

IMG = json.loads((ROOT / "tools" / "images.json").read_text())

PHONE = "076 741 25 27"
PHONE_NB = "076 741 25 27"
TEL = "tel:+41767412527"
EMAIL = "info@vivaservice24.ch"
WA = "https://wa.me/41767412527?text="
GOOGLE = "https://www.google.com/maps/search/?api=1&query=Entreprise%20de%20nettoyage%20VIVA%20service24%20Crissier"
TOWNS = ["Lausanne", "Renens", "Crissier", "Ecublens", "Prilly", "Bussigny", "Morges", "Pully", "Lutry",
         "Epalinges", "Le Mont-sur-Lausanne", "Cheseaux-sur-Lausanne", "Chavannes-près-Renens"]


def wa(text):
    return WA + re.sub(r"[^A-Za-z0-9\-_.~]", lambda m: "".join("%%%02X" % b for b in m.group(0).encode()), text)


def esc(s):
    return html.escape(s, quote=True)


# ------------------------------------------------------------------ images
def pic(rel, key, alt, sizes, cls="", eager=False, ratio=None, extra=""):
    info = IMG[key]
    ws = info["w"]
    w0, h0 = info["ratio"]
    base = f"{rel}img/{key}"
    avif = ", ".join(f"{base}-{w}.avif {w}w" for w in ws)
    webp = ", ".join(f"{base}-{w}.webp {w}w" for w in ws)
    big = max(ws)
    h = round(h0 * big / w0)
    load = 'fetchpriority="high" decoding="async"' if eager else 'loading="lazy" decoding="async"'
    c = f' class="{cls}"' if cls else ""
    return (f'<picture><source type="image/avif" srcset="{avif}" sizes="{sizes}">'
            f'<img src="{base}-{min(ws, key=lambda w: abs(w - 800))}.webp" srcset="{webp}" sizes="{sizes}" '
            f'width="{big}" height="{h}" alt="{esc(alt)}" {load}{c}{extra}></picture>')


def ic(name, cls="ic"):
    return f'<svg class="{cls}" aria-hidden="true"><use href="#i-{name}"></use></svg>'


STARS = '<span class="stars" aria-hidden="true">' + "".join(
    '<svg viewBox="0 0 24 24"><use href="#i-star"></use></svg>' for _ in range(5)) + "</span>"


# ------------------------------------------------------------------ sprite
SPRITE = """<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false">
<defs>
<symbol id="i-phone" viewBox="0 0 24 24"><path d="M6.6 3.8h2.6l1.5 3.9-1.9 1.2a10.6 10.6 0 0 0 5.3 5.3l1.2-1.9 3.9 1.5v2.6a2 2 0 0 1-2.1 2A14.6 14.6 0 0 1 4.6 5.9a2 2 0 0 1 2-2.1z"/></symbol>
<symbol id="i-wa" viewBox="0 0 24 24"><path stroke="none" fill="currentColor" d="M12.04 2.5a9.43 9.43 0 0 0-8.1 14.24L2.6 21.5l4.88-1.28a9.43 9.43 0 1 0 4.56-17.72zm0 17.26a7.8 7.8 0 0 1-3.98-1.09l-.29-.17-2.9.76.78-2.83-.19-.3a7.82 7.82 0 1 1 6.58 3.63zm4.29-5.86c-.24-.12-1.4-.69-1.61-.77-.22-.08-.38-.12-.54.12-.16.24-.62.77-.76.93-.14.16-.28.18-.52.06-.24-.12-1-.37-1.91-1.18-.7-.63-1.18-1.41-1.32-1.65-.14-.24-.01-.37.1-.49.11-.11.24-.28.36-.42.12-.14.16-.24.24-.4.08-.16.04-.3-.02-.42-.06-.12-.54-1.3-.74-1.78-.2-.47-.4-.4-.54-.41h-.46a.89.89 0 0 0-.64.3 2.7 2.7 0 0 0-.84 2c0 1.18.86 2.32.98 2.48.12.16 1.69 2.58 4.1 3.62.57.25 1.02.4 1.37.51.58.18 1.1.16 1.52.1.46-.07 1.4-.57 1.6-1.13.2-.55.2-1.03.14-1.13-.06-.1-.22-.16-.46-.28z"/></symbol>
<symbol id="i-check" viewBox="0 0 24 24"><path d="M5 12.6l4.3 4.2L19 7.2"/></symbol>
<symbol id="i-clock" viewBox="0 0 24 24"><circle cx="12" cy="12" r="8.6"/><path d="M12 7.4V12l3.1 2"/></symbol>
<symbol id="i-pin" viewBox="0 0 24 24"><path d="M12 21.2s-6.6-5.7-6.6-11.1a6.6 6.6 0 0 1 13.2 0c0 5.4-6.6 11.1-6.6 11.1z"/><circle cx="12" cy="10.1" r="2.4"/></symbol>
<symbol id="i-mail" viewBox="0 0 24 24"><rect x="3.4" y="5.4" width="17.2" height="13.2" rx="2"/><path d="M4.2 7.2l7.8 6 7.8-6"/></symbol>
<symbol id="i-arrow" viewBox="0 0 24 24"><path d="M4.8 12h14.2M13.4 6.2l5.8 5.8-5.8 5.8"/></symbol>
<symbol id="i-chev" viewBox="0 0 24 24"><path d="M6.4 9.2l5.6 5.6 5.6-5.6"/></symbol>
<symbol id="i-back" viewBox="0 0 24 24"><path d="M19.2 12H5M10.6 6.2L4.8 12l5.8 5.8"/></symbol>
<symbol id="i-star" viewBox="0 0 24 24"><path stroke="none" fill="currentColor" d="M12 2.9l2.8 5.8 6.3.9-4.6 4.4 1.1 6.3L12 17.3l-5.6 3 1.1-6.3-4.6-4.4 6.3-.9z"/></symbol>
<symbol id="i-cal" viewBox="0 0 24 24"><rect x="3.8" y="5.4" width="16.4" height="14.8" rx="2"/><path d="M3.8 10h16.4M8.4 3.4v4M15.6 3.4v4"/></symbol>
<symbol id="i-reply" viewBox="0 0 24 24"><path d="M5.2 5.2h13.6a1.6 1.6 0 0 1 1.6 1.6v8.6a1.6 1.6 0 0 1-1.6 1.6H10l-4.6 3.4V17H5.2a1.6 1.6 0 0 1-1.6-1.6V6.8a1.6 1.6 0 0 1 1.6-1.6z"/><path d="M7.6 9.6h8.8M7.6 12.8h5.4"/></symbol>
<symbol id="i-home" viewBox="0 0 24 24"><path d="M3.8 11.2L12 4.6l8.2 6.6M6.2 9.4v10.4h11.6V9.4M10 19.8v-5h4v5"/></symbol>
<symbol id="i-key" viewBox="0 0 24 24"><circle cx="8" cy="15.6" r="4.2"/><path d="M11 12.6l8.6-8.6M16.2 7.4l2.4 2.4M13.8 9.8l2 2"/></symbol>
<symbol id="i-camera" viewBox="0 0 24 24"><rect x="3.4" y="7" width="17.2" height="12.4" rx="2"/><circle cx="12" cy="13.2" r="3.4"/><path d="M8.6 7l1.6-2.6h3.6L15.4 7"/></symbol>
<symbol id="i-drop" viewBox="0 0 24 24"><path d="M12 3.4s6.2 6.5 6.2 10.8a6.2 6.2 0 0 1-12.4 0C5.8 9.9 12 3.4 12 3.4z"/><path d="M9.2 14.6a2.9 2.9 0 0 0 2.6 2.6"/></symbol>
<symbol id="i-spark" viewBox="0 0 24 24"><path d="M12 2.8c.7 4.8 2.6 6.7 7.4 7.4-4.8.7-6.7 2.6-7.4 7.4-.7-4.8-2.6-6.7-7.4-7.4 4.8-.7 6.7-2.6 7.4-7.4z"/><path d="M18.6 16.4c.3 1.7 1 2.4 2.6 2.6-1.7.3-2.4 1-2.6 2.6-.3-1.7-1-2.4-2.6-2.6 1.7-.2 2.4-.9 2.6-2.6z"/></symbol>
<symbol id="i-building" viewBox="0 0 24 24"><path d="M5 20.4V4.6h9.4v15.8M14.4 9.4H19v11M3.4 20.4h17.2"/><path d="M8 8h3.4M8 11.4h3.4M8 14.8h3.4"/></symbol>
<symbol id="i-window" viewBox="0 0 24 24"><rect x="4.2" y="3.6" width="15.6" height="16.8" rx="1.4"/><path d="M12 3.6v16.8M4.2 12h15.6"/></symbol>
<symbol id="i-solar" viewBox="0 0 24 24"><path d="M3.4 18.4l3.1-10.6h11l3.1 10.6z"/><path d="M4.9 13.2h14.2M10.1 7.8l-1.1 10.6M13.9 7.8l1.1 10.6M12 18.4v2.4M8.6 20.8h6.8"/></symbol>
<symbol id="i-helmet" viewBox="0 0 24 24"><path d="M3.6 17.2h16.8M5.2 17.2a6.8 6.8 0 0 1 13.6 0"/><path d="M10 10.6V7h4v3.6"/></symbol>
<symbol id="i-leaf" viewBox="0 0 24 24"><path d="M5.2 19.4c0-8.2 5-13.6 14-13.6 0 9.2-5.2 14.4-13.4 14.4"/><path d="M5.2 19.4l7.4-7.6"/></symbol>
<symbol id="i-spray" viewBox="0 0 24 24"><path d="M8 9.4h5.6v11H8zM9.2 9.4V6.6h3.2v2.8M12.4 6.6h2.2M17 5.2h.01M19.2 7.4h.01M17 9.6h.01M19.2 3h.01"/></symbol>
<symbol id="i-play" viewBox="0 0 24 24"><path stroke="none" fill="currentColor" d="M8.4 5.6v12.8l10-6.4z"/></symbol>
<symbol id="i-pause" viewBox="0 0 24 24"><path d="M9 6v12M15 6v12"/></symbol>
<symbol id="i-x" viewBox="0 0 24 24"><path d="M6.4 6.4l11.2 11.2M17.6 6.4L6.4 17.6"/></symbol>
<symbol id="i-g" viewBox="0 0 48 48"><path stroke="none" fill="#FFC107" d="M43.6 20.5H42V20H24v8h11.3C33.7 32.7 29.2 36 24 36c-6.6 0-12-5.4-12-12s5.4-12 12-12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 13 4 4 13 4 24s9 20 20 20 20-9 20-20c0-1.3-.1-2.4-.4-3.5z"/><path stroke="none" fill="#FF3D00" d="M6.3 14.7l6.6 4.8C14.7 15.1 19 12 24 12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 16.3 4 9.7 8.3 6.3 14.7z"/><path stroke="none" fill="#4CAF50" d="M24 44c5.2 0 9.9-2 13.4-5.2l-6.2-5.2A11.9 11.9 0 0 1 24 36c-5.2 0-9.6-3.3-11.3-8l-6.5 5C9.5 39.6 16.2 44 24 44z"/><path stroke="none" fill="#1976D2" d="M43.6 20.5H42V20H24v8h11.3a12 12 0 0 1-4.1 5.6l6.2 5.2C37 39.2 44 34 44 24c0-1.3-.1-2.4-.4-3.5z"/></symbol>
</defs></svg>"""

# ------------------------------------------------------------------ prices
BAIL_PRICES = [
    ("studio", "Studio", "dès CHF 350", "Studio ou 1 pièce"),
    ("2", "2 pièces", "CHF 450 à 590", "2 pièces"),
    ("3", "3 pièces", "CHF 580 à 750", "3 pièces"),
    ("4", "4 pièces", "CHF 750 à 950", "4 pièces"),
    ("5", "5+ pièces", "dès CHF 900", "5 pièces et plus"),
]

PRICE_NOTE = "Prix indicatifs, devis exact gratuit et sans engagement."
URGENCE = "Urgence et week-end : supplément de 20 à 50 %, indiqué dans le devis."

SERVICE_CHIPS = ["Fin de bail", "Vitres", "Panneaux solaires", "Fin de chantier", "Immeuble / bureau", "Autre"]
ROOMS = ["Studio", "2", "2.5", "3", "3.5", "4", "4.5", "5+"]

# ------------------------------------------------------------------ head
LOCAL_BUSINESS = {
    "@context": "https://schema.org",
    "@type": ["LocalBusiness", "HomeAndConstructionBusiness"],
    "@id": BASE_URL + "#entreprise",
    "name": "Viva Service24",
    "alternateName": "Entreprise de nettoyage VIVA service24",
    "legalName": "Viva service24 Sàrl",
    "slogan": "Nettoyage & entretien technique",
    "url": BASE_URL,
    "logo": BASE_URL + "img/brand/logo.png",
    "image": BASE_URL + "img/real/equipe-tshirt-1360.webp",
    "telephone": "+41 76 741 25 27",
    "email": EMAIL,
    "priceRange": "CHF 45 à 950",
    "currenciesAccepted": "CHF",
    "address": {"@type": "PostalAddress", "streetAddress": "Rue du Jura 11", "postalCode": "1023",
                "addressLocality": "Crissier", "addressRegion": "VD", "addressCountry": "CH"},
    "geo": {"@type": "GeoCoordinates", "latitude": 46.5395, "longitude": 6.5783},
    "openingHoursSpecification": [{
        "@type": "OpeningHoursSpecification",
        "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        "opens": "00:00", "closes": "23:59"}],
    "areaServed": [{"@type": "City", "name": t} for t in TOWNS] + [
        {"@type": "AdministrativeArea", "name": "Canton de Vaud"}],
    "sameAs": [GOOGLE],
}


def head(p, rel):
    url = BASE_URL + p["path"]
    og = BASE_URL + "img/og-share.jpg"
    ld = [LOCAL_BUSINESS] + p.get("ld", [])
    ld_html = "\n".join(
        f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False, separators=(",", ":"))}</script>'
        for x in ld)
    preload = p.get("preload", "")
    critical = (ROOT / "css" / "critical.css").read_text()
    critical = re.sub(r"/\*[\s\S]*?\*/", "", critical)
    critical = re.sub(r"\s*\n\s*", "", critical)
    critical = critical.replace("url(../fonts/", f"url({rel}fonts/")
    robots = '<meta name="robots" content="noindex">' if p.get("noindex") else ""
    base_fix = p.get("base_fix", "")
    return f"""<!doctype html>
<html lang="fr-CH">
<head>
<meta charset="utf-8">
{base_fix}<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(p['title'])}</title>
<meta name="description" content="{esc(p['desc'])}">
{robots}<link rel="canonical" href="{url}">
<meta name="theme-color" content="#042448">
<meta property="og:type" content="website">
<meta property="og:locale" content="fr_CH">
<meta property="og:site_name" content="Viva Service24">
<meta property="og:title" content="{esc(p.get('og_title', p['title']))}">
<meta property="og:description" content="{esc(p['desc'])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Membre de l'équipe Viva Service24 en t-shirt de l'entreprise, sur un toit de panneaux solaires">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(p.get('og_title', p['title']))}">
<meta name="twitter:description" content="{esc(p['desc'])}">
<meta name="twitter:image" content="{og}">
<link rel="icon" href="{rel}favicon.ico" sizes="any">
<link rel="icon" href="{rel}img/brand/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{rel}img/brand/apple-touch-icon.png">
<link rel="manifest" href="{rel}site.webmanifest">
<link rel="preload" href="{rel}fonts/figtree-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{rel}fonts/instrument-sans-latin.woff2" as="font" type="font/woff2" crossorigin>
{preload}<style>{critical}</style>
<link rel="preload" href="{rel}css/site.css?v={V}" as="style" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link rel="stylesheet" href="{rel}css/site.css?v={V}"></noscript>
<script>document.documentElement.classList.add('js')</script>
{ld_html}
</head>
"""


# ------------------------------------------------------------------ header / footer
NAV = [("fin-de-bail/", "Fin de bail"), ("vitres/", "Vitres"), ("panneaux-solaires/", "Panneaux solaires"),
       ("fin-de-chantier/", "Fin de chantier"), ("entretien-immeubles/", "Immeubles et bureaux")]


NAV_SHORT = [("fin-de-bail/", "Fin de bail"), ("vitres/", "Vitres"), ("panneaux-solaires/", "Solaire"),
             ("fin-de-chantier/", "Chantier"), ("entretien-immeubles/", "Immeubles")]


def header(p, rel):
    home = f'{rel}' if rel else "./"
    nav = ""
    if not p.get("minimal"):
        nav = '<nav class="hd__nav" aria-label="Services"><ul>' + "".join(
            f'<li><a href="{rel}{href}">{label}</a></li>' for href, label in NAV_SHORT) + "</ul></nav>"
    return f"""<a class="skip" href="#contenu">Aller au contenu</a>
<header class="hd" data-header>
  <div class="hd__in container">
    <a class="hd__logo" href="{home}" aria-label="Viva Service24, accueil">
      <img src="{rel}img/brand/logo-221.png" srcset="{rel}img/brand/logo-221.png 221w, {rel}img/brand/logo.png 442w" sizes="110px" width="221" height="120" alt="Viva Service24">
    </a>
    {nav}
    <div class="hd__act">
      <span class="live"><i class="live__dot"></i>Disponible 7j/7</span>
      <a class="btn btn--ghost hd__tel" href="{TEL}">{ic('phone')}<span>{PHONE_NB}</span></a>
      <a class="hd__call" href="{TEL}" aria-label="Appeler le {PHONE}">{ic('phone')}</a>
      <a class="btn btn--primary hd__cta" href="{p.get('form_href', '#devis')}" data-to-form><span class="lg">Devis gratuit</span><span class="sm">Devis</span></a>
    </div>
  </div>
</header>
"""


def footer(rel, p):
    links = "".join(f'<li><a href="{rel}{h}">{l}</a></li>' for h, l in NAV)
    home = rel if rel else "./"
    return f"""<footer class="ft">
  <div class="container ft__grid">
    <div class="ft__brand">
      <img src="{rel}img/brand/logo-white-221.png" width="221" height="120" alt="Viva Service24" loading="lazy">
      <p>Nettoyage et entretien technique pour particuliers, régies, entreprises et commerces. Basés à Crissier, dans tout le canton de Vaud.</p>
      <a class="ft__google" href="{GOOGLE}" target="_blank" rel="noopener">{ic('g', 'ic ic--g')}<span><b>5,0</b> {STARS} <span>16 avis Google</span></span></a>
    </div>
    <div>
      <h2 class="ft__h">Contact</h2>
      <ul class="ft__list">
        <li><a href="{TEL}">{ic('phone')}{PHONE_NB}</a></li>
        <li><a href="{wa(p['wa'])}" data-wa target="_blank" rel="noopener">{ic('wa')}WhatsApp</a></li>
        <li><a href="mailto:{EMAIL}">{ic('mail')}{EMAIL}</a></li>
        <li><span>{ic('pin')}Rue du Jura 11, 1023 Crissier</span></li>
        <li><span>{ic('clock')}7 jours sur 7, 24h/24</span></li>
      </ul>
    </div>
    <div>
      <h2 class="ft__h">Services</h2>
      <ul class="ft__list ft__list--plain"><li><a href="{home}">Tous nos services</a></li>{links}</ul>
    </div>
    <div>
      <h2 class="ft__h">Informations</h2>
      <ul class="ft__list ft__list--plain">
        <li><a href="{rel}mentions-legales/">Mentions légales</a></li>
        <li><a href="{rel}confidentialite/">Protection des données</a></li>
        <li><a href="{GOOGLE}" target="_blank" rel="noopener">Laisser un avis Google</a></li>
      </ul>
    </div>
  </div>
  <div class="container ft__bottom">
    <p>© 2026 Viva service24 Sàrl · Rue du Jura 11, 1023 Crissier</p>
    <p>Prix indicatifs en francs suisses. Seul le devis écrit fait foi.</p>
  </div>
</footer>
"""


def mobile_bar(p):
    return f"""<nav class="mbar" aria-label="Contact rapide" data-mbar>
  <a href="{TEL}">{ic('phone')}<span>Appeler</span></a>
  <a href="{wa(p['wa'])}" data-wa target="_blank" rel="noopener">{ic('wa')}<span>WhatsApp</span></a>
  <a href="{p.get('form_href', '#devis')}" data-to-form class="mbar__cta">{ic('mail')}<span>Devis</span></a>
</nav>
<a class="wafloat" href="{wa(p['wa'])}" data-wa target="_blank" rel="noopener" aria-label="Écrire sur WhatsApp">{ic('wa')}<span>Écrire sur WhatsApp</span></a>
"""


def scripts(rel, extra=""):
    return f"""<script src="{rel}js/config.js?v={V}" defer></script>
<script src="{rel}js/reviews.js?v={V}" defer></script>
<script src="{rel}js/main.js?v={V}" defer></script>{extra}
"""


# ------------------------------------------------------------------ hero + form
def gbadge(rel=""):
    return (f'<a class="gbadge" href="#avis">{ic("g", "ic ic--g")}<b>5,0</b>{STARS}'
            f'<span>16 avis Google</span></a>')


def hero(p, rel):
    if p["hero"] == "video":
        media = (pic(rel, "stock/hero-poster", "", "100vw", cls="hero__img", eager=True) +
                 f'<video class="hero__video" muted playsinline loop preload="none" '
                 f'data-sm="{rel}video/hero-768" data-lg="{rel}video/hero-1280"></video>')
    else:
        media = pic(rel, p["hero"], "", "100vw", cls="hero__img", eager=True)
    points = "".join(f"<li>{ic(i)}<span>{t}</span></li>" for i, t in p["points"])
    return f"""<section class="hero" aria-labelledby="h1">
  <div class="hero__media" aria-hidden="true">{media}</div>
  <div class="container hero__grid">
    <div class="hero__copy">
      {gbadge(rel)}
      <h1 id="h1">{p['h1']}</h1>
      <p class="hero__sub">{p['sub']}</p>
      <div class="hero__ctas">
        <a class="btn btn--primary btn--lg" href="#devis" data-to-form>Recevoir mon devis gratuit{ic('arrow')}</a>
        <a class="btn btn--light btn--lg" href="{TEL}">{ic('phone')}Appeler {PHONE_NB}</a>
      </div>
      <ul class="hero__points">{points}</ul>
    </div>
    <div class="hero__form" id="devis">{quote_form(p, rel)}</div>
  </div>
</section>
"""


def quote_form(p, rel):
    pre = p.get("service")
    chips = "".join(
        f'<label class="chip"><input type="radio" name="service" value="{s}"{" checked" if s == pre else ""}><span>{s}</span></label>'
        for s in SERVICE_CHIPS)
    rooms = "".join(
        f'<label class="chip chip--sm"><input type="radio" name="pieces" value="{r}"><span>{r}</span></label>'
        for r in ROOMS)
    towns = "".join(f'<option value="{t}"></option>' for t in TOWNS)
    bail_hidden = "" if (pre in (None, "Fin de bail")) else " hidden"
    return f"""<form class="qf" id="devis-form" action="https://formsubmit.co/{EMAIL}" method="POST" novalidate data-merci="{rel}merci/" data-page="{esc(p['title'])}">
  <div class="qf__head">
    <p class="qf__title">Votre devis gratuit</p>
    <p class="qf__sub">2 étapes, moins d'une minute.</p>
    <div class="qf__prog" aria-hidden="true"><span class="qf__stepno">Étape <b data-stepno>1</b> sur 2</span><span class="qf__bar"><i></i></span></div>
  </div>
  <fieldset class="qf__step" data-step="1">
    <legend class="qf__legend">Quel nettoyage ?</legend>
    <div class="chips" data-group="service">{chips}</div>
    <p class="qf__err" data-err="service"></p>
    <div class="qf__bail" data-bail{bail_hidden}>
      <p class="qf__legend qf__legend--sm" id="lbl-pieces">Taille du logement (pièces)</p>
      <div class="chips chips--rooms" role="group" aria-labelledby="lbl-pieces" data-group="pieces">{rooms}</div>
      <p class="qf__err" data-err="pieces"></p>
    </div>
    <label class="field"><span class="field__l">Date souhaitée <em>facultatif</em></span><input type="date" name="date" class="field__i"></label>
    <button type="button" class="btn btn--primary btn--block btn--lg" data-next>Continuer{ic('arrow')}</button>
  </fieldset>
  <fieldset class="qf__step" data-step="2">
    <legend class="qf__legend">Où vous rappeler ?</legend>
    <label class="field"><span class="field__l">Nom et prénom</span><input name="nom" class="field__i" autocomplete="name" required autocapitalize="words"></label>
    <p class="qf__err" data-err="nom"></p>
    <label class="field"><span class="field__l">Téléphone</span><input type="tel" name="telephone" class="field__i" inputmode="tel" autocomplete="tel" required placeholder="076 123 45 67"></label>
    <p class="qf__err" data-err="telephone"></p>
    <label class="field"><span class="field__l">Localité</span><input name="localite" class="field__i" list="towns" autocomplete="address-level2" placeholder="Lausanne, Renens, Morges…"></label>
    <datalist id="towns">{towns}</datalist>
    <label class="field"><span class="field__l">E-mail <em>facultatif</em></span><input type="email" name="email" class="field__i" inputmode="email" autocomplete="email"></label>
    <p class="qf__err" data-err="email"></p>
    <label class="field"><span class="field__l">Message <em>facultatif</em></span><textarea name="message" class="field__i" rows="3" placeholder="Accès, étage, état du logement, date de l'état des lieux…"></textarea></label>
    <div class="hp" aria-hidden="true"><label>Laisser vide<input name="_honey" tabindex="-1" autocomplete="off"></label></div>
    <input type="hidden" name="_subject" value="Nouvelle demande de devis · site web">
    <input type="hidden" name="_template" value="table">
    <input type="hidden" name="_captcha" value="false">
    <input type="hidden" name="_next" value="{BASE_URL}merci/">
    <button type="submit" class="btn btn--primary btn--block btn--lg" data-submit>Recevoir mon devis gratuit</button>
    <p class="qf__fine">Gratuit et sans engagement · Réponse rapide · Vos données restent confidentielles</p>
    <button type="button" class="qf__back" data-prev>{ic('back')}Modifier le service</button>
  </fieldset>
  <p class="qf__status" role="status" aria-live="polite" data-status></p>
  <a class="qf__wa" href="{wa(p['wa_photos'])}" data-wa target="_blank" rel="noopener">{ic('wa')}<span><b>Plus rapide ?</b> {p['wa_photos_label']}</span></a>
</form>"""


def trustbar():
    items = [
        (ic("g", "ic ic--g"), "<b>5,0 sur Google</b> 16 avis, tous 5 étoiles"),
        (ic("clock"), "<b>7j/7, 24h/24</b> même en urgence"),
        (ic("pin"), "<b>Crissier, Lausanne</b> et tout le canton de Vaud"),
        (ic("reply"), "<b>Devis gratuit</b> et sans engagement"),
    ]
    li = "".join(f"<li>{i}<span>{t}</span></li>" for i, t in items)
    return f'<section class="trust" aria-label="En bref"><ul class="container trust__in">{li}</ul></section>'


# ------------------------------------------------------------------ reusable sections
def cta_row(p, primary="Obtenir mon devis", center=False):
    c = " cta-row--c" if center else ""
    return f"""<div class="cta-row{c}">
  <a class="btn btn--primary" href="#devis" data-to-form>{primary}{ic('arrow')}</a>
  <a class="btn btn--ghost" href="{TEL}">{ic('phone')}Appeler maintenant</a>
  <a class="btn btn--wa" href="{wa(p['wa'])}" data-wa target="_blank" rel="noopener">{ic('wa')}Écrire sur WhatsApp</a>
</div>"""


def pull(quote, name, cls=""):
    return (f'<figure class="pq {cls}"><blockquote><p>« {quote} »</p></blockquote>'
            f'<figcaption>{ic("g", "ic ic--g")}<span><b>{name}</b> {STARS} avis Google</span></figcaption></figure>')


def estimator(rel):
    opts = "".join(
        f'<label class="seg__o"><input type="radio" name="est" value="{k}" data-price="{price}" data-label="{lab}"'
        f'{" checked" if k == "3" else ""}><span>{short}</span></label>'
        for k, short, price, lab in BAIL_PRICES)
    return f"""<div class="est" data-est>
  <p class="est__q" id="est-q">Votre logement</p>
  <div class="seg" role="radiogroup" aria-labelledby="est-q">{opts}</div>
  <div class="est__out" aria-live="polite">
    <p class="est__lab">Estimation indicative · <span data-est-label>3 pièces</span></p>
    <p class="est__price" data-est-price>CHF 580 à 750</p>
    <p class="est__note">Vitres, stores et four compris. 2.5, 3.5 ou 4.5 pièces : prenez la taille la plus proche, le devis précise le prix.</p>
  </div>
  <a class="btn btn--primary btn--block" href="#devis" data-est-cta>Recevoir mon prix exact{ic('arrow')}</a>
</div>"""


def bail_price_table():
    rows = "".join(f"<tr><th scope=\"row\">{lab}</th><td>{price}</td></tr>" for _, _, price, lab in BAIL_PRICES)
    return f"""<table class="ptable">
  <caption>Nettoyage de fin de bail</caption>
  <tbody>{rows}</tbody>
</table>
<p class="ptable__note">Compris dans le prix : vitres, stores et four. {URGENCE} {PRICE_NOTE}</p>"""


def simple_table(caption, rows, note=""):
    r = "".join(f'<tr><th scope="row">{a}{f"<small>{c}</small>" if c else ""}</th><td>{b}</td></tr>' for a, b, c in rows)
    return f"""<table class="ptable"><caption>{caption}</caption><tbody>{r}</tbody></table>
<p class="ptable__note">{note + ' ' if note else ''}{URGENCE} {PRICE_NOTE}</p>"""


STATIC_REVIEWS = [
    ("Amir Ali", "Fin de bail", "octobre 2026",
     "J'ai eu une excellente expérience avec VIVA Service 24. J'avais besoin d'un nettoyage de fin de bail en urgence, et ils ont réussi à intervenir dès le lendemain. Franchement, cela m'a évité beaucoup de stress et de complications. Le nettoyage a été très bien fait et dans les délais convenus, exactement comme promis. Le plus important, c'est que la régie était satisfaite du résultat et a accepté le nettoyage sans aucun problème. Le prix était également très raisonnable par rapport aux autres devis que j'avais reçus. Un service sérieux, un prix correct et une équipe fiable. Je recommande vivement VIVA Service 24 pour les services de nettoyage dans la région de Lausanne, Renens et Crissier !"),
    ("leila unkown", "Fin de bail", "octobre 2026",
     "J'ai contacté vivaservice pour un nettoyage complet de mon appartement, à l'issue de mon déménagement. Et j'en suis ravie le service de qualité apporte une réelle tranquillité d'esprit à l'approche de l'état des lieux. La propreté de l'appartement a même été soulignée a l'état des lieux. Et tout ça pour un prix très correct avec un employé sympathique et à l'écoute. Je vous les recommande vivement et je ferai maintenant appelle a vivaservice à l'avenir si besoin."),
    ("vXv Barber's", "Vitres", "octobre 2026", "Merci pour le nettoyage de nos vitres excellent travail"),
]


def rcard_static(name, service, date, text, i):
    return (f'<li class="rc rc--c{i % 5}"><div class="rc__top"><span class="rc__av" aria-hidden="true">{esc(name[0].upper())}</span>'
            f'<span class="rc__who"><b>{esc(name)}</b><span class="rc__meta">{STARS}<span>{date}</span></span></span>'
            f'{ic("g", "ic ic--g rc__g")}</div><p class="rc__t">{esc(text)}</p>'
            f'{f"<span class=rc__tag>{service}</span>" if service else ""}</li>')


def reviews(p, rel, title="Ce que disent nos clients", intro=None, filt=""):
    intro = intro or "16 avis sur Google, tous 5 étoiles. Ils sont affichés tels quels, sans retouche."
    static = "".join(rcard_static(*r, i) for i, r in enumerate(STATIC_REVIEWS))
    bars = "".join(
        f'<li><span>{n}</span><span class="rsum__bar"><i style="width:{100 if n == 5 else 0}%"></i></span><span>{16 if n == 5 else 0}</span></li>'
        for n in (5, 4, 3, 2, 1))
    return f"""<section class="sec reviews" id="avis" aria-labelledby="avis-h">
  <div class="container reviews__head">
    <div class="reviews__intro">
      <h2 id="avis-h">{title}</h2>
      <p>{intro}</p>
    </div>
    <div class="rsum">
      <div class="rsum__score">{ic('g', 'ic ic--g rsum__g')}<b>5,0</b><span>{STARS}<span>16 avis · 100 % de 5 étoiles</span></span></div>
      <ul class="rsum__bars" aria-label="Répartition des notes : 16 avis 5 étoiles, aucun avis de 1 à 4 étoiles">{bars}</ul>
      <div class="rsum__btns">
        <a class="btn btn--ghost btn--sm" href="{GOOGLE}" target="_blank" rel="noopener">Voir tous les avis sur Google</a>
        <a class="btn btn--text btn--sm" href="{GOOGLE}" target="_blank" rel="noopener">Laisser un avis</a>
      </div>
    </div>
  </div>
  <div class="rwall" data-reviews data-filter="{filt}">
    <ul class="rgrid container">{static}</ul>
  </div>
  <div class="container">{cta_row(p, "Obtenir mon devis", center=True)}</div>
</section>
"""


def review_strip(names):
    """3 short reviews right under the form (rendered from reviews.js, static fallback here)."""
    return f'<div class="rstrip" data-strip="{esc("|".join(names))}"></div>'


def ba_pairs(rel, pairs, title="Avant, après", intro=""):
    tabs, panes = "", ""
    for i, (key, label, note, alt_b, alt_a) in enumerate(pairs):
        sel = "true" if i == 0 else "false"
        tabs += f'<button type="button" role="tab" id="bat-{key}" aria-controls="bap-{key}" aria-selected="{sel}" tabindex="{0 if i == 0 else -1}">{label}</button>'
        hidden = "" if i == 0 else " hidden"
        panes += f"""<div class="ba__pane" role="tabpanel" id="bap-{key}" aria-labelledby="bat-{key}"{hidden}>
  <div class="ba" data-ba style="--pos:50%">
    <div class="ba__after">{pic(rel, f"ba/{key}-apres", alt_a, "(min-width: 980px) 760px, 100vw")}</div>
    <div class="ba__before">{pic(rel, f"ba/{key}-avant", alt_b, "(min-width: 980px) 760px, 100vw")}</div>
    <span class="ba__tag ba__tag--b">Avant</span><span class="ba__tag ba__tag--a">Après</span>
    <span class="ba__line" aria-hidden="true"></span>
    <button type="button" class="ba__handle" role="slider" aria-label="Glisser pour comparer avant et après ({label.lower()})" aria-valuemin="0" aria-valuemax="100" aria-valuenow="50" aria-valuetext="50 %">{ic('back')}{ic('arrow')}</button>
  </div>
  <p class="ba__note">{note}</p>
</div>"""
    tablist = f'<div class="ba__tabs" role="tablist" aria-label="Choisir une comparaison">{tabs}</div>' if len(pairs) > 1 else ""
    return f"""<section class="sec ba-sec" aria-labelledby="ba-h">
  <div class="container ba-sec__grid">
    <div class="ba-sec__copy">
      <h2 id="ba-h">{title}</h2>
      <p>{intro}</p>
      {tablist}
    </div>
    <div class="ba-sec__view">{panes}</div>
  </div>
</section>
"""


BA_VITRINE = ("vitrine", "Vitrine", "Photos réelles : vitrine du salon vXv Barber's à Crissier, images tirées de notre vidéo d'intervention.",
              "Vitrine du salon vXv Barber's couverte de produit de lavage, pendant le nettoyage",
              "Même vitrine du salon vXv Barber's, propre et sans traces")
BA_CUISINE = ("cuisine", "Cuisine", "Photos d'illustration (deux photos différentes, banque d'images).",
              "Plan de cuisson ancien, encrassé et taché de rouille", "Plan de cuisson à gaz propre et brillant")
BA_SDB = ("sdb", "Salle de bain", "Photos d'illustration (deux photos différentes, banque d'images).",
          "Lavabo taché de calcaire et de traces sombres autour de la robinetterie", "Lavabo et robinet chromé propres, sans traces de calcaire")


def steps(p):
    items = [
        ("Vous demandez un devis", "Par le formulaire, par téléphone ou sur WhatsApp. Quelques photos nous aident à chiffrer plus vite."),
        ("On vous rappelle et fixe la date", "Vous recevez un prix écrit, gratuit et sans engagement. Pour les grandes surfaces, nous passons voir les lieux."),
        (p.get("step3", "On nettoie, vous rendez les clés tranquille"), p.get("step3_t", "Nous intervenons à la date convenue, avec notre matériel et nos produits professionnels.")),
    ]
    li = "".join(f'<li><span class="steps__n" aria-hidden="true">{i + 1}</span><h3>{h}</h3><p>{t}</p></li>' for i, (h, t) in enumerate(items))
    return f"""<section class="sec steps-sec" aria-labelledby="steps-h">
  <div class="container">
    <h2 id="steps-h">Comment ça se passe</h2>
    <ol class="steps">{li}</ol>
    {cta_row(p, "Demander mon devis")}
  </div>
</section>
"""


def cas_client(rel, p):
    return f"""<section class="sec case" aria-labelledby="case-h">
  <div class="container case__grid">
    <div class="case__media">
      <figure class="case__photo">{pic(rel, "real/vitres-vxv-barbers", "Employé de Viva Service24 lavant la vitrine du salon vXv Barber's à Crissier avec une perche", "(min-width: 980px) 420px, 80vw")}</figure>
      <figure class="case__video vclip">
        <video muted playsinline loop preload="none" poster="{rel}img/real/poster-vitrine-2-400.webp" data-autoplay data-src="{rel}video/real-vitrine-2.mp4" aria-label="Vidéo : finition d'une vitrine du salon vXv Barber's à la raclette"></video>
        <figcaption>Vidéo de l'intervention</figcaption>
      </figure>
    </div>
    <div class="case__copy">
      <p class="case__kicker">Cas client · Vitres · Crissier</p>
      <h2 id="case-h">Les vitrines du salon vXv Barber's</h2>
      <p>Lavage des grandes vitrines du salon de coiffure vXv Barber's, à Crissier : produit de lavage, raclette sur perche, finition des cadres. Le client nous a ensuite laissé un avis sur Google.</p>
      {pull("Merci pour le nettoyage de nos vitres excellent travail", "vXv Barber's", "pq--light")}
      <a class="btn btn--primary" href="#devis" data-to-form data-service="Vitres">Un devis pour vos vitres{ic('arrow')}</a>
    </div>
  </div>
</section>
"""


def field_videos(rel, items, title="Sur le terrain", intro="Nos équipes au travail chez nos clients de la région. Vidéos réelles, non retouchées."):
    figs = "".join(
        f'<figure class="vclip"><video muted playsinline loop preload="none" poster="{rel}img/real/poster-{v}-400.webp" data-autoplay data-src="{rel}video/real-{v}.mp4" aria-label="{esc(cap)}"></video><figcaption>{cap}</figcaption></figure>'
        for v, cap in items)
    return f"""<section class="sec terrain" aria-labelledby="field-h">
  <div class="container">
    <div class="terrain__head"><h2 id="field-h">{title}</h2><p>{intro}</p></div>
    <div class="terrain__row">{figs}</div>
  </div>
</section>
"""


def about(rel, p):
    return f"""<section class="sec about" id="entreprise" aria-labelledby="about-h">
  <div class="container about__grid">
    <div class="about__photos">
      <figure class="about__a">{pic(rel, "real/equipe-tshirt", "Dos d'un employé portant le t-shirt Viva Service24, Nettoyage et entretien technique", "(min-width: 980px) 560px, 92vw")}</figure>
      <figure class="about__b">{pic(rel, "real/solaire-toit-vegetal", "Employé de Viva Service24 nettoyant des panneaux solaires sur un toit végétalisé avec une perche à eau pure", "(min-width: 980px) 260px, 45vw")}</figure>
    </div>
    <div class="about__copy">
      <h2 id="about-h">Une entreprise locale, basée à Crissier</h2>
      <p>Viva Service24 est une entreprise de nettoyage et d'entretien technique installée à Crissier, aux portes de Lausanne. Nous travaillons pour les particuliers, les régies, les entreprises et les commerces de la région.</p>
      <ul class="ticks">
        <li>{ic('check')}<span><b>Un seul interlocuteur</b> pour le nettoyage, les vitres, les panneaux solaires, la conciergerie et le jardin.</span></li>
        <li>{ic('check')}<span><b>Matériel et produits professionnels</b>, adaptés à chaque surface.</span></li>
        <li>{ic('check')}<span><b>Eau pure</b> pour les panneaux solaires et les vitres : elle sèche sans traces ni calcaire.</span></li>
        <li>{ic('check')}<span><b>Un devis écrit</b> avant chaque intervention, pour savoir exactement ce que vous payez.</span></li>
      </ul>
    </div>
  </div>
</section>
"""


def zone_map():
    K = 4650.0

    def P(lat, lon):
        return ((lon - 6.47) * 0.6884 * K, (46.60 - lat) * K)

    shore = [(46.497, 6.47), (46.503, 6.49), (46.5065, 6.50), (46.508, 6.52), (46.509, 6.545), (46.5105, 6.56),
             (46.514, 6.58), (46.517, 6.597), (46.513, 6.612), (46.5065, 6.627), (46.505, 6.643), (46.5065, 6.66),
             (46.503, 6.676), (46.4995, 6.69), (46.495, 6.705), (46.49, 6.725)]
    pts = [P(a, b) for a, b in shore]
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + f" L{P(46.47, 6.725)[0]:.1f},600 L0,600 Z"
    towns = [
        ("Lausanne", 46.5197, 6.6323, 14, -16, "big"), ("Renens", 46.5399, 6.5881, 4, 32, "mid"),
        ("Ecublens", 46.5277, 6.5615, -12, 24, "end"), ("Prilly", 46.5370, 6.6050, 12, -10, "minor"),
        ("Bussigny", 46.5510, 6.5560, -12, -10, "end"), ("Morges", 46.5110, 6.4980, 0, -16, "mid"),
        ("Pully", 46.5100, 6.6620, 10, -12, ""), ("Lutry", 46.5030, 6.6860, 0, -16, "mid"),
        ("Epalinges", 46.5480, 6.6700, 12, 6, ""), ("Le Mont", 46.5580, 6.6310, 12, -8, ""),
        ("Cheseaux", 46.5830, 6.5970, 12, 6, ""), ("Chavannes", 46.5300, 6.5710, 10, 24, "minor"),
    ]
    cx, cy = P(46.5395, 6.5783)
    km = K / 111.0
    t = ""
    for name, la, lo, dx, dy, kind in towns:
        x, y = P(la, lo)
        anchor = "end" if kind == "end" else ("middle" if kind == "mid" else "start")
        cls = "m-town m-town--big" if kind == "big" else ("m-town m-town--minor" if kind == "minor" else "m-town")
        t += f'<circle class="m-dot{" m-dot--big" if kind == "big" else ""}" cx="{x:.1f}" cy="{y:.1f}" r="{5.5 if kind == "big" else 4}"/><text class="{cls}" x="{x + dx:.1f}" y="{y + dy:.1f}" text-anchor="{anchor}">{name}</text>'
    rings = (f'<circle class="m-ring" cx="{cx:.1f}" cy="{cy:.1f}" r="{5 * km:.1f}"/>'
             f'<text class="m-km" x="{cx:.1f}" y="{cy - 5 * km - 8:.1f}" text-anchor="middle">5 km</text>')
    lake_label = P(46.488, 6.585)
    return f"""<svg class="map" viewBox="30 30 740 500" role="img" aria-labelledby="map-t">
  <title id="map-t">Carte schématique de la région lausannoise : Viva Service24 est basée à Crissier, à environ 5 km de Lausanne</title>
  <rect width="800" height="600" class="m-bg"/>
  <path d="{d}" class="m-lake"/>
  <text class="m-lake-l" x="{lake_label[0]:.0f}" y="{lake_label[1]:.0f}">Lac Léman</text>
  {rings}
  {t}
  <g class="m-base"><circle cx="{cx:.1f}" cy="{cy:.1f}" r="15" class="m-base-halo"/><circle cx="{cx:.1f}" cy="{cy:.1f}" r="7.5" class="m-base-dot"/></g>
  <text class="m-base-l" x="{cx - 16:.1f}" y="{cy - 22:.1f}" text-anchor="end">Crissier, notre base</text>
</svg>"""


def zone(rel, p):
    chips = "".join(f"<li>{t}</li>" for t in TOWNS)
    return f"""<section class="sec zone" id="zone" aria-labelledby="zone-h">
  <div class="container zone__grid">
    <div class="zone__copy">
      <h2 id="zone-h">Zone d'intervention</h2>
      <p>Basés à Crissier, nous sommes à quelques minutes de Lausanne et de tout l'Ouest lausannois.</p>
      <ul class="towns">{chips}</ul>
      <p class="zone__more">{ic('pin')}<span>Tout le canton de Vaud. Genève, Fribourg, Neuchâtel, Valais et Jura sur demande.</span></p>
      <a class="btn btn--ghost" href="#devis" data-to-form>Vérifier pour ma commune{ic('arrow')}</a>
    </div>
    <div class="zone__map">{zone_map()}</div>
  </div>
</section>
"""


def photo_band(rel, key, alt, text):
    return f"""<section class="band" aria-label="{esc(alt)}">
  {pic(rel, key, alt, "100vw", cls="band__img")}
  <div class="container band__in"><p>{text}</p></div>
</section>
"""


def faq(items, title="Questions fréquentes"):
    q = "".join(
        f'<details class="faq__i"><summary><span>{a}</span>{ic("chev")}</summary><div class="faq__a"><p>{b}</p></div></details>'
        for a, b in items)
    return f"""<section class="sec faq" id="faq" aria-labelledby="faq-h">
  <div class="container faq__grid">
    <div class="faq__intro"><h2 id="faq-h">{title}</h2><p>Une autre question ? Appelez-nous au <a href="{TEL}">{PHONE_NB}</a>, nous répondons 7 jours sur 7.</p></div>
    <div class="faq__list">{q}</div>
  </div>
</section>
"""


def faq_ld(items):
    strip = lambda s: re.sub(r"<[^>]+>", "", s)
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": strip(a), "acceptedAnswer": {"@type": "Answer", "text": strip(b)}} for a, b in items]}


def final_cta(p):
    return f"""<section class="final" aria-labelledby="final-h">
  <div class="container final__in">
    <div>
      <h2 id="final-h">{p.get('final_h', 'Votre devis gratuit en quelques minutes')}</h2>
      <p>Décrivez votre besoin, nous vous rappelons rapidement avec un prix. 7 jours sur 7.</p>
    </div>
    <div class="final__btns">
      <a class="btn btn--primary btn--lg" href="#devis" data-to-form>Remplir le formulaire{ic('arrow')}</a>
      <a class="btn btn--light btn--lg" href="{TEL}">{ic('phone')}{PHONE_NB}</a>
      <a class="btn btn--wa btn--lg" href="{wa(p['wa'])}" data-wa target="_blank" rel="noopener">{ic('wa')}WhatsApp</a>
    </div>
  </div>
</section>
"""


def inclus(groups, title="Ce qui est inclus", intro=""):
    cols = ""
    for g in groups:
        name, icon, items = g[0], g[1], g[2]
        photo = g[3] if len(g) > 3 else ""
        li = "".join(f"<li>{ic('check')}<span>{x}</span></li>" for x in items)
        cols += f'<div class="inc__g">{photo}<h3>{ic(icon)}{name}</h3><ul class="ticks ticks--sm">{li}</ul></div>'
    return f"""<section class="sec inc" id="inclus" aria-labelledby="inc-h">
  <div class="container">
    <div class="sec__head"><h2 id="inc-h">{title}</h2><p>{intro}</p></div>
    <div class="inc__grid">{cols}</div>
  </div>
</section>
"""


def prices_sec(p, table_html, aside="", title="Nos prix", intro=PRICE_NOTE, sid="prix"):
    return f"""<section class="sec prices" id="{sid}" aria-labelledby="{sid}-h">
  <div class="container prices__grid">
    <div class="prices__copy"><h2 id="{sid}-h">{title}</h2><p>{intro}</p>{table_html}</div>
    <div class="prices__aside">{aside}</div>
  </div>
</section>
"""


# ------------------------------------------------------------------ FAQ content
FAQ_PRICE = ("Combien coûte un nettoyage de fin de bail ?",
             "Comptez dès CHF 350 pour un studio, CHF 450 à 590 pour un 2 pièces, CHF 580 à 750 pour un 3 pièces, CHF 750 à 950 pour un 4 pièces et dès CHF 900 pour un 5 pièces. Vitres, stores et four sont compris. Ce sont des prix indicatifs : le devis, gratuit et sans engagement, fixe le prix exact selon la surface et l'état du logement.")
FAQ_INCLUS = ("Qu'est-ce qui est compris dans un nettoyage de fin de bail ?",
              "La cuisine complète (four, plaques, hotte, réfrigérateur, armoires dedans et dehors), la salle de bain et les WC avec détartrage, les fenêtres et leurs cadres, les stores, les sols, les portes et poignées, les placards et le balcon. Le détail figure dans le devis.")
FAQ_PRESENT = ("Dois-je être présent pendant le nettoyage ?",
               "Pas forcément. Dites-nous au moment du devis comment vous préférez procéder (présence sur place ou remise des clés) et nous organisons l'intervention en conséquence.")
FAQ_REGIE = ("Et si la régie n'est pas satisfaite ?",
             "Appelez-nous dès l'état des lieux. Nous regardons avec vous les remarques de la régie et nous trouvons une solution ensemble. Nos clients nous écrivent régulièrement que la régie a accepté le nettoyage sans problème.")
FAQ_DELAI = ("En combien de temps pouvez-vous intervenir ?",
             "Rapidement, souvent dès le lendemain selon nos disponibilités. Nous travaillons 7 jours sur 7, y compris en urgence. Urgence et week-end : supplément de 20 à 50 %, indiqué dans le devis.")
FAQ_PAIEMENT = ("Comment se passe le paiement ?",
                "Les modalités de paiement sont indiquées dans votre devis. Posez-nous la question au moment de la demande, nous vous répondons tout de suite.")
FAQ_PRODUITS = ("Quels produits utilisez-vous ?",
                "Des produits et du matériel professionnels, choisis selon la surface : dégraissant pour la cuisine, détartrant pour les sanitaires. Pour les panneaux solaires, de l'eau pure filtrée sur place, sans détergent.")
FAQ_WEEKEND = ("Travaillez-vous le soir et le week-end ?",
               "Oui, 7 jours sur 7 et 24h/24, comme indiqué sur notre fiche Google. Un supplément de 20 à 50 % s'applique pour les urgences et le week-end ; il est toujours indiqué dans le devis.")
FAQ_VIDE = ("Le logement doit-il être vide ?",
            "Oui, idéalement. Le nettoyage de fin de bail se fait dans un logement vidé de ses meubles et cartons, pour que chaque surface, placard et sol soit accessible.")

FAQ_HOME = [FAQ_PRICE, FAQ_INCLUS, FAQ_PRESENT, FAQ_REGIE, FAQ_DELAI, FAQ_PAIEMENT, FAQ_PRODUITS, FAQ_WEEKEND]
FAQ_BAIL = [FAQ_PRICE, FAQ_INCLUS, FAQ_REGIE, FAQ_PRESENT, FAQ_VIDE, FAQ_DELAI,
            ("Les vitres et les stores sont-ils compris ?", "Oui. Vitres, cadres, stores et four sont compris dans nos prix de fin de bail."),
            FAQ_PAIEMENT, FAQ_WEEKEND]
FAQ_VITRES = [
    ("Combien coûte un nettoyage de vitres ?", "Entre CHF 50 et 70 de l'heure selon la taille et le nombre de vitres, leur accès et leur état. Le devis, gratuit, fixe le prix exact."),
    ("Nettoyez-vous les vitrines de commerces ?", "Oui : vitrines, portes vitrées, baies et vérandas. Nous avons par exemple nettoyé les vitrines du salon vXv Barber's à Crissier."),
    ("Les cadres et les stores sont-ils compris ?", "Oui, nous nettoyons les vitres, les cadres et les stores. Précisez-le dans votre demande pour que le devis en tienne compte."),
    ("Pouvez-vous nettoyer des vitres en hauteur ?", "Oui, nous travaillons en hauteur quand c'est nécessaire, avec une perche télescopique depuis le sol ou le matériel adapté au bâtiment."),
    ("Proposez-vous un nettoyage régulier ?", "Oui. Nous intervenons ponctuellement ou selon un planning fixe (mensuel, trimestriel), pour les particuliers comme pour les commerces."),
    FAQ_WEEKEND,
]
FAQ_SOLAIRE = [
    ("Pourquoi nettoyer ses panneaux solaires ?", "Poussière, pollen, feuilles et fientes se déposent sur les modules et réduisent leur production. Un nettoyage régulier aide à garder des panneaux propres et performants."),
    ("Comment nettoyez-vous les panneaux ?", "À l'eau pure (déminéralisée), filtrée sur place, sans aucun produit chimique, avec une brosse douce adaptée au verre des modules. L'eau pure détache les salissures et sèche sans traces ni calcaire."),
    ("Combien coûte le nettoyage ?", "Dès CHF 180. Comptez CHF 180 à 250 pour 20 à 30 m², CHF 250 à 350 pour 30 à 50 m². Les grandes installations sont chiffrées sur devis."),
    ("Et si le toit n'est pas accessible ?", "Nous travaillons depuis le sol avec une perche télescopique et, pour les toits difficiles d'accès, avec une nacelle élévatrice."),
    ("Quels types d'installations ?", "Villas, immeubles, halles industrielles et agricoles, toits plats et toits végétalisés."),
    ("À quelle fréquence faut-il nettoyer ?", "Cela dépend de l'environnement (arbres, routes, champs, oiseaux). Nous vous conseillons lors du devis, selon l'état de vos panneaux."),
]
FAQ_CHANTIER = [
    ("Que comprend un nettoyage de fin de chantier ?", "Poussière fine sur toutes les surfaces, traces de plâtre, de peinture et de silicone, vitres et cadres, sols, sanitaires et cuisine. Nous rendons des locaux prêts à être occupés."),
    ("Combien coûte un nettoyage de fin de chantier ?", "Entre CHF 55 et 75 de l'heure, selon la surface, le nombre d'étages et le nombre de bâtiments. Le devis fixe le prix exact."),
    ("Travaillez-vous pour les entreprises et les régies ?", "Oui : entreprises générales, architectes, régies, commerces et particuliers après une rénovation."),
    ("Pouvez-vous intervenir rapidement ?", "Oui, 7 jours sur 7, y compris pour respecter une date de remise des locaux. Urgence et week-end : supplément de 20 à 50 %, indiqué dans le devis."),
    ("Faut-il une visite avant le devis ?", "Pour les grandes surfaces ou les cas particuliers, nous passons voir les lieux avant d'établir le devis. Pour un appartement, des photos suffisent souvent."),
]
FAQ_IMMEUBLE = [
    ("Proposez-vous des contrats d'entretien réguliers ?", "Oui. Passages quotidiens, hebdomadaires ou mensuels selon un planning fixe, pour les immeubles, les bureaux, les cabinets et les commerces."),
    ("Que comprend la conciergerie ?", "L'entretien des parties communes, la gestion des containers, le contrôle des locaux techniques et le suivi avec la gérance."),
    ("Quels sont vos tarifs ?", "Entretien d'immeubles, bureaux et commerces : CHF 45 à 50 de l'heure. Conciergerie : CHF 50 à 60 de l'heure. Espaces verts : CHF 55 à 75 de l'heure. Suppression de tags et nettoyages spéciaux : dès CHF 250 au forfait."),
    ("Supprimez-vous les tags et graffitis ?", "Oui, sur façades, murs, portes de garage et mobilier. La méthode est choisie selon le support : crépi, pierre, béton, métal ou bois."),
    ("Faites-vous aussi les espaces verts ?", "Oui : tonte, taille des haies, désherbage, ramassage des feuilles et entretien de saison des extérieurs."),
    ("Avec qui suis-je en contact ?", "Avec un seul interlocuteur pour le nettoyage, la conciergerie, les vitres, les panneaux solaires et le jardin, et une seule facture."),
]


# ------------------------------------------------------------------ services grid (home)
def services_grid(rel):
    tiles = [
        ("big", "fin-de-bail/", "stock/appart-vide-2", "Appartement vide et lumineux, parquet propre, prêt pour l'état des lieux",
         "Nettoyage de fin de bail", "Tout le logement avant l'état des lieux : cuisine, four, salle de bain, vitres, stores, balcon.", "dès CHF 350", "Voir la fin de bail"),
        ("", "vitres/", "real/vitres-vxv-barbers", "Employé de Viva Service24 lavant une vitrine à Crissier",
         "Vitres et vitrines", "Fenêtres, baies, vérandas, vitrines. Cadres et stores.", "CHF 50 à 70 / h", "Vitres"),
        ("", "panneaux-solaires/", "real/solaire-toit-vegetal", "Nettoyage de panneaux solaires sur un toit végétalisé",
         "Panneaux solaires", "À l'eau pure, sans détergent. Perche ou nacelle.", "dès CHF 180", "Panneaux solaires"),
        ("", "fin-de-chantier/", "stock/chantier", "Cuisine en fin de rénovation, meubles encore protégés",
         "Fin de chantier", "Poussière, plâtre, peinture, silicone. Locaux prêts à occuper.", "CHF 55 à 75 / h", "Fin de chantier"),
        ("", "entretien-immeubles/", "stock/escalier", "Cage d'escalier d'immeuble propre",
         "Immeubles, bureaux, commerces", "Cages d'escalier et parties communes. Planning fixe.", "CHF 45 à 50 / h", "Immeubles"),
        ("", "entretien-immeubles/#conciergerie", "stock/immeuble", "Immeuble résidentiel avec balcons, montagnes en arrière-plan",
         "Conciergerie", "Immeubles et centres commerciaux, suivi avec la gérance.", "CHF 50 à 60 / h", "Conciergerie"),
        ("", "entretien-immeubles/#exterieurs", "stock/haie", "Taille d'une haie au taille-haie",
         "Espaces verts", "Tonte, haies, désherbage, feuilles.", "CHF 55 à 75 / h", "Espaces verts"),
        ("", "entretien-immeubles/#exterieurs", "stock/tags-karcher", "Nettoyage haute pression d'un sol urbain",
         "Tags et nettoyages spéciaux", "Graffitis, dégâts d'eau, moquettes, remise en état.", "dès CHF 250", "Tags"),
    ]
    out = ""
    for size, href, img, alt, h, t, price, _ in tiles:
        cls = "svc svc--big" if size == "big" else "svc"
        sizes = "(min-width: 980px) 600px, 100vw" if size == "big" else "(min-width: 980px) 300px, (min-width: 640px) 45vw, 100vw"
        out += f"""<a class="{cls}" href="{rel}{href}">
  <span class="svc__img">{pic(rel, img, alt, sizes)}</span>
  <span class="svc__body"><span class="svc__h">{h}</span><span class="svc__t">{t}</span>
  <span class="svc__foot"><span class="svc__p">{price}</span>{ic('arrow')}</span></span>
</a>"""
    out += f"""<div class="svc svc--cta">
  <span class="svc__h">Un autre besoin ?</span>
  <span class="svc__t">Décrivez-nous la situation, nous vous rappelons rapidement avec un prix.</span>
  <span class="svc__btns"><a class="btn btn--primary btn--block" href="#devis" data-to-form data-service="Autre">Demander un devis</a>
  <a class="btn btn--light btn--block" href="{TEL}">{ic('phone')}{PHONE_NB}</a></span>
</div>"""
    return f"""<section class="sec svcs" id="services" aria-labelledby="svc-h">
  <div class="container">
    <div class="sec__head sec__head--split"><h2 id="svc-h">Tout l'entretien de vos bâtiments, <span class="hl">un seul interlocuteur</span></h2>
    <p>Interventions ponctuelles ou contrats réguliers, pour les particuliers, les régies, les entreprises et les commerces. {PRICE_NOTE}</p></div>
    <div class="svcs__grid">{out}</div>
  </div>
</section>
"""


def bail_focus(rel, p, landing=False):
    h = "Votre état des lieux, sans stress"
    return f"""<section class="sec bail" id="fin-de-bail" aria-labelledby="bail-h">
  <div class="container bail__grid">
    <div class="bail__media">
      <figure class="bail__main">{pic(rel, "stock/appart-vide", "Appartement vide, parquet et murs blancs propres, prêt pour la remise des clés", "(min-width: 980px) 640px, 100vw")}</figure>
      {pull("La propreté de l'appartement a même été soulignée a l'état des lieux.", "leila unkown", "pq--float")}
    </div>
    <div class="bail__copy">
      <h2 id="bail-h">{h}</h2>
      <p class="lead">Vous rendez les clés, nous nous occupons du reste. Un nettoyage complet, pensé pour ce que la régie contrôle.</p>
      <ul class="ticks">
        <li>{ic('check')}<span><b>Tout est compris</b> : cuisine et four, salle de bain, vitres, stores, sols, armoires et balcon.</span></li>
        <li>{ic('check')}<span><b>Un prix connu à l'avance</b>, dans un devis écrit, gratuit et sans engagement.</span></li>
        <li>{ic('check')}<span><b>Intervention rapide</b>, souvent dès le lendemain, 7 jours sur 7.</span></li>
        <li>{ic('check')}<span><b>Une équipe locale</b>, basée à Crissier, qui connaît la région lausannoise.</span></li>
      </ul>
      {estimator(rel) if not landing else cta_row(p, "Recevoir mon devis gratuit")}
      {'' if landing else f'<a class="link-arrow" href="{rel}fin-de-bail/">En savoir plus sur la fin de bail{ic("arrow")}</a>'}
    </div>
  </div>
</section>
"""


# ------------------------------------------------------------------ pages
POINTS_DEFAULT = [("reply", "Réponse rapide"), ("clock", "Disponible 7j/7"), ("pin", "Basés à Crissier")]


def page_shell(p, rel, body):
    return (head(p, rel) + "<body>\n" + SPRITE + header(p, rel) + f'<main id="contenu">\n{body}\n</main>\n' +
            footer(rel, p) + mobile_bar(p) + scripts(rel))


def build_home():
    rel = ""
    p = dict(
        path="", title="Entreprise de nettoyage à Lausanne · Devis gratuit · Viva Service24",
        desc="Nettoyage de fin de bail, vitres, panneaux solaires, chantiers et immeubles à Lausanne et dans tout le canton de Vaud. 5,0 sur Google, 7j/7. Devis gratuit.",
        h1='Nettoyage professionnel à <span class="hl">Lausanne</span> et dans tout le canton de Vaud',
        sub="Fin de bail, vitres, panneaux solaires, chantiers et immeubles. Intervention rapide, même en urgence, 7 jours sur 7.",
        hero="video", points=POINTS_DEFAULT, service=None,
        wa="Bonjour, je souhaite un devis.",
        wa_photos="Bonjour, je vous envoie des photos pour un devis.",
        wa_photos_label="Envoyez des photos de votre logement sur WhatsApp",
        preload=f'<link rel="preload" as="image" type="image/avif" imagesrcset="img/stock/hero-poster-768.avif 768w, img/stock/hero-poster-1280.avif 1280w, img/stock/hero-poster-1600.avif 1600w" imagesizes="100vw" fetchpriority="high">\n',
    )
    p["ld"] = [faq_ld(FAQ_HOME)]
    body = (hero(p, rel) + review_strip(["Amir Ali", "vXv Barber's", "Merita Rushiti"]) + trustbar() +
            bail_focus(rel, p) + services_grid(rel) + reviews(p, rel) +
            ba_pairs(rel, [BA_VITRINE, BA_CUISINE, BA_SDB], "Avant, après",
                     "La première comparaison montre une vraie intervention de notre équipe. Les deux autres sont des photos d'illustration, en attendant nos propres photos de chantiers.") +
            steps(p) + cas_client(rel, p) + about(rel, p) +
            field_videos(rel, [("vitrine-1", "Vitrine, lavage à la perche"), ("solaire-brosse", "Panneaux solaires, brosse à eau pure"),
                               ("solaire-toit", "Toit plat, panneaux solaires"), ("vitrine-3", "Vitrine, rinçage")]) +
            photo_band(rel, "stock/lausanne", "Lausanne, le port d'Ouchy au bord du Léman", "Basés à Crissier, aux portes de Lausanne.") +
            zone(rel, p) + faq(FAQ_HOME) + final_cta(p))
    return p, rel, body


def landing(path, **kw):
    p = dict(path=path, minimal=True, points=POINTS_DEFAULT)
    p.update(kw)
    return p


def build_bail():
    rel = "../"
    p = landing(
        "fin-de-bail/", title="Nettoyage fin de bail Lausanne · Devis gratuit · Viva Service24",
        desc="Nettoyage de fin de bail à Lausanne et dans le canton de Vaud, accepté par la régie. Dès CHF 350, vitres, stores et four compris. 5,0 sur Google. Devis gratuit.",
        h1='Nettoyage de fin de bail à Lausanne, <span class="hl">accepté par la régie</span>',
        sub="Un nettoyage complet avant l'état des lieux. Intervention rapide, même en urgence, 7 jours sur 7. Dès CHF 350, vitres, stores et four compris.",
        hero="video", service="Fin de bail",
        points=[("reply", "Réponse rapide"), ("clock", "Disponible 7j/7"), ("home", "Vitres, stores et four compris")],
        wa="Bonjour, je souhaite un devis pour un nettoyage de fin de bail.",
        wa_photos="Bonjour, je vous envoie des photos de mon logement pour un devis de fin de bail.",
        wa_photos_label="Envoyez des photos de votre logement sur WhatsApp",
        final_h="Votre état des lieux approche ? Demandez votre prix",
        preload=f'<link rel="preload" as="image" type="image/avif" imagesrcset="../img/stock/hero-poster-768.avif 768w, ../img/stock/hero-poster-1280.avif 1280w, ../img/stock/hero-poster-1600.avif 1600w" imagesizes="100vw" fetchpriority="high">\n',
    )
    p["ld"] = [service_ld("Nettoyage de fin de bail", "fin-de-bail/", "350",
                          "Nettoyage complet de fin de bail avant l'état des lieux : cuisine, four, salle de bain, vitres, stores, sols, armoires, balcon."),
               faq_ld(FAQ_BAIL)]
    groups = [
        ("Cuisine", "spark", ["Four : intérieur, grilles, plaques et porte vitrée", "Plaques de cuisson et crédence", "Hotte et filtres",
                              "Réfrigérateur et congélateur, dedans et dehors", "Armoires et tiroirs, dedans et dehors", "Évier, robinetterie et détartrage"],
         pic(rel, "stock/four-grille", "Nettoyage des grilles et de l'intérieur d'un four, gants de ménage", "(min-width: 980px) 280px, 45vw", cls="inc__img")),
        ("Salle de bain et WC", "drop", ["Baignoire, douche et parois vitrées", "Détartrage de la robinetterie et du carrelage", "Lavabo, miroir et armoire de toilette",
                                        "WC complet, dedans et dehors", "Joints et ventilation"],
         pic(rel, "stock/douche", "Paroi de douche nettoyée à la raclette", "(min-width: 980px) 280px, 45vw", cls="inc__img")),
        ("Fenêtres et stores", "window", ["Vitres, dedans et dehors", "Cadres, joints et rails", "Stores et volets", "Tablettes de fenêtre"],
         pic(rel, "stock/vitre-chiffon", "Vitre essuyée avec un chiffon microfibre", "(min-width: 980px) 280px, 45vw", cls="inc__img")),
        ("Pièces, sols et balcon", "home", ["Sols aspirés et lavés, plinthes", "Portes, poignées et interrupteurs", "Placards et armoires murales, dedans et dehors",
                                           "Radiateurs", "Balcon ou terrasse"],
         pic(rel, "stock/appart-vide-2", "Pièce vide au parquet propre", "(min-width: 980px) 280px, 45vw", cls="inc__img")),
    ]
    aside = (pull("Le plus important, c'est que la régie était satisfaite du résultat et a accepté le nettoyage sans aucun problème.", "Amir Ali") +
             estimator(rel))
    urg = f"""<section class="sec urg" aria-labelledby="urg-h">
  <div class="container urg__grid">
    <div class="urg__copy">
      <h2 id="urg-h">Une urgence ? Nous travaillons aussi le soir et le week-end</h2>
      <p>État des lieux avancé, déménagement qui déborde, imprévu de dernière minute : nous intervenons 7 jours sur 7 et 24h/24. Supplément urgence ou week-end de 20 à 50 %, toujours indiqué dans le devis.</p>
      <div class="cta-row"><a class="btn btn--primary" href="{TEL}">{ic('phone')}Appeler {PHONE_NB}</a><a class="btn btn--wa" href="{wa("Bonjour, j'ai besoin d'un nettoyage en urgence.")}" data-wa target="_blank" rel="noopener">{ic('wa')}Urgence sur WhatsApp</a></div>
    </div>
    {pull("j'ai réservé sur le site un nettoyage pour 01h00 du matin et le service étais effectué avec un très …", "Sagvane Suleyvani", "pq--light")}
  </div>
</section>
"""
    body = (hero(p, rel) + review_strip(["Amir Ali", "leila unkown", "Boran Karaca"]) + trustbar() +
            bail_focus(rel, p, landing=True) +
            inclus(groups, "Ce qui est inclus", "Le détail de ce que nous nettoyons, pièce par pièce. C'est aussi ce que la régie contrôle à l'état des lieux.") +
            prices_sec(p, bail_price_table(), aside, "Prix d'un nettoyage de fin de bail") +
            reviews(p, rel, "Ils ont rendu leurs clés tranquilles", filt="Fin de bail") +
            ba_pairs(rel, [BA_CUISINE, BA_SDB, BA_VITRINE], "Avant, après",
                     "Cuisine et salle de bain : photos d'illustration, en attendant nos propres photos de fins de bail. La vitrine est une vraie intervention de notre équipe.") +
            urg + steps(p) + about(rel, p) + zone(rel, p) + faq(FAQ_BAIL) + final_cta(p))
    return p, rel, body


def service_ld(name, path, min_price, desc):
    return {"@context": "https://schema.org", "@type": "Service", "name": name, "serviceType": name,
            "description": desc, "url": BASE_URL + path, "provider": {"@id": BASE_URL + "#entreprise"},
            "areaServed": [{"@type": "City", "name": "Lausanne"}, {"@type": "AdministrativeArea", "name": "Canton de Vaud"}],
            "offers": {"@type": "Offer", "priceCurrency": "CHF", "price": min_price,
                       "description": "Prix indicatif, devis exact gratuit et sans engagement"}}


def build_vitres():
    rel = "../"
    p = landing(
        "vitres/", title="Nettoyage de vitres Lausanne · Devis gratuit · Viva Service24",
        desc="Nettoyage de vitres, vitrines, baies vitrées et stores à Lausanne et dans le canton de Vaud. CHF 50 à 70 / h, sans traces. 5,0 sur Google. Devis gratuit.",
        h1='Nettoyage de vitres et vitrines à Lausanne, <span class="hl">sans traces</span>',
        sub="Fenêtres, baies vitrées, vérandas et vitrines de commerces, cadres et stores compris. Particuliers et commerces, 7 jours sur 7.",
        hero="stock/hero-vitres", service="Vitres",
        points=[("reply", "Réponse rapide"), ("clock", "Disponible 7j/7"), ("window", "Cadres et stores")],
        wa="Bonjour, je souhaite un devis pour un nettoyage de vitres.",
        wa_photos="Bonjour, je vous envoie des photos de mes vitres pour un devis.",
        wa_photos_label="Envoyez des photos de vos vitres sur WhatsApp",
        step3="On nettoie, vous profitez de la vue", step3_t="Nous intervenons à la date convenue, avec perche, raclettes et produits professionnels.",
        preload='<link rel="preload" as="image" type="image/avif" imagesrcset="../img/stock/hero-vitres-640.avif 640w, ../img/stock/hero-vitres-1000.avif 1000w, ../img/stock/hero-vitres-1600.avif 1600w" imagesizes="100vw" fetchpriority="high">\n',
    )
    p["ld"] = [service_ld("Nettoyage de vitres", "vitres/", "50", "Nettoyage de fenêtres, vitrines, baies vitrées, vérandas, cadres et stores."), faq_ld(FAQ_VITRES)]
    groups = [
        ("Vitres", "window", ["Vitres dedans et dehors", "Baies vitrées et portes-fenêtres", "Vérandas et verrières", "Velux et fenêtres de toit accessibles"]),
        ("Cadres et finitions", "spark", ["Cadres, joints et rails", "Tablettes de fenêtre", "Finition à la raclette, sans traces", "Essuyage des bords"]),
        ("Stores", "home", ["Stores à lamelles", "Stores en toile et volets", "Selon accès, sur demande"]),
        ("Commerces", "building", ["Vitrines et portes vitrées", "Enseignes vitrées accessibles", "Passages réguliers sur planning"]),
    ]
    rows = [("Nettoyage de vitres", "CHF 50 à 70 / h", "Selon la taille et le nombre de vitres")]
    aside = pull("le travail impeccable, aucune trace, tout propre, personnel super sympas. Je recommande !", "rafaela dias lima") + \
        f'<figure class="aside-photo">{pic(rel, "stock/vitre-raclette", "Raclette passée sur une vitre savonneuse", "(min-width: 980px) 380px, 90vw")}</figure>'
    body = (hero(p, rel) + review_strip(["vXv Barber's", "rafaela dias lima", "Izi bos"]) + trustbar() +
            inclus(groups, "Ce qui est inclus", "Ce que comprend un nettoyage de vitres. Dites-nous ce que vous voulez, le devis s'adapte.") +
            cas_client(rel, p) +
            prices_sec(p, simple_table("Nettoyage de vitres", rows), aside, "Prix du nettoyage de vitres") +
            ba_pairs(rel, [BA_VITRINE], "Avant, après", "Une vraie intervention : la vitrine du salon vXv Barber's à Crissier, pendant et après le lavage.") +
            reviews(p, rel, "Ce que disent nos clients", filt="Vitres") +
            field_videos(rel, [("vitrine-1", "Lavage d'une vitrine, Crissier"), ("vitrine-3", "Rinçage à la perche"), ("solaire-toit", "Panneaux solaires, toit plat")]) +
            steps(p) + zone(rel, p) + faq(FAQ_VITRES) + final_cta(p))
    return p, rel, body


def build_solaire():
    rel = "../"
    p = landing(
        "panneaux-solaires/", title="Nettoyage panneaux solaires Vaud · Eau pure · Viva Service24",
        desc="Nettoyage de panneaux solaires à l'eau pure, sans détergent, à Lausanne et dans tout le canton de Vaud. Dès CHF 180. Villas, immeubles, halles. Devis gratuit.",
        h1='Nettoyage de panneaux solaires <span class="hl">à l\'eau pure</span>, dans tout le canton de Vaud',
        sub="Sans produit chimique, sans traces ni calcaire. Villas, immeubles, halles industrielles et agricoles. Perche depuis le sol ou nacelle.",
        hero="stock/hero-solaire", service="Panneaux solaires",
        points=[("drop", "Eau pure, sans détergent"), ("clock", "Disponible 7j/7"), ("pin", "Basés à Crissier")],
        wa="Bonjour, je souhaite un devis pour le nettoyage de panneaux solaires.",
        wa_photos="Bonjour, je vous envoie des photos de mes panneaux solaires pour un devis.",
        wa_photos_label="Envoyez une photo de votre toit sur WhatsApp",
        step3="On nettoie, vos panneaux respirent", step3_t="Nous intervenons à la date convenue, avec notre système d'eau pure et notre matériel.",
        preload='<link rel="preload" as="image" type="image/avif" imagesrcset="../img/stock/hero-solaire-640.avif 640w, ../img/stock/hero-solaire-1000.avif 1000w, ../img/stock/hero-solaire-1600.avif 1600w" imagesizes="100vw" fetchpriority="high">\n',
    )
    p["ld"] = [service_ld("Nettoyage de panneaux solaires", "panneaux-solaires/", "180", "Nettoyage de panneaux solaires à l'eau pure, sans détergent."), faq_ld(FAQ_SOLAIRE)]
    method = f"""<section class="sec method" aria-labelledby="method-h">
  <div class="container method__grid">
    <div class="method__photos">
      <figure class="method__a">{pic(rel, "real/solaire-toit-vegetal", "Employé de Viva Service24 nettoyant des panneaux solaires sur un toit végétalisé, lac Léman en arrière-plan", "(min-width: 980px) 360px, 60vw")}</figure>
      <figure class="method__b vclip"><video muted playsinline loop preload="none" poster="{rel}img/real/poster-solaire-brosse-400.webp" data-autoplay data-src="{rel}video/real-solaire-brosse.mp4" aria-label="Vidéo : brosse à eau pure sur un panneau solaire"></video><figcaption>Brosse à eau pure, vidéo réelle</figcaption></figure>
    </div>
    <div class="method__copy">
      <h2 id="method-h">Notre méthode : de l'eau pure, filtrée sur place</h2>
      <p class="lead">Poussière, pollen, feuilles et fientes réduisent la production de vos panneaux. Nous les nettoyons avec de l'eau déminéralisée : elle détache les salissures et sèche sans laisser de traces ni de calcaire.</p>
      <ul class="ticks">
        <li>{ic('check')}<span><b>Eau pure par osmose</b>, aucun produit chimique</span></li>
        <li>{ic('check')}<span><b>Brosse douce</b>, adaptée au verre des modules</span></li>
        <li>{ic('check')}<span><b>Depuis le sol</b>, avec une perche télescopique</span></li>
        <li>{ic('check')}<span><b>Nacelle élévatrice</b> pour les toits difficiles d'accès</span></li>
        <li>{ic('check')}<span>Villas, immeubles, halles industrielles et agricoles</span></li>
      </ul>
      {cta_row(p, "Devis pour mes panneaux")}
    </div>
  </div>
</section>
"""
    rows = [("Petite installation", "dès CHF 180", ""), ("20 à 30 m²", "CHF 180 à 250", ""), ("30 à 50 m²", "CHF 250 à 350", ""), ("Grande installation", "sur devis", "Immeubles, halles, agricole")]
    aside = f'<figure class="aside-photo">{pic(rel, "real/equipe-tshirt", "Employé de Viva Service24 en t-shirt de l entreprise sur un toit de panneaux solaires", "(min-width: 980px) 420px, 90vw")}<figcaption>Notre équipe sur un toit à panneaux solaires.</figcaption></figure>'
    body = (hero(p, rel) + review_strip(["Merita Rushiti", "Izi bos", "Doris Polli"]) + trustbar() + method +
            prices_sec(p, simple_table("Nettoyage de panneaux solaires", rows, "Prix selon la surface des panneaux et l'accès."), aside, "Prix du nettoyage de panneaux solaires") +
            field_videos(rel, [("solaire-toit", "Toit plat, nettoyage à la perche"), ("solaire-brosse", "Brosse à eau pure")], "Sur le terrain", "Deux de nos interventions sur des toits de la région. Vidéos réelles, non retouchées.") +
            reviews(p, rel, "Ce que disent nos clients", filt="Panneaux solaires") +
            steps(p) + about(rel, p) + zone(rel, p) + faq(FAQ_SOLAIRE) + final_cta(p))
    return p, rel, body


def build_chantier():
    rel = "../"
    p = landing(
        "fin-de-chantier/", title="Nettoyage fin de chantier Lausanne · Devis gratuit · Viva Service24",
        desc="Nettoyage de fin de chantier et après rénovation à Lausanne et dans le canton de Vaud : poussière, plâtre, peinture, silicone. CHF 55 à 75 / h. Devis gratuit.",
        h1='Nettoyage de fin de chantier à Lausanne : <span class="hl">des locaux prêts à être occupés</span>',
        sub="Après construction ou rénovation : poussière fine, plâtre, peinture, silicone, vitres et sols. Pour les entreprises, les régies et les particuliers.",
        hero="stock/hero-chantier", service="Fin de chantier",
        points=[("reply", "Réponse rapide"), ("clock", "Disponible 7j/7"), ("helmet", "Entreprises et particuliers")],
        wa="Bonjour, je souhaite un devis pour un nettoyage de fin de chantier.",
        wa_photos="Bonjour, je vous envoie des photos du chantier pour un devis.",
        wa_photos_label="Envoyez des photos du chantier sur WhatsApp",
        step3="On nettoie, vous remettez les locaux", step3_t="Nous intervenons à la date convenue, avec notre matériel et nos produits professionnels.",
        preload='<link rel="preload" as="image" type="image/avif" imagesrcset="../img/stock/hero-chantier-640.avif 640w, ../img/stock/hero-chantier-1000.avif 1000w, ../img/stock/hero-chantier-1600.avif 1600w" imagesizes="100vw" fetchpriority="high">\n',
    )
    p["ld"] = [service_ld("Nettoyage de fin de chantier", "fin-de-chantier/", "55", "Nettoyage après construction ou rénovation : poussière, plâtre, peinture, silicone, vitres, sols."), faq_ld(FAQ_CHANTIER)]
    groups = [
        ("Poussière et résidus", "helmet", ["Poussière fine sur toutes les surfaces", "Traces de plâtre et de peinture", "Résidus de silicone et de colle", "Aspiration complète"],
         pic(rel, "stock/chantier", "Cuisine en fin de rénovation", "(min-width: 980px) 280px, 45vw", cls="inc__img")),
        ("Vitres et menuiseries", "window", ["Vitres, cadres et rails", "Retrait des autocollants et protections", "Portes, poignées, interrupteurs"],
         pic(rel, "stock/vitre-raclette", "Vitre nettoyée à la raclette", "(min-width: 980px) 280px, 45vw", cls="inc__img")),
        ("Sanitaires et cuisine", "drop", ["Sanitaires et carrelage", "Robinetterie", "Meubles de cuisine dedans et dehors"],
         pic(rel, "stock/sdb-vapeur", "Nettoyage du carrelage d'une salle de bain au nettoyeur vapeur", "(min-width: 980px) 280px, 45vw", cls="inc__img")),
        ("Sols", "home", ["Sols aspirés et lavés", "Plinthes", "Cages d'escalier et parties communes"],
         pic(rel, "stock/appart-vide", "Sol en parquet propre dans une pièce vide", "(min-width: 980px) 280px, 45vw", cls="inc__img")),
    ]
    rows = [("Nettoyage de fin de chantier", "CHF 55 à 75 / h", "Selon la surface, les étages et le nombre de bâtiments")]
    aside = f'<figure class="aside-photo">{pic(rel, "stock/evier", "Nettoyage d un évier en inox avec une éponge", "(min-width: 980px) 420px, 90vw")}</figure>'
    body = (hero(p, rel) + review_strip(["Izi bos", "Merita Rushiti", "Doris Polli"]) + trustbar() +
            inclus(groups, "Ce qui est inclus", "Nous remettons les locaux propres, prêts pour la remise des clés ou l'emménagement.") +
            prices_sec(p, simple_table("Fin de chantier", rows), aside, "Prix du nettoyage de fin de chantier") +
            reviews(p, rel, "Ce que disent nos clients", filt="Fin de chantier") +
            steps(p) + about(rel, p) + zone(rel, p) + faq(FAQ_CHANTIER) + final_cta(p))
    return p, rel, body


def build_immeubles():
    rel = "../"
    p = landing(
        "entretien-immeubles/", title="Entretien d'immeubles et conciergerie Lausanne · Viva Service24",
        desc="Entretien d'immeubles, bureaux, commerces et cages d'escalier, conciergerie, espaces verts et tags à Lausanne et dans le canton de Vaud. Dès CHF 45 / h. Devis gratuit.",
        h1='Entretien d\'immeubles, bureaux et <span class="hl">conciergerie</span> à Lausanne',
        sub="Cages d'escalier, parties communes, bureaux et commerces, sur un planning fixe. Conciergerie, espaces verts et suppression de tags. Un seul interlocuteur.",
        hero="stock/hero-immeuble", service="Immeuble / bureau",
        points=[("reply", "Réponse rapide"), ("building", "Régies et entreprises"), ("cal", "Planning fixe")],
        wa="Bonjour, je souhaite un devis pour l'entretien d'un immeuble ou de bureaux.",
        wa_photos="Bonjour, je souhaite un devis d'entretien. Voici quelques informations sur les locaux.",
        wa_photos_label="Décrivez vos locaux sur WhatsApp",
        step3="Nous passons selon le planning", step3_t="Quotidien, hebdomadaire ou mensuel : nous intervenons aux jours convenus, avec notre matériel.",
        final_h="Un contrat d'entretien ? Parlons-en",
        preload='<link rel="preload" as="image" type="image/avif" imagesrcset="../img/stock/hero-immeuble-640.avif 640w, ../img/stock/hero-immeuble-1000.avif 1000w, ../img/stock/hero-immeuble-1600.avif 1600w" imagesizes="100vw" fetchpriority="high">\n',
    )
    p["ld"] = [service_ld("Entretien d'immeubles et conciergerie", "entretien-immeubles/", "45", "Entretien d'immeubles, bureaux, commerces, cages d'escalier, conciergerie, espaces verts, suppression de tags."), faq_ld(FAQ_IMMEUBLE)]

    def block(i, sid, img, alt, h, t, items, price):
        li = "".join(f"<li>{ic('check')}<span>{x}</span></li>" for x in items)
        flip = " alt--flip" if i % 2 else ""
        return f"""<div class="alt{flip}" id="{sid}">
  <figure class="alt__img">{pic(rel, img, alt, "(min-width: 980px) 560px, 100vw")}</figure>
  <div class="alt__copy"><h3>{h}</h3><p>{t}</p><ul class="ticks ticks--sm">{li}</ul><p class="alt__price">{price}</p></div>
</div>"""
    blocks = "".join([
        block(0, "entretien", "stock/escalier", "Cage d'escalier d'immeuble", "Immeubles, bureaux et commerces",
              "Passages quotidiens, hebdomadaires ou mensuels selon un planning fixe.",
              ["Cages d'escalier et parties communes", "Bureaux, cabinets et commerces", "Sanitaires et cuisines d'entreprise", "Vitres des parties communes"], "CHF 45 à 50 / h"),
        block(1, "conciergerie", "stock/immeuble", "Immeuble résidentiel avec balcons", "Conciergerie",
              "Pour les immeubles et les centres commerciaux, en lien direct avec la gérance.",
              ["Entretien des parties communes", "Gestion des containers", "Contrôle des locaux techniques", "Suivi avec la gérance"], "CHF 50 à 60 / h"),
        block(2, "exterieurs", "stock/haie", "Taille d'une haie", "Espaces verts",
              "L'entretien de saison des extérieurs de votre immeuble ou de votre villa.",
              ["Tonte du gazon", "Taille des haies", "Désherbage", "Ramassage des feuilles"], "CHF 55 à 75 / h"),
        block(3, "tags", "stock/tags", "Volets roulants couverts de tags", "Tags et nettoyages spéciaux",
              "Graffitis sur façades, murs, portes de garage et mobilier. Méthode choisie selon le support. Remise en état après dégât d'eau, moquettes, logement encombré.",
              ["Crépi, pierre, béton, métal, bois", "Dégâts d'eau et sinistres", "Moquettes", "Logement très sale ou encombré"], "dès CHF 250 (forfait)"),
    ])
    services = f"""<section class="sec alts" aria-labelledby="alts-h">
  <div class="container">
    <div class="sec__head"><h2 id="alts-h">Nos prestations pour les immeubles et les entreprises</h2><p>Contrats réguliers ou interventions ponctuelles. {PRICE_NOTE}</p></div>
    {blocks}
  </div>
</section>
"""
    rows = [("Entretien d'immeubles, bureaux, commerces", "CHF 45 à 50 / h", "Cages d'escalier comprises"), ("Conciergerie", "CHF 50 à 60 / h", "Immeubles, centres commerciaux"),
            ("Espaces verts", "CHF 55 à 75 / h", ""), ("Suppression de tags", "dès CHF 250", "Forfait"), ("Nettoyages spéciaux", "dès CHF 250", "Dégâts d'eau, moquettes, remise en état")]
    aside = f'<figure class="aside-photo">{pic(rel, "stock/bureau", "Aspiration de la moquette d un bureau", "(min-width: 980px) 420px, 90vw")}</figure>'
    body = (hero(p, rel) + review_strip(["Izi bos", "vXvbarbercrissier", "Doris Polli"]) + trustbar() + services +
            prices_sec(p, simple_table("Entretien et conciergerie", rows), aside, "Nos tarifs") +
            reviews(p, rel, "Ce que disent nos clients", filt="Immeuble") +
            steps(p) + about(rel, p) + zone(rel, p) + faq(FAQ_IMMEUBLE) + final_cta(p))
    return p, rel, body


def simple_page(path, title, desc, h1, content, rel="../", noindex=False, extra_js="", base_fix=""):
    p = dict(path=path, title=title, desc=desc, minimal=True, wa="Bonjour, je souhaite un devis.", noindex=noindex, base_fix=base_fix,
             form_href=(rel or "./") + "#devis")
    body = f'<section class="page"><div class="container page__in"><h1>{h1}</h1>{content}</div></section>'
    return (head(p, rel) + "<body class=\"is-simple\">\n" + SPRITE + header(p, rel) + f'<main id="contenu">\n{body}\n</main>\n' +
            footer(rel, p) + mobile_bar(p) + scripts(rel, extra_js))


def build_merci():
    content = f"""<div class="merci">
  <p class="merci__lead" data-merci-name>Votre demande est bien envoyée.</p>
  <p>Nous vous rappelons rapidement pour fixer les détails et vous donner un prix. Gardez votre téléphone à portée de main.</p>
  <div class="merci__box">
    <p><b>C'est urgent ?</b> Appelez-nous directement, 7 jours sur 7.</p>
    <div class="cta-row"><a class="btn btn--primary btn--lg" href="{TEL}">{ic('phone')}{PHONE_NB}</a>
    <a class="btn btn--wa btn--lg" href="{wa('Bonjour, je viens d envoyer une demande de devis sur votre site.')}" data-wa target="_blank" rel="noopener">{ic('wa')}WhatsApp</a></div>
  </div>
  <a class="gbadge gbadge--dark" href="{GOOGLE}" target="_blank" rel="noopener">{ic('g', 'ic ic--g')}<b>5,0</b>{STARS}<span>16 avis Google</span></a>
  <p><a class="link-arrow" href="../">{ic('back')}Retour à l'accueil</a></p>
</div>"""
    return simple_page("merci/", "Merci, votre demande est envoyée · Viva Service24",
                       "Votre demande de devis a bien été envoyée à Viva Service24. Nous vous rappelons rapidement.",
                       "Merci !", content, noindex=True, extra_js='\n<script>window.VIVA_PAGE="merci"</script>')


def build_legal():
    content = f"""<div class="prose">
<p class="muted">Dernière mise à jour : 20 octobre 2026</p>
<h2>Éditeur du site</h2>
<p><b>Viva service24 Sàrl</b><br>Société à responsabilité limitée de droit suisse<br>Rue du Jura 11, 1023 Crissier, Suisse</p>
<p>Téléphone : <a href="{TEL}">+41 76 741 25 27</a><br>E-mail : <a href="mailto:{EMAIL}">{EMAIL}</a></p>
<p>Inscrite au registre du commerce du canton de Vaud<br>IDE : CHE-391.619.790<br>TVA : non assujettie</p>
<h2>Hébergement</h2>
<p>Ce site est hébergé par GitHub Pages, un service de GitHub, Inc., 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, États-Unis.</p>
<h2>Photographies et vidéos</h2>
<p>Les photos et vidéos présentées comme réelles montrent des interventions réalisées par Viva Service24. Les autres photographies sont des images d'illustration issues des banques d'images Unsplash et Pexels, utilisées conformément à leur licence. Elles ne représentent pas des interventions de l'entreprise.</p>
<h2>Prix et contenu</h2>
<p>Les prix affichés sont indicatifs et ne constituent pas une offre contractuelle. Les prestations, les délais et les prix sont fixés dans le devis écrit remis au client : seul ce devis accepté fait foi.</p>
<h2>Avis clients</h2>
<p>Les avis affichés proviennent de la fiche Google de l'entreprise. Ils sont reproduits tels quels, sans correction.</p>
<h2>Propriété intellectuelle</h2>
<p>Les textes, la mise en page, le nom et le logotype Viva Service24 sont protégés. Toute reproduction sans autorisation écrite préalable est interdite.</p>
<h2>Responsabilité</h2>
<p>Dans les limites autorisées par la loi, nous déclinons toute responsabilité pour les dommages résultant de l'accès au site, de son utilisation ou d'une indisponibilité temporaire. Les liens vers des sites tiers sont fournis à titre d'information.</p>
<h2>Droit applicable</h2>
<p>Le présent site est soumis au droit suisse. Le for est au siège de l'entreprise, sous réserve des fors impératifs prévus par la loi.</p>
<p>Le traitement des données personnelles est décrit dans la page <a href="../confidentialite/">Protection des données</a>.</p>
</div>"""
    return simple_page("mentions-legales/", "Mentions légales · Viva Service24", "Mentions légales du site de Viva service24 Sàrl, entreprise de nettoyage à Crissier.",
                       "Mentions légales", content)


def build_privacy():
    content = f"""<div class="prose">
<p class="muted">Dernière mise à jour : 20 octobre 2026</p>
<p>Cette page explique quelles données personnelles nous traitons via ce site, pourquoi, et quels sont vos droits, conformément à la loi fédérale sur la protection des données (nLPD) et, lorsqu'il s'applique, au RGPD.</p>
<h2>Responsable du traitement</h2>
<p>Viva service24 Sàrl, Rue du Jura 11, 1023 Crissier, Suisse. Contact : <a href="mailto:{EMAIL}">{EMAIL}</a>, <a href="{TEL}">+41 76 741 25 27</a>.</p>
<h2>Formulaire de demande de devis</h2>
<p>Lorsque vous envoyez le formulaire, nous recevons : le service souhaité, la taille du logement, la date souhaitée, vos nom et prénom, votre numéro de téléphone, votre localité, votre adresse e-mail et votre message si vous les indiquez, ainsi que la page d'où vous écrivez et, si vous arrivez depuis une annonce, les paramètres de campagne de l'adresse (par exemple gclid, utm_source).</p>
<p><b>But :</b> vous recontacter et établir un devis (mesures précontractuelles). Nous ne vendons pas vos données et ne les utilisons pas pour de la prospection sans votre accord.</p>
<p><b>Sous-traitant :</b> le formulaire est transmis par le service FormSubmit (formsubmit.co), qui nous l'envoie par e-mail. Ce service peut traiter les données hors de Suisse. Nos e-mails sont conservés par notre fournisseur de messagerie.</p>
<p><b>Durée :</b> les demandes sans suite sont supprimées au plus tard après 12 mois. Les données liées à un mandat sont conservées selon nos obligations légales (comptabilité : 10 ans).</p>
<h2>WhatsApp et téléphone</h2>
<p>Les boutons WhatsApp sont de simples liens : rien n'est transmis à WhatsApp tant que vous ne cliquez pas. Si vous nous écrivez sur WhatsApp, vos messages et votre numéro sont aussi traités par WhatsApp (Meta Platforms), y compris hors de Suisse, selon ses propres conditions.</p>
<h2>Hébergement et journaux techniques</h2>
<p>Le site est hébergé par GitHub Pages (GitHub, Inc., États-Unis). Lors de chaque visite, GitHub enregistre des données techniques comme l'adresse IP, à des fins de sécurité et de bon fonctionnement.</p>
<h2>Mesure des demandes (Google Ads)</h2>
<p>Si nous activons la mesure des conversions Google Ads, le site charge le script Google (gtag.js) pour savoir combien de demandes, d'appels et de messages WhatsApp proviennent de nos annonces. Google peut déposer des cookies et traiter des données hors de Suisse. Un bandeau vous en informe et vous permet de refuser. Tant que cette mesure n'est pas activée, le site ne dépose aucun cookie et ne charge aucun outil de mesure.</p>
<p>Le site enregistre dans votre navigateur (stockage de session) les paramètres de campagne de l'adresse, pour les joindre à votre demande. Ils sont effacés à la fermeture de l'onglet.</p>
<h2>Vos droits</h2>
<p>Vous pouvez demander à accéder à vos données, à les faire rectifier ou supprimer, ou vous opposer à leur traitement, en écrivant à <a href="mailto:{EMAIL}">{EMAIL}</a>. Vous pouvez aussi vous adresser au Préposé fédéral à la protection des données et à la transparence (PFPDT).</p>
</div>"""
    return simple_page("confidentialite/", "Protection des données · Viva Service24",
                       "Protection des données du site Viva Service24 : données du formulaire de devis, sous-traitants, durée de conservation et vos droits (nLPD).",
                       "Protection des données", content)


def build_404():
    base_fix = ("<script>(function(){var p=location.pathname.split('/');var b=location.hostname.slice(-10)==='github.io'&&p.length>2?'/'+p[1]+'/':'/';"
                "document.write('<base href=\"'+b+'\">');})()</script>\n")
    content = f"""<div class="merci">
  <p class="merci__lead">Cette page n'existe pas ou a été déplacée.</p>
  <p>Vous cherchiez peut-être l'un de nos services :</p>
  <ul class="ticks">{''.join(f'<li>{ic("arrow")}<a href="{h}">{l}</a></li>' for h, l in NAV)}</ul>
  <div class="cta-row"><a class="btn btn--primary" href="./">Retour à l'accueil</a><a class="btn btn--ghost" href="{TEL}">{ic('phone')}{PHONE_NB}</a></div>
</div>"""
    return simple_page("404.html", "Page introuvable · Viva Service24", "Cette page n'existe pas. Retrouvez nos services de nettoyage à Lausanne.",
                       "Page introuvable", content, rel="", noindex=True, base_fix=base_fix)


# ------------------------------------------------------------------ typography + write
NB_RULES = [(" ?", " ?"), (" !", " !"), (" :", " :"), (" ;", " ;"), ("« ", "« "), (" »", " »"),
            ("CHF ", "CHF "), (" %", " %"), (" / h", " / h"), ("7j/7", "7j/7"), (" m²", " m²")]


def typo(doc):
    parts = re.split(r"(<script[\s\S]*?</script>|<style[\s\S]*?</style>|<[^>]+>)", doc)
    for i in range(0, len(parts), 2):
        t = parts[i]
        for a, b in NB_RULES:
            t = t.replace(a, b)
        t = t.replace(PHONE, PHONE_NB)
        parts[i] = t
    return "".join(parts)


def write(rel_path, doc):
    out = ROOT / rel_path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(typo(doc))
    print("wrote", rel_path, f"{len(doc) // 1024} KB")


def main():
    pages = [("index.html", build_home), ("fin-de-bail/index.html", build_bail), ("vitres/index.html", build_vitres),
             ("panneaux-solaires/index.html", build_solaire), ("fin-de-chantier/index.html", build_chantier),
             ("entretien-immeubles/index.html", build_immeubles)]
    for f, fn in pages:
        p, rel, body = fn()
        write(f, page_shell(p, rel, body))
    write("merci/index.html", build_merci())
    write("mentions-legales/index.html", build_legal())
    write("confidentialite/index.html", build_privacy())
    write("404.html", build_404())

    urls = ["", "fin-de-bail/", "vitres/", "panneaux-solaires/", "fin-de-chantier/", "entretien-immeubles/", "mentions-legales/", "confidentialite/"]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
        f"  <url><loc>{BASE_URL}{u}</loc><lastmod>2026-10-20</lastmod><priority>{'1.0' if u in ('', 'fin-de-bail/') else '0.8' if 'legal' not in u and 'confid' not in u and 'mentions' not in u else '0.2'}</priority></url>\n"
        for u in urls) + "</urlset>\n"
    (ROOT / "sitemap.xml").write_text(sm)
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /merci/\n\nSitemap: {BASE_URL}sitemap.xml\n")
    print("wrote sitemap.xml, robots.txt")


if __name__ == "__main__":
    main()
