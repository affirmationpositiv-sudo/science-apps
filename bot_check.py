#!/usr/bin/env python3
"""Check Telegram bot and try to promote in groups."""

import os
import requests
import json
import re

# Read the .env file
env_path = os.path.expanduser("~/.hermes/.env")
token = None
with open(env_path) as f:
    for line in f:
        if "YESAR_BOT_TOKEN" in line:
            parts = line.strip().split("=", 1)
            if len(parts) == 2:
                token = parts[1].strip().strip("\"'").strip()
            break

if not token:
    print("❌ Token not found")
    exit(1)

API = f"https://api.telegram.org/bot{token}"
print(f"🤖 Bot: ...{token[-8:]}")

# Check bot info
me = requests.get(f"{API}/getMe").json()
print(f"🤖 Bot name: {me.get('result', {}).get('first_name', '?')}")
print(f"🤖 Username: @{me.get('result', {}).get('username', '?')}")

# Set commands for the 40 projects
commands_resp = requests.post(f"{API}/setMyCommands", json={
    "commands": [
        {"command": "start", "description": "🏠 Start / Alle 40 Projekte"},
        {"command": "projekte", "description": "🛒 Shop-Übersicht öffnen"},
        {"command": "hilfe", "description": "❓ Hilfe & Kontakt"},
    ]
})
print(f"📋 Commands: {'✅' if commands_resp.ok else '❌'}")

# Check if bot already has a webhook or is polling
info = requests.get(f"{API}/getWebhookInfo").json()
print(f"🌐 Webhook: {info.get('result', {}).get('url', 'none')}")

# Get recent updates (to see if anyone messaged us)
updates = requests.get(f"{API}/getUpdates", params={"timeout": 2, "limit": 10}).json()
msgs = []
if updates.get("ok"):
    for upd in updates.get("result", []):
        msg = upd.get("message") or upd.get("callback_query", {}).get("message")
        if msg:
            chat = msg.get("chat", {})
            text = msg.get("text", "") or upd.get("callback_query", {}).get("data", "")
            msgs.append({
                "chat_id": chat.get("id"),
                "chat_title": chat.get("title", chat.get("first_name", "?")),
                "text": text[:80] if text else "(no text)",
                "type": chat.get("type", "?"),
                "date": msg.get("date", 0),
                "update_id": upd.get("update_id"),
            })

print(f"\n📨 Letzte {len(msgs)} Nachrichten:")
for m in msgs:
    print(f"  [{m['type']}] {m['chat_title']} (ID:{m['chat_id']}): {m['text'][:60]}")

# Check if any are groups we could post in
groups = [m for m in msgs if m['type'] in ('group', 'supergroup')]
print(f"\n👥 Gefundene Gruppen zum Posten: {len(groups)}")
for g in groups:
    print(f"  📢 {g['chat_title']} (ID: {g['chat_id']})")

# Try to find groups via search
if not groups:
    print("\n🔍 Keine Gruppen gefunden. Versuche über Web zu suchen...")
    
    # Try tgramlinks.com
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        r = requests.get("https://tgramlinks.com/search?q=KI+Business+Selbstaendig", 
                        headers=headers, timeout=10)
        # Extract group links
        links = re.findall(r'href="/([^"]+)"', r.text)
        grp_links = [f"https://t.me/{l}" for l in links if len(l) > 5 and '/' not in l]
        print(f"  Gefunden: {len(grp_links)} Links")
        for l in grp_links[:10]:
            print(f"    {l}")
    except Exception as e:
        print(f"  Fehler: {e}")

print("\n✅ Bot-Check abgeschlossen!")
