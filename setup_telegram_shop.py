import os, requests, json, sys

# Read bot token from .env
token = ""
with open(os.path.expanduser("~/.hermes/.env")) as f:
    for line in f:
        if "YESAR_BOT_TOKEN" in line and "=" in line:
            token = line.split("=", 1)[1].strip()
            break

if not token:
    print("NO TOKEN FOUND")
    sys.exit(1)

BASE = f"https://api.telegram.org/bot{token}"

# Test
r = requests.get(f"{BASE}/getMe")
data = r.json()
print(f"BOT: {data.get('ok')} - {data.get('result', {}).get('username', 'ERROR')}")

if not data.get('ok'):
    print(f"ERROR: {data}")
    sys.exit(1)

# Set commands
commands = [
    {"command": "start", "description": "🏪 Shop öffnen"},
    {"command": "buecher", "description": "📚 Alle Bücher anzeigen"},
    {"command": "bestellen", "description": "🛒 Bestellvorgang starten"},
    {"command": "hilfe", "description": "❓ Hilfe"},
    {"command": "kontakt", "description": "📧 Kontakt"},
]
requests.post(f"{BASE}/setMyCommands", json={"commands": commands})

# Set up the bot description
requests.post(f"{BASE}/setMyDescription", json={
    "description": "🏪 Licht & Schatten Verlag - Deutscher Buchladen auf Telegram!\n\nPraxisnahe Ratgeber zu KI, Finanzen, Minimalismus und mehr.\n\n👉 /start um den Shop zu öffnen"
})

# Create the welcome message with inline keyboard
welcome_text = """🎯 *Willkommen im Licht & Schatten Verlag!*

Dein deutscher Buchladen für praxisnahe Ratgeber.

📚 *Unsere Bücher:*
• Passives Einkommen mit KI 2026 - 9,99€
• KI-Tools für Anfänger 2026 - 8,99€
• Duales Studium 2026 - 9,99€
• Steuererklärung 2026 - 9,99€
• Notvorrat für Familien 2026 - 7,99€
• Krypto für Anfänger 2026 - 8,99€
• KI-Kunst 2026 - 8,99€
• ChatGPT für Handwerker 2026 - 8,99€

💳 *Zahlung:* PayPal an affirmation.positiv@gmail.com
📎 *Lieferung:* PDF per E-Mail

👉 /buecher - Alle Bücher anzeigen
👉 /bestellen - Bestellvorgang starten"""

keyboard = {
    "inline_keyboard": [
        [{"text": "📚 Alle Bücher", "callback_data": "buecher"}],
        [{"text": "🛒 Jetzt bestellen", "callback_data": "bestellen"}],
        [{"text": "📧 Kontakt", "callback_data": "kontakt"}]
    ]
}

# Set webhook or polling? For now, just save as reference.
# Since we can't run a persistent webhook, we'll create a system
# where the bot is triggered by user messages

# Save bot configuration
bot_config = {
    "token_last5": token[-5:],
    "bot_username": data['result']['username'],
    "bot_id": data['result']['id'],
    "welcome_text": welcome_text,
    "keyboard": keyboard,
    "products": [
        {"id": 1, "title": "Passives Einkommen mit KI 2026", "price": "9,99€", "desc": "Praktische Strategien für automatisierte Einkommensquellen mit KI", "file": "KDP_Books/Passives_Einkommen_mit_KI_2026.docx"},
        {"id": 2, "title": "KI-Tools für Anfänger 2026", "price": "8,99€", "desc": "Der praktische Einstieg in ChatGPT, Midjourney und Co.", "file": "KDP_Books/KI_Tools_fuer_Anfaenger_2026.docx"},
        {"id": 3, "title": "Duales Studium 2026", "price": "9,99€", "desc": "Der komplette Guide - von der Bewerbung bis zum Berufseinstieg", "file": "KDP_Books/Duales_Studium_2026.docx"},
        {"id": 4, "title": "Steuererklärung 2026 für Freiberufler", "price": "9,99€", "desc": "Schritt für Schritt zu mehr Rückerstattung", "file": "KDP_Books/Steuererklaerung_2026_Freiberufler.docx"},
        {"id": 5, "title": "Notvorrat für Familien 2026", "price": "7,99€", "desc": "14 Tage Autarkie mit Kindern - inkl. vegetarischer Optionen", "file": "KDP_Books/Notvorrat_fuer_Familien_2026.docx"},
        {"id": 6, "title": "Krypto für Anfänger 2026", "price": "8,99€", "desc": "Bitcoin, Ethereum und KI-Trading verständlich erklärt", "file": "KDP_Books/Krypto_fuer_Anfaenger_2026.docx"},
        {"id": 7, "title": "KI-Kunst erstellen & verkaufen 2026", "price": "8,99€", "desc": "Midjourney, DALL-E und Stable Diffusion", "file": "KDP_Books/ki_kunst_2026.docx"},
        {"id": 8, "title": "ChatGPT für Handwerker 2026", "price": "8,99€", "desc": "Rechnungen, Angebote und Kundenkommunikation mit KI", "file": "KDP_Books/ChatGPT_fuer_Handwerker_2026.docx"}
    ]
}

with open("/Users/f.cinar/Desktop/gh-pages/telegram_bot_config.json", "w", encoding="utf-8") as f:
    json.dump(bot_config, f, ensure_ascii=False, indent=2)

print(f"\n✅ BOT KONFIGURIERT: @{bot_config['bot_username']}")
print(f"✅ Produkte: {len(bot_config['products'])}")
print(f"✅ Config gespeichert: telegram_bot_config.json")
