#!/usr/bin/env python3
"""Create Renaissance video slides and combine with audio into MP4"""
import subprocess, os, textwrap

out_dir = os.path.dirname(os.path.abspath(__file__))

videos = [
    {
        "name": "01_renaissance_intro",
        "title": "Was ist Renaissance?",
        "subtitle": "Der neue Weg, der Sucht durch Wachstum ersetzt",
        "slides": [
            ("Bist du bereit für eine Veränderung?", "Die meisten Ansätze scheitern, weil sie von außen kommen. Renaissance ist anders."),
            ("Das Problem", "Blocker-Apps umgehst du. Scham macht es schlimmer. Reine Enthaltsamkeit ohne Wachstum ist eine Zeitbombe."),
            ("Die Lösung", "Werde zu jemandem, für den das kein Thema mehr ist. Ersetze die Leere durch echtes Wachstum."),
            ("Dein KI-Coach", "24/7 für dich da. Kennt deine Fortschritte. Gibt dir den richtigen Push. Niemals verurteilend."),
            ("12 Wochen Programm", "Jede Woche ein neues Modul. Skills die dich stärker machen. Eine Community die dich trägt."),
            ("Fang heute an", "Buche dein kostenloses Erstgespräch. 30 Minuten. Kein Druck. Nur ein ehrliches Gespräch."),
        ]
    },
    {
        "name": "02_warum_dieser_ansatz",
        "title": "Warum dieser Ansatz?",
        "subtitle": "Die Wissenschaft hinter Renaissance",
        "slides": [
            ("Ehrliche Frage", "Wie oft hast du versucht aufzuhören? Wie oft bist du zurückgefallen?"),
            ("Warum Methoden scheitern", "Verbot erzeugt Widerstand. Widerstand erzeugt Scham. Scham erzeugt mehr Konsum."),
            ("Die Abwärtsspirale", "Je mehr du kämpfst, desto tiefer sinkst du. Nicht weil du schwach bist, sondern weil die Methode falsch ist."),
            ("Der Renaissance-Unterschied", "Statt 'Was muss ich aufgeben?' fragen wir: 'Was willst du werden?'"),
            ("34 Bücher, 1 System", "Cialdini, Kahneman, James Clear, Cal Newport. Die beste Wissenschaft in einem System."),
            ("Dein Team", "KI-Coach + Jason (Qualität) + Yesar (Motivation). Drei KI-Persönlichkeiten, ein Ziel: Dein Wachstum."),
        ]
    },
    {
        "name": "03_so_startest_du",
        "title": "So startest du in 7 Tagen",
        "subtitle": "Dein Fahrplan zur Veränderung",
        "slides": [
            ("Tag 1: Das Gespräch", "30 Minuten mit einem echten Coach. Du erzählst. Wir hören zu. Gemeinsam entscheiden wir, ob es passt."),
            ("Tag 2-3: Dein Start", "Wähle deinen ersten Skill. Gitarre, Sport, Programmieren, Sprache. Was immer dich antreibt."),
            ("Tag 4-5: Routine", "Tägliche Quests. Kurze, machbare Aufgaben. Der KI-Coach erinnert dich, Jason fordert dich, Yesar feiert dich."),
            ("Tag 6-7: Erste Erfolge", "Eine neue Gewohnheit. Ein neuer Skill. Der Drang wird schwächer. Nicht weil du kämpfst, sondern weil du wächst."),
            ("Ab Woche 2", "Das volle Programm. Modul für Modul. Community-Herausforderungen. Live-Coaching."),
            ("Dein erster Schritt", "Buche jetzt dein kostenloses Gespräch. Der schwerste Schritt ist der erste. Aber du gehst ihn nicht alleine."),
        ]
    }
]

def create_slide_image(text, subtitle, slide_num, total, output_path, bg_color="#0a0a1a"):
    """Create an SVG slide image"""
    # Escape text for SVG
    text_escaped = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
    sub_escaped = subtitle.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
    
    # Wrap long text
    sub_lines = textwrap.wrap(sub_escaped, width=50) if len(sub_escaped) > 60 else [sub_escaped]
    sub_formatted = "\\n".join(sub_lines)
    
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="1920" height="1080" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#0a0a1a"/>
      <stop offset="100%" stop-color="#12122a"/>
    </linearGradient>
    <linearGradient id="gold" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#f59e0b"/>
      <stop offset="100%" stop-color="#d97706"/>
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  <rect width="1920" height="1080" fill="url(#bg)"/>
  <!-- Decorative circles -->
  <circle cx="100" cy="100" r="200" fill="rgba(245,158,11,0.03)"/>
  <circle cx="1820" cy="980" r="300" fill="rgba(99,102,241,0.03)"/>
  <!-- Top accent line -->
  <rect x="0" y="0" width="1920" height="4" fill="url(#gold)"/>
  <!-- Progress bar -->
  <rect x="100" y="40" width="1720" height="3" rx="1.5" fill="#1a1a3e"/>
  <rect x="100" y="40" width="{1720 * slide_num // total}" height="3" rx="1.5" fill="#f59e0b"/>
  <!-- Slide number -->
  <text x="100" y="120" font-family="system-ui, sans-serif" font-size="18" fill="#6366f1" font-weight="600">{slide_num}/{total}</text>
  <!-- Main text -->
  <text x="160" y="120" font-family="system-ui, sans-serif" font-size="18" fill="#8892b0">{subtitle}</text>
  <!-- Title -->
  <text x="100" y="380" font-family="system-ui, sans-serif" font-size="64" fill="#ffffff" font-weight="700" filter="url(#glow)">{text_escaped}</text>
  <!-- Subtitle -->
  <text x="100" y="470" font-family="system-ui, sans-serif" font-size="28" fill="#ccd6f6" opacity="0.9">
    <tspan x="100" dy="0">{sub_lines[0] if sub_lines else ''}</tspan>
    {"".join(f'<tspan x="100" dy="38">{line}</tspan>' for line in sub_lines[1:])}
  </text>
  <!-- Decorative gold line -->
  <rect x="100" y="520" width="80" height="3" rx="1.5" fill="#f59e0b"/>
  <!-- Bottom branding -->
  <text x="960" y="1030" font-family="system-ui, sans-serif" font-size="16" fill="#6366f1" text-anchor="middle" font-weight="600">RENAISSANCE</text>
  <text x="960" y="1055" font-family="system-ui, sans-serif" font-size="12" fill="#8892b0" text-anchor="middle">IKUNE KI-Coaching</text>
</svg>'''
    with open(output_path, 'w') as f:
        f.write(svg)

for vid in videos:
    name = vid["name"]
    slides = vid["slides"]
    total = len(slides)
    print(f"\n🎬 {vid['title']} ({len(slides)} Slides)")
    
    # Create slide images
    slide_dir = os.path.join(out_dir, f"slides_{name}")
    os.makedirs(slide_dir, exist_ok=True)
    
    for i, (main_text, sub_text) in enumerate(slides, 1):
        svg_path = os.path.join(slide_dir, f"slide_{i:02d}.svg")
        png_path = os.path.join(slide_dir, f"slide_{i:02d}.png")
        
        if not os.path.exists(png_path):
            create_slide_image(main_text, vid["subtitle"], i, total, svg_path)
            # Convert SVG to PNG
            subprocess.run([
                "ffmpeg", "-y", "-i", svg_path, "-vf", "scale=1920:1080",
                "-frames:v", "1", png_path
            ], capture_output=True, timeout=30)
            print(f"  Slide {i}/{total}: ✅", end=" ")
    
    # Get audio duration
    audio_path = os.path.join(out_dir, f"{name}.mp3")
    result = subprocess.run([
        "ffmpeg", "-i", audio_path, "-f", "null", "-"
    ], capture_output=True, text=True, timeout=30)
    # Parse duration from stderr like "Duration: 01:23:45.67"
    import re
    match = re.search(r"Duration: (\d+):(\d+):(\d+)\.(\d+)", result.stderr)
    if match:
        h, m, s, ms = map(int, match.groups())
        audio_duration = h * 3600 + m * 60 + s + ms / 100
    else:
        audio_duration = 120  # fallback
    print(f"\n  Audio: {audio_duration:.0f}s")
    
    # Calculate time per slide
    time_per_slide = audio_duration / total
    print(f"  Time per slide: {time_per_slide:.1f}s")
    
    # Create concat file for ffmpeg
    concat_file = os.path.join(out_dir, f"concat_{name}.txt")
    with open(concat_file, 'w') as f:
        for i in range(1, total + 1):
            png_path = os.path.join(slide_dir, f"slide_{i:02d}.png")
            f.write(f"file '{png_path}'\n")
            f.write(f"duration {time_per_slide:.2f}\n")
        # Last frame needs to be written twice (ffmpeg quirk)
        f.write(f"file '{os.path.join(slide_dir, f'slide_{total:02d}.png')}'\n")
    
    # Create video
    output_video = os.path.join(out_dir, f"{name}.mp4")
    subprocess.run([
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", concat_file,
        "-i", audio_path,
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-vf", "fps=24",
        "-shortest",
        output_video
    ], capture_output=True, timeout=300)
    
    video_size = os.path.getsize(output_video)
    print(f"  🎥 Video: {video_size/1024:.0f} KB")
    
    # Cleanup (optional - keep for debugging)
    # shutil.rmtree(slide_dir, ignore_errors=True)
    # os.remove(concat_file)

print("\n✅ ALLE 3 VIDEOS FERTIG!")
