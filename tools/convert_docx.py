#!/usr/bin/env python3
"""
Convert IBM Fusion Demo Guide .docx to Jekyll/GitHub Pages Markdown site.
"""

import sys
import os
import re
import json
import shutil
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

DOCX_PATH = "IBM Fusion Demo Guide v2.13.1.docx"
OUTPUT_DIR = "fusion-demo-guide"
IMAGES_DIR = f"{OUTPUT_DIR}/assets/images"

NS = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'v': 'urn:schemas-microsoft-com:vml',
    'o': 'urn:schemas-microsoft-com:office:office',
    'mc': 'http://schemas.openxmlformats.org/markup-compatibility/2006',
    'w14': 'http://schemas.microsoft.com/office/word/2010/wordml',
    'w15': 'http://schemas.microsoft.com/office/word/2012/wordml',
}

# Style → Markdown mapping
STYLE_MAP = {
    # Headings
    'heading1': '# ',
    'heading2': '## ',
    'heading3': '### ',
    'heading4': '#### ',
    'heading5': '##### ',
    # LCD styles
    'lcd-narration': 'blockquote',
    'lcd-narration1': 'blockquote',
    'lcd-narration2': 'blockquote',
    'lcd-narration3': 'blockquote',
    'lcd-uielement-bold': 'bold',
    'lcd-codeelement-mono': 'inline_code',
    'lcd-code': 'code_block',
    'lcd-code1': 'code_block',
    'lcd-code2': 'code_block',
    'lcd-code3': 'code_block',
    'codeblock': 'code_block',
    'htmlcode': 'code_block',
    'htmlpreformatted': 'code_block',
    # Lists
    'lcd-bulletlistcompact1': 'bullet_1',
    'lcd-bulletlistcompact2': 'bullet_2',
    'lcd-bulletlistcompact3': 'bullet_3',
    'lcd-bulletlist1': 'bullet_1',
    'lcd-bulletlist2': 'bullet_2',
    'lcd-bulletlist3': 'bullet_3',
    'lcd-listnumbering1': 'num_1',
    'lcd-listnumbering2': 'num_2',
    'lcd-listnumbering3': 'num_3',
    'listparagraph': 'bullet_1',
    # Notes
    'lcd-narration1': 'blockquote',
    # Skip
    'lcd-toc': 'skip',
    'toc1': 'skip',
    'toc2': 'skip',
    'toc3': 'skip',
    'toc4': 'skip',
    'toc5': 'skip',
    'lcd-disclaimer': 'skip',
    'lcd-doctitle': 'title',
    'lcd-doctitle2': 'subtitle',
    'lcd-caption': 'caption',
    'lcd-caption1': 'caption',
    'lcd-caption2': 'caption',
    'lcd-caption3': 'caption',
    'lcd-graphic': 'skip',
    'lcd-graphic1': 'skip',
    'lcd-graphic2': 'skip',
    'lcd-graphic3': 'skip',
    'lcd-spacer': 'skip',
    'tocheading': 'skip',
}

def get_style_key(style_id):
    """Normalize style ID for lookup."""
    if not style_id:
        return 'normal'
    return style_id.lower().replace(' ', '-').replace('_', '-')

def extract_hyperlinks(doc_zip):
    """Build a map from relationship ID to URL."""
    try:
        rels_xml = doc_zip.read('word/_rels/document.xml.rels')
        rels_root = ET.fromstring(rels_xml)
        links = {}
        for rel in rels_root:
            rid = rel.get('Id')
            target = rel.get('Target', '')
            rtype = rel.get('Type', '')
            if rid:
                links[rid] = target
        return links
    except:
        return {}

def extract_image_map(doc_zip):
    """Build a map from relationship ID to image filename."""
    try:
        rels_xml = doc_zip.read('word/_rels/document.xml.rels')
        rels_root = ET.fromstring(rels_xml)
        images = {}
        for rel in rels_root:
            rid = rel.get('Id')
            target = rel.get('Target', '')
            rtype = rel.get('Type', '')
            if rid and 'image' in rtype.lower():
                # target is like ../media/image1.png → media/image1.png
                filename = os.path.basename(target)
                images[rid] = filename
        return images
    except:
        return {}

def get_run_text(run, ns):
    """Extract text from a run, preserving hyperlinks."""
    parts = []
    for child in run:
        tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
        if tag == 't':
            parts.append(child.text or '')
        elif tag == 'br':
            parts.append('\n')
    return ''.join(parts)

def get_para_text_and_links(para, ns, hyperlinks):
    """Extract text with hyperlink markdown from a paragraph."""
    parts = []
    
    def process_run(run):
        text = get_run_text(run, ns)
        if not text:
            return
        # Check for bold/italic in run properties
        rPr = run.find('w:rPr', ns)
        is_bold = rPr is not None and (
            rPr.find('w:b', ns) is not None or 
            rPr.find('w:bCs', ns) is not None
        )
        is_italic = rPr is not None and rPr.find('w:i', ns) is not None
        is_code = rPr is not None and rPr.find('w:rStyle', ns) is not None and \
                  any(s in (rPr.find('w:rStyle', ns).get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val', '') or '').lower() 
                      for s in ['code', 'mono'])
        
        # Get style from run
        style_val = ''
        if rPr is not None:
            rStyle = rPr.find('w:rStyle', ns)
            if rStyle is not None:
                style_val = rStyle.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val', '')
        
        style_key = get_style_key(style_val)
        if 'lcd-uielement-bold' in style_key or 'uielement' in style_key:
            text = f'**{text}**'
        elif 'lcd-codeelement' in style_key or 'code-element' in style_key or 'codeelem' in style_key:
            text = f'`{text}`'
        elif is_code:
            text = f'`{text}`'
        
        parts.append(text)
    
    for child in para:
        tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
        
        if tag == 'r':
            process_run(child)
        elif tag == 'hyperlink':
            rid = child.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')
            url = hyperlinks.get(rid, '') if rid else ''
            # Also check anchor
            anchor = child.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}anchor', '')
            link_text = ''
            for run in child.findall('w:r', ns):
                link_text += get_run_text(run, ns)
            if link_text and url:
                parts.append(f'[{link_text}]({url})')
            elif link_text:
                parts.append(link_text)
        elif tag == 'ins':
            # Track changes - treat as inserted text
            for run in child.findall('w:r', ns):
                process_run(run)
    
    return ''.join(parts)

def get_para_images(para, ns, image_map):
    """Return list of image filenames referenced in this paragraph."""
    images = []
    blip_ns = 'http://schemas.openxmlformats.org/drawingml/2006/main'
    for blip in para.findall(f'.//{{{blip_ns}}}blip'):
        rid = blip.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')
        if rid and rid in image_map:
            images.append(image_map[rid])
    # Also check VML
    for img in para.findall('.//v:imagedata', ns):
        rid = img.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')
        if rid and rid in image_map:
            images.append(image_map[rid])
    return images

def slugify(text):
    """Convert heading text to a URL slug."""
    text = text.strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s]+', '-', text)
    text = text.lower().strip('-')
    return text or 'section'

def para_to_markdown(style_key, text, images, num_counter=None):
    """Convert a paragraph to markdown string(s)."""
    lines = []
    mapped = STYLE_MAP.get(style_key, 'normal')
    
    # Images first
    for img in images:
        lines.append(f'![Screenshot]({{{{ site.baseurl }}}}/assets/images/{img})\n')
    
    if not text.strip() and not images:
        return []
    
    if mapped == 'skip':
        return lines  # skip text, keep images if any
    if mapped == 'title':
        lines.append(f'# {text}')
    elif mapped == 'subtitle':
        lines.append(f'*{text}*')
    elif mapped == 'caption':
        lines.append(f'*{text}*')
    elif mapped == 'blockquote':
        lines.append(f'> {text}')
    elif mapped == 'bold':
        lines.append(f'**{text}**')
    elif mapped == 'inline_code':
        lines.append(f'`{text}`')
    elif mapped == 'code_block':
        lines.append(f'```\n{text}\n```')
    elif mapped == '# ':
        lines.append(f'# {text}')
    elif mapped in ('## ', '### ', '#### ', '##### '):
        lines.append(f'{mapped}{text}')
    elif mapped.startswith('bullet_'):
        level = int(mapped[-1])
        indent = '  ' * (level - 1)
        lines.append(f'{indent}- {text}')
    elif mapped.startswith('num_'):
        level = int(mapped[-1])
        indent = '  ' * (level - 1)
        lines.append(f'{indent}1. {text}')
    else:
        if text.strip():
            lines.append(text)
    
    return lines

def get_table_markdown(table, ns, hyperlinks):
    """Convert a table element to GFM markdown."""
    rows = table.findall('.//w:tr', ns)
    if not rows:
        return []
    
    all_row_cells = []
    for row in rows:
        cells = row.findall('w:tc', ns)
        row_texts = []
        for cell in cells:
            cell_text = ''
            for para in cell.findall('w:p', ns):
                cell_text += get_para_text_and_links(para, ns, hyperlinks)
            row_texts.append(cell_text.strip().replace('|', '\\|'))
        all_row_cells.append(row_texts)
    
    if not all_row_cells:
        return []
    
    lines = []
    # Header row
    header = all_row_cells[0]
    lines.append('| ' + ' | '.join(header) + ' |')
    lines.append('| ' + ' | '.join(['---'] * len(header)) + ' |')
    # Data rows
    for row in all_row_cells[1:]:
        # Pad to header length
        while len(row) < len(header):
            row.append('')
        lines.append('| ' + ' | '.join(row[:len(header)]) + ' |')
    
    return lines

def build_section_slug(heading_text, existing_slugs):
    """Build a unique slug for a heading."""
    base = slugify(heading_text)
    if not base:
        base = 'section'
    slug = base
    i = 2
    while slug in existing_slugs:
        slug = f'{base}-{i}'
        i += 1
    existing_slugs.add(slug)
    return slug

# ─── MAIN ────────────────────────────────────────────────────────────────────

print("Opening docx...")
with zipfile.ZipFile(DOCX_PATH) as zf:
    doc_xml = zf.read('word/document.xml')
    hyperlinks = extract_hyperlinks(zf)
    image_map = extract_image_map(zf)
    
    # Copy images
    os.makedirs(IMAGES_DIR, exist_ok=True)
    for name in zf.namelist():
        if name.startswith('word/media/'):
            filename = os.path.basename(name)
            dest = os.path.join(IMAGES_DIR, filename)
            with zf.open(name) as src, open(dest, 'wb') as dst:
                dst.write(src.read())

print(f"Extracted {len(image_map)} image references")
print(f"Copied images to {IMAGES_DIR}")

# Parse document
root = ET.fromstring(doc_xml)
body = root.find('.//w:body', NS)

# First pass: collect all paragraphs and tables with metadata
elements = []
for child in body:
    tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
    
    if tag == 'p':
        pPr = child.find('w:pPr', NS)
        style_id = 'Normal'
        if pPr is not None:
            pStyle = pPr.find('w:pStyle', NS)
            if pStyle is not None:
                style_id = pStyle.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val', 'Normal')
        
        text = get_para_text_and_links(child, NS, hyperlinks)
        images = get_para_images(child, NS, image_map)
        elements.append({'type': 'para', 'style': style_id, 'text': text, 'images': images})
    
    elif tag == 'tbl':
        table_md = get_table_markdown(child, NS, hyperlinks)
        elements.append({'type': 'table', 'lines': table_md})
    
    elif tag == 'sectPr':
        pass  # skip section properties

print(f"Parsed {len(elements)} elements")

# Identify H1 sections to split into pages
# Skip front matter (ToC, legal, title page) - start from first Heading1
pages = []
current_page = None
in_toc = True
existing_slugs = set()

for elem in elements:
    if elem['type'] != 'para':
        if current_page is not None:
            current_page['elements'].append(elem)
        continue
    
    style_key = get_style_key(elem['style'])
    text = elem['text'].strip()
    
    # Skip TOC entries
    if style_key in ('toc1', 'toc2', 'toc3', 'toc4', 'toc5', 'toc6', 'toc7', 'toc8', 'toc9', 'lcd-toc', 'tocheading'):
        continue
    
    is_h1 = style_key in ('heading1',)
    
    if is_h1 and text:
        # Start a new page
        slug = build_section_slug(text, existing_slugs)
        current_page = {
            'title': text,
            'slug': slug,
            'elements': []
        }
        pages.append(current_page)
    elif current_page is not None:
        current_page['elements'].append(elem)
    # else: front matter before first H1 - skip

print(f"Identified {len(pages)} sections")

# Build markdown for each page
def elements_to_markdown(elements):
    lines = []
    code_block_open = False
    prev_was_code = False
    
    for elem in elements:
        if elem['type'] == 'table':
            if code_block_open:
                lines.append('```')
                code_block_open = False
            lines.append('')
            lines.extend(elem['lines'])
            lines.append('')
            prev_was_code = False
            continue
        
        style_key = get_style_key(elem['style'])
        text = elem['text'].strip()
        images = elem.get('images', [])
        
        # Handle images
        for img in images:
            if code_block_open:
                lines.append('```')
                code_block_open = False
            lines.append('')
            lines.append(f'![Screenshot]({{{{ site.baseurl }}}}/assets/images/{img})')
            lines.append('')
        
        if not text:
            if not images:
                # Blank paragraph - close code block if open
                if code_block_open:
                    lines.append('```')
                    code_block_open = False
                    lines.append('')
            continue
        
        mapped = STYLE_MAP.get(style_key, 'normal')
        
        if mapped == 'skip':
            continue
        elif mapped == 'code_block':
            if not code_block_open:
                lines.append('')
                lines.append('```')
                code_block_open = True
            lines.append(text)
            prev_was_code = True
            continue
        else:
            if code_block_open:
                lines.append('```')
                code_block_open = False
                lines.append('')
            prev_was_code = False
        
        md_lines = para_to_markdown(style_key, text, [])  # images already handled
        for ml in md_lines:
            lines.append(ml)
    
    if code_block_open:
        lines.append('```')
    
    return '\n'.join(lines)

# Create output directories
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(f'{OUTPUT_DIR}/_pages', exist_ok=True)
os.makedirs(f'{OUTPUT_DIR}/_data', exist_ok=True)
os.makedirs(f'{OUTPUT_DIR}/_layouts', exist_ok=True)

# Write each page
nav_items = []
for i, page in enumerate(pages):
    content = elements_to_markdown(page['elements'])
    slug = page['slug']
    title = page['title']
    
    if i == 0:
        # First section becomes index.md
        filepath = f'{OUTPUT_DIR}/index.md'
        permalink = '/'
    else:
        filepath = f'{OUTPUT_DIR}/_pages/{slug}.md'
        permalink = f'/{slug}/'
    
    front_matter = f"""---
layout: default
title: "{title}"
permalink: {permalink}
nav_order: {i + 1}
---

# {title}

"""
    with open(filepath, 'w') as f:
        f.write(front_matter + content)
    
    nav_items.append({'title': title, 'url': permalink, 'slug': slug})
    print(f"  Written: {filepath}")

# Write _config.yml
config = """title: IBM Fusion Demo Guide
description: Platform modernization with IBM Fusion - Hands-on demo guide v2.13.1
baseurl: "/fusion-demo-guide"
url: ""

theme: minima

# Build settings
markdown: kramdown
highlighter: rouge

kramdown:
  input: GFM
  syntax_highlighter: rouge

# Collections
collections:
  pages:
    output: true
    permalink: /:name/

# Navigation
header_pages:
  - index.md
"""

with open(f'{OUTPUT_DIR}/_config.yml', 'w') as f:
    f.write(config)

# Write nav data
nav_data = {'nav': nav_items}
with open(f'{OUTPUT_DIR}/_data/navigation.yml', 'w') as f:
    f.write('nav:\n')
    for item in nav_items:
        f.write(f'  - title: "{item["title"]}"\n')
        f.write(f'    url: "{item["url"]}"\n')

# Write a simple default layout
layout_html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{ page.title }} | {{ site.title }}</title>
  <link rel="stylesheet" href="{{ site.baseurl }}/assets/css/style.css">
</head>
<body>
  <nav class="site-nav">
    <div class="nav-inner">
      <a class="site-title" href="{{ site.baseurl }}/">{{ site.title }}</a>
      <ul class="nav-links">
        {% for item in site.data.navigation.nav %}
          <li><a href="{{ site.baseurl }}{{ item.url }}"{% if page.url == item.url %} class="active"{% endif %}>{{ item.title }}</a></li>
        {% endfor %}
      </ul>
    </div>
  </nav>
  <main class="content">
    {{ content }}
  </main>
</body>
</html>
"""
with open(f'{OUTPUT_DIR}/_layouts/default.html', 'w') as f:
    f.write(layout_html)

# Write CSS
os.makedirs(f'{OUTPUT_DIR}/assets/css', exist_ok=True)
css = """/* IBM Fusion Demo Guide - GitHub Pages Styles */
*, *::before, *::after { box-sizing: border-box; }

body {
  font-family: -apple-system, "Segoe UI", system-ui, sans-serif;
  font-size: 15px;
  line-height: 1.7;
  color: #1f2328;
  background: #ffffff;
  margin: 0;
}

.site-nav {
  background: #0f62fe;
  color: #ffffff;
  padding: 0 1rem;
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav-inner {
  max-width: 960px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  gap: 1.5rem;
  padding: 0.75rem 0;
  flex-wrap: wrap;
}

.site-title {
  font-weight: 700;
  font-size: 1rem;
  color: #ffffff;
  text-decoration: none;
  white-space: nowrap;
}

.nav-links {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-wrap: wrap;
  gap: 0.25rem;
}

.nav-links li a {
  color: rgba(255,255,255,0.85);
  text-decoration: none;
  font-size: 0.85rem;
  padding: 0.2rem 0.5rem;
  border-radius: 3px;
}

.nav-links li a:hover,
.nav-links li a.active {
  background: rgba(255,255,255,0.2);
  color: #ffffff;
}

.content {
  max-width: 860px;
  margin: 2rem auto;
  padding: 0 1.5rem 4rem;
}

h1 { font-size: 1.9rem; border-bottom: 2px solid #e5e7eb; padding-bottom: 0.4rem; margin-top: 2.5rem; }
h2 { font-size: 1.4rem; margin-top: 2rem; color: #1f2328; }
h3 { font-size: 1.15rem; margin-top: 1.5rem; }
h4 { font-size: 1rem; margin-top: 1.25rem; color: #57606a; }

p { margin: 0.75rem 0; }

blockquote {
  margin: 1rem 0;
  padding: 0.75rem 1rem;
  border-left: 4px solid #0f62fe;
  background: #f0f4ff;
  color: #1f2328;
  border-radius: 0 4px 4px 0;
}

blockquote p { margin: 0; }

pre {
  background: #1e1e1e;
  color: #d4d4d4;
  padding: 1rem 1.25rem;
  border-radius: 6px;
  overflow-x: auto;
  font-size: 0.875rem;
  line-height: 1.5;
  margin: 1rem 0;
}

code {
  background: #f0f0f0;
  padding: 0.15em 0.4em;
  border-radius: 3px;
  font-size: 0.875em;
  font-family: "IBM Plex Mono", "SFMono-Regular", Consolas, monospace;
}

pre code {
  background: none;
  padding: 0;
  color: inherit;
}

img {
  max-width: 100%;
  height: auto;
  border: 1px solid #e5e7eb;
  border-radius: 4px;
  margin: 1rem 0;
  display: block;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin: 1.25rem 0;
  font-size: 0.9rem;
}

th {
  background: #0f62fe;
  color: #ffffff;
  text-align: left;
  padding: 0.6rem 0.9rem;
}

td {
  padding: 0.5rem 0.9rem;
  border: 1px solid #e5e7eb;
}

tr:nth-child(even) td { background: #f7f8fa; }

ul, ol { margin: 0.5rem 0; padding-left: 1.75rem; }
li { margin: 0.25rem 0; }

strong { font-weight: 600; }

a { color: #0f62fe; }
a:hover { text-decoration: underline; }
"""

with open(f'{OUTPUT_DIR}/assets/css/style.css', 'w') as f:
    f.write(css)

# Write .gitignore and Gemfile for Jekyll
with open(f'{OUTPUT_DIR}/.gitignore', 'w') as f:
    f.write("_site/\n.sass-cache/\n.jekyll-cache/\n.jekyll-metadata\nvendor/\n")

with open(f'{OUTPUT_DIR}/Gemfile', 'w') as f:
    f.write("""source "https://rubygems.org"
gem "github-pages", group: :jekyll_plugins
gem "jekyll-feed", "~> 0.12"
""")

print(f"\nDone! Output written to: {OUTPUT_DIR}/")
print(f"Pages created: {len(pages)}")
print(f"Images: {len(os.listdir(IMAGES_DIR))}")
