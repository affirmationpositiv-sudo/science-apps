#!/usr/bin/env python3
"""Bulk SEO-Seiten Generator – 20+ Traffic-Seiten auf einmal (0,00€)"""
import os

CDIR = "/Users/f.cinar/Desktop/gh-pages/traffic"
os.makedirs(CDIR, exist_ok=True)

SHOP = "https://affirmationpositiv-sudo.github.io/science-apps/40projekte/"
BOT = "https://t.me/Yesaryour_bot"
PAYPAL = "affirmation.positiv@gmail.com"

pages = [
    "KI-Automation-Starter", "Passives-Einkommen-KI", "ChatGPT-Business-Tools",
    "Telegram-Bot-Verkauf", "KI-Bilder-Service", "Online-Coaching-KI",
    "Digitale-Produkte-verkaufen", "KI-Text-Service", "Affiliate-Marketing-KI",
    "SEO-mit-KI-Tools", "Social-Media-Automation", "Email-Marketing-KI",
    "Kunden-Akquise-automatisch", "KI-Business-Plan", "Online-Kurs-erstellen",
    "KI-Vorlagen-Pakete", "Newsletter-Automation", "KI-Analytics-Tools",
    "Webdesign-mit-KI", "KI-Workflow-Automation",
    "Freelancer-KI-Tools", "Existenzgruendung-KI", "Nebenverdienst-KI",
    "KI-Produktivitaet", "Zeitmanagement-KI",
]

TEMPLATE = """<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} – Ratgeber 2026</title>
<meta name="description" content="Praktischer Ratgeber zu {title}. Tipps, Tools und Strategien.">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,sans-serif;background:#0a0a0a;color:#e0e0e0;line-height:1.8;padding:20px}}
.container{{max-width:800px;margin:0 auto;padding:20px}}
h1{{color:#d4a843;font-size:2em;margin-bottom:20px}}
h2{{color:#fff;margin:30px 0 15px}}
p{{color:#999;margin-bottom:15px}}
.cta{{background:#111;border:1px solid #d4a843;border-radius:12px;padding:30px;margin:40px 0;text-align:center}}
.cta h3{{color:#d4a843;margin-bottom:10px}}
.btn{{display:inline-block;padding:12px 30px;border-radius:8px;background:#d4a843;color:#0a0a0a;text-decoration:none;font-weight:600;margin:10px}}
.btn-sec{{display:inline-block;padding:12px 30px;border-radius:8px;background:#222;color:#e0e0e0;text-decoration:none;border:1px solid #333;margin:10px}}
footer{{text-align:center;color:#555;padding:40px 0;border-top:1px solid #1a1a1a;margin-top:40px}}
footer a{{color:#888;text-decoration:none}}
</style>
</head>
<body>
<div class="container">
<h1>{title}</h1>
<p class="meta">IKUNE Verlag – 2026</p>
<p>In diesem Ratgeber erfaehrst du alles Wichtige zu <strong>{title}</strong>. Praktische Tipps, nuetzliche Tools und bewaehrte Strategien.</p>
<h2>So startest du noch heute</h2>
<p>Der einfachste Weg: Nutze unseren Telegram Bot <strong>@Yesaryour_bot</strong>. Alle Tools, Vorlagen und Services – ab 3 Stars oder per PayPal.</p>
<div class="cta">
<h3>Bereit durchzustarten?</h3>
<a class="btn" href="{bot}">Telegram Bot</a>
<a class="btn-sec" href="{shop}">Shop</a>
<p style="margin-top:15px;color:#666;">PayPal: {paypal}</p>
</div>
<footer>
<a href="../impressum/">Impressum</a> - <a href="../datenschutz/">Datenschutz</a><br>
IKUNE Verlag
</footer>
</div>
</body>
</html>"""

for slug in pages:
    title = slug.replace("-", " ")
    html = TEMPLATE.format(title=title, bot=BOT, shop=SHOP, paypal=PAYPAL)
    with open(f"{CDIR}/{slug}.html", "w") as f:
        f.write(html)
    print(f"  {slug}.html")

# Sitemap
sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for slug in pages:
    sitemap += f'  <url><loc>https://affirmationpositiv-sudo.github.io/science-apps/traffic/{slug}.html</loc><changefreq>monthly</changefreq><priority>0.6</priority></url>\n'
sitemap += '</urlset>'
with open("/Users/f.cinar/Desktop/gh-pages/sitemap_traffic.xml", "w") as f:
    f.write(sitemap)

print(f"\n✅ {len(pages)} Traffic-Seiten erstellt + Sitemap")
print(f"💰 Kosten: 0,00€")
