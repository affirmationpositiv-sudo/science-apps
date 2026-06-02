#!/usr/bin/env python3
"""
High-quality T-shirt design generator.
Generates 1200x1200 PNG mockups with gradients, patterns, and realistic shirt shapes.
"""

import math
import random
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

OUT_DIR = os.path.expanduser("~/Desktop/gh-pages/tshirt_designs")
SIZE = 1200
W, H = SIZE, SIZE

# ── Colour palettes ──────────────────────────────────────────────

PALETTES = {
    "minimal": {
        "bg": (15, 15, 20),
        "accent1": (99, 102, 241),    # Indigo
        "accent2": (168, 85, 247),    # Purple
        "accent3": (236, 72, 153),    # Pink
        "light": (240, 240, 255),
        "mid": (120, 120, 160),
    },
    "ki_ai": {
        "bg": (5, 5, 30),
        "accent1": (0, 200, 255),     # Cyan
        "accent2": (0, 120, 255),     # Blue
        "accent3": (120, 0, 255),     # Violet
        "light": (200, 240, 255),
        "mid": (80, 160, 255),
    },
    "money": {
        "bg": (10, 20, 10),
        "accent1": (255, 215, 0),     # Gold
        "accent2": (34, 197, 94),     # Green
        "accent3": (250, 204, 21),    # Yellow
        "light": (255, 250, 220),
        "mid": (150, 200, 100),
    },
    "gamer": {
        "bg": (25, 5, 35),
        "accent1": (255, 0, 128),     # Hot pink / magenta
        "accent2": (0, 255, 200),     # Teal
        "accent3": (255, 200, 0),     # Gold
        "light": (240, 220, 255),
        "mid": (200, 100, 255),
    },
    "geometric": {
        "bg": (10, 10, 18),
        "accent1": (255, 107, 107),   # Coral
        "accent2": (72, 219, 251),    # Sky
        "accent3": (255, 215, 100),   # Warm yellow
        "light": (240, 240, 255),
        "mid": (180, 180, 220),
    },
    "pets": {
        "bg": (30, 20, 15),
        "accent1": (255, 160, 122),   # Salmon
        "accent2": (200, 150, 100),   # Tan
        "accent3": (255, 200, 150),   # Peach
        "light": (255, 240, 230),
        "mid": (200, 160, 140),
    },
    "mountain": {
        "bg": (10, 15, 30),
        "accent1": (52, 211, 153),    # Emerald
        "accent2": (96, 165, 250),    # Blue
        "accent3": (251, 191, 36),    # Amber
        "light": (220, 240, 255),
        "mid": (100, 150, 200),
    },
    "cosmos": {
        "bg": (5, 2, 20),
        "accent1": (180, 100, 255),   # Violet
        "accent2": (0, 200, 255),     # Cyan
        "accent3": (255, 100, 200),   # Pink
        "light": (230, 220, 255),
        "mid": (150, 100, 200),
    },
}

# ── Drawing helpers ──────────────────────────────────────────────

def _rgba(c, a=255):
    """Convert a 3-tuple colour to 4-tuple with given alpha."""
    r, g, b = c
    return (r, g, b, a)


def make_gradient(w, h, colours, vertical=True):
    """Generate a gradient image."""
    img = Image.new("RGBA", (w, h))
    draw = ImageDraw.Draw(img)
    n = len(colours)
    band_h = h / (n - 1) if vertical else w / (n - 1)
    for i in range(n - 1):
        c1 = colours[i]
        c2 = colours[i + 1]
        for step in range(int(band_h) + 1):
            t = step / band_h if band_h > 0 else 0
            r = int(c1[0] * (1 - t) + c2[0] * t)
            g = int(c1[1] * (1 - t) + c2[1] * t)
            b = int(c1[2] * (1 - t) + c2[2] * t)
            if vertical:
                y0 = int(i * band_h) + step
                draw.line([(0, y0), (w, y0)], fill=(r, g, b))
            else:
                x0 = int(i * band_h) + step
                draw.line([(x0, 0), (x0, h)], fill=(r, g, b))
    return img


def radial_gradient(w, h, cx, cy, inner_colour, outer_colour):
    """Create a radial gradient."""
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    max_r = math.sqrt(max(cx, w - cx) ** 2 + max(cy, h - cy) ** 2)
    for r in range(int(max_r) + 1, 0, -1):
        t = r / max_r
        col = tuple(
            int(inner_colour[i] * (1 - t) + outer_colour[i] * t) for i in range(3)
        )
        draw.ellipse(
            [cx - r, cy - r, cx + r, cy + r],
            fill=(*col, min(255, int(255 * (1 - t) * 2))),
        )
    return img


def draw_rounded_rect(draw, xy, radius, fill=None, outline=None, width=1):
    """Draw a rounded rectangle."""
    x1, y1, x2, y2 = xy
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def draw_collared_shirt(base, colour, light_dir="left"):
    """
    Draw a t-shirt silhouette (front-facing crew neck / collared tee)
    onto 'base' image. The shirt body is a rounded trapezoid.
    """
    draw = ImageDraw.Draw(base)
    c = colour

    # ── Shirt body ──
    body_top = int(H * 0.12)
    body_bot = int(H * 0.94)
    neck_w = int(W * 0.22)
    neck_h = int(H * 0.06)
    shoulder_w = int(W * 0.18)
    hem_w = int(W * 0.28)

    cx = W // 2

    # Body polygon (trapezoid with rounded shoulders)
    points = [
        (cx - shoulder_w, body_top + neck_h),           # left shoulder
        (cx + shoulder_w, body_top + neck_h),           # right shoulder
        (cx + hem_w, body_bot),                         # right hem
        (cx - hem_w, body_bot),                         # left hem
    ]

    # Draw body
    draw.polygon(points, fill=c)

    # ── Neck (crew neck cutout) ──
    neck_colour = (max(0, c[0] - 25), max(0, c[1] - 25), max(0, c[2] - 25))
    draw.ellipse(
        [cx - neck_w // 2, body_top - 5, cx + neck_w // 2, body_top + neck_h + 10],
        fill=neck_colour,
    )

    # ── Collar band ──
    collar_colour = (min(255, c[0] + 20), min(255, c[1] + 20), min(255, c[2] + 20))
    draw.arc(
        [cx - neck_w // 2 - 8, body_top - 8, cx + neck_w // 2 + 8, body_top + neck_h + 12],
        start=0, end=180, fill=collar_colour, width=6,
    )

    # ── Sleeve lines (subtle) ──
    sleeve_colour = (max(0, c[0] - 15), max(0, c[1] - 15), max(0, c[2] - 15))
    # Left sleeve line
    draw.line(
        [(cx - shoulder_w, body_top + neck_h), (cx - shoulder_w - 40, body_top + int(H * 0.18))],
        fill=sleeve_colour, width=5,
    )
    # Right sleeve line
    draw.line(
        [(cx + shoulder_w, body_top + neck_h), (cx + shoulder_w + 40, body_top + int(H * 0.18))],
        fill=sleeve_colour, width=5,
    )

    # ── Bottom hem ──
    hem_colour = (max(0, c[0] - 10), max(0, c[1] - 10), max(0, c[2] - 10))
    draw.line(
        [(cx - hem_w, body_bot), (cx + hem_w, body_bot)],
        fill=hem_colour, width=4,
    )


def add_noise(base, intensity=8):
    """Add subtle film grain / noise."""
    noise = Image.effect_noise(base.size, intensity).convert("L")
    noise = noise.filter(ImageFilter.GaussianBlur(0.3))
    return ImageChops.overlay(base, noise.convert("RGBA"))


def add_vignette(base):
    """Add a subtle dark vignette around the edges."""
    v = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(v)
    cx, cy = W // 2, H // 2
    max_r = int(math.sqrt(cx ** 2 + cy ** 2) * 1.2)
    for r in range(max_r, 0, -1):
        t = r / max_r
        alpha = int(120 * (1 - t))
        if alpha > 0:
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(0, 0, 0, alpha))
    return Image.alpha_composite(base, v)


def draw_text_outlined(draw, xy, text, font, fill, outline_colour=(0, 0, 0, 180), outline_width=2):
    """Draw text with outline."""
    x, y = xy
    for dx in range(-outline_width, outline_width + 1):
        for dy in range(-outline_width, outline_width + 1):
            if dx != 0 or dy != 0:
                draw.text((x + dx, y + dy), text, font=font, fill=outline_colour)
    draw.text((x, y), text, font=font, fill=fill)


def create_texture(w, h, scale=20):
    """Create a subtle organic texture pattern."""
    img = Image.new("L", (w, h), 128)
    pixels = img.load()
    for x in range(w):
        for y in range(h):
            v = int(
                128
                + 30 * math.sin(x / scale)
                + 20 * math.cos(y / (scale * 0.7))
                + 10 * math.sin((x + y) / (scale * 0.5))
            )
            pixels[x, y] = max(0, min(255, v))
    return img


# ══════════════════════════════════════════════════════════════════
#  Design functions
# ══════════════════════════════════════════════════════════════════

def design1_minimal(palette):
    """Minimal Wave – clean sweeping curves with gradient fill."""
    img = Image.new("RGBA", (SIZE, SIZE), palette["bg"])
    draw = ImageDraw.Draw(img)

    # Background gradient
    bg_grad = make_gradient(W, H, [palette["bg"], (20, 20, 35), palette["bg"]])
    img = Image.alpha_composite(img, bg_grad)

    # Create a clipping mask for the shirt area
    shirt = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    draw_collared_shirt(shirt, (255, 255, 255, 25), light_dir="left")
    shirt = shirt.filter(ImageFilter.GaussianBlur(3))

    # Sweeping wave lines
    for offset in range(0, 4):
        amp = 80 + offset * 15
        freq = 0.008 - offset * 0.001
        y_base = 350 + offset * 110
        colour = (
            palette["accent1"][0] + offset * 20,
            palette["accent1"][1] + offset * 10,
            palette["accent2"][2] - offset * 20,
        )
        points = []
        for x in range(0, W + 2, 4):
            y = y_base + amp * math.sin(x * freq + offset * 1.5)
            points.append((x, y))
        if offset % 2 == 0:
            draw.line(points, fill=(*colour, 180 - offset * 20), width=8 - offset)
        else:
            draw.line(points, fill=(*colour, 150 - offset * 15), width=6 - offset)

    # Accent circles
    for i in range(12):
        r = random.randint(4, 12)
        x = random.randint(100, W - 100)
        y = random.randint(100, H - 100)
        alpha = random.randint(40, 100)
        col = palette["accent2"] if i % 3 == 0 else palette["accent1"] if i % 3 == 1 else palette["accent3"]
        draw.ellipse([x - r, y - r, x + r, y + r], fill=(*col, alpha))

    # Central text
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 72)
        font_small = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 32)
    except (IOError, OSError):
        font = ImageFont.load_default()
        font_small = ImageFont.load_default()

    draw_text_outlined(
        draw, (W // 2 - 180, H // 2 - 40), "WAVE", font,
        fill=(255, 255, 255, 220), outline_colour=(0, 0, 0, 160), outline_width=3,
    )
    draw_text_outlined(
        draw, (W // 2 - 100, H // 2 + 50), "minimal", font_small,
        fill=palette["accent1"] + (200,), outline_colour=(0, 0, 0, 120), outline_width=2,
    )

    img = Image.alpha_composite(img, shirt)
    img = add_vignette(img)
    img = img.filter(ImageFilter.SMOOTH)
    return img


def design2_ki_ai(palette):
    """KI · Artificial Intelligence – circuit-board inspired neural network."""
    img = Image.new("RGBA", (SIZE, SIZE), palette["bg"])
    draw = ImageDraw.Draw(img)

    # Deep tech background
    bg_grad = make_gradient(W, H, [palette["bg"], (0, 10, 40), palette["bg"]])
    img = Image.alpha_composite(img, bg_grad)

    # Grid pattern
    grid = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(grid)
    spacing = 40
    for x in range(0, W, spacing):
        gdraw.line([(x, 0), (x, H)], fill=(0, 200, 255, 15), width=1)
    for y in range(0, H, spacing):
        gdraw.line([(0, y), (W, y)], fill=(0, 200, 255, 15), width=1)
    img = Image.alpha_composite(img, grid)

    # Neural network nodes and connections
    nodes = []
    random.seed(42)
    for _ in range(30):
        nx = random.randint(80, W - 80)
        ny = random.randint(80, H - 80)
        nodes.append((nx, ny))

    # Connections
    for i, (x1, y1) in enumerate(nodes):
        for j, (x2, y2) in enumerate(nodes):
            if i < j and random.random() < 0.12:
                dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                alpha = max(20, int(80 - dist / 8))
                draw.line(
                    [(x1, y1), (x2, y2)],
                    fill=(0, 200, 255, alpha), width=random.randint(1, 3),
                )

    # Nodes
    for (nx, ny) in nodes:
        r = random.randint(4, 12)
        col = random.choice([palette["accent1"], palette["accent2"], palette["accent3"]])
        draw.ellipse(
            [nx - r, ny - r, nx + r, ny + r],
            fill=(*col, 200),
        )
        draw.ellipse(
            [nx - r - 3, ny - r - 3, nx + r + 3, ny + r + 3],
            fill=(*col, 40),
        )

    # Brain-like central shape
    cx, cy = W // 2, H // 2
    for r in range(60, 120, 6):
        t = (r - 60) / 60
        alpha = int(50 * (1 - t))
        col = tuple(
            int(palette["accent1"][i] * t + palette["accent2"][i] * (1 - t))
            for i in range(3)
        )
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(*col, alpha), width=2)

    # Text
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 64)
        font_sub = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 30)
    except (IOError, OSError):
        font = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    draw_text_outlined(
        draw, (W // 2 - 160, H // 2 - 170), "K I", font,
        fill=palette["light"] + (230,), outline_colour=(0, 0, 0, 180), outline_width=4,
    )
    draw_text_outlined(
        draw, (W // 2 - 200, H // 2 + 140), "artificial intelligence", font_sub,
        fill=palette["accent1"] + (200,), outline_colour=(0, 0, 0, 140), outline_width=2,
    )

    # Glow
    glow = radial_gradient(W, H, cx, cy, palette["accent1"], (0, 0, 0, 0))
    img = Image.alpha_composite(img, glow)

    img = add_vignette(img)
    img = img.filter(ImageFilter.SMOOTH)
    return img


def design3_money(palette):
    """Money Mindset – dollar/euro symbols with rising graph."""
    img = Image.new("RGBA", (SIZE, SIZE), palette["bg"])
    draw = ImageDraw.Draw(img)

    # Gradient background
    bg_grad = make_gradient(W, H, [palette["bg"], (15, 30, 15), palette["bg"]])
    img = Image.alpha_composite(img, bg_grad)

    # Rising chart line
    points = []
    for x in range(50, W - 50, 8):
        y = H - 100 - 200 * math.sin(x / 300) - 80 * math.cos(x / 100)
        points.append((x, y))

    # Gradient fill under chart
    poly_points = [(50, H)] + points + [(W - 50, H)]
    draw.polygon(poly_points, fill=(255, 215, 0, 30))

    # Chart line glow
    for w in range(8, 0, -2):
        draw.line(points, fill=(255, 215, 0, 30 + w * 10), width=w)

    draw.line(points, fill=(255, 215, 0, 255), width=5)

    # Dollar / Euro symbols floating up
    symbols = ["$", "€", "£", "¥"]
    for i in range(25):
        sym = random.choice(symbols)
        x = random.randint(80, W - 80)
        y = random.randint(80, H - 80)
        size = random.randint(20, 60)
        alpha = random.randint(30, 100)
        col = palette["accent1"] if random.random() > 0.5 else palette["accent2"]
        try:
            sfont = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size)
        except (IOError, OSError):
            sfont = ImageFont.load_default()
        draw.text((x, y), sym, font=sfont, fill=(*col, alpha))

    # Central "MONEY" text with gold gradient
    try:
        font_big = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 80)
        font_sub = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 28)
    except (IOError, OSError):
        font_big = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    draw_text_outlined(
        draw, (W // 2 - 180, H // 2 - 60), "MONEY", font_big,
        fill=(255, 215, 0, 240), outline_colour=(0, 0, 0, 180), outline_width=4,
    )
    draw_text_outlined(
        draw, (W // 2 - 120, H // 2 + 60), "min•dset", font_sub,
        fill=palette["accent2"] + (200,), outline_colour=(0, 0, 0, 120), outline_width=2,
    )

    # Sparkle dots
    for _ in range(50):
        x = random.randint(0, W)
        y = random.randint(0, H)
        r = random.uniform(0.5, 2.5)
        draw.ellipse(
            [x - r, y - r, x + r, y + r],
            fill=(255, 215, 0, random.randint(40, 180)),
        )

    img = add_vignette(img)
    img = img.filter(ImageFilter.SMOOTH)
    return img


def design4_gamer(palette):
    """Gamer Mode – retro controller with pixel-art aesthetic."""
    img = Image.new("RGBA", (SIZE, SIZE), palette["bg"])
    draw = ImageDraw.Draw(img)

    # Scanline background
    for y in range(0, H, 6):
        draw.rectangle([(0, y), (W, y + 2)], fill=(40, 10, 55, 60))

    # Neon glow background
    glow = radial_gradient(W, H, W // 2, H // 2, palette["accent1"], (0, 0, 0, 0))
    img = Image.alpha_composite(img, glow)

    # Game controller shape
    cx, cy = W // 2, H // 2 + 20

    # Controller body
    body_colour = (60, 20, 80)
    body_w, body_h = 320, 160
    draw.rounded_rectangle(
        [cx - body_w // 2, cy - body_h // 2, cx + body_w // 2, cy + body_h // 2],
        radius=40, fill=body_colour,
    )

    # Controller outline glow
    for i in range(3, 0, -1):
        draw.rounded_rectangle(
            [cx - body_w // 2 - i * 4, cy - body_h // 2 - i * 4,
             cx + body_w // 2 + i * 4, cy + body_h // 2 + i * 4],
            radius=40 + i * 4, outline=(255, 0, 128, 15 * i), width=1,
        )

    # D-pad (left)
    dpad_colour = (100, 100, 120)
    draw.rounded_rectangle(
        [cx - 120, cy - 30, cx - 60, cy + 30],
        radius=6, fill=dpad_colour,
    )
    draw.rounded_rectangle(
        [cx - 90, cy - 60, cx - 30, cy],
        radius=6, fill=dpad_colour,
    )

    # ABXY buttons (right)
    btn_r = 18
    btn_colours = [(0, 200, 100), (255, 50, 50), (50, 100, 255), (255, 200, 0)]
    btn_positions = [
        (cx + 60, cy - 50),   # Y
        (cx + 100, cy - 10),  # B
        (cx + 60, cy + 30),   # A
        (cx + 20, cy - 10),   # X
    ]
    for (bx, by), bcol in zip(btn_positions, btn_colours):
        draw.ellipse([bx - btn_r, by - btn_r, bx + btn_r, by + btn_r], fill=bcol)
        # Glow
        draw.ellipse([bx - btn_r - 2, by - btn_r - 2, bx + btn_r + 2, by + btn_r + 2],
                     outline=(*bcol, 100), width=2)

    # Center buttons (select / start)
    for offset in [-30, 30]:
        draw.ellipse(
            [cx + offset - 10, cy - 8, cx + offset + 10, cy + 8],
            fill=(80, 80, 100),
        )

    # Joysticks
    for offset_x in [-140, 140]:
        draw.ellipse(
            [cx + offset_x - 25, cy + 10, cx + offset_x + 25, cy + 60],
            fill=(80, 75, 90),
        )
        draw.ellipse(
            [cx + offset_x - 15, cy + 20, cx + offset_x + 15, cy + 50],
            fill=(130, 130, 150),
        )

    # Text
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 70)
        font_sub = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 28)
    except (IOError, OSError):
        font = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    draw_text_outlined(
        draw, (W // 2 - 200, H // 2 - 250), "GAMER", font,
        fill=(255, 255, 255, 230), outline_colour=(255, 0, 128, 160), outline_width=3,
    )
    draw_text_outlined(
        draw, (W // 2 - 100, H // 2 + 200), "press start", font_sub,
        fill=palette["accent2"] + (200,), outline_colour=(0, 0, 0, 140), outline_width=2,
    )

    img = add_vignette(img)
    img = img.filter(ImageFilter.SMOOTH)
    return img


def design5_geometric(palette):
    """Geometric Vision – layered polygons and sacred geometry."""
    img = Image.new("RGBA", (SIZE, SIZE), palette["bg"])
    draw = ImageDraw.Draw(img)

    # Background gradient
    bg_grad = make_gradient(W, H, [palette["bg"], (15, 15, 30), palette["bg"]])
    img = Image.alpha_composite(img, bg_grad)

    cx, cy = W // 2, H // 2 + 30

    # Concentric geometric rings
    for r in range(60, 480, 30):
        t = (r - 60) / 420
        alpha = int(60 * (1 - t))
        col = tuple(
            int(palette["accent1"][i] * (1 - t) + palette["accent2"][i] * t)
            for i in range(3)
        )
        draw.ellipse(
            [cx - r, cy - r, cx + r, cy + r],
            outline=(*col, alpha), width=2,
        )

    # Hexagon
    hex_radius = 200
    hex_points = []
    for i in range(6):
        angle = math.pi / 3 * i - math.pi / 6
        hx = cx + hex_radius * math.cos(angle)
        hy = cy + hex_radius * math.sin(angle)
        hex_points.append((hx, hy))
    draw.polygon(hex_points, outline=palette["accent1"] + (180,), width=4)
    # Inner hexagon
    hex_inner = [
        (cx + r * math.cos(a), cy + r * math.sin(a))
        for r in [130]
        for a in [math.pi / 3 * i - math.pi / 6 for i in range(6)]
    ]
    draw.polygon(hex_inner, outline=palette["accent3"] + (120,), width=2)

    # Triangle
    tri_radius = 280
    tri_points = []
    for i in range(3):
        angle = 2 * math.pi / 3 * i - math.pi / 2
        tx = cx + tri_radius * math.cos(angle)
        ty = cy + tri_radius * math.sin(angle)
        tri_points.append((tx, ty))
    draw.polygon(tri_points, outline=palette["accent3"] + (100,), width=2)

    # Star / compass lines from center
    for i in range(12):
        angle = math.pi / 6 * i
        ex = cx + 350 * math.cos(angle)
        ey = cy + 350 * math.sin(angle)
        col = palette["accent2"] if i % 2 == 0 else palette["accent1"]
        draw.line([(cx, cy), (ex, ey)], fill=(*col, 50), width=1)

    # Central dot
    draw.ellipse(
        [cx - 10, cy - 10, cx + 10, cy + 10],
        fill=palette["light"] + (200,),
    )

    # Text
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 56)
        font_sub = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 26)
    except (IOError, OSError):
        font = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    draw_text_outlined(
        draw, (W // 2 - 220, H // 2 - 290), "GEOMETRIC", font,
        fill=(255, 255, 255, 220), outline_colour=(0, 0, 0, 160), outline_width=3,
    )
    draw_text_outlined(
        draw, (W // 2 - 140, H // 2 + 320), "vision", font_sub,
        fill=palette["accent2"] + (200,), outline_colour=(0, 0, 0, 120), outline_width=2,
    )

    img = add_vignette(img)
    img = img.filter(ImageFilter.SMOOTH)
    return img


def design6_pets(palette):
    """Pet Love – cat and dog silhouette with hearts."""
    img = Image.new("RGBA", (SIZE, SIZE), palette["bg"])
    draw = ImageDraw.Draw(img)

    # Warm background
    bg_grad = make_gradient(W, H, [palette["bg"], (40, 25, 18), palette["bg"]])
    img = Image.alpha_composite(img, bg_grad)

    # Paw prints in background
    for i in range(12):
        px = random.randint(60, W - 60)
        py = random.randint(60, H - 60)
        alpha = random.randint(15, 40)
        pr = random.randint(20, 40)
        col = palette["mid"]
        # Main pad
        draw.ellipse([px - pr, py - pr, px + pr, py + pr], fill=(*col, alpha))
        # Toe pads
        for angle_offset in [0, 0.8, -0.8]:
            tx = px + pr * 1.1 * math.cos(angle_offset)
            ty = py + pr * 1.1 * math.sin(angle_offset)
            draw.ellipse([tx - pr * 0.5, ty - pr * 0.5, tx + pr * 0.5, ty + pr * 0.5],
                         fill=(*col, alpha))

    # Cat silhouette (simplified)
    cx_cat = W // 2 - 120
    cy_cat = H // 2 + 20
    cat_colour = palette["accent3"]

    # Cat body
    draw.ellipse([cx_cat - 70, cy_cat - 40, cx_cat + 70, cy_cat + 50], fill=(*cat_colour, 200))
    # Cat head
    draw.ellipse([cx_cat - 45, cy_cat - 100, cx_cat + 45, cy_cat - 20], fill=(*cat_colour, 200))
    # Cat ears
    ear_points_left = [(cx_cat - 35, cy_cat - 90), (cx_cat - 50, cy_cat - 140), (cx_cat - 15, cy_cat - 105)]
    ear_points_right = [(cx_cat + 35, cy_cat - 90), (cx_cat + 50, cy_cat - 140), (cx_cat + 15, cy_cat - 105)]
    draw.polygon(ear_points_left, fill=(*cat_colour, 200))
    draw.polygon(ear_points_right, fill=(*cat_colour, 200))
    # Cat eyes
    draw.ellipse([cx_cat - 20, cy_cat - 65, cx_cat - 8, cy_cat - 50], fill=(255, 255, 255, 200))
    draw.ellipse([cx_cat + 8, cy_cat - 65, cx_cat + 20, cy_cat - 50], fill=(255, 255, 255, 200))
    draw.ellipse([cx_cat - 15, cy_cat - 60, cx_cat - 12, cy_cat - 54], fill=(0, 0, 0, 200))
    draw.ellipse([cx_cat + 12, cy_cat - 60, cx_cat + 15, cy_cat - 54], fill=(0, 0, 0, 200))

    # Dog silhouette (simplified)
    cx_dog = W // 2 + 120
    cy_dog = H // 2 + 10
    dog_colour = palette["accent1"]

    # Dog body
    draw.ellipse([cx_dog - 75, cy_dog - 30, cx_dog + 75, cy_dog + 55], fill=(*dog_colour, 200))
    # Dog head
    draw.ellipse([cx_dog - 50, cy_dog - 95, cx_dog + 50, cy_dog - 25], fill=(*dog_colour, 200))
    # Dog ears (floppy)
    draw.ellipse([cx_dog - 55, cy_dog - 90, cx_dog - 30, cy_dog - 50], fill=(*dog_colour, 180))
    draw.ellipse([cx_dog + 30, cy_dog - 90, cx_dog + 55, cy_dog - 50], fill=(*dog_colour, 180))
    # Dog nose
    draw.ellipse([cx_dog - 8, cy_dog - 60, cx_dog + 8, cy_dog - 48], fill=(0, 0, 0, 200))
    # Dog eyes
    draw.ellipse([cx_dog - 22, cy_dog - 72, cx_dog - 12, cy_dog - 60], fill=(255, 255, 255, 200))
    draw.ellipse([cx_dog + 12, cy_dog - 72, cx_dog + 22, cy_dog - 60], fill=(255, 255, 255, 200))
    draw.ellipse([cx_dog - 18, cy_dog - 68, cx_dog - 15, cy_dog - 63], fill=(0, 0, 0, 200))
    draw.ellipse([cx_dog + 15, cy_dog - 68, cx_dog + 18, cy_dog - 63], fill=(0, 0, 0, 200))

    # Hearts floating
    heart_colour = (255, 80, 120)
    for heart_x, heart_y in [
        (W // 2 - 200, 180),
        (W // 2 + 200, 160),
        (W // 2, 280),
        (W // 2 - 150, 350),
        (W // 2 + 150, 330),
    ]:
        for scale in [1.0, 0.7, 0.4]:
            if random.random() < 0.5:
                continue
            r = 20 * scale
            draw.ellipse([heart_x - r, heart_y - r, heart_x, heart_y + r],
                         fill=(*heart_colour, int(150 * scale)))
            draw.ellipse([heart_x, heart_y - r, heart_x + r, heart_y + r],
                         fill=(*heart_colour, int(150 * scale)))
            draw.polygon(
                [(heart_x - r, heart_y), (heart_x + r, heart_y), (heart_x, heart_y + r * 1.4)],
                fill=(*heart_colour, int(150 * scale)),
            )

    # Text
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 60)
        font_sub = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 28)
    except (IOError, OSError):
        font = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    draw_text_outlined(
        draw, (W // 2 - 160, H // 2 - 260), "PET LOVE", font,
        fill=(255, 240, 230, 230), outline_colour=(0, 0, 0, 160), outline_width=3,
    )
    draw_text_outlined(
        draw, (W // 2 - 120, H // 2 + 280), "fur-ever", font_sub,
        fill=heart_colour + (200,), outline_colour=(0, 0, 0, 120), outline_width=2,
    )

    img = add_vignette(img)
    img = img.filter(ImageFilter.SMOOTH)
    return img


def design7_mountain(palette):
    """Mountain Calling – layered mountain silhouettes with sun gradient."""
    img = Image.new("RGBA", (SIZE, SIZE), palette["bg"])
    draw = ImageDraw.Draw(img)

    # Sky gradient: dark blue -> orange/pink -> dark
    sky_grad = make_gradient(W, H, [
        (5, 5, 30),
        (20, 15, 50),
        (60, 40, 80),
        (100, 60, 70),
        (150, 90, 60),
        (80, 60, 70),
        (10, 15, 30),
    ])
    img = Image.alpha_composite(img, sky_grad)

    # Sun
    sun_cx, sun_cy = W // 2, 200
    sun_r = 80
    for r in range(sun_r + 30, sun_r - 5, -2):
        t = (r - sun_r + 30) / 30
        alpha = int(60 * t)
        draw.ellipse(
            [sun_cx - r, sun_cy - r, sun_cx + r, sun_cy + r],
            fill=(255, 200, 100, alpha),
        )
    draw.ellipse(
        [sun_cx - sun_r, sun_cy - sun_r, sun_cx + sun_r, sun_cy + sun_r],
        fill=(255, 220, 120, 255),
    )

    # Mountain layers (back to front)
    mountains = [
        {"peaks": [(80, 600), (250, 350), (400, 500), (580, 280), (750, 450), (920, 320), (1120, 550)],
         "colour": (40, 30, 60, 120), "offset": 0},
        {"peaks": [(50, 700), (180, 450), (350, 550), (550, 380), (700, 520), (900, 350), (1150, 600)],
         "colour": (30, 40, 70, 160), "offset": 20},
        {"peaks": [(20, 800), (200, 550), (400, 650), (600, 460), (800, 580), (1000, 420), (1180, 650)],
         "colour": (20, 25, 50, 200), "offset": 40},
        {"peaks": [(0, 900), (150, 650), (350, 750), (550, 580), (750, 680), (950, 550), (1200, 700)],
         "colour": (15, 18, 35, 240), "offset": 60},
    ]

    for layer in mountains:
        pts = layer["peaks"]
        # Build polygon: left base -> peaks -> right base
        poly = [(pts[0][0] - 50, H)]
        for px, py in pts:
            poly.append((px, py + layer["offset"]))
        poly.append((pts[-1][0] + 50, H))
        draw.polygon(poly, fill=layer["colour"])

        # Snow caps
        for i in range(len(pts) - 1):
            px1, py1 = pts[i]
            px2, py2 = pts[i + 1]
            if py1 < py2 and py1 < 550:
                snow_h = 20
                draw.polygon(
                    [(px1 - 15, py1 + layer["offset"]),
                     (px1 + 15, py1 + layer["offset"]),
                     (px1 + 15, py1 + layer["offset"] + snow_h),
                     (px1 - 15, py1 + layer["offset"] + snow_h)],
                    fill=(255, 255, 255, int(100 * (1 - layer["offset"] / 80))),
                )

    # Stars
    random.seed(999)
    for _ in range(80):
        sx = random.randint(0, W)
        sy = random.randint(0, int(H * 0.35))
        sr = random.uniform(0.5, 2.0)
        alpha = random.randint(100, 220)
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(255, 255, 255, alpha))

    # Text
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 60)
        font_sub = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 26)
    except (IOError, OSError):
        font = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    draw_text_outlined(
        draw, (W // 2 - 240, 60), "MOUNTAIN", font,
        fill=(255, 255, 255, 230), outline_colour=(0, 0, 0, 180), outline_width=3,
    )
    draw_text_outlined(
        draw, (W // 2 - 120, 120), "calling", font_sub,
        fill=(255, 200, 100, 200), outline_colour=(0, 0, 0, 120), outline_width=2,
    )

    img = add_vignette(img)
    img = img.filter(ImageFilter.SMOOTH)
    return img


def design8_cosmos(palette):
    """Cosmos Explorer – nebula, stars, and planets."""
    img = Image.new("RGBA", (SIZE, SIZE), palette["bg"])
    draw = ImageDraw.Draw(img)

    # Deep space background
    bg_grad = make_gradient(W, H, [
        (2, 0, 10),
        (5, 2, 25),
        (10, 5, 35),
        (5, 2, 20),
        (2, 0, 10),
    ])
    img = Image.alpha_composite(img, bg_grad)

    # Nebula clouds (radial gradients placed around)
    nebula_spots = [
        (200, 300, palette["accent3"], 200),
        (900, 400, palette["accent1"], 180),
        (600, 700, palette["accent2"], 150),
        (350, 800, (100, 0, 150), 120),
        (850, 150, (0, 100, 200), 140),
    ]
    for nx, ny, ncol, nr in nebula_spots:
        neb = radial_gradient(W, H, nx, ny, ncol, (0, 0, 0, 0))
        # Scale down opacity
        neb = neb.point(lambda p: p * 0.15 if p > 0 else 0)
        img = Image.alpha_composite(img, neb)

    # Stars (large variety)
    random.seed(12345)
    for _ in range(400):
        sx = random.randint(0, W)
        sy = random.randint(0, H)
        sr = random.uniform(0.3, 3.0)
        alpha = random.randint(60, 255)
        col = (255, 255, 255) if random.random() > 0.3 else \
              palette["accent1"] if random.random() > 0.5 else palette["accent2"]
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(*col, alpha))

    # Star glow crosses (for bright stars)
    for _ in range(20):
        sx = random.randint(100, W - 100)
        sy = random.randint(100, H - 100)
        cross_len = random.randint(10, 25)
        col = (255, 255, 255, random.randint(40, 100))
        draw.line([(sx - cross_len, sy), (sx + cross_len, sy)], fill=col, width=1)
        draw.line([(sx, sy - cross_len), (sx, sy + cross_len)], fill=col, width=1)

    # Planet
    planet_cx, planet_cy = W // 2 + 100, H // 2 + 100
    planet_r = 60
    # Planet body gradient
    for r in range(planet_r, 0, -1):
        t = r / planet_r
        col = tuple(
            int(palette["accent1"][i] * (1 - t) + palette["accent2"][i] * t)
            for i in range(3)
        )
        draw.ellipse(
            [planet_cx - r, planet_cy - r, planet_cx + r, planet_cy + r],
            fill=(*col, 220),
        )
    # Planet ring
    draw.ellipse(
        [planet_cx - planet_r - 30, planet_cy - planet_r // 3,
         planet_cx + planet_r + 30, planet_cy + planet_r // 3],
        outline=(*palette["accent3"], 120), width=4,
    )
    # Planet shadow
    draw.ellipse(
        [planet_cx - planet_r, planet_cy - planet_r + 15,
         planet_cx + planet_r, planet_cy + planet_r],
        fill=(0, 0, 0, 60),
    )

    # Small moon
    moon_cx, moon_cy = planet_cx - 150, planet_cy - 80
    moon_r = 18
    draw.ellipse(
        [moon_cx - moon_r, moon_cy - moon_r, moon_cx + moon_r, moon_cy + moon_r],
        fill=(200, 200, 220, 200),
    )
    draw.ellipse(
        [moon_cx - moon_r // 2, moon_cy - moon_r // 2,
         moon_cx + moon_r // 2, moon_cy + moon_r // 2],
        fill=(100, 100, 120, 80),
    )

    # Orbit ring
    draw.ellipse(
        [planet_cx - 180, planet_cy - 120, planet_cx + 180, planet_cy + 120],
        outline=(255, 255, 255, 30), width=1,
    )

    # Text
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 62)
        font_sub = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 26)
    except (IOError, OSError):
        font = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    draw_text_outlined(
        draw, (W // 2 - 280, 60), "COSMOS", font,
        fill=(255, 255, 255, 230), outline_colour=(100, 0, 150, 160), outline_width=4,
    )
    draw_text_outlined(
        draw, (W // 2 - 160, 120), "explorer", font_sub,
        fill=palette["accent1"] + (200,), outline_colour=(0, 0, 0, 140), outline_width=2,
    )

    img = add_vignette(img)
    img = img.filter(ImageFilter.SMOOTH)
    return img


# ══════════════════════════════════════════════════════════════════
#  Main
# ══════════════════════════════════════════════════════════════════

def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    designs = [
        ("design1_minimal.png", design1_minimal, "minimal"),
        ("design2_ki_ai.png", design2_ki_ai, "ki_ai"),
        ("design3_money.png", design3_money, "money"),
        ("design4_gamer.png", design4_gamer, "gamer"),
        ("design5_geometric.png", design5_geometric, "geometric"),
        ("design6_pets.png", design6_pets, "pets"),
        ("design7_mountain.png", design7_mountain, "mountain"),
        ("design8_cosmos.png", design8_cosmos, "cosmos"),
    ]

    for filename, func, palette_key in designs:
        print(f"Generating {filename} ...", end=" ", flush=True)
        palette = PALETTES[palette_key]
        img = func(palette)
        out_path = os.path.join(OUT_DIR, filename)
        img.convert("RGB").save(out_path, "PNG", optimize=True)
        size_kb = os.path.getsize(out_path) / 1024
        print(f"done ({size_kb:.0f} KB)")

    print(f"\nAll designs saved to {OUT_DIR}")


if __name__ == "__main__":
    main()
