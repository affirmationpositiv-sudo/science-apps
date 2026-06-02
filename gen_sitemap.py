#!/usr/bin/env python3
"""Generate complete sitemap.xml for science-apps GitHub Pages."""
import os

base_url = 'https://affirmationpositiv-sudo.github.io/science-apps'
exclude_dirs = {'node_modules', '.git', 'dist', 'assets', '__pycache__', '.expo', '.fseventsd'}
exclude_files = {'admin.html'}

today = '2026-06-03'

dir_priority = {
    '': 1.0,
    'blog': 0.8,
    'GalaxyBlog': 0.7,
    'affiliate': 0.6,
}
dir_freq = {
    '': 'weekly',
    'blog': 'weekly',
    'GalaxyBlog': 'weekly',
    'affiliate': 'monthly',
}

entries = []
for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if d not in exclude_dirs and not d.startswith('.')]
    for f in files:
        if not f.endswith('.html') or f in exclude_files:
            continue
        fpath = os.path.join(root, f)
        relpath = os.path.relpath(fpath, '.')

        # Skip certain patterns
        if relpath.startswith('shop/prompts-'):
            continue

        url = f'{base_url}/{relpath}'

        top_dir = relpath.split('/')[0] if '/' in relpath else ''
        prio = dir_priority.get(top_dir, 0.5)
        freq = dir_freq.get(top_dir, 'monthly')

        # Root index gets highest priority
        if relpath == 'index.html':
            prio = 1.0
            freq = 'weekly'
        # Blog articles get higher priority
        elif top_dir == 'blog':
            prio = 0.8
            freq = 'weekly'
        # Affiliate ratgeber articles
        elif top_dir == 'affiliate' and '/ratgeber/' in relpath:
            prio = 0.6
            freq = 'monthly'

        entries.append((relpath, url, prio, freq))

entries.sort(key=lambda x: x[0])

xml_parts = ['<?xml version="1.0" encoding="UTF-8"?>']
xml_parts.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
for relpath, url, prio, freq in entries:
    xml_parts.append('  <url>')
    xml_parts.append(f'    <loc>{url}</loc>')
    xml_parts.append(f'    <lastmod>{today}</lastmod>')
    xml_parts.append(f'    <changefreq>{freq}</changefreq>')
    xml_parts.append(f'    <priority>{prio}</priority>')
    xml_parts.append('  </url>')
xml_parts.append('</urlset>')

sitemap = '\n'.join(xml_parts)
with open('sitemap.xml', 'w', encoding='utf-8') as f:
    f.write(sitemap)

print(f'Sitemap written with {len(entries)} URLs ({len(sitemap):,} bytes)')
