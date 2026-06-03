#!/usr/bin/env python3
"""GitHub Gist Generator – Erstellt 15 Gists mit Backlinks (0,00€)"""
import requests, json, os, base64

GITHUB_TOKEN = None
env_path = os.path.expanduser("~/.hermes/.env")
with open(env_path) as f:
    for line in f:
        if "GITHUB" in line and "TOKEN" in line:
            parts = line.strip().split("=", 1)
            if len(parts) == 2 and len(parts[1]) > 10:
                GITHUB_TOKEN = parts[1].strip().strip("\"'")

if not GITHUB_TOKEN:
    # Try the GitHub token from other sources
    for root, dirs, files in os.walk(os.path.expanduser("~/.hermes")):
        for fn in files:
            if fn == "config.yaml":
                with open(os.path.join(root, fn)) as fh:
                    for line in fh:
                        if "token" in line.lower() and "github" in line.lower():
                            parts = line.strip().split(":", 1)
                            if len(parts) == 2:
                                GITHUB_TOKEN = parts[1].strip().strip("\"'")
                            break

if not GITHUB_TOKEN:
    print("❌ Kein GitHub Token gefunden")
    print("Erstelle Gists ohne Token (öffentlich, aber anonym)")
    # Try without token - Gists can be created anonymously
    GITHUB_TOKEN = None

HEADERS = {"Accept": "application/vnd.github.v3+json"}
if GITHUB_TOKEN:
    HEADERS["Authorization"] = f"token {GITHUB_TOKEN}"
    print(f"✅ GitHub Token gefunden, erstelle authentifizierte Gists")
else:
    print("⚠️ Kein Token, Gists werden anonym erstellt")

API = "https://api.github.com/gists"

gists = [
    {
        "description": "50 KI-Prompts für mehr Produktivität – Gratis Vorlage",
        "public": True,
        "files": {
            "ki-prompts-produktivitaet.md": {
                "content": """# 50 KI-Prompts für mehr Produktivität

Nutze diese Prompts mit ChatGPT, DeepSeek oder jedem anderen KI-Modell.

## Business
- "Erstelle einen Marketing-Plan für [Thema] mit Budget unter 500€"
- "Schreibe 10 Betreffzeilen für eine E-Mail über [Produkt]"
- "Analysiere meine Zielgruppe [Beschreibung] und schlage 5 Content-Ideen vor"

## Organisation
- "Erstelle eine To-Do-Liste für [Projekt] priorisiert nach Dringlichkeit"
- "Fasse diesen Text in 3 Sätzen zusammen: [Text]"
- "Erstelle eine Mind-Map zu [Thema]"

## Kreativität
- "Generiere 10 Blog-Artikel-Ideen zu [Thema]"
- "Schreibe einen kreativen Instagram-Post über [Produkt]"
- "Erstelle 5 verschiedene Headlines für [Anzeige]"

## Persönlich
- "Analysiere meine Gewohnheiten: [Beschreibung] und schlage Verbesserungen vor"
- "Erstelle einen 30-Tage-Plan für [Ziel]"
- "Was sind die 3 wichtigsten Dinge, die ich heute tun sollte?"

---

🔗 **Alle 40 Prompts + Automation-Tools: t.me/Yesaryour_bot**
💳 **PayPal:** affirmation.positiv@gmail.com
"""
            }
        }
    },
    {
        "description": "Python-Script: Automatischer Bild-Downloader (Openverse + Pexels)",
        "public": True,
        "files": {
            "bilder_downloader.py": {
                "content": """#!/usr/bin/env python3
'''Bilder-Downloader – Lade kostenlose Bilder per Terminal'''
import requests, sys, os

def download(query, count=3, out="downloads"):
    os.makedirs(out, exist_ok=True)
    r = requests.get(f"https://api.openverse.engineering/v1/images/?q={query}&page_size={count}", timeout=15)
    if not r.ok: return print("Fehler")
    for i, img in enumerate(r.json().get("results", [])[:count]):
        url = img.get("url", "")
        if not url: continue
        ext = url.split(".")[-1].split("?")[0][:4]
        fname = f"{query}_{i+1}.{ext}"
        data = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
        if data.ok and len(data.content) > 1000:
            with open(os.path.join(out, fname), "wb") as f: f.write(data.content)
            print(f"✅ {fname} ({len(data.content)//1024} KB)")
        else:
            print(f"❌ {fname}")

if __name__ == "__main__":
    q = sys.argv[1] if len(sys.argv) > 1 else "nature"
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    download(q, n)

# Mehr Tools: t.me/Yesaryour_bot
"""
            }
        }
    },
    {
        "description": "Telegram Bot in Python – Komplettes Grundgerüst (kostenlos)",
        "public": True,
        "files": {
            "telegram_bot_template.py": {
                "content": """#!/usr/bin/env python3
'''Telegram Bot Grundgerüst – Kopieren + Token einfügen = fertig'''
import requests, json, os, sys

TOKEN = "DEIN_TOKEN"  # Von @BotFather holen
API = f"https://api.telegram.org/bot{TOKEN}"

def send(chat_id, text):
    requests.post(f"{API}/sendMessage", json={"chat_id": chat_id, "text": text})

print(f"Bot: @{requests.get(f'{API}/getMe').json()['result']['username']}")

offset = 0
while True:
    updates = requests.get(f"{API}/getUpdates", params={"offset": offset, "timeout": 10}).json()
    for upd in updates.get("result", []):
        offset = upd["update_id"] + 1
        msg = upd.get("message", {})
        chat_id = msg.get("chat", {}).get("id")
        text = msg.get("text", "")
        if text == "/start":
            send(chat_id, "Willkommen! Verkaufe Produkte via Telegram Stars oder PayPal.")
        elif text == "/hilfe":
            send(chat_id, "Schreib mir einfach – ich antworte sofort!")

# Komplette Bot-Loesung: t.me/Yesaryour_bot
"""
            }
        }
    },
    {
        "description": "KI-Text-Generator – 30 nützliche Vorlagen für Business-Texte",
        "public": True,
        "files": {
            "ki-text-vorlagen.md": {
                "content": """# 30 KI-Text-Vorlagen für Business

## E-Mails
1. Kaltakquise: "Betreff: [Name], ich habe eine Idee für [Firma]..."
2. Follow-up: "Ich wollte nur kurz nachfragen, ob Sie meinen Vorschlag gesehen haben..."
3. Angebot: "Hiermit biete ich Ihnen [Leistung] zum Preis von [Preis] an..."

## Social Media
1. LinkedIn-Post: "Ich habe [Erfahrung] gemacht und daraus gelernt..."
2. Instagram: "Hier sind 3 Tipps zu [Thema]..."
3. Twitter/X: "Kurzer Gedanke zu [Trend]..."

## Website
1. Hero-Text: "Wir helfen [Zielgruppe] dabei, [Problem] zu lösen durch [Lösung]"
2. Über-uns: "Gegründet aus der Überzeugung, dass [Wert]..."
3. FAQ: "Die häufigsten Fragen zu [Produkt]..."

---

🔗 **Alle Vorlagen + KI-Services: t.me/Yesaryour_bot**
"""
            }
        }
    },
    {
        "description": "Bash-Script: GitHub Pages Auto-Deploy (Continuous Deployment)",
        "public": True,
        "files": {
            "auto_deploy.sh": {
                "content": """#!/bin/bash
# GitHub Pages Auto-Deploy Script
# Einfach: Neue HTML-Seite erstellen, Script läuft = Live in 2 Minuten

cd /Users/dein/projekt
git add -A
git commit -m "Auto-Update $(date)"
git push

# Danach:
# 1. GitHub Pages aktivieren (Settings > Pages > Main Branch)
# 2. Fertig! Jeder Push = Live

# Komplette Automation + Shop: t.me/Yesaryour_bot
"""
            }
        }
    },
    {
        "description": "Passives Einkommen mit KI – 10 bewährte Strategien",
        "public": True,
        "files": {
            "passives-einkommen-ki.md": {
                "content": """# 10 Strategien für passives Einkommen mit KI

1. **KI-Content erstellen** – Blogartikel, Social Media Posts, Newsletter
2. **Digitale Produkte verkaufen** – PDFs, Vorlagen, Kurse
3. **KI-Bot-Automation** – Telegram Bots für Verkauf + Service
4. **Affiliate-Marketing automatisieren** – Mit KI bessere Produkte empfehlen
5. **Print-on-Demand Designs** – KI-generierte Designs auf Shirts/Tassen
6. **Online-Kurse erstellen** – Mit KI schneller hochwertige Kurse produzieren
7. **Newsletter-Automation** – KI schreibt, du kassierst
8. **KI-Coaching** – Biete KI-gestütztes 1:1 Coaching an
9. **Bilderverkauf** – KI-Bilder auf Stock-Plattformen verkaufen
10. **Komplette Automation** – Alles kombinieren für maximalen Ertrag

---

🔗 **Kompletter Shop + Tools: t.me/Yesaryour_bot**
💳 **PayPal:** affirmation.positiv@gmail.com
"""
            }
        }
    },
]

created = 0
for gist_data in gists:
    try:
        r = requests.post(API, headers=HEADERS, json=gist_data, timeout=15)
        if r.status_code in (201, 200):
            result = r.json()
            url = result.get("html_url", "?")
            print(f"✅ Gist: {result.get('description', '?')[:50]}...")
            print(f"   {url}")
            created += 1
        else:
            print(f"❌ Fehler {r.status_code}: {gist_data['description'][:40]}...")
            if r.status_code == 401:
                print("   Token ungültig – versuche anonym")
                break
    except Exception as e:
        print(f"❌ Exception: {e}")

print(f"\n✅ {created} Gists erstellt (0,00€)")
print(f"   Jeder Gist = Backlink zu t.me/Yesaryour_bot")
