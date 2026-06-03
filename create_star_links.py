#!/usr/bin/env python3
"""Create Telegram Star invoice links for all products and save them."""
import requests
import os
import json

with open(os.path.expanduser("~/.hermes/.env")) as f:
    token = None
    for line in f:
        if "YESAR_BOT_TOKEN" in line:
            token = line.strip().split("=", 1)[1].strip().strip("'\"")

API = "https://api.telegram.org/bot" + token

products = [
    ("KI Texte-Service", "10 Blogartikel mit KI. Lieferung in 48h.", 50),
    ("KI Bilder-Service", "50 einzigartige KI-Bilder. Kommerziell nutzbar.", 30),
    ("KI Bot-Bau", "Massgeschneiderter Telegram-Bot fuer dein Business.", 80),
    ("KI Automation Starter", "Eine einfache KI-Automation + 30 Min Setup-Call.", 50),
    ("KI Automation Pro", "Komplette Geschaeftsprozesse automatisiert.", 200),
    ("KI Automation Enterprise", "Massiv skalieren mit KI. VIP-Support 1 Monat.", 500),
    ("Prompt-Pack Vol.1", "50 profitable KI-Prompts fuer Marketing.", 10),
    ("Prompt-Pack Vol.2", "50 fortgeschrittene Business-Prompts.", 10),
    ("Prompt-Pack Vol.3", "50 KI-Prompts fuer deutsche Unternehmer.", 10),
    ("30-Min-KI-Coaching", "30 Min 1:1 KI-Coaching per Video-Call.", 30),
    ("60-Min-KI-Coaching", "1h intensives KI-Coaching + Aktionsplan.", 50),
    ("Business Booster 3h", "3h Power-Session: Business auf KI umgestellt.", 100),
    ("VIP-KI-Tag 8h", "Ganzer Tag: Bots, Automation, Strategie.", 200),
    ("KI-Strategie-Call", "45 Min Strategie-Beratung.", 80),
    ("Notion Business Planner", "Komplette Notion-Vorlage fuer dein Business.", 7),
    ("Excel Gewinn-Rechner", "Umsatz, Kosten, Gewinn auf einen Blick.", 5),
    ("Social Media Content Plan", "30-Tage Content-Plan, fertig zum Posten.", 10),
    ("Newsletter-Vorlagen", "10 professionelle E-Mail-Vorlagen.", 10),
    ("E-Mail-Sequenzen Paket", "5 automatisierte E-Mail-Sequenzen.", 12),
    ("Business Plan Vorlage", "Komplette Vorlage fuer Gruendung.", 8),
    ("Marketing Strategie", "Komplette Strategie zum Ausfuellen.", 10),
    ("Produktivitaets-System", "Persoenliches System nach GTD.", 7),
    ("Kundenakquise Playbook", "10 Methoden + Skripte fuer Anruf/Email.", 15),
    ("Lead-Magnet Vorlagen", "5 fertige Lead-Magnete.", 5),
    ("CV Optimierung", "KI-gestuetzte Optimierung deines Lebenslaufs.", 20),
    ("LinkedIn Profil Optimierung", "Dein Profil wird zur Kundenmaschine.", 30),
    ("SEO Quick-Check", "30+ SEO-Faktoren geprueft + Report.", 30),
    ("Website Texte Service", "Professionelle Texte fuer deine Website.", 50),
    ("Social Media Management", "10 Posts/Woche, 1 Monat.", 100),
    ("Newsletter Service", "4 Newsletter-Ausgaben/Monat.", 50),
    ("KI Grundlagen Kurs", "5 Lektionen: KI verstehen + Geld verdienen.", 20),
    ("Passive Income Guide", "10 passive Einkommensquellen mit KI.", 15),
    ("Sales Copy Guide", "Texte schreiben, die verkaufen.", 12),
    ("ChatGPT Mastery Guide", "50 fortgeschrittene Techniken.", 10),
    ("KI Tools Uebersicht 2026", "100 wichtigste KI-Tools.", 7),
    ("Telegram Premium Gruppe", "Taegliche KI-Tipps, Vorlagen, Austausch.", 10),
    ("Premium Newsletter", "Woechentliche KI-Strategien + Insider-Tipps.", 7),
    ("KI Tipps WhatsApp", "Taeglich eine KI-Empfehlung.", 5),
    ("KI News Weekly", "Woechentliche KI-Zusammenfassung.", 3),
    ("Business Tools Zugang", "Alle Vorlagen, Rechner, Tools.", 20),
]

results = []
for title, desc, stars in products:
    payload = "prod_" + str(len(results) + 1).zfill(3)
    r = requests.post(f"{API}/createInvoiceLink", data={
        "title": title,
        "description": desc,
        "payload": payload,
        "currency": "XTR",
        "prices": json.dumps([{"label": title, "amount": stars}]),
    }, timeout=10)
    if r.ok:
        link = r.json().get("result", "")
        results.append({"title": title, "stars": stars, "link": link, "payload": payload})
        print(f"✅ {title} ({stars}★)")
    else:
        print(f"❌ {title}: {r.text[:80]}")

# Save to JSON
output = {
    "bot": "Yesaryour_bot",
    "products": results,
    "total_products": len(results),
    "min_stars": min(r["stars"] for r in results),
    "max_stars": max(r["stars"] for r in results),
    "total_stars_value": sum(r["stars"] for r in results),
}

path = "/Users/f.cinar/Desktop/gh-pages/telegram_star_products.json"
with open(path, "w") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f"\n{'='*50}")
print(f"✅ {len(results)}/{len(products)} Produkte als Telegram Stars erstellt!")
print(f"💰 Preise: {output['min_stars']} - {output['max_stars']} Stars")
print(f"📁 Gespeichert: {path}")
print(f"\nBeispiel-Links:")
for r in results[:3]:
    print(f"  🔗 {r['title']}: {r['link'][:50]}...")
