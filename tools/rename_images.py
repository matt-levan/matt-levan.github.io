#!/usr/bin/env python3
"""
Rename extracted images from imageX.png to section-slug-NN.png
by tracing each image back to the heading it appears under in the document.
Also updates all {{ site.baseurl }}/assets/images/imageX references in the Markdown files.
"""

import os
import re
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

DOCX_PATH = "IBM Fusion Demo Guide v2.13.1.docx"
IMAGES_DIR = "fusion-demo-guide/assets/images"
PAGES_DIR  = "fusion-demo-guide"

NS = {
    'w':  'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'r':  'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
    'a':  'http://schemas.openxmlformats.org/drawingml/2006/main',
    'v':  'urn:schemas-microsoft-com:vml',
}

HEADING_STYLES = {
    'heading1', 'heading2', 'heading3', 'heading4', 'heading5',
}

def slugify(text):
    text = text.strip()
    # clean up common special chars
    text = re.sub(r'[–—]', '-', text)
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s/\\]+', '-', text)
    text = re.sub(r'-{2,}', '-', text)
    return text.lower().strip('-')[:60]

def get_style(para, ns):
    pPr = para.find('w:pPr', ns)
    if pPr is None:
        return 'normal'
    pStyle = pPr.find('w:pStyle', ns)
    if pStyle is None:
        return 'normal'
    val = pStyle.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val', '')
    return val.lower()

def get_text(para, ns):
    return ''.join(t.text or '' for t in para.findall('.//w:t', ns)).strip()

def get_images_in_para(para, ns, rel_map):
    """Return list of original filenames referenced by this paragraph."""
    imgs = []
    blip_ns = 'http://schemas.openxmlformats.org/drawingml/2006/main'
    for blip in para.findall(f'.//{{{blip_ns}}}blip'):
        rid = blip.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')
        if rid and rid in rel_map:
            imgs.append(rel_map[rid])
    for imgdata in para.findall('.//v:imagedata', ns):
        rid = imgdata.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')
        if rid and rid in rel_map:
            imgs.append(rel_map[rid])
    return imgs

# ── Load relationships ────────────────────────────────────────────────────────
with zipfile.ZipFile(DOCX_PATH) as zf:
    rels_xml = zf.read('word/_rels/document.xml.rels')
    doc_xml  = zf.read('word/document.xml')

rels_root = ET.fromstring(rels_xml)
rel_map = {}   # rId → basename (e.g. "image36.png")
for rel in rels_root:
    rid    = rel.get('Id')
    target = rel.get('Target', '')
    rtype  = rel.get('Type', '')
    if rid and 'image' in rtype.lower():
        rel_map[rid] = os.path.basename(target)

# ── Walk document body ────────────────────────────────────────────────────────
root = ET.fromstring(doc_xml)
body = root.find('.//w:body', NS)

# Build ordered list of (current_heading_slug, image_filename)
image_assignments = []   # [(heading_slug, original_filename), ...]
current_heading   = 'introduction'

for child in body:
    tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag

    if tag == 'p':
        style = get_style(child, NS)
        text  = get_text(child, NS)

        if style in HEADING_STYLES and text:
            current_heading = slugify(text)

        imgs = get_images_in_para(child, NS, rel_map)
        for img in imgs:
            image_assignments.append((current_heading, img))

    elif tag == 'tbl':
        # Images inside table cells
        for para in child.findall('.//w:p', NS):
            imgs = get_images_in_para(para, NS, rel_map)
            for img in imgs:
                image_assignments.append((current_heading, img))

print(f"Found {len(image_assignments)} image placements")

# ── Build rename map ──────────────────────────────────────────────────────────
# Counter per heading slug
heading_counters = {}
rename_map = {}   # original_filename → new_filename

for heading_slug, orig in image_assignments:
    if orig in rename_map:
        continue   # already assigned (image referenced more than once)

    heading_counters[heading_slug] = heading_counters.get(heading_slug, 0) + 1
    n = heading_counters[heading_slug]
    ext = os.path.splitext(orig)[1].lower()
    new_name = f"{heading_slug}-{n:02d}{ext}"
    rename_map[orig] = new_name

print(f"Unique images to rename: {len(rename_map)}")

# Preview first 20
for orig, new in list(rename_map.items())[:20]:
    print(f"  {orig:30s} → {new}")
print("  ...")

# ── Rename files on disk ──────────────────────────────────────────────────────
renamed = 0
skipped = 0
for orig, new in rename_map.items():
    src = os.path.join(IMAGES_DIR, orig)
    dst = os.path.join(IMAGES_DIR, new)
    if os.path.exists(src):
        os.rename(src, dst)
        renamed += 1
    else:
        print(f"  WARNING: file not found: {src}")
        skipped += 1

print(f"\nRenamed {renamed} files, skipped {skipped}")

# ── Update Markdown references ────────────────────────────────────────────────
md_files = list(Path(PAGES_DIR).glob('**/*.md'))
updated_files = 0

for md_path in md_files:
    content = md_path.read_text(encoding='utf-8')
    new_content = content
    for orig, new in rename_map.items():
        new_content = new_content.replace(f'/assets/images/{orig}', f'/assets/images/{new}')
    if new_content != content:
        md_path.write_text(new_content, encoding='utf-8')
        updated_files += 1

print(f"Updated {updated_files} Markdown files")
print("\nDone!")
