#!/usr/bin/env python3
"""Telegram Stars Bot: Watch for payments + auto-respond with product links."""
import requests
import os
import json
import time

# Config
with open(os.path.expanduser("~/.hermes/.env")) as f:
    token = None
    for line in f:
        if "YESAR_BOT_TOKEN" in line:
            token = line.strip().split("=", 1)[1].strip().strip("'\"")

API = f"https://api.telegram.org/bot{token}"
OFFSET_FILE = os.path.expanduser("~/.hermes/telegram_offset.txt")
LINKS_FILE = "/Users/f.cinar/Desktop/gh-pages/telegram_star_products.json"

# Load products
with open(LINKS_FILE) as f:
    star_data = json.load(f)

products = {p["title"]: p for p in star_data["products"]}

# Get offset
offset = 0
if os.path.exists(OFFSET_FILE):
    with open(OFFSET_FILE) as f:
        try:
            offset = int(f.read().strip())
        except:
            offset = 0

# Get updates
updates = requests.get(f"{API}/getUpdates", params={
    "offset": offset,
    "timeout": 5,
    "limit": 100
}, timeout=10).json()

new_offset = offset
payments_found = []

if updates.get("ok"):
    for upd in updates.get("result", []):
        new_offset = max(new_offset, upd["update_id"] + 1)
        msg = upd.get("message") or {}
        
        # Check for payment
        if "successful_payment" in msg:
            pay = msg["successful_payment"]
            invoice_payload = pay.get("invoice_payload", "")
            total = pay.get("total_amount", 0)
            currency = pay.get("currency", "")
            print(f"💰 ZAHLUNG EINGEGANGEN! Payload: {invoice_payload}, {total} {currency}")
            payments_found.append({
                "payload": invoice_payload,
                "amount": total,
                "currency": currency,
                "from": msg["from"]["id"],
                "date": msg["date"],
            })
        
        # Handle commands
        text = msg.get("text", "")
        chat_id = msg.get("chat", {}).get("id")
        
        if text == "/start" or text == "/projekte":
            # Send category selection
            keyboard = {
                "inline_keyboard": [
                    [{"text": "🤖 KI & Automation (ab 10★)", "callback_data": "cat_ki"}],
                    [{"text": "🎯 Coaching (ab 30★)", "callback_data": "cat_coaching"}],
                    [{"text": "📄 Vorlagen (ab 5★)", "callback_data": "cat_vorlagen"}],
                    [{"text": "🔧 Services (ab 20★)", "callback_data": "cat_services"}],
                    [{"text": "📚 Kurse (ab 7★)", "callback_data": "cat_kurse"}],
                    [{"text": "💎 Abos (ab 3★)", "callback_data": "cat_abo"}],
                    [{"text": "🌐 Alle 40 Produkte", "url": "https://affirmationpositiv-sudo.github.io/science-apps/40projekte/"}],
                ]
            }
            welcome = (
                "🎯 *40 Geldquellen – Jetzt kaufen!*\n\n"
                "💎 *Zahlen mit Telegram Stars:* Kein PayPal, keine Karte – einfach Stars aufladen und kaufen.\n"
                "💰 *Zahlen mit PayPal:* affirmation.positiv@gmail.com\n\n"
                "Waehle eine Kategorie:"
            )
            requests.post(f"{API}/sendMessage", json={
                "chat_id": chat_id,
                "text": welcome,
                "parse_mode": "Markdown",
                "reply_markup": keyboard,
            })
        
        elif text == "/stars":
            # Show all star products sorted by price
            sorted_prods = sorted(products.values(), key=lambda x: x["stars"])
            msg_text = "🌟 *Alle Produkte in Telegram Stars:*\n\n"
            for p in sorted_prods:
                msg_text += f"{p['title']} – {p['stars']}★\n"
            msg_text += f"\n👉 Zum Kaufen einfach auf den Link klicken:\nhttps://t.me/Yesaryour_bot"
            requests.post(f"{API}/sendMessage", json={
                "chat_id": chat_id,
                "text": msg_text,
                "parse_mode": "Markdown",
            })
        
        # Handle callback queries (button clicks)
        if "callback_query" in upd:
            cb = upd["callback_query"]
            cb_data = cb.get("data", "")
            cb_msg = cb.get("message", {})
            cb_chat = cb_msg.get("chat", {})
            cb_id = cb_chat.get("id")
            
            cat_map = {
                "cat_ki": [p for p in products.values() if p["stars"] >= 10 and p["stars"] <= 100],
                "cat_coaching": [p for p in products.values() if 30 <= p["stars"] <= 200],
                "cat_vorlagen": [p for p in products.values() if p["stars"] <= 15],
                "cat_services": [p for p in products.values() if 20 <= p["stars"] <= 100],
                "cat_kurse": [p for p in products.values() if 7 <= p["stars"] <= 20],
                "cat_abo": [p for p in products.values() if p["stars"] <= 10],
            }
            
            if cb_data in cat_map:
                prods = cat_map[cb_data]
                keyboard = {"inline_keyboard": []}
                msg_text = f"📋 *Kategorie Produkte:*\n\n"
                for p in prods:
                    msg_text += f"• {p['title']} – {p['stars']}★\n"
                    keyboard["inline_keyboard"].append(
                        [{"text": f"{p['title']} ({p['stars']}★)", "url": p["link"]}]
                    )
                keyboard["inline_keyboard"].append(
                    [{"text": "🔙 Zurueck", "callback_data": "back"}]
                )
                requests.post(f"{API}/sendMessage", json={
                    "chat_id": cb_id,
                    "text": msg_text,
                    "parse_mode": "Markdown",
                    "reply_markup": keyboard,
                })
                # Answer callback
                requests.post(f"{API}/answerCallbackQuery", json={
                    "callback_query_id": cb["id"],
                })
            
            if cb_data == "back":
                keyboard = {
                    "inline_keyboard": [
                        [{"text": "🤖 KI & Automation (ab 10★)", "callback_data": "cat_ki"}],
                        [{"text": "🎯 Coaching (ab 30★)", "callback_data": "cat_coaching"}],
                        [{"text": "📄 Vorlagen (ab 5★)", "callback_data": "cat_vorlagen"}],
                        [{"text": "🔧 Services (ab 20★)", "callback_data": "cat_services"}],
                        [{"text": "📚 Kurse (ab 7★)", "callback_data": "cat_kurse"}],
                        [{"text": "💎 Abos (ab 3★)", "callback_data": "cat_abo"}],
                    ]
                }
                requests.post(f"{API}/sendMessage", json={
                    "chat_id": cb_id,
                    "text": "🎯 *Kategorie waehlen:*",
                    "parse_mode": "Markdown",
                    "reply_markup": keyboard,
                })
                requests.post(f"{API}/answerCallbackQuery", json={
                    "callback_query_id": cb["id"],
                })

# Save offset
with open(OFFSET_FILE, "w") as f:
    f.write(str(new_offset))

# Report – nur bei neuen Zahlungen
if payments_found:
    print(f"\n💰 NEUE ZAHLUNGEN ({len(payments_found)}):")
    for p in payments_found:
        print(f"  {p['amount']} {p['currency']} – Payload: {p['payload']} – User: {p['from']}")
# Silent wenn nichts – kein "Keine neuen Zahlungen" Spam mehr
