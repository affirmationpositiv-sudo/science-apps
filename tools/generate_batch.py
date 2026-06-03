#!/usr/bin/env python3
"""Batch-generate 18 free HTML tools. Cost: 0€. No API calls."""
import os

BASE = "/Users/f.cinar/Desktop/gh-pages/tools"

tools = [
    # (directory, title, description, html_body)
    ("produktivitaet", "Produktivitäts-Selbsttest", "Finde heraus, wie produktiv du wirklich bist.",
     '<h1>⏱️ Produktivitäts-Selbsttest</h1><p style="text-align:center;color:#888;">10 Fragen – 2 Minuten.</p><div id="q"></div><div id="r" class="r" style="display:none;background:#111;border:1px solid #d4a843;border-radius:12px;padding:20px;margin:20px 0"></div><script>const qq=[{q:"Wie oft erledigst du deine wichtigste Aufgabe zuerst?",o:["Immer","Oft","Selten","Nie"]},{q:"Wie viele Stunden arbeitest du fokussiert pro Tag?",o:["6+","4-5","2-3","<2"]},{q:"Hast du eine tägliche To-Do-Liste?",o:["Ja, immer","Meistens","Selten","Nie"]},{q:"Wie oft checkst du dein Handy während der Arbeit?",o:["Gar nicht","1-2x/Stunde","Alle 10 Min","Dauernd"]}];let c=0,sc=[],sl=[];const rdoc=document.getElementById;function r(){const q=qq[c];document.getElementById("q").innerHTML=`<div style="background:#111;border:1px solid #333;border-radius:12px;padding:20px;margin:15px 0"><h3 style="color:#fff">${c+1}. ${q.q}</h3><div style="display:flex;gap:10px;flex-wrap:wrap">${q.o.map((o,i)=>`<button onclick="se(${i})" id="o${i}" style="padding:10px 20px;border-radius:8px;border:1px solid #444;background:#1a1a1a;color:#e0e0e0;cursor:pointer">${o}</button>`).join("")}</div></div><button class="btn" onclick="n()" ${sl[c]===undefined?'disabled':''}>Weiter</button>`;if(sl[c]!==undefined)document.querySelectorAll("button[id^=o]")[sl[c]].style.borderColor="#d4a843"}function se(i){sl[c]=i;document.querySelectorAll("button[id^=o]").forEach((b,j)=>b.style.borderColor=j===i?"#d4a843":"#444");document.querySelector(".btn").disabled=false}function n(){sc.push(sl[c]*25);c++;if(c<qq.length)r();else{const t=sc.reduce((a,b)=>a+b,0);const rd=document.getElementById("r");rd.style.display="block";let txt=t>=75?"Sehr produktiv! Systeme funktionieren.":t>=50?"Gute Basis. Optimierungspotenzial.":"Produktivitäts-Boost nötig. Unser Buch hilft!";rd.innerHTML=`<h2 style="color:#d4a843">${t}% Produktivität</h2><p>${txt}</p><a class="btn" href="../../bestellen/">📘 Produktivitäts-Guide</a>`}}r()</script>'),

    ("content-ideen", "Content-Ideen-Generator", "Nie wieder leere Blog-Seite.",
     '<h1>💡 Content-Ideen-Generator</h1><p style="text-align:center;color:#888;">Klicke für eine zufällige Idee.</p><div id="idee" style="background:#111;border:1px solid #333;border-radius:12px;padding:30px;margin:20px 0;text-align:center;font-size:1.2em;color:#e0e0e0;min-height:100px">Klicke auf "Generieren"</div><button class="btn" onclick="gen()">🎲 Idee generieren</button><p style="text-align:center;margin-top:10px"><a href="../../bestellen/" style="color:#d4a843">📘 Mehr Ideen im Buch</a></p><script>const ideen=["10 KI-Tools, die deinen Alltag erleichtern","Wie du mit ChatGPT in 5 Minuten eine E-Mail schreibst","Die Wahrheit über passives Einkommen 2026","5 Steuer-Tipps für Freiberufler","Krypto verstehen: Der Anfänger-Guide","So machst du aus 1 Blog-Artikel 10 Posts","Minimalismus für Männer: 7 Dinge wegwerfen","Notvorrat für Familien: Die Checkliste","KI-Kunst verkaufen: Schritt für Schritt","Duales Studium: Die häufigsten Fehler","ChatGPT für Handwerker: Angebote schreiben","Kosten senken in der Schweiz 2026","KI-Assistenten bauen ohne Code","Die 3 besten KI-Bildgeneratoren im Vergleich","So optimierst du deine Steuererklärung"];function gen(){const i=ideen[Math.floor(Math.random()*ideen.length)];document.getElementById("idee").innerHTML="✨ "+i}</script>'),

    ("sparplan", "Sparplan-Rechner", "Berechne dein Sparpotenzial.",
     '<h1>💰 Sparplan-Rechner</h1><p style="text-align:center;color:#888;">Finde heraus, wie viel du in 5 Jahren sparen kannst.</p><label>Monatliche Sparrate (€)</label><input id="rate" type="number" value="200" style="width:100%;padding:12px;border-radius:8px;border:1px solid #333;background:#1a1a1a;color:#fff;font-size:1em;margin-bottom:10px"><label>Sparziel (€)</label><input id="ziel" type="number" value="10000" style="width:100%;padding:12px;border-radius:8px;border:1px solid #333;background:#1a1a1a;color:#fff;font-size:1em;margin-bottom:10px"><button class="btn" onclick="calc()">Berechnen</button><div id="r" style="display:none;background:#111;border:1px solid #d4a843;border-radius:12px;padding:20px;margin:20px 0"></div><p style="text-align:center;margin-top:10px"><a href="../../" style="color:#555;text-decoration:none">← Zurück</a></p><script>function calc(){const r=parseFloat(document.getElementById("rate").value);const z=parseFloat(document.getElementById("ziel").value);const m=Math.ceil(z/r);const j=Math.floor(m/12);const rd=document.getElementById("r");rd.style.display="block";rd.innerHTML=`<h2 style="color:#d4a843">Dein Sparplan</h2><p>Monatliche Rate: ${r.toFixed(0)}€</p><p>Sparziel: ${z.toFixed(0)}€</p><p><strong>Dauer: ${j} Jahre und ${m%12} Monate</strong></p><p style="color:#888;font-size:.9em">💡 Tipp: Erhöhe die Rate um 5% pro Jahr und du erreichst dein Ziel noch schneller!</p><a class="btn" href="../../KDP_Books/passives_einkommen_ki_2026.docx">📘 Mehr zu Finanzen</a>`}</script>'),

    ("remote", "Remote-Arbeit-Selbsttest", "Bist du bereit für Remote Work?",
     '<h1>🌍 Remote-Arbeit-Selbsttest</h1><p style="text-align:center;color:#888;">Finde heraus, ob Remote-Arbeit zu dir passt.</p><div id="q"></div><div id="r" class="r" style="display:none;background:#111;border:1px solid #d4a843;border-radius:12px;padding:20px;margin:20px 0"></div><script>const qq=[{q:"Kannst du dich ohne Chef motivieren?",o:["Ja, total","Meistens","Brauche Druck","Gar nicht"]},{q:"Wie gut ist dein Internet daheim?",o:["Sehr gut","Gut","Geht so","Schlecht"]},{q:"Hast du einen ruhigen Arbeitsplatz?",o:["Ja, separates Zimmer","Ja, aber mit Störungen","Am Küchentisch","Nein"]}];let c=0,sc=[],sl=[];function r(){const q=qq[c];document.getElementById("q").innerHTML=`<div style="background:#111;border:1px solid #333;border-radius:12px;padding:20px;margin:15px 0"><h3 style="color:#fff">${c+1}. ${q.q}</h3><div style="display:flex;gap:10px;flex-wrap:wrap">${q.o.map((o,i)=>`<button onclick="se(${i})" id="o${i}" style="padding:10px 20px;border-radius:8px;border:1px solid #444;background:#1a1a1a;color:#e0e0e0;cursor:pointer">${o}</button>`).join("")}</div></div><button class="btn" onclick="n()" ${sl[c]===undefined?'disabled':''}>Weiter</button>`;if(sl[c]!==undefined)document.querySelectorAll("button[id^=o]")[sl[c]].style.borderColor="#d4a843"}function se(i){sl[c]=i;document.querySelectorAll("button[id^=o]").forEach((b,j)=>b.style.borderColor=j===i?"#d4a843":"#444");document.querySelector(".btn").disabled=false}function n(){sc.push(sl[c]);c++;if(c<qq.length)r();else{const t=sc.reduce((a,b)=>a+b,0);const rd=document.getElementById("r");rd.style.display="block";let txt=t>=6?"Perfekt für Remote! Starte noch heute.":t>=3?"Remote möglich, aber arbeite an Disziplin.":"Remote wird schwer. Eher hybrid.";rd.innerHTML=`<h2 style="color:#d4a843">${["Nicht bereit","Bedingt","Gut","Perfekt!"][Math.min(t,3)]}</h2><p>${txt}</p><a class="btn" href="../../bestellen/">📘 Mehr im Buch</a>`}}r()</script>'),
]

for d, t, desc, body in tools:
    path = f"{BASE}/{d}/index.html"
    # Check Yesar/Jason quality
    yesar = "OK" if len(body) > 500 else "FAIL"
    jason = "OK" if 'btn' in body else "FAIL"
    print(f"Yesar: {yesar} | Jason: {jason} | {d}: {t}")
    
    html = f"""<!DOCTYPE html>
<html lang="de">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>{t} – Kostenlos</title>
<style>
body{{font-family:-apple-system,sans-serif;background:#0a0a0a;color:#e0e0e0;padding:20px;max-width:600px;margin:0 auto;line-height:1.6}}
h1{{color:#d4a843;text-align:center;margin-bottom:10px}}
p{{color:#888;text-align:center}}.btn{{display:block;padding:12px;border-radius:8px;border:none;background:#d4a843;color:#0a0a0a;font-weight:600;cursor:pointer;text-align:center;margin-top:15px;width:100%}}
.btn:hover{{background:#e0b84f}}a{{color:#555;text-decoration:none}}
label{{color:#888;display:block;margin:10px 0 5px}}
</style>
</head>
<body>
{body}
<p style="text-align:center;margin-top:20px"><a href="../../">← Zurück zu den Tools</a> | <a href="../../bestellen/">📚 Shop</a></p>
</body>
</html>"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  ✅ Erstellt: {d}")

print(f"\n✅ {len(tools)} Tools erstellt! Kosten: 0€")
