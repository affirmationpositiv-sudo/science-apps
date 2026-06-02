#!/usr/bin/env python3
"""Generate Renaissance video frames with Pillow + combine with ffmpeg"""
import subprocess, os, shutil, textwrap, math
from PIL import Image, ImageDraw, ImageFont

out_dir = os.path.dirname(os.path.abspath(__file__))

videos = [
    {
        "name": "v01_intro",
        "title": "Was ist Renaissance?",
        "label": "Der neue Weg",
        "slides": [
            ("Bist du bereit für eine echte Veränderung?", "Die meisten Ansätze scheitern, weil sie von außen kommen.\nRenaissance ist anders. Von innen heraus."),
            ("Nicht blocken. Wachsen.", "Blocker-Apps umgehst du.\nScham macht es schlimmer.\nEnthaltsamkeit ohne Wachstum ist eine Zeitbombe."),
            ("Werde zu jemandem, für den\ndas kein Thema mehr ist", "Ersetze die Leere nicht mit Verboten.\nSondern mit echtem Wachstum.\nMit Skills, die dich stärker machen."),
            ("24/7 für dich da", "Dein KI-Coach kennt deine Fortschritte.\nGibt dir den richtigen Push.\nNiemals verurteilend. Immer für dich."),
            ("12 Wochen Programm", "Jede Woche ein neues Modul.\nSkills, die du wirklich lernen kannst.\nEine Community, die dich trägt."),
            ("Fang heute an", "Buche dein kostenloses Erstgespräch.\n30 Minuten. Kein Druck.\nNur ein ehrliches Gespräch."),
        ]
    },
    {
        "name": "v02_ansatz",
        "title": "Warum dieser Ansatz?",
        "label": "Die Wissenschaft",
        "slides": [
            ("Ehrliche Frage", "Wie oft hast du versucht aufzuhören?\nWie oft bist du zurückgefallen?\nDu bist nicht allein."),
            ("Warum Methoden scheitern", "Verbot erzeugt Widerstand.\nWiderstand erzeugt Scham.\nScham erzeugt mehr Konsum.\nEine Abwärtsspirale."),
            ("Der Renaissance-Unterschied", "Statt: Was muss ich aufgeben?\nFragen wir: Was willst du werden?\nEin fundamentaler Unterschied."),
            ("34 Bücher, 1 System", "Cialdini, Kahneman, James Clear.\nDie beste Wissenschaft in einem System.\nKI-gestützt. Für dich."),
            ("Dein persönliches Team", "KI-Coach + Jason (Qualität)\n+ Yesar (Motivation)\nDrei Persönlichkeiten. Ein Ziel: Dein Wachstum."),
            ("Jetzt starten", "Buche dein kostenloses Erstgespräch.\n30 Minuten. Kein Druck.\nLass uns loslegen."),
        ]
    },
    {
        "name": "v03_start",
        "title": "So startest du in 7 Tagen",
        "label": "Dein Fahrplan",
        "slides": [
            ("Tag 1: Das Gespräch", "30 Minuten mit einem echten Coach.\nDu erzählst. Wir hören zu.\nGemeinsam entscheiden wir, ob es passt."),
            ("Tag 2-3: Dein Start", "Wähle deinen ersten Skill.\nGitarre, Sport, Programmieren.\nWas immer dich antreibt."),
            ("Tag 4-5: Routine", "Tägliche Quests. Kurze Aufgaben.\nKI erinnert. Jason fordert.\nYesar feiert."),
            ("Tag 6-7: Erste Erfolge", "Neue Gewohnheit. Neuer Skill.\nDer Drang wird schwächer.\nNicht kämpfen. Wachsen."),
            ("Ab Woche 2", "Das volle Programm.\nModul für Modul. Community.\nLive-Coaching. Dein Weg."),
            ("Dein erster Schritt", "Buche dein kostenloses Gespräch.\nDer schwerste Schritt ist der erste.\nDu gehst ihn nicht alleine."),
        ]
    }
]

for vid in videos:
    print(f"\n🎬 {vid['title']}")
    name = vid["name"]
    slides = vid["slides"]
    audio_file = os.path.join(out_dir, f"{name}.mp3")
    
    if not os.path.exists(audio_file):
        print(f"  ❌ Audio nicht gefunden: {audio_file}")
        continue
    
    # Get audio duration
    result = subprocess.run(["ffmpeg", "-i", audio_file, "-f", "null", "-"],
                          capture_output=True, text=True, timeout=30)
    import re
    match = re.search(r"Duration: (\d+):(\d+):(\d+)\.(\d+)", result.stderr)
    if match:
        h, m, s, ms = map(int, match.groups())
        duration = h * 3600 + m * 60 + s + ms / 100
    else:
        duration = 120
    time_per_slide = duration / len(slides)
    fps = 1
    frames_per_slide = int(time_per_slide * fps)
    print(f"  Audio: {duration:.0f}s | Slides: {len(slides)} | {time_per_slide:.1f}s/slide")
    
    # Create frames directory
    frames_dir = os.path.join(out_dir, f"frames_{name}")
    os.makedirs(frames_dir, exist_ok=True)
    
    W, H = 1920, 1080
    
    # Try to find a font
    font_paths = [
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/HelveticaNeue.ttc",
        "/System/Library/Fonts/SFNS.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
    ]
    font_path = None
    for fp in font_paths:
        if os.path.exists(fp):
            font_path = fp
            break
    
    title_font = ImageFont.truetype(font_path or font_paths[-1], 72) if font_path else None
    subtitle_font = ImageFont.truetype(font_path or font_paths[-1], 36) if font_path else None
    info_font = ImageFont.truetype(font_path or font_paths[-1], 28) if font_path else None
    small_font = ImageFont.truetype(font_path or font_paths[-1], 20) if font_path else None
    
    for si, (title, subtitle) in enumerate(slides):
        for fi in range(frames_per_slide):
            frame_num = si * frames_per_slide + fi
            
            img = Image.new('RGB', (W, H), (10, 10, 26))
            draw = ImageDraw.Draw(img)
            
            # Background gradient
            for y in range(H):
                r = int(10 + (18 - 10) * y / H)
                g = int(10 + (18 - 10) * y / H)
                b = int(26 + (42 - 26) * y / H)
                draw.line([(0, y), (W, y)], fill=(r, g, b))
            
            # Decorative circles
            for cx, cy, r, c in [(100, 100, 200, (245, 158, 11, 8)), (1820, 980, 300, (99, 102, 241, 8))]:
                draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=None, outline=c, width=1)
            
            # Gold accent line at top
            draw.rectangle([(0, 0), (W, 4)], fill=(245, 158, 11))
            
            # Progress bar
            total_frames = len(slides) * frames_per_slide
            progress = (si * frames_per_slide + fi) / total_frames
            bar_w = int(1720 * progress)
            draw.rectangle([(100, 40), (100 + bar_w, 43)], fill=(245, 158, 11))
            draw.rectangle([(100 + bar_w, 40), (1820, 43)], fill=(26, 26, 62))
            
            # Slide counter
            if small_font:
                draw.text((100, 80), f"{si+1}/{len(slides)}", fill=(99, 102, 241), font=small_font)
                draw.text((160, 81), vid["title"], fill=(136, 146, 176), font=small_font)
            else:
                draw.text((100, 80), f"{si+1}/{len(slides)}", fill=(99, 102, 241))
                draw.text((160, 81), vid["title"], fill=(136, 146, 176))
            
            # Badge
            badge_text = f"✨ {vid['label']}"
            if small_font:
                draw.text((100, 130), badge_text, fill=(99, 102, 241), font=small_font)
            
            # Main title
            lines = title.split('\n')
            y_start = 350
            for li, line in enumerate(lines):
                y = y_start + li * 80
                if title_font:
                    draw.text((100, y), line, fill=(255, 255, 255), font=title_font)
                else:
                    draw.text((100, y), line, fill=(255, 255, 255))
            
            # Gold line
            draw.rectangle([(100, y_start + len(lines) * 80 + 20), (180, y_start + len(lines) * 80 + 23)], fill=(245, 158, 11))
            
            # Subtitle
            sub_lines = subtitle.split('\n')
            sub_y = y_start + len(lines) * 80 + 50
            for sli, sline in enumerate(sub_lines):
                if subtitle_font:
                    draw.text((100, sub_y + sli * 42), sline, fill=(204, 214, 246), font=subtitle_font)
                else:
                    draw.text((100, sub_y + sli * 42), sline, fill=(204, 214, 246))
            
            # Bottom branding
            if info_font:
                draw.text((W//2, 1000), "RENAISSANCE", fill=(99, 102, 241), font=info_font, anchor="mt")
                draw.text((W//2, 1035), "IKUNE KI-Coaching", fill=(136, 146, 176), font=small_font, anchor="mt")
            else:
                draw.text((W//2, 1000), "RENAISSANCE", fill=(99, 102, 241), anchor="mt")
                draw.text((W//2, 1035), "IKUNE KI-Coaching", fill=(136, 146, 176), anchor="mt")
            
            frame_path = os.path.join(frames_dir, f"frame_{frame_num:05d}.png")
            img.save(frame_path, "PNG")
        
        print(f"  Slides {si+1}/{len(slides)}: ✅ ({frames_per_slide} frames)")
    
    # Combine frames + audio into video
    video_path = os.path.join(out_dir, f"{name}.mp4")
    subprocess.run([
        "ffmpeg", "-y",
        "-framerate", str(fps),
        "-i", os.path.join(frames_dir, "frame_%05d.png"),
        "-i", audio_file,
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        "-movflags", "+faststart",
        video_path
    ], capture_output=True, timeout=300)
    
    size = os.path.getsize(video_path)
    print(f"  🎥 Video: {size/1024:.0f} KB")
    
    # Cleanup frames
    shutil.rmtree(frames_dir, ignore_errors=True)

print("\n✅ ALLE 3 VIDEOS FERTIG!")
