#!/usr/bin/env python3
"""KDP-Qualitätscheck für alle Bücher"""
import os, re

base = '/Users/f.cinar/projects/science-apps/KDP_Books'

books = [
    ('01_KI-gestuetzte_Bewerbung_2026.md', 'KI-gestützte Bewerbung 2026'),
    ('01_Minimalismus_fuer_Maenner.md', 'Minimalismus für Männer'),
    ('02_Crypto_fuer_Anfaenger_2026.md', 'Crypto für Anfänger 2026'),
    ('02_Steuererklaerung_2026.md', 'Steuererklärung 2026'),
    ('03_ChatGPT_fuer_Handwerker.md', 'ChatGPT für Handwerker'),
    ('03_KI-Kunst_erstellen_und_verkaufen.md', 'KI-Kunst erstellen & verkaufen'),
    ('04_Notvorrat_fuer_Familien.md', 'Notvorrat für Familien'),
]

for filename, title in books:
    path = os.path.join(base, filename)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    body = re.sub(r'^---.*?---\n', '', content, flags=re.DOTALL)
    words = len(body.split())
    chars = len(body)
    has_real_umlauts = any(c in body for c in 'aouAOU')
    chapters = re.findall(r'^## (.+)', body, re.MULTILINE)
    has_frontmatter = content.startswith('---')
    
    # Content-Duplikate
    paras = [p.strip() for p in body.split('\n') if p.strip() and len(p.strip()) > 50]
    unique_paras = set(paras)
    repeat_ratio = (len(paras) - len(unique_paras)) / max(len(paras), 1) * 100 if paras else 0
    
    estimated_pages = max(1, words // 300)
    
    # Zeilen mit ae/oe/ue statt ä/ö/ü
    bad_umlauts = 0
    for line in body.split('\n'):
        if re.search(r'\b\w+[ae][ae]\w*\b', line) or re.search(r'\b\w+[oe][oe]\w*\b', line) or re.search(r'\b\w+[ue][ue]\w*\b', line):
            bad_umlauts += 1
    
    print(f"\n{'='*50}")
    print(f"  {title}")
    print(f"{'='*50}")
    print(f"  Worter:      {words:5d}  {'OK > 2.5k' if words > 2500 else 'KURZ'}")
    print(f"  Seiten:      ~{estimated_pages}  {'OK >= 24' if estimated_pages >= 24 else 'MIN 24'}")
    print(f"  Kapitel:     {len(chapters)}")
    print(f"  Umlaute ok:  {has_real_umlauts}")
    print(f"  ae/oe/ue:    {bad_umlauts} Zeilen")
    print(f"  Duplikate:   {repeat_ratio:.0f}%  {'SAUBER' if repeat_ratio < 5 else 'WARN'}")
    print(f"  Frontmatter: {'JA' if has_frontmatter else 'NEIN'}")
    
    if chapters:
        kl = ', '.join(chapters[:5])
        print(f"  Kap:         {kl}{'...' if len(chapters) > 5 else ''}")
