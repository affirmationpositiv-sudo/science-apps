#!/usr/bin/env python3
"""BILDER-DOWNLOADER – Lade jedes Bild kostenlos per Terminal

Nutzung: python3 bilder.py "suchbegriff" [anzahl] [ordner]

Beispiele:
  python3 bilder.py "Berlin Skyline" 5
  python3 bilder.py "Business Meeting" 3
  python3 bilder.py "Nature Landscape" 2
  python3 bilder.py "Technologie Hintergrund" 5
"""

import requests
import sys
import os
import json
from urllib.parse import quote

def download_pexels(query, count=3, output_dir="downloads"):
    """Lade Bilder von Pexels (kostenlos, 80/Monat)"""
    os.makedirs(output_dir, exist_ok=True)
    
    headers = {
        "Authorization": "563492ad6f917000010000010e7a6e8f8d4c4c4a8c6b6e8f8d4c4c4a",
        "User-Agent": "Mozilla/5.0"
    }
    
    url = f"https://api.pexels.com/v1/search?query={quote(query)}&per_page={count}&orientation=landscape"
    
    r = requests.get(url, headers=headers, timeout=15)
    if not r.ok:
        print(f"❌ Pexels Fehler: {r.status_code}")
        return []
    
    data = r.json()
    photos = data.get("photos", [])
    downloaded = []
    
    for i, photo in enumerate(photos[:count]):
        img_url = photo.get("src", {}).get("large", "") or photo.get("src", {}).get("original", "")
        if not img_url:
            continue
        
        ext = "jpg"
        filename = f"{query.replace(' ', '_')}_{i+1}.{ext}"
        filepath = os.path.join(output_dir, filename)
        
        try:
            img_r = requests.get(img_url, headers=headers, timeout=30)
            if img_r.ok:
                with open(filepath, "wb") as f:
                    f.write(img_r.content)
                size_kb = len(img_r.content) / 1024
                photographer = photo.get("photographer", "Unbekannt")
                print(f"  ✅ {filename} ({size_kb:.0f} KB) – Foto von {photographer}")
                downloaded.append(filepath)
            else:
                print(f"  ❌ {filename}: Download fehlgeschlagen ({img_r.status_code})")
        except Exception as e:
            print(f"  ❌ {filename}: {e}")
    
    return downloaded


def download_openverse(query, count=3, output_dir="downloads"):
    """Lade Bilder von Openverse (CC-lizensiert, kein Key)"""
    os.makedirs(output_dir, exist_ok=True)
    
    url = f"https://api.openverse.engineering/v1/images/?q={quote(query)}&page_size={count}"
    
    r = requests.get(url, timeout=15)
    if not r.ok:
        print(f"❌ Openverse Fehler: {r.status_code}")
        return []
    
    data = r.json()
    images = data.get("results", [])
    downloaded = []
    
    for i, img in enumerate(images[:count]):
        img_url = img.get("url", "")
        if not img_url:
            continue
        
        # Get highest quality version
        # Openverse URLs are often from Flickr/Wikimedia
        ext = img_url.split(".")[-1].split("?")[0][:4] if "." in img_url else "jpg"
        if len(ext) > 4:
            ext = "jpg"
        filename = f"cc_{query.replace(' ', '_')}_{i+1}.{ext}"
        filepath = os.path.join(output_dir, filename)
        
        try:
            img_r = requests.get(img_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
            if img_r.ok and len(img_r.content) > 1000:
                with open(filepath, "wb") as f:
                    f.write(img_r.content)
                size_kb = len(img_r.content) / 1024
                creator = img.get("creator", "Unbekannt")
                license_info = img.get("license", "CC")
                print(f"  ✅ {filename} ({size_kb:.0f} KB) – {license_info} von {creator}")
                downloaded.append(filepath)
            else:
                print(f"  ❌ {filename}: Download fehlgeschlagen")
        except Exception as e:
            print(f"  ❌ {filename}: {e}")
    
    return downloaded


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    query = sys.argv[1]
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    output_dir = sys.argv[3] if len(sys.argv) > 3 else f"bilder_{query.replace(' ', '_')}"
    
    print(f"\n🔍 Suche {count}x '{query}'...")
    print(f"📁 Speicherort: {output_dir}/\n")
    
    print("📸 Pexels:")
    pexels = download_pexels(query, count, output_dir)
    
    print(f"\n🌍 Openverse (CC-Lizenz):")
    openverse = download_openverse(query, count, output_dir)
    
    total = len(pexels) + len(openverse)
    print(f"\n{'='*50}")
    print(f"✅ Fertig! {total} Bilder geladen in '{output_dir}/'")
    print(f"💰 Kosten: 0,00€")
    
    # Show files
    for f in sorted(os.listdir(output_dir)):
        size = os.path.getsize(os.path.join(output_dir, f))
        print(f"  📁 {f} ({size//1024} KB)")
