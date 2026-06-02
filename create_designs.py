"""Create t-shirt designs 6-8 using PIL."""
from PIL import Image, ImageDraw, ImageFont
import os, math, random

OUT = os.path.expanduser("~/Desktop/gh-pages/tshirt_designs")
os.makedirs(OUT, exist_ok=True)

W, H = 800, 800
BG = (245, 245, 240)  # cream

try:
    FONT = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
    FONT_S = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 16)
    FONT_L = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 36)
except:
    FONT = ImageFont.load_default()
    FONT_S = FONT
    FONT_L = FONT

def add_text(draw, text, pos, font=FONT, fill=(80,80,80), anchor="mm"):
    bbox = draw.textbbox((0,0), text, font=font)
    tw = bbox[2]-bbox[0]
    th = bbox[3]-bbox[1]
    draw.text((pos[0]-tw//2, pos[1]-th//2), text, fill=fill, font=font)

# ─── Design 6: Pets (Cat + Dog silhouettes) ───
def design6_pets():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    # Cat silhouette
    cx, cy = W//3, H//2-20
    cat_body = [(cx-40,cy+20),(cx+40,cy+20),(cx+50,cy-10),(cx+30,cy-20),
                (cx+30,cy-40),(cx+20,cy-50),(cx+10,cy-35),(cx-10,cy-35),
                (cx-20,cy-50),(cx-30,cy-40),(cx-30,cy-20),(cx-50,cy-10)]
    draw.polygon(cat_body, fill=(60,60,60))
    # Cat ears (triangles)
    draw.polygon([(cx-20,cy-40),(cx-25,cy-60),(cx-5,cy-45)], fill=(60,60,60))
    draw.polygon([(cx+20,cy-40),(cx+25,cy-60),(cx+5,cy-45)], fill=(60,60,60))
    # Cat tail
    tail = [(cx-48,cy-10),(cx-65,cy-25),(cx-70,cy-15),(cx-55,cy-5)]
    draw.line(tail, fill=(60,60,60), width=6)
    # Cat eyes
    draw.ellipse([cx-15,cy-15,cx-5,cy-5], fill=(255,200,100))
    draw.ellipse([cx+5,cy-15,cx+15,cy-5], fill=(255,200,100))
    draw.ellipse([cx-12,cy-12,cx-8,cy-8], fill=(40,40,40))
    draw.ellipse([cx+8,cy-12,cx+12,cy-8], fill=(40,40,40))
    # Cat nose
    draw.polygon([(cx-3,cy-2),(cx+3,cy-2),(cx,cy+2)], fill=(255,150,150))
    # Cat whiskers
    for yy in [cy-5, cy-2, cy+1]:
        draw.line([(cx-30,yy),(cx-10,yy-2)], fill=(100,100,100), width=1)
        draw.line([(cx+30,yy),(cx+10,yy-2)], fill=(100,100,100), width=1)

    # Dog silhouette
    dx, dy = 2*W//3, H//2
    # Dog head
    draw.ellipse([dx-35,dy-35,dx+5,dy+10], fill=(100,80,60))
    # Dog snout
    draw.ellipse([dx-5,dy-15,dx+30,dy+10], fill=(100,80,60))
    # Dog body
    draw.rounded_rectangle([dx-25,dy-15,dx+50,dy+40], radius=15, fill=(100,80,60))
    # Dog ears (floppy)
    draw.ellipse([dx-40,dy-35,dx-15,dy-5], fill=(80,60,40))
    draw.ellipse([dx+5,dy-35,dx+30,dy-5], fill=(80,60,40))
    # Dog nose
    draw.ellipse([dx+15,dy-8,dx+25,dy-2], fill=(40,40,40))
    # Dog eye
    draw.ellipse([dx-15,dy-22,dx-5,dy-12], fill=(40,40,40))
    # Dog tongue
    draw.ellipse([dx+18,dy-1,dx+26,dy+8], fill=(255,100,100))
    # Dog tail
    draw.line([(dx+48,dy+10),(dx+60,dy-5),(dx+55,dy-20)], fill=(100,80,60), width=6)
    # Dog collar
    draw.line([(dx-22,dy-8),(dx+28,dy-5)], fill=(200,50,50), width=4)
    # Dog tag
    draw.ellipse([dx-10,dy-5,dx+2,dy+5], fill=(255,200,50))

    # Hearts between them
    hx, hy = W//2, H//2-30
    for i in range(3):
        ox = hx + (i-1)*30
        oy = hy + (i%2)*20
        draw.ellipse([ox-10,oy-10,ox,oy], fill=(200,80,80))
        draw.ellipse([ox,oy-10,ox+10,oy], fill=(200,80,80))
        draw.polygon([(ox-10,oy-3),(ox+10,oy-3),(ox,oy+12)], fill=(200,80,80))

    add_text(draw, "Meine besten Freunde", (W//2, H-60), FONT_L, fill=(80,80,80))
    add_text(draw, "Licht und Schatten", (W//2, H-20), FONT_S, fill=(120,120,120))
    img.save(os.path.join(OUT, "design6_pets.png"))
    print("✓ design6_pets.png")

# ─── Design 7: Mountain landscape minimal ───
def design7_mountain():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    # Sky gradient
    for y in range(H//2):
        t = y / (H//2)
        r = int(40 + t * 40)
        g = int(40 + t * 50)
        b = int(80 + t * 60)
        draw.line([(0,y),(W,y)], fill=(r,g,b))

    # Stars
    for _ in range(30):
        sx = random.randint(0, W-1)
        sy = random.randint(0, H//3)
        sr = random.randint(1, 2)
        draw.ellipse([sx-sr, sy-sr, sx+sr, sy+sr], fill=(255,255,220))

    # Crescent moon
    mx, my = W-120, 80
    draw.ellipse([mx-30,my-30,mx+30,my+30], fill=(255,240,200))
    draw.ellipse([mx-15,my-20,mx+25,my+25], fill=(40,40,80,0))

    # Mountains
    mountains = [
        [(0,520), (100,250), (200,450), (300,200), (400,480), (500,280), (600,500)],
        [(50,560), (150,380), (250,530), (350,350), (450,520), (550,400), (650,550)],
        [(200,580), (350,420), (500,560)],
    ]
    colors = [(60,70,90), (70,80,100), (80,90,110)]
    for i, mtn in enumerate(mountains):
        pts = [(0,H)] + mtn + [(W,H)]
        draw.polygon(pts, fill=colors[i])

    # Snow caps
    snow_caps = [
        [(280,220),(300,200),(320,220),(300,210)],
        [(180,280),(200,250),(220,280),(200,265)],
    ]
    for cap in snow_caps:
        draw.polygon(cap, fill=(240,245,250))

    # Tree silhouettes
    for tx in [30, 60, 110, W-40, W-80, W-120]:
        tree_h = random.randint(40, 80)
        draw.polygon([(tx,540),(tx-8,540-tree_h),(tx+8,540-tree_h)], fill=(30,40,30))
        draw.rectangle([(tx-2,540),(tx+2,550)], fill=(50,40,30))

    # Ground
    draw.rectangle([(0,550),(W,H)], fill=(30,40,30))

    # Lake reflection
    for y in range(550, 620):
        alpha = 1 - (y-550)/70
        r = int(40 + (60-40)*alpha)
        g = int(50 + (70-50)*alpha)
        b = int(50 + (80-50)*alpha)
        draw.line([(0,y),(W,y)], fill=(r,g,b))

    add_text(draw, "GIPFELSTÜRMER", (W//2, H-65), FONT_L, fill=(200,200,200))
    add_text(draw, "Licht und Schatten", (W//2, H-25), FONT_S, fill=(150,150,150))
    img.save(os.path.join(OUT, "design7_mountain.png"))
    print("✓ design7_mountain.png")

# ─── Design 8: Cosmos (stars and space) ───
def design8_cosmos():
    img = Image.new("RGB", (W, H), (5, 5, 25))
    draw = ImageDraw.Draw(img)

    # Nebula gradient
    for y in range(H):
        t = y / H
        # nebula colors shifting
        r = int(5 + 30 * math.sin(t * math.pi * 2) ** 2)
        g = int(5 + 20 * math.cos(t * math.pi * 1.5) ** 2)
        b = int(20 + 60 * math.sin(t * math.pi * 1.8) ** 2)
        draw.line([(0,y),(W,y)], fill=(r,g,b))

    # Stars - many layers
    for _ in range(200):
        sx = random.randint(0, W-1)
        sy = random.randint(0, H-1)
        sr = random.uniform(0.5, 2.5)
        brightness = random.randint(150, 255)
        draw.ellipse([sx-sr, sy-sr, sx+sr, sy+sr], fill=(brightness, brightness, brightness-20))

    # Big bright stars with glow
    big_stars = [(120,100,12), (W-80,60,10), (W//2,180,8), (200, H-100,14), (W-150, H-80,9)]
    for sx, sy, sr in big_stars:
        # Glow
        for r in range(sr+8, sr, -1):
            a = int(30 * (1 - (r-sr)/8))
            draw.ellipse([sx-r, sy-r, sx+r, sy+r], fill=(200,200,255,a))
        draw.ellipse([sx-sr, sy-sr, sx+sr, sy+sr], fill=(255,255,240))

    # Galaxy band (diagonal)
    for i in range(300):
        t = i / 300
        gx = int(W * (0.2 + t * 0.6) + random.randint(-20, 20))
        gy = int(H * (0.1 + t * 0.8) + random.randint(-15, 15))
        size = random.randint(2, 5)
        color_val = random.randint(120, 200)
        color = (color_val, color_val-20, color_val+20) if random.random() > 0.5 else (color_val+10, color_val, color_val-10)
        draw.ellipse([gx-size, gy-size, gx+size, gy+size], fill=color)

    # Shooting stars
    for sx, sy, angle in [(300,80,45), (500,200,30), (150,350,60)]:
        length = random.randint(40, 80)
        ex = sx + int(length * math.cos(math.radians(angle)))
        ey = sy + int(length * math.sin(math.radians(angle)))
        for i in range(length):
            t = i / length
            x = int(sx + (ex-sx)*t)
            y = int(sy + (ey-sy)*t)
            a = int(255 * (1-t))
            draw.ellipse([x-2, y-2, x+2, y+2], fill=(255,255,255,a))

    # Planet
    px, py, pr = W//2, H//2-30, 50
    # Planet body
    draw.ellipse([px-pr, py-pr, px+pr, py+pr], fill=(80,100,180))
    # Planet bands
    for i in range(3):
        by = py - 15 + i*15
        draw.arc([px-pr-5, by-5, px+pr+5, by+5], 0, 180, fill=(100,130,200), width=3)
    # Planet glow
    draw.ellipse([px-pr-5, py-pr-5, px+pr+5, py+pr+5], fill=(100,130,255,30))

    # Ring around planet
    draw.ellipse([px-pr-25, py-8, px+pr+25, py+8], fill=(150,160,200,60))
    draw.ellipse([px-pr-20, py-5, px+pr+20, py+5], fill=(130,140,180,40))

    # Small planet/moon
    mpx, mpy = px+90, py-20
    draw.ellipse([mpx-10, mpy-10, mpx+10, mpy+10], fill=(180,170,150))

    # Constellations
    constellations = [
        [(150,120),(180,90),(220,100),(250,70)],
        [(W-120,H-100),(W-80,H-130),(W-50,H-90)],
    ]
    for stars in constellations:
        for i in range(len(stars)-1):
            draw.line([stars[i], stars[i+1]], fill=(200,200,255,60), width=1)
        for sx, sy in stars:
            draw.ellipse([sx-3, sy-3, sx+3, sy+3], fill=(255,255,255))

    add_text(draw, "UNENDLICHE WEITEN", (W//2, H-70), FONT_L, fill=(200,200,255))
    add_text(draw, "Licht und Schatten", (W//2, H-30), FONT_S, fill=(150,150,200))
    img.save(os.path.join(OUT, "design8_cosmos.png"))
    print("✓ design8_cosmos.png")

if __name__ == "__main__":
    design6_pets()
    design7_mountain()
    design8_cosmos()
    print("All 3 designs created!")
