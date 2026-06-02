#!/usr/bin/env python3
"""Convert KDP book DOCX to PDF for Gumroad"""
import os, sys, re
from docx import Document
from reportlab.lib.pagesizes import A5
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.colors import HexColor

def esc(t):
    return t.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('"','&quot;')

base = '/Users/f.cinar/projects/science-apps/KDP_Books'
docx_path = f'{base}/KI-gestützte_Bewerbung_2026_KDP.docx'
pdf_path = f'{base}/KI-gestützte_Bewerbung_2026.pdf'

doc = Document(docx_path)

pdf = SimpleDocTemplate(pdf_path, pagesize=A5,
    topMargin=18*mm, bottomMargin=15*mm,
    leftMargin=14*mm, rightMargin=14*mm)

ts = ParagraphStyle('T', fontSize=18, spaceAfter=4, alignment=TA_CENTER,
    fontName='Helvetica-Bold', textColor=HexColor('#1a1a1a'))
ss = ParagraphStyle('S', fontSize=11, spaceAfter=24, alignment=TA_CENTER,
    fontName='Helvetica', textColor=HexColor('#666666'))
hs = ParagraphStyle('H', fontSize=13, spaceBefore=12, spaceAfter=4,
    fontName='Helvetica-Bold', textColor=HexColor('#222222'))
bs = ParagraphStyle('B', fontSize=10, leading=14, spaceAfter=3,
    fontName='Helvetica', textColor=HexColor('#333333'))

story = [
    Paragraph('KI-gestützte Bewerbung 2026', ts),
    Paragraph('Wie du mit ChatGPT &amp; Co. den perfekten Job bekommst', ss),
    Paragraph('<i>Licht und Schatten</i>', ss),
    Spacer(1, 24),
]

for p in doc.paragraphs:
    t = p.text.strip()
    if not t or t == 'Inhaltsverzeichnis':
        continue
    bold = p.runs and p.runs[0].bold
    sz = p.runs[0].font.size.pt if (p.runs and p.runs[0].font.size) else 11
    
    if bold and sz >= 14:
        story.append(Paragraph(esc(t), hs))
    elif bold and sz >= 12:
        s2 = ParagraphStyle('H2', parent=hs, fontSize=12)
        story.append(Paragraph(esc(t), s2))
    elif t.startswith('- ') or t.startswith('• '):
        story.append(Paragraph(f'&nbsp;&nbsp;•&nbsp;{esc(t[2:])}', bs))
    else:
        story.append(Paragraph(esc(t), bs))

pdf.build(story)
size = os.path.getsize(pdf_path) // 1024
print(f'✅ PDF: {pdf_path} ({size} KB)')
