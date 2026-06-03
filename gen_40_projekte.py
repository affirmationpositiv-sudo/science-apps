#!/usr/bin/env python3
"""Generate 40 real money-generating project pages with PayPal buy buttons."""

import os
import json

BASE = "/Users/f.cinar/Desktop/gh-pages/40projekte"
os.makedirs(BASE, exist_ok=True)

projects = [
    ("ki-texte", "KI Texte-Service", 49, "Blogartikel, Produktbeschreibungen, Newsletter – ich schreibe für dich mit KI. 10 professionelle Artikel, fertig in 48h.", "einmalig"),
    ("ki-bilder", "KI Bilder-Service", 29, "50 einzigartige KI-Bilder für deine Website, Social Media oder Produkte. Midjourney-Qualität, kommerziell nutzbar.", "einmalig"),
    ("ki-bot-bau", "KI Bot-Bau", 79, "Massgeschneiderter Telegram-Bot für dein Business. Automatische Antworten, Bestellungen, Kundenbetreuung – 24/7.", "einmalig"),
    ("ki-automation-starter", "KI Automation Starter", 49, "Eine einfache KI-Automation für dein Business. Wiederkehrende Aufgaben erledigt sich von selbst. Inkl. 30 Min Setup-Call.", "einmalig"),
    ("ki-automation-pro", "KI Automation Pro", 197, "Komplette Geschäftsprozesse automatisiert. Leads, E-Mails, Rechnungen, Social Media – alles läuft von allein. Inkl. 2h Call.", "einmalig"),
    ("ki-automation-enterprise", "KI Automation Enterprise", 497, "Massiv skalieren mit KI. Maßgeschneiderte Automation für dein ganzes Unternehmen. VIP-Support, 1 Monat Begleitung.", "einmalig"),
    ("prompt-pack-1", "KI Prompt-Pack Volume 1", 9, "50 profitable KI-Prompts für Marketing, Vertrieb und Content. Einfach kopieren, einfügen, Geld verdienen.", "einmalig"),
    ("prompt-pack-2", "KI Prompt-Pack Volume 2", 9, "50 fortgeschrittene Prompts für Business-Analyse, Strategie und Automatisierung. Dein KI-Coach im Taschenformat.", "einmalig"),
    ("prompt-pack-3", "KI Prompt-Pack Volume 3", 9, "50 KI-Prompts speziell für deutsche Unternehmer: Steuern, Recht, Personal – KI-gestützte Entscheidungen.", "einmalig"),
    ("coaching-30min", "30-Min-KI-Coaching", 29, "30 Minuten 1:1 KI-Coaching per Video-Call. Deine Fragen, meine Antworten. Schnell, konkret, umsetzbar.", "einmalig"),
    ("coaching-60min", "60-Min-KI-Coaching", 49, "Eine Stunde intensives KI-Coaching. Strategie, Tools, Umsetzung. Inkl. Zusammenfassung und Aktionsplan.", "einmalig"),
    ("business-booster", "Business Booster 3h", 97, "3 Stunden Power-Session: Dein komplettes Business auf KI umgestellt. Inkl. fertige Automation, die sofort läuft.", "einmalig"),
    ("vip-tag", "VIP-KI-Tag (8h)", 197, "Ein ganzer Tag mit mir. Ich baue dir alles, was du brauchst: Bots, Automationen, Strategie. Komplett-Setup in 8 Stunden.", "einmalig"),
    ("strategie-call", "KI-Strategie-Call 45min", 79, "45 Minuten Strategie-Beratung. Ich analysiere dein Business und zeige dir genau, wo KI dir Geld spart oder einbringt.", "einmalig"),
    ("notion-planner", "Notion Business Planner", 7, "Komplette Notion-Vorlage für dein Business: Aufgaben, Ziele, Finanzen, Kunden. Strukturiert, übersichtlich, motivierend.", "einmalig"),
    ("excel-rechner", "Excel Gewinn-Rechner", 5, "Fertiger Excel-Rechner: Umsatz, Kosten, Gewinn, Steuern – auf einen Blick. Inkl. 5-Jahres-Prognose.", "einmalig"),
    ("social-plan", "Social Media Content Plan", 9, "30-Tage-Content-Plan für Instagram, LinkedIn & Co. Fertige Posts, Bilder, Hashtags. Einfach übernehmen und posten.", "einmalig"),
    ("newsletter-vorlagen", "Newsletter-Vorlagen-Paket", 9, "10 professionelle E-Mail-Vorlagen für Willkommen, Angebot, Follow-up, Verkauf. Zum sofort Verwenden.", "einmalig"),
    ("email-sequenzen", "E-Mail-Sequenzen Paket", 12, "5 automatisierte E-Mail-Sequenzen: Willkommen, Verkauf, Wiederbelebung, Empfehlung, Abschluss. Inkl. Betreffzeilen.", "einmalig"),
    ("businessplan-vorlage", "Business Plan Vorlage", 8, "Professionelle Businessplan-Vorlage für Gründung oder Finanzierung. Alle Kapitel, inkl. Finanzplan.", "einmalig"),
    ("marketing-strategie", "Marketing Strategie Vorlage", 10, "Komplette Marketing-Strategie zum Ausfüllen. Zielgruppe, Kanäle, Budget, Timeline. Dein Fahrplan zum Erfolg.", "einmalig"),
    ("produktivitaet", "Produktivitäts-System Vorlage", 7, "Dein persönliches Produktivitätssystem: Aufgaben, Projekte, Gewohnheiten, Reflexion. Basiert auf Getting Things Done.", "einmalig"),
    ("kundenakquise", "Kundenakquise Playbook", 15, "10 konkrete Methoden, um sofort Kunden zu gewinnen. Schritt-für-Schritt-Anleitung mit Skripten für Anruf und E-Mail.", "einmalig"),
    ("leadmagnete", "Lead-Magnet Vorlagen Paket", 5, "5 fertige Lead-Magnete: Checkliste, PDF-Guide, Vorlage, Quiz, Webinar. Inkl. E-Mail-Vorlage zur Bewerbung.", "einmalig"),
    ("cv-optimierung", "CV/Lebenslauf Optimierung", 19, "KI-gestützte Optimierung deines Lebenslaufs. Modernes Design, ATS-kompatibel, personalisiert auf deine Wunschposition.", "einmalig"),
    ("linkedin-optimierung", "LinkedIn Profil Optimierung", 29, "Dein LinkedIn-Profil wird zur Kundenmaschine. Headline, About, Experience, Featured – alles optimiert für Sichtbarkeit.", "einmalig"),
    ("seo-check", "SEO Quick-Check", 29, "Ich prüfe deine Website auf 30+ SEO-Faktoren. Report mit konkreten Verbesserungen – in 24h.", "einmalig"),
    ("website-texte", "Website Texte Service", 49, "Professionelle Texte für deine Website: Homepage, Über uns, Leistungen, Kontakt. KI-optimiert, menschengeschrieben.", "einmalig"),
    ("social-media-management", "Social Media Management", 97, "Ich manage deine Social Media Kanäle: 10 Posts/Woche, Stories, Antworten. 1 Monat, feste Rate, kündbar.", "monatlich"),
    ("newsletter-service", "E-Mail Newsletter Service", 49, "Ich schreibe und versende deinen Newsletter: 4 Ausgaben/Monat, inkl. Vorlagen und Analyse. Fertig für dein Business.", "monatlich"),
    ("ki-grundlagen-kurs", "KI Grundlagen Mini-Kurs", 19, "5 Lektionen: Was ist KI, wie nutze ich sie, welche Tools, wie verdiene ich Geld damit. PDF + Video-Links.", "einmalig"),
    ("passive-income-guide", "Passive Income Strategie Guide", 14, "10 bewährte passive Einkommensquellen mit KI. Schritt-für-Schritt-Aufbau, Kosten, Zeitaufwand. Inkl. Checkliste.", "einmalig"),
    ("sales-copy-guide", "Sales Copy Guide", 12, "Schreibe Texte, die verkaufen. Formeln, Beispiele, Vorlagen für Anzeigen, Landing Pages, E-Mails.", "einmalig"),
    ("chatgpt-guide", "ChatGPT Mastery Guide", 9, "50 fortgeschrittene ChatGPT-Techniken für Business, Content und Automatisierung. Inkl. Prompt-Bibliothek.", "einmalig"),
    ("ki-tools-uebersicht", "KI Tools Übersicht 2026", 7, "Die 100 wichtigsten KI-Tools für Business, Kreativität und Produktivität. Mit Bewertungen und Preisen.", "einmalig"),
    ("telegram-premium", "Telegram Premium Gruppe", 9, "Exklusive Telegram-Gruppe: Tägliche KI-Tipps, Vorlagen, exklusive Angebote. Direkter Austausch mit mir und anderen.", "monatlich"),
    ("newsletter-premium", "Premium Newsletter", 7, "Wöchentliche KI-Strategien und Insider-Tipps. Exklusive Tools, Early Access zu neuen Produkten, Rabatte.", "monatlich"),
    ("whatsapp-ki-tipps", "KI Tipps WhatsApp", 5, "Täglich eine KI-Empfehlung per WhatsApp. Kurz, praktisch, sofort umsetzbar. 30 Tage – kündbar.", "monatlich"),
    ("ki-news-weekly", "KI News Weekly", 3, "Wöchentliche Zusammenfassung der wichtigsten KI-Entwicklungen. Kurz, relevant, auf Deutsch. Per E-Mail.", "monatlich"),
    ("business-tools", "Business Tools Zugang", 19, "Zugang zu allen meinen Business-Vorlagen, Rechnern und Tools. Monatlich neue Inhalte. Jederzeit kündbar.", "monatlich"),
]

PAYPAL_EMAIL = "affirmation.positiv@gmail.com"

# Build index
pages = []

for slug, name, price, desc, billing in projects:
    price_str = f"{price}€"
    billing_text = "pro Monat" if billing == "monatlich" else "einmalig"
    
    # PayPal direct payment link
    paypal_link = f"https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business={PAYPAL_EMAIL}&item_name={name}&currency_code=EUR&amount={price}"
    
    html = f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{name} kaufen – {price} – Licht & Schatten Verlag</title>
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ font-family: -apple-system, 'Segoe UI', sans-serif; background: #0a0a0a; color: #e0e0e0; line-height: 1.6; }}
  .container {{ max-width: 700px; margin: 0 auto; padding: 40px 20px; }}
  .badge {{ display: inline-block; background: #1a1a1a; color: #d4a843; padding: 4px 12px; border-radius: 20px; font-size: .8em; border: 1px solid #333; margin-bottom: 20px; }}
  h1 {{ font-size: 2em; color: #fff; margin-bottom: 10px; }}
  .price-tag {{ font-size: 2.5em; color: #d4a843; font-weight: 700; margin: 20px 0; }}
  .price-tag small {{ font-size: .5em; color: #888; }}
  .description {{ color: #999; font-size: 1.1em; margin-bottom: 30px; }}
  .delivery {{ background: #111; border: 1px solid #222; border-radius: 12px; padding: 20px; margin: 20px 0; }}
  .delivery h3 {{ color: #d4a843; margin-bottom: 10px; }}
  .delivery p {{ color: #888; }}
  .btn-paypal {{ display: inline-block; width: 100%; padding: 18px; border-radius: 12px; border: none; background: #ffc439; color: #0a0a0a; font-size: 1.2em; font-weight: 700; text-align: center; text-decoration: none; cursor: pointer; transition: transform .2s; }}
  .btn-paypal:hover {{ transform: translateY(-2px); background: #ffd45c; }}
  .btn-paypal img {{ vertical-align: middle; height: 24px; margin-right: 8px; }}
  .back {{ display: inline-block; margin-top: 30px; color: #d4a843; text-decoration: none; }}
  .back:hover {{ text-decoration: underline; }}
  .features {{ margin: 30px 0; }}
  .features li {{ color: #999; padding: 8px 0; list-style: none; }}
  .features li:before {{ content: "✓ "; color: #d4a843; }}
  .guarantee {{ text-align: center; padding: 20px; border: 1px solid #333; border-radius: 12px; margin: 30px 0; }}
  .guarantee h3 {{ color: #d4a843; margin-bottom: 5px; }}
  .guarantee p {{ color: #666; font-size: .9em; }}
</style>
</head>
<body>
<div class="container">
  <div class="badge">{billing_text}</div>
  <h1>{name}</h1>
  <div class="price-tag">{price_str} <small>{billing_text}</small></div>
  <p class="description">{desc}</p>
  
  <ul class="features">
    <li>Sofort-Zugang nach Zahlung</li>
    <li>Deutsche Anleitung & Support</li>
    <li>100% Zufriedenheits-Garantie</li>
    <li>Keine versteckten Kosten</li>
  </ul>
  
  <a href="{paypal_link}" target="_blank" class="btn-paypal">
    💳 Jetzt kaufen – {price_str}
  </a>
  
  <div class="delivery">
    <h3>📦 So funktioniert's</h3>
    <p>1. Klicke auf "Jetzt kaufen"<br>
    2. Bezahle sicher per PayPal (oder Kreditkarte)<br>
    3. Du erhältst dein Produkt innerhalb von 24h per E-Mail<br>
    4. Bei Fragen: Telegram @Yesaryour_bot</p>
  </div>
  
  <div class="guarantee">
    <h3>🔒 Sichere Zahlung</h3>
    <p>Zahlung via PayPal – Käuferschutz inklusive. Deine Daten sind sicher.</p>
  </div>
  
  <a href="../" class="back">← Zurück zur Übersicht</a>
</div>
</body>
</html>"""
    
    filepath = os.path.join(BASE, f"{slug}.html")
    with open(filepath, "w") as f:
        f.write(html)
    print(f"✅ {slug}.html – {name} – {price}€")
    pages.append((slug, name, price, billing))

# Generate index page
index_html = """<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>40 Geldquellen – Shop – Licht & Schatten Verlag</title>
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  body { font-family: -apple-system, 'Segoe UI', sans-serif; background: #0a0a0a; color: #e0e0e0; line-height: 1.6; }
  .container { max-width: 1000px; margin: 0 auto; padding: 40px 20px; }
  header { text-align: center; margin-bottom: 50px; }
  header h1 { color: #d4a843; font-size: 2.5em; margin-bottom: 10px; }
  header p { color: #888; font-size: 1.1em; }
  .projects { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; }
  .project-card { background: #111; border: 1px solid #222; border-radius: 12px; padding: 20px; transition: all .3s; }
  .project-card:hover { border-color: #d4a843; transform: translateY(-4px); box-shadow: 0 20px 40px rgba(0,0,0,.4); }
  .project-card h3 { color: #fff; margin-bottom: 5px; }
  .project-card .price { color: #d4a843; font-weight: 700; font-size: 1.2em; }
  .project-card p { color: #888; font-size: .9em; margin: 10px 0; }
  .project-card .badge { display: inline-block; background: #1a1a1a; color: #888; padding: 2px 8px; border-radius: 10px; font-size: .75em; border: 1px solid #333; }
  .project-card a { display: inline-block; margin-top: 10px; color: #d4a843; text-decoration: none; font-weight: 600; }
  .project-card a:hover { text-decoration: underline; }
  .stats { text-align: center; padding: 30px; background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%); border-radius: 12px; margin-bottom: 40px; border: 1px solid #222; }
  .stats h2 { color: #fff; font-size: 2em; }
  .stats .count { color: #d4a843; font-size: 3em; font-weight: 700; }
  .stats p { color: #888; margin-top: 5px; }
  .paypal-info { text-align: center; background: #111; border: 1px solid #222; border-radius: 12px; padding: 20px; margin-top: 40px; }
  .paypal-info h3 { color: #d4a843; }
  footer { text-align: center; color: #555; padding: 40px 0 20px; font-size: .85em; border-top: 1px solid #1a1a1a; margin-top: 40px; }
  footer a { color: #888; text-decoration: none; }
  .categories { display: flex; gap: 10px; flex-wrap: wrap; justify-content: center; margin-bottom: 40px; }
  .category { background: #1a1a1a; color: #888; padding: 8px 16px; border-radius: 20px; font-size: .85em; border: 1px solid #222; }
</style>
</head>
<body>
<div class="container">
  <header>
    <h1>🛒 40 Geldquellen – Shop</h1>
    <p>Echte Produkte & Dienstleistungen. Bezahle sicher per PayPal. Sofort loslegen.</p>
  </header>
  
  <div class="stats">
    <div class="count">40</div>
    <h2>Projekte – 40 Geldquellen</h2>
    <p>Jedes Projekt = ein Produkt oder eine Dienstleistung, die dir Geld einbringt</p>
  </div>
  
  <div class="categories">
    <span class="category">🤖 KI & Automation</span>
    <span class="category">🎯 Coaching & Beratung</span>
    <span class="category">📄 Digitale Produkte</span>
    <span class="category">🔧 Services</span>
    <span class="category">📚 Bildung & Know-how</span>
    <span class="category">💎 Mitgliedschaften</span>
  </div>
  
  <div class="projects">
"""

for slug, name, price, billing in pages:
    price_str = f"{price}€"
    billing_text = "/Monat" if billing == "monatlich" else ""
    badge_class = "monatlich" if billing == "monatlich" else "einmalig"
    index_html += f"""    <div class="project-card">
      <h3>{name}</h3>
      <div class="price">{price_str} <span class="badge">{badge_class}</span></div>
      <a href="{slug}.html">→ Kaufen</a>
    </div>
"""

index_html += """  </div>
  
  <div class="paypal-info">
    <h3>💳 Alle Zahlungen via PayPal</h3>
    <p>Zahle sicher mit PayPal oder Kreditkarte an: <strong>affirmation.positiv@gmail.com</strong></p>
    <p style="color:#666;font-size:.9em;margin-top:10px;">Du brauchst kein PayPal-Konto – Kreditkarte reicht.</p>
  </div>
  
  <footer>
    <a href="../impressum/">Impressum</a> &bull; <a href="../datenschutz/">Datenschutz</a><br>
    <span style="margin-top:10px;display:block;">Licht & Schatten Verlag – © 2026</span>
  </footer>
</div>
</body>
</html>"""

with open(os.path.join(BASE, "index.html"), "w") as f:
    f.write(index_html)

print(f"\n✅ {len(pages)} Projektseiten + index.html erstellt")
print(f"📁 {BASE}/")
print(f"💰 Preise: {min(p[2] for p in pages)}€ bis {max(p[2] for p in pages)}€")
print(f"💳 PayPal: {PAYPAL_EMAIL}")
print(f"📊 Monatlich: {sum(1 for p in pages if p[3]=='monatlich')} | Einmalig: {sum(1 for p in pages if p[3]=='einmalig')}")
