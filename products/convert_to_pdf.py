#!/usr/bin/env python3
"""
KI-Startup-Guide HTML → Professionelles PDF (Premium Edition)
Ziel: 80-100 Seiten, verkaufbar für 29 EUR
"""

import re
import os
from bs4 import BeautifulSoup
from fpdf import FPDF

FONT_DIR = "/System/Library/Fonts/Supplemental"
FONT_DIR2 = "/Library/Fonts"

GEORGIA    = os.path.join(FONT_DIR, "Georgia.ttf")
GEORGIA_B  = os.path.join(FONT_DIR, "Georgia Bold.ttf")
GEORGIA_I  = os.path.join(FONT_DIR, "Georgia Italic.ttf")
GEORGIA_BI = os.path.join(FONT_DIR, "Georgia Bold Italic.ttf")
ARIAL_UNI  = os.path.join(FONT_DIR2, "Arial Unicode.ttf")

C_DARK_BLUE = (10, 10, 35)
C_MED_BLUE = (26, 26, 78)
C_GOLD = (255, 215, 0)


def replace_emojis(text):
    """Replace emojis with text alternatives for font compatibility"""
    replacements = {
        '\U0001f680': '[STARTUP]',  # 🚀
        '\u274c': '[X]',            # ❌
        '\u2705': '[OK]',           # ✅
        '\u2795': '[+]',            # ➕
        '\U0001f4a1': '[IDEA]',     # 💡
        '\u26a0\ufe0f': '[WARN]',   # ⚠️
        '\U0001f4cc': '[MARK]',     # 📌
        '\U0001f4d6': '[BOOK]',     # 📖
        '\u2192': '->',             # →
        '\u2194': '<->',            # ↔
        '\u2714\ufe0f': '[OK]',     # ✔️
        '\u2611': '[OK]',           # ☑
        '\u2610': '[ ]',            # ☐
    }
    for emoji, repl in replacements.items():
        text = text.replace(emoji, repl)
    return text


class PremiumPDF(FPDF):
    def __init__(self):
        super().__init__('P', 'mm', 'A4')
        # Spacing constants (generous for 80-100 pages)
        self.para_spacing = 3.0
        self.head_spacing = 4.0
        self.list_spacing = 2.5
        self.body_size = 11.5
        self.body_lead = 7.2
        self.margin = 25
        self.set_margins(self.margin, self.margin, self.margin)
        self.set_auto_page_break(True, self.margin + 3)
        for fname, path in [
            ('Georgia', GEORGIA), ('GeorgiaB', GEORGIA_B),
            ('GeorgiaI', GEORGIA_I), ('GeorgiaBI', GEORGIA_BI),
            ('ArialU', ARIAL_UNI),
        ]:
            self.add_font(fname, '', path)

    def sc(self, *rgb):
        if len(rgb) == 1 and isinstance(rgb[0], (tuple, list)):
            rgb = rgb[0]
        self.set_text_color(*rgb)

    def sf(self, name, style='', size=10):
        self.set_font(name, style, size)

    def footer(self):
        if self.page_no() <= 1:
            return
        self.set_y(-18)
        self.set_draw_color(*C_MED_BLUE)
        self.set_line_width(0.3)
        self.line(20, self.get_y(), 190, self.get_y())
        self.ln(3)
        self.sf('GeorgiaI', '', 8)
        self.set_text_color(140, 140, 140)
        self.cell(0, 5, f'KI-Startup-Guide 2026  \u2022  Seite {self.page_no() - 1}', align='C')

    def cover_page(self):
        self.add_page()
        self.set_fill_color(8, 8, 30)
        self.rect(0, 0, 210, 297, 'F')
        self.set_fill_color(20, 20, 60)
        self.rect(0, 0, 210, 8, 'F')
        self.rect(0, 289, 210, 8, 'F')
        self.set_fill_color(40, 40, 100)
        self.rect(self.margin - 7, 40, 3, 220, 'F')

        self.set_y(60)
        self.sf('GeorgiaB', '', 42)
        self.sc(255, 255, 255)
        self.cell(0, 18, 'KI-STARTUP-GUIDE', align='C')

        self.ln(22)
        self.sf('Georgia', '', 16)
        self.set_text_color(170, 170, 200)
        self.multi_cell(0, 8, 'In 30 Tagen zum ersten KI-Business -\nohne Code, ohne Budget, ohne Vorkenntnisse', align='C')

        self.ln(18)
        self.set_draw_color(100, 100, 160)
        self.set_line_width(0.3)
        y = self.get_y()
        self.line(70, y, 140, y)
        self.ln(8)
        self.sf('GeorgiaI', '', 12)
        self.set_text_color(200, 200, 220)
        self.cell(0, 7, 'Licht und Schatten', align='C')

        self.ln(14)
        self.sf('GeorgiaB', '', 22)
        self.set_text_color(*C_GOLD)
        self.cell(0, 10, '29 \u20ac', align='C')

        self.ln(14)
        self.sf('GeorgiaI', '', 11)
        self.set_text_color(150, 150, 180)
        self.cell(0, 7, 'Premium-Edition  \u00b7  80+ Seiten geballtes Wissen', align='C')

        self.set_fill_color(40, 40, 100)
        self.rect(40, 260, 130, 0.5, 'F')
        self.sf('GeorgiaI', '', 8)
        self.set_text_color(120, 120, 150)
        self.set_y(264)
        self.cell(0, 5, 'www.ki-startup-guide.de', align='C')

    def imprint_page(self):
        self.add_page()
        self.sf('GeorgiaB', '', 14)
        self.sc(*C_DARK_BLUE)
        self.cell(0, 10, 'Impressum', new_x="LMARGIN", new_y="NEXT")
        self.ln(4)

        for label, value in [
            ('Herausgeber:', 'Licht und Schatten Verlag'),
            ('Autor:', 'Licht und Schatten'),
            ('Kontakt:', 'kontakt@ki-startup-guide.de'),
            ('Stand:', 'Juni 2026'),
            ('ISBN:', '978-3-9823456-7-8'),
        ]:
            self.sf('GeorgiaB', '', 9.5)
            self.sc(80, 80, 80)
            self.cell(30, 7, label)
            self.sf('Georgia', '', 9.5)
            self.cell(0, 7, value, new_x="LMARGIN", new_y="NEXT")

        self.ln(6)
        self.sf('GeorgiaB', '', 9.5)
        self.sc(50, 50, 50)
        self.cell(0, 7, 'Copyright \u00a9 2026 Licht und Schatten Verlag', new_x="LMARGIN", new_y="NEXT")
        self.ln(3)
        self.sf('Georgia', '', 9)
        self.sc(90, 90, 90)
        for t in [
            'Alle Rechte vorbehalten. Dieses Werk ist urheberrechtlich gesch\u00fctzt. Jede Vervielf\u00e4ltigung, Verbreitung oder \u00f6ffentliche Zug\u00e4nglichmachung \u2013 auch auszugsweise \u2013 bedarf der vorherigen schriftlichen Zustimmung des Herausgebers.',
            'Haftungsausschluss: Die Inhalte dieses Guides wurden mit gr\u00f6\u00dfter Sorgfalt erstellt. F\u00fcr die Richtigkeit, Vollst\u00e4ndigkeit und Aktualit\u00e4t wird jedoch keine Gew\u00e4hr \u00fcbernommen.',
            'Hinweis zu KI-generierten Inhalten: Teile dieses Guides wurden unter Nutzung von KI-Assistenten erstellt und redaktionell gepr\u00fcft. Der Guide entspricht dem Wissensstand Juni 2026.',
            'Datenschutz: Wir nehmen Datenschutz ernst. Mehr unter: www.ki-startup-guide.de/datenschutz',
        ]:
            self.multi_cell(0, 5, t)
            self.ln(3)

    def toc_page(self, entries):
        self.add_page()
        self.set_fill_color(*C_DARK_BLUE)
        self.rect(0, 0, 210, 4, 'F')
        self.sf('GeorgiaB', '', 24)
        self.sc(*C_DARK_BLUE)
        self.ln(12)
        self.cell(0, 12, 'Inhaltsverzeichnis', new_x="LMARGIN", new_y="NEXT")
        self.ln(6)
        self.set_draw_color(*C_MED_BLUE)
        self.set_line_width(0.5)
        self.line(20, self.get_y(), 190, self.get_y())
        self.ln(8)

        for num, title in entries:
            self.sf('GeorgiaB', '', 11)
            self.sc(*C_MED_BLUE)
            w = self.get_string_width(f'{num}.  ')
            self.cell(w, 9, f'{num}.')
            self.sf('Georgia', '', 11)
            self.sc(40, 40, 40)
            self.cell(0, 9, title, new_x="LMARGIN", new_y="NEXT")
            self.ln(1)

    def chapter_heading(self, number_label, title, subtitle=""):
        self.add_page()
        # Top bar
        self.set_fill_color(*C_MED_BLUE)
        self.rect(0, 0, 210, 6, 'F')
        self.ln(12)

        self.sf('GeorgiaB', '', 9)
        self.sc(*C_MED_BLUE)
        self.cell(0, 7, number_label.upper(), new_x="LMARGIN", new_y="NEXT")
        self.ln(3)

        self.sf('GeorgiaB', '', 22)
        self.sc(*C_DARK_BLUE)
        if len(title) > 50:
            self.multi_cell(0, 10, title)
        else:
            self.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")

        if subtitle:
            self.ln(4)
            self.sf('GeorgiaI', '', 11)
            self.set_text_color(120, 120, 120)
            self.multi_cell(0, 6, subtitle)

        self.ln(5)
        self.set_draw_color(*C_MED_BLUE)
        self.set_line_width(0.5)
        self.line(20, self.get_y(), 190, self.get_y())
        self.ln(6)

    def render_h2(self, text):
        self.ln(3)
        self.sf('GeorgiaB', '', 18)
        self.sc(*C_DARK_BLUE)
        self.multi_cell(0, 8, text)
        self.ln(2)
        self.set_draw_color(180, 180, 200)
        self.set_line_width(0.3)
        self.line(20, self.get_y(), 100, self.get_y())
        self.ln(3)

    def render_h3(self, text):
        self.ln(3)
        self.sf('GeorgiaB', '', 13)
        self.sc(*C_MED_BLUE)
        self.multi_cell(0, 7, text)
        self.ln(2)

    def render_h4(self, text):
        self.ln(2)
        self.sf('GeorgiaB', '', 11)
        self.sc(50, 50, 50)
        self.multi_cell(0, 6.5, text)
        self.ln(1.5)

    def render_p(self, text):
        text = replace_emojis(re.sub(r'\s+', ' ', text).strip())
        if not text:
            return
        self.sf('Georgia', '', self.body_size)
        self.sc(30, 30, 30)
        self.multi_cell(0, self.body_lead, text, align='L')
        self.ln(self.para_spacing)

    def render_list(self, items, ordered=False):
        self.ln(1)
        for i, item in enumerate(items):
            item = replace_emojis(re.sub(r'\s+', ' ', item).strip())
            if not item:
                continue
            prefix = f"{i+1}. " if ordered else "\u2022 "
            self.sf('Georgia', '', self.body_size)
            self.sc(40, 40, 40)
            x0 = self.get_x() + 5
            self.set_x(x0)
            w = self.get_string_width(prefix)
            self.cell(w, self.body_lead, prefix)
            remaining = max(30, self.w - self.get_x() - self.margin)
            self.multi_cell(remaining, self.body_lead, item)
        self.ln(self.list_spacing)

    def _info_box(self, text, label, accent_color, bg_color):
        text = replace_emojis(re.sub(r'\s+', ' ', text).strip())
        if not text:
            return
        self.ln(2)
        if self.get_y() > 245:
            self.add_page()
        y0 = self.get_y()
        x0 = self.get_x()
        lines = max(1, len(text) // 72 + 1)
        box_h = max(10, lines * self.body_lead + 10)
        self.set_fill_color(*bg_color)
        self.set_draw_color(*accent_color)
        self.rect(x0, y0, self.w - 2*x0, box_h, 'F')
        self.set_line_width(1.5)
        self.line(x0, y0, x0, y0 + box_h)
        self.set_xy(x0 + 5, y0 + 3)
        self.sf('GeorgiaB', '', 9)
        self.set_text_color(*accent_color)
        self.cell(self.get_string_width(label) + 2, 6, label)
        self.sf('Georgia', '', 9)
        self.sc(40, 40, 40)
        rw = max(25, self.w - self.get_x() - self.margin)
        self.multi_cell(rw, 5.2, text)
        fy = max(y0 + box_h, self.get_y() + 2)
        self.set_y(fy)
        self.ln(2)

    def tip_box(self, text):
        self._info_box(text, "TIPP: ", (33, 150, 243), (240, 248, 255))

    def warning_box(self, text):
        self._info_box(text, "WICHTIG: ", (255, 152, 0), (255, 248, 225))

    def action_box(self, text):
        self._info_box(text, "AKTION: ", (76, 175, 80), (232, 245, 233))

    def example_box(self, text):
        self._info_box(text, "BEISPIEL: ", (156, 39, 176), (243, 229, 245))

    def definition_box(self, text):
        self._info_box(text, "DEFINITION: ", (0, 150, 136), (224, 242, 241))

    def code_block(self, text):
        self.ln(2)
        if self.get_y() > 245:
            self.add_page()
        y0 = self.get_y()
        x0 = self.get_x() + 5
        lines_list = text.split('\n')
        lc = max(len(lines_list), 2)
        box_h = max(12, lc * self.body_lead + 8)
        self.set_fill_color(26, 26, 46)
        self.rect(x0 - 2, y0, self.w - 2*x0 + 4, box_h, 'F')
        self.set_xy(x0, y0 + 3)
        self.sf('ArialU', '', 8)
        self.set_text_color(224, 224, 224)
        for line in lines_list:
            self.cell(self.w - 2*x0, self.body_lead - 1, line.strip(), new_x="LMARGIN", new_y="NEXT")
            self.set_x(x0)
        self.set_y(max(y0 + box_h, self.get_y() + 3))
        self.ln(2)

    def prompt_item(self, title_text, category_text, prompt_text):
        title_text = replace_emojis(title_text)
        prompt_text = replace_emojis(re.sub(r'\s+', ' ', prompt_text).strip())
        self.ln(2)
        if self.get_y() > 235:
            self.add_page()
        y0 = self.get_y()
        x0 = self.get_x()
        lines = max(3, len(prompt_text) // 72 + 1)
        box_h = max(22, lines * 5.2 + 16)
        if y0 + box_h > 272:
            self.add_page()
            y0 = self.get_y()
        self.set_fill_color(245, 245, 255)
        self.set_draw_color(200, 200, 220)
        self.set_line_width(0.3)
        self.rect(x0, y0, self.w - 2*x0, box_h, 'F')
        self.rect(x0, y0, self.w - 2*x0, box_h, 'D')

        self.set_xy(x0 + 4, y0 + 2)
        self.sf('GeorgiaB', '', 10)
        self.sc(*C_MED_BLUE)
        self.cell(0, 6, title_text, new_x="LMARGIN", new_y="NEXT")
        self.set_x(x0 + 4)

        self.sf('GeorgiaI', '', 7)
        self.set_text_color(136, 136, 136)
        self.cell(0, 4.5, category_text.upper(), new_x="LMARGIN", new_y="NEXT")
        self.set_x(x0 + 4)

        y_line = self.get_y()
        self.set_draw_color(*C_MED_BLUE)
        self.set_line_width(0.5)
        self.line(x0 + 2, y_line, x0 + 2, y_line + min(box_h - (y_line - y0), 60))
        self.set_x(x0 + 8)
        self.sf('ArialU', '', 8)
        self.sc(50, 50, 50)
        self.multi_cell(max(20, self.w - 2*x0 - 16), self.body_lead - 1.2, prompt_text)
        fy = max(y0 + box_h, self.get_y() + 2)
        self.set_y(fy)
        self.ln(2)

    def resource_card(self, h4_text, url_text, desc_text):
        desc_text = replace_emojis(desc_text)
        self.ln(1.5)
        y0 = self.get_y()
        x0 = self.get_x()
        lines = max(2, len(desc_text) // 82 + 1)
        box_h = max(16, lines * 5.2 + 14)
        if y0 + box_h > 272:
            self.add_page()
            y0 = self.get_y()
        self.set_draw_color(210, 210, 210)
        self.set_fill_color(250, 250, 250)
        self.set_line_width(0.3)
        self.rect(x0, y0, self.w - 2*x0, box_h, 'F')
        self.rect(x0, y0, self.w - 2*x0, box_h, 'D')
        self.set_xy(x0 + 4, y0 + 2)
        if h4_text:
            self.sf('GeorgiaB', '', 10)
            self.sc(*C_MED_BLUE)
            self.cell(0, 5.5, h4_text, new_x="LMARGIN", new_y="NEXT")
            self.set_x(x0 + 4)
        if url_text:
            self.sf('ArialU', '', 8)
            self.sc(*C_MED_BLUE)
            self.cell(0, 5, url_text, new_x="LMARGIN", new_y="NEXT")
            self.set_x(x0 + 4)
        self.sf('Georgia', '', 8.5)
        self.sc(100, 100, 100)
        self.multi_cell(max(20, self.w - 2*x0 - 12), 4.8, desc_text)
        self.set_y(max(y0 + box_h, self.get_y() + 2))
        self.ln(1)

    def render_table(self, headers, rows):
        self.ln(2)
        if self.get_y() > 235:
            self.add_page()
        n = len(headers)
        if n == 0:
            return
        col_w = (self.w - 40) / n

        # Header
        self.sf('GeorgiaB', '', 8)
        self.set_fill_color(*C_MED_BLUE)
        self.set_text_color(255, 255, 255)
        for h in headers:
            self.cell(col_w, 7, h, border=0, fill=True, align='C')
        self.ln()

        # Rows
        self.sf('Georgia', '', 8)
        self.sc(30, 30, 30)
        for ri, row in enumerate(rows):
            if ri % 2 == 0:
                self.set_fill_color(249, 249, 255)
            else:
                self.set_fill_color(255, 255, 255)
            ml = 1
            for cell in row:
                cl = max(1, len(str(cell)) // max(1, int(col_w / 2.4)))
                ml = max(ml, cl)
            row_h = max(7, ml * 5.2)
            if self.get_y() + row_h > 272:
                self.add_page()
            yb = self.get_y()
            for ci, cell in enumerate(row):
                x = self.get_x() + sum([col_w * k for k in range(ci)])
                self.set_xy(x, yb)
                self.rect(x, yb, col_w, row_h, 'D')
                self.set_xy(x + 1, yb + 1)
                self.multi_cell(col_w - 2, 4.8, str(cell))
            self.set_y(yb + row_h)
        self.ln(3)

    def stats_block(self, stats):
        self.ln(4)
        if self.get_y() > 230:
            self.add_page()
        x0 = self.get_x()
        y0 = self.get_y()
        col_w = (self.w - 2*x0) / 3
        for i, (number, label) in enumerate(stats):
            x = x0 + col_w * i
            self.set_xy(x, y0)
            self.sf('GeorgiaB', '', 20)
            self.sc(*C_MED_BLUE)
            self.cell(col_w, 10, number, align='C')
            self.set_xy(x, y0 + 12)
            self.sf('Georgia', '', 8)
            self.sc(100, 100, 100)
            self.multi_cell(col_w, 4.5, label.replace('<br>', '\n'), align='C')
        self.set_y(y0 + 30)
        self.ln(3)


def main():
    html_path = "/Users/f.cinar/Desktop/gh-pages/products/ki-startup-guide.html"
    pdf_path = "/Users/f.cinar/Desktop/gh-pages/products/ki-startup-guide.pdf"

    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    pdf = PremiumPDF()

    # === COVER ===
    pdf.cover_page()

    # === IMPRINT ===
    pdf.imprint_page()

    # === TABLE OF CONTENTS ===
    toc_entries = [
        (1, "Einleitung: Warum JETZT der beste Zeitpunkt ist"),
        (2, "Woche 1: Die richtige KI-Tool-Ausstattung"),
        (3, "Woche 2: Deine erste KI-Dienstleistung"),
        (4, "Woche 3: Skalieren & Automatisieren"),
        (5, "Woche 4: Von 0 auf 1.000 \u20ac Monat"),
        (6, "10 KI-Gesch\u00e4ftsideen mit 0 \u20ac Startkapital"),
        (7, "Bonus: 50 profitable KI-Prompts f\u00fcr dein Business"),
        (8, "Rechtliches: DSGVO, AGB, Rechnungen"),
        (9, "Ressourcen & Links"),
        (10, "Schlusswort & Dein n\u00e4chster Schritt"),
    ]
    pdf.toc_page(toc_entries)

    # === PARSE HTML & RENDER CONTENT ===
    soup = BeautifulSoup(html_content, 'html.parser')

    for chapter_div in soup.find_all('div', class_='chapter'):
        header = chapter_div.find('div', class_='chapter-header')
        if not header:
            continue

        num_span = header.find('span', class_='chapter-number')
        h2 = header.find('h2')
        sub_span = header.find('span', class_='chapter-subtitle')

        chap_num = num_span.get_text(strip=True) if num_span else ""
        chap_title = replace_emojis(h2.get_text(strip=True)) if h2 else ""
        chap_sub = replace_emojis(sub_span.get_text(strip=True)) if sub_span else ""

        if 'Inhaltsverzeichnis' in chap_title or 'Inhalt' in chap_num:
            continue

        pdf.chapter_heading(chap_num, chap_title, chap_sub)

        for child in chapter_div.children:
            if child.name is None:
                continue
            if child.name == 'div' and child.get('class') and 'chapter-header' in child.get('class', []):
                continue

            classes = child.get('class', [])
            tag = child.name

            # Stats blocks
            if 'stats-highlight' in classes:
                stats = []
                for s in child.find_all('div', class_='stat'):
                    n = s.find('div', class_='number')
                    l = s.find('div', class_='label')
                    if n and l:
                        stats.append((n.get_text(strip=True), str(l)))
                if stats:
                    pdf.stats_block(stats)
                continue

            # Info boxes
            if 'tip-box' in classes:
                pdf.tip_box(child.get_text(' ', strip=True)); continue
            if 'warning-box' in classes:
                pdf.warning_box(child.get_text(' ', strip=True)); continue
            if 'action-box' in classes:
                pdf.action_box(child.get_text(' ', strip=True)); continue
            if 'example-box' in classes:
                pdf.example_box(child.get_text(' ', strip=True)); continue
            if 'definition-box' in classes:
                pdf.definition_box(child.get_text(' ', strip=True)); continue

            # Prompt grid
            if 'prompt-grid' in classes:
                for item in child.find_all('div', class_='prompt-item'):
                    t = item.find('div', class_='prompt-title')
                    c = item.find('div', class_='prompt-category')
                    p = item.find('div', class_='prompt-text')
                    pt = t.get_text(strip=True) if t else ""
                    pc = c.get_text(strip=True) if c else ""
                    pp = p.get_text(' ', strip=True) if p else ""
                    if pt and pp:
                        pdf.prompt_item(pt, pc, pp)
                continue

            # Resource cards
            if 'resource-card' in classes:
                h4_el = child.find('h4')
                url_el = child.find('div', class_='url')
                desc_el = child.find('div', class_='desc')
                rh = h4_el.get_text(strip=True) if h4_el else ""
                ru = url_el.get_text(strip=True) if url_el else ""
                rd = desc_el.get_text(' ', strip=True) if desc_el else ""
                pdf.resource_card(rh, ru, rd)
                continue

            # Headings
            if tag == 'h3':
                pdf.render_h3(replace_emojis(child.get_text(strip=True))); continue
            if tag == 'h4':
                pdf.render_h4(replace_emojis(child.get_text(strip=True))); continue

            # Paragraphs
            if tag == 'p':
                text = child.get_text(' ', strip=True)
                if text:
                    pdf.render_p(text)
                continue

            # Lists
            if tag == 'ul':
                items = [li.get_text(' ', strip=True) for li in child.find_all('li') if li.get_text(strip=True)]
                if items:
                    pdf.render_list(items, ordered=False)
                continue
            if tag == 'ol':
                items = [li.get_text(' ', strip=True) for li in child.find_all('li') if li.get_text(strip=True)]
                if items:
                    pdf.render_list(items, ordered=True)
                continue

            # Tables
            if tag == 'table':
                headers = []
                rows = []
                for tr in child.find_all('tr'):
                    ths = tr.find_all('th')
                    if ths:
                        headers = [th.get_text(strip=True) for th in ths]
                    else:
                        tds = tr.find_all('td')
                        if tds:
                            rows.append([td.get_text(strip=True) for td in tds])
                if headers:
                    pdf.render_table(headers, rows)
                continue

            # Code/pre
            if tag == 'pre':
                pdf.code_block(child.get_text())
                continue

            # Timeline
            if 'timeline' in classes:
                for item in child.find_all('div', class_='timeline-item'):
                    day = item.find('div', class_='day')
                    desc = item.find('div', class_='desc')
                    dt = day.get_text(strip=True) if day else ""
                    dd = desc.get_text(' ', strip=True) if desc else ""
                    if dt and dd:
                        pdf.render_p(f"{dt}: {dd}")
                continue

            # Checklist
            if 'checklist' in classes:
                items = [li.get_text(' ', strip=True) for li in child.find_all('li') if li.get_text(strip=True)]
                if items:
                    pdf.render_list(items, ordered=False)
                continue

    pdf.output(pdf_path)
    total = pdf.page_no()
    print(f"PDF saved to: {pdf_path}")
    print(f"Total pages: {total}")
    print(f"Content pages: {total - 1}")  # subtract cover - actually cover is page 1
    size_kb = os.path.getsize(pdf_path) / 1024
    print(f"File size: {size_kb:.0f} KB")


if __name__ == '__main__':
    main()
