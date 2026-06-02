import os, json, requests, time

# Load DeepSeek key
key = ''
with open(os.path.expanduser('~/.hermes/.env')) as f:
    for line in f:
        if 'DEEPSEEK_API_KEY' in line and '=' in line:
            key = line.split('=', 1)[1].strip()
            break

def gen_chapter(book, num, title, wt=1800):
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "Du bist ein deutscher Sachbuchautor ohne KI-Fuelltext. Schreibe direkt, persoenlich, praktisch."},
            {"role": "user", "content": f"Schreibe Kapitel {num}: '{title}' fuer '{book}'. Mindestens {wt} Woerter auf Deutsch. Praktische Tipps, echte Beispiele."}
        ],
        "max_tokens": 3500, "temperature": 0.82
    }
    resp = requests.post("https://api.deepseek.com/v1/chat/completions", headers=headers, json=payload, timeout=60)
    return resp.json()["choices"][0]["message"]["content"] if resp.status_code == 200 else f"[ERROR {resp.status_code}]"

# Book 7: KI-Kunst
book = "KI-Kunst erstellen und verkaufen 2026"
chapters = [
    (1, "Die Revolution der KI-Kunst"),
    (2, "Midjourney, DALL-E, Stable Diffusion: Die Werkzeuge"),
    (3, "Der perfekte Prompt: Techniken fuer beeindruckende Bilder"),
    (4, "Verkaufsplattformen: Etsy, Redbubble, Displate und Co."),
    (5, "Rechtliche Grundlagen: Darf ich KI-Kunst verkaufen?"),
    (6, "Pricing: Wie viel sind deine Bilder wert?"),
    (7, "Print-on-Demand: Vom Bild zum Produkt"),
    (8, "30-Tage-Fahrplan: Dein erstes KI-Kunst-Einkommen")
]

text = f"# {book}\n\n---\n\n"
for n, t in chapters:
    c = gen_chapter(book, n, t, 1600)
    wc = len(c.split())
    text += f"\n\n## Kapitel {n}: {t}\n\n{c}\n\n"
    print(f"Kap {n}: {wc} Woerter")
    time.sleep(0.5)

with open("ki_kunst_2026.md", "w", encoding="utf-8") as f:
    f.write(text)
print(f"\nBUCH 7: {len(text.split())} Woerter")
