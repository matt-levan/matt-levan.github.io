#!/usr/bin/env python3
"""
1. Extracts shared includes:
      _includes/shared/reserve-techzone-environment.md  (from Demo Guide reserve-or-provision.md)
      _includes/shared/install-fusion-operator.md       (from Demo Guide ibm-fusion.md)
2. Converts IBM Fusion - HCP Lab Guide v2.11.0.0.docx
   to docs/hcp-lab-guide/ pages
3. Updates B&R Guide reservation page to use the shared include
4. Adds HCP guide card to the landing page
"""

import os
import re
import sys
import zipfile
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path

DOCX_PATH = "IBM Fusion - HCP Lab Guide v2.11.0.0.docx"
BASE       = Path("fusion-demo-guide")
DOCS_DIR   = BASE / "docs" / "hcp-lab-guide"
IMAGES_DIR = BASE / "assets" / "images" / "hcp-lab-guide"
INCLUDES   = BASE / "_includes" / "shared"
DOC_SLUG   = "hcp-lab-guide"
DOC_TITLE  = "IBM Fusion HCP Lab Guide"

NS = {
    'w':  'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'r':  'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
    'a':  'http://schemas.openxmlformats.org/drawingml/2006/main',
    'v':  'urn:schemas-microsoft-com:vml',
}

HEADING_STYLES = {'heading1', 'heading2', 'heading3', 'heading4', 'heading5'}

STYLE_MAP = {
    'heading1': '# ', 'heading2': '## ', 'heading3': '### ', 'heading4': '#### ',
    'lcd-narration': 'blockquote', 'lcd-narration1': 'blockquote',
    'lcd-narration2': 'blockquote', 'lcd-narration3': 'blockquote',
    'lcd-uielement-bold': 'bold', 'lcd-codeelement-mono': 'inline_code',
    'lcd-code': 'code_block', 'lcd-code1': 'code_block',
    'lcd-code2': 'code_block', 'lcd-code3': 'code_block',
    'codeblock': 'code_block', 'htmlcode': 'code_block',
    'lcd-bulletlistcompact1': 'bullet_1', 'lcd-bulletlistcompact2': 'bullet_2',
    'lcd-bulletlistcompact3': 'bullet_3', 'lcd-bulletlist1': 'bullet_1',
    'lcd-bulletlist2': 'bullet_2', 'lcd-bulletlist3': 'bullet_3',
    'lcd-listnumbering1': 'num_1', 'lcd-listnumbering2': 'num_2',
    'lcd-listnumbering3': 'num_3', 'listparagraph': 'bullet_1',
    'toc1': 'skip', 'toc2': 'skip', 'toc3': 'skip', 'toc4': 'skip',
    'lcd-toc': 'skip', 'lcd-disclaimer': 'skip', 'tocheading': 'skip',
    'lcd-doctitle': 'title', 'lcd-doctitle2': 'subtitle',
    'lcd-caption': 'caption', 'lcd-caption1': 'caption',
    'lcd-caption2': 'caption', 'lcd-caption3': 'caption',
    'lcd-graphic': 'skip', 'lcd-graphic1': 'skip',
    'lcd-graphic2': 'skip', 'lcd-graphic3': 'skip', 'lcd-spacer': 'skip',
}


# ── Helpers ────────────────────────────────────────────────────────────────────

def slugify(text):
    text = text.strip()
    text = re.sub(r'[–—/\\]', '-', text)
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s]+', '-', text)
    text = re.sub(r'-{2,}', '-', text)
    return text.lower().strip('-')[:60]


def get_style(para):
    pPr = para.find('w:pPr', NS)
    if pPr is None: return 'normal'
    pStyle = pPr.find('w:pStyle', NS)
    if pStyle is None: return 'normal'
    return pStyle.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val', '').lower()


def get_para_text_links(para, hyperlinks):
    parts = []

    def proc_run(run):
        text = ''.join(t.text or '' for t in run.findall('.//w:t', NS))
        if not text: return
        style_val = ''
        rpr = run.find('w:rPr', NS)
        if rpr is not None:
            rs = rpr.find('w:rStyle', NS)
            if rs is not None:
                style_val = rs.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val', '').lower()
        if 'uielement' in style_val or 'ui-element' in style_val:
            text = f'**{text}**'
        elif 'codeelem' in style_val or 'code-element' in style_val or 'mono' in style_val:
            text = f'`{text}`'
        parts.append(text)

    for child in para:
        tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
        if tag == 'r':
            proc_run(child)
        elif tag == 'hyperlink':
            rid = child.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id', '')
            url = hyperlinks.get(rid, '')
            link_text = ''.join(t.text or '' for t in child.findall('.//w:t', NS))
            if link_text and url and url != link_text:
                parts.append(f'[{link_text}]({url})')
            elif link_text:
                parts.append(link_text)
        elif tag == 'ins':
            for r in child.findall('w:r', NS):
                proc_run(r)
    return ''.join(parts)


def get_images(para, rel_map):
    imgs = []
    blip_ns = 'http://schemas.openxmlformats.org/drawingml/2006/main'
    for blip in para.findall(f'.//{{{blip_ns}}}blip'):
        rid = blip.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed', '')
        if rid in rel_map: imgs.append(rel_map[rid])
    for imgdata in para.findall('.//v:imagedata', NS):
        rid = imgdata.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id', '')
        if rid in rel_map: imgs.append(rel_map[rid])
    return imgs


def table_to_md(table, hyperlinks):
    rows = table.findall('.//w:tr', NS)
    if not rows: return []
    all_cells = []
    for row in rows:
        cells = []
        for tc in row.findall('w:tc', NS):
            txt = ''
            for p in tc.findall('w:p', NS):
                txt += get_para_text_links(p, hyperlinks)
            cells.append(txt.strip().replace('|', '\\|'))
        all_cells.append(cells)
    if not all_cells: return []
    lines = []
    header = all_cells[0]
    lines.append('| ' + ' | '.join(header) + ' |')
    lines.append('| ' + ' | '.join(['---'] * len(header)) + ' |')
    for row in all_cells[1:]:
        while len(row) < len(header): row.append('')
        lines.append('| ' + ' | '.join(row[:len(header)]) + ' |')
    return lines


def para_to_md(style, text, images, slug):
    lines = []
    for img in images:
        lines.append(f'\n![Screenshot]({{{{ site.baseurl }}}}/assets/images/{slug}/{img})\n')
    if not text.strip() and not images:
        return []
    mapped = STYLE_MAP.get(style, 'normal')
    if mapped == 'skip': return lines
    elif mapped == 'title': lines.append(f'# {text}')
    elif mapped == 'subtitle': lines.append(f'*{text}*')
    elif mapped == 'caption': lines.append(f'*{text}*')
    elif mapped == 'blockquote': lines.append(f'> {text}')
    elif mapped == 'bold': lines.append(f'**{text}**')
    elif mapped == 'inline_code': lines.append(f'`{text}`')
    elif mapped == 'code_block': lines.append(f'```\n{text}\n```')
    elif mapped in ('# ', '## ', '### ', '#### ', '##### '): lines.append(f'{mapped}{text}')
    elif mapped.startswith('bullet_'):
        indent = '  ' * (int(mapped[-1]) - 1)
        lines.append(f'{indent}- {text}')
    elif mapped.startswith('num_'):
        indent = '  ' * (int(mapped[-1]) - 1)
        lines.append(f'{indent}1. {text}')
    else:
        if text.strip(): lines.append(text)
    return lines


def elements_to_markdown(elements, slug):
    lines = []
    code_open = False
    code_lines = []

    def flush_code():
        nonlocal code_open, code_lines
        if code_open:
            # detect language
            block = '\n'.join(code_lines)
            if re.search(r'^(apiVersion|kind|metadata|spec|name|namespace)\s*:', block, re.MULTILINE):
                lang = 'yaml'
            elif re.search(r'^(ssh|oc |kubectl|curl|sudo|lsblk|ls |chmod|tar |cat |echo |export |mkdir|cd )', block, re.MULTILINE):
                lang = 'bash'
            else:
                lang = 'bash'
            lines.append(f'```{lang}')
            lines.extend(code_lines)
            lines.append('```')
            code_open = False
            code_lines = []
            lines.append('')

    for elem in elements:
        if elem['type'] == 'table':
            flush_code()
            lines.append('')
            lines.extend(elem['lines'])
            lines.append('')
            continue
        style = elem['style']
        text = elem['text'].strip()
        images = elem.get('images', [])
        for img in images:
            flush_code()
            lines.append(f'\n![Screenshot]({{{{ site.baseurl }}}}/assets/images/{slug}/{img})\n')
        if not text:
            if code_open:
                pass  # blank lines inside code block are OK — don't flush
            continue
        mapped = STYLE_MAP.get(style, 'normal')
        if mapped == 'skip':
            continue
        if mapped == 'code_block':
            code_open = True
            code_lines.append(text)
            continue
        # Any non-code content flushes an open block
        flush_code()
        md = para_to_md(style, text, [], slug)
        lines.extend(md)

    flush_code()
    return '\n'.join(lines)


# ── Step 1: Write shared includes ─────────────────────────────────────────────
INCLUDES.mkdir(parents=True, exist_ok=True)

# reserve-techzone-environment.md — extracted from Demo Guide reserve-or-provision.md
# (strip the front matter / H1 heading; include only the body starting at ## Reserve an environment)
fdg_reserve_src = BASE / "docs" / "fusion-demo-guide" / "reserve-or-provision.md"
if fdg_reserve_src.exists():
    body = fdg_reserve_src.read_text()
    # Remove YAML front matter
    body = re.sub(r'^---.*?---\s*', '', body, flags=re.DOTALL)
    # Remove the top-level H1 heading line
    body = re.sub(r'^# .+\n', '', body, count=1)
    body = body.strip() + '\n'
    INCLUDES.joinpath("reserve-techzone-environment.md").write_text(body)
    print("Written: _includes/shared/reserve-techzone-environment.md")
else:
    print("WARNING: reserve-or-provision.md not found — shared include not written")

# install-fusion-operator.md — Install + Connect sections from Demo Guide ibm-fusion.md
# Keep only through "## Connect to Fusion" and the steps under it (before "### Managing IBM Fusion")
fdg_fusion_src = BASE / "docs" / "fusion-demo-guide" / "ibm-fusion.md"
if fdg_fusion_src.exists():
    body = fdg_fusion_src.read_text()
    body = re.sub(r'^---.*?---\s*', '', body, flags=re.DOTALL)
    body = re.sub(r'^# .+\n', '', body, count=1)
    # Trim everything from "### Managing IBM Fusion" onward
    body = re.sub(r'\n### Managing IBM Fusion.*', '', body, flags=re.DOTALL)
    body = body.strip() + '\n'
    INCLUDES.joinpath("install-fusion-operator.md").write_text(body)
    print("Written: _includes/shared/install-fusion-operator.md")
else:
    print("WARNING: ibm-fusion.md not found — shared include not written")


# ── Step 2: Parse docx ────────────────────────────────────────────────────────
print(f"\nParsing {DOCX_PATH}...")
with zipfile.ZipFile(DOCX_PATH) as zf:
    doc_xml  = zf.read('word/document.xml')
    rels_xml = zf.read('word/_rels/document.xml.rels')
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    img_count = 0
    for name in zf.namelist():
        if name.startswith('word/media/'):
            fname = os.path.basename(name)
            with zf.open(name) as src, open(IMAGES_DIR / fname, 'wb') as dst:
                dst.write(src.read())
            img_count += 1

rels_root  = ET.fromstring(rels_xml)
rel_map    = {}
hyperlinks = {}
for rel in rels_root:
    rid    = rel.get('Id', '')
    target = rel.get('Target', '')
    rtype  = rel.get('Type', '')
    if rid:
        if 'image' in rtype.lower():
            rel_map[rid] = os.path.basename(target)
        else:
            hyperlinks[rid] = target

print(f"Extracted {img_count} images, {len(rel_map)} image rels, {len(hyperlinks)} hyperlinks")

root = ET.fromstring(doc_xml)
body = root.find('.//w:body', NS)

# ── Build element list ─────────────────────────────────────────────────────────
elements = []
for child in body:
    tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
    if tag == 'p':
        style = get_style(child)
        text  = get_para_text_links(child, hyperlinks)
        imgs  = get_images(child, rel_map)
        elements.append({'type': 'para', 'style': style, 'text': text, 'images': imgs})
    elif tag == 'tbl':
        elements.append({'type': 'table', 'lines': table_to_md(child, hyperlinks)})

# ── Rename images by section ───────────────────────────────────────────────────
heading_counters = {}
rename_map       = {}
current_heading  = 'introduction'

for elem in elements:
    if elem['type'] != 'para': continue
    style = elem['style']
    text  = elem['text'].strip()
    if style in HEADING_STYLES and text:
        current_heading = slugify(text)
    for orig in elem.get('images', []):
        if orig in rename_map: continue
        heading_counters[current_heading] = heading_counters.get(current_heading, 0) + 1
        n   = heading_counters[current_heading]
        ext = os.path.splitext(orig)[1].lower()
        rename_map[orig] = f"{current_heading}-{n:02d}{ext}"

for orig, new in rename_map.items():
    src = IMAGES_DIR / orig
    dst = IMAGES_DIR / new
    if src.exists(): src.rename(dst)

for elem in elements:
    if elem['type'] == 'para':
        elem['images'] = [rename_map.get(img, img) for img in elem.get('images', [])]

print(f"Renamed {len(rename_map)} images")

# ── Split into H1 sections (pages) ────────────────────────────────────────────
pages = []
current_page = None
skip_front   = True   # skip everything before first heading1

for elem in elements:
    if elem['type'] == 'para':
        style = elem['style']
        text  = elem['text'].strip()
        # Skip TOC entries
        if style in ('toc1', 'toc2', 'toc3', 'toc4', 'lcd-toc', 'tocheading'): continue
        if style == 'heading1' and text:
            skip_front   = False
            current_page = {'title': text, 'slug': slugify(text), 'elements': []}
            pages.append(current_page)
        elif current_page is not None and not skip_front:
            current_page['elements'].append(elem)
    elif current_page is not None and not skip_front:
        current_page['elements'].append(elem)

print(f"Identified {len(pages)} H1 sections: {[p['title'] for p in pages]}")

# ── Create output dir ──────────────────────────────────────────────────────────
DOCS_DIR.mkdir(parents=True, exist_ok=True)

# ── Page metadata ──────────────────────────────────────────────────────────────
# slug → (display title, nav_order, parent, grand_parent)
PAGE_META = {
    'introduction':                      (DOC_TITLE,                                          1,  None,      None),
    'prerequisites-getting-started':     ("Prerequisites & Getting Started",                  2,  DOC_TITLE, None),
    'reserve-a-technology-zone-environment': ("Reserve TechZone Environment",                 3,  DOC_TITLE, None),
    'hosted-control-plane-lab-prerequisites': ("Lab Prerequisites",                           4,  DOC_TITLE, None),
    'lvm-storage':                       ("LVM Storage",                                      5,  DOC_TITLE, None),
    'fusion-data-foundation-provider-mode-install': ("FDF Provider Mode Install",             6,  DOC_TITLE, None),
    'hosted-control-plane-prerequisites': ("HCP Prerequisites",                               7,  DOC_TITLE, None),
    'create-hosted-cluster':             ("Create Hosted Cluster",                            8,  DOC_TITLE, None),
    'addendum':                          ("Addendum",                                         9,  DOC_TITLE, None),
}

# ── Write pages ────────────────────────────────────────────────────────────────
for i, page in enumerate(pages):
    slug      = page['slug']
    raw_title = page['title']
    meta      = PAGE_META.get(slug)
    if meta:
        title, nav_order, parent, grand_parent = meta
    else:
        title        = raw_title
        nav_order    = i + 1
        parent       = DOC_TITLE
        grand_parent = None

    content = elements_to_markdown(page['elements'], DOC_SLUG)

    # ── Inject shared includes ────────────────────────────────────────────────
    # Getting help section → shared include
    if '## Getting help' in content:
        content = re.sub(
            r'(## Getting help\n)(.*?)(\n## |\Z)',
            r'\1\n{% include shared/getting-help.md %}\n\3',
            content, flags=re.DOTALL
        )

    # Product disclaimer section → shared include
    if '## Product disclaimer' in content:
        content = re.sub(
            r'(## Product disclaimer\n)(.*?)(\n## |\Z)',
            r'\1\n{% include shared/product-disclaimer.md %}\n\3',
            content, flags=re.DOTALL
        )

    # Reserve TechZone section → shared include + HCP-specific callout
    if slug == 'reserve-a-technology-zone-environment':
        hcp_callout = (
            "\n> **Important (HCP-specific):** When reserving the HCP environment, "
            "set **OCS/ODF size** to **None** to disable automatic ODF deployment — "
            "you will install and configure FDF manually as described in this guide. "
            "Also ensure the environment includes **infra nodes** "
            "(3 nodes with 2 TB internal storage for LVM etcd storage).\n"
        )
        content = (
            "{% include shared/reserve-techzone-environment.md %}\n"
            + hcp_callout
        )

    # Install Fusion Operator section → shared include
    if slug == 'hosted-control-plane-lab-prerequisites':
        # Replace the "Install the IBM Fusion Operator" and "Connect to Fusion"
        # subsections with the shared include
        content = re.sub(
            r'(## Install the IBM Fusion Operator\n)(.*?)(## LVM Storage|\Z)',
            r'## Install the IBM Fusion Operator\n\n{% include shared/install-fusion-operator.md %}\n\n\3',
            content, flags=re.DOTALL
        )

    if slug == 'introduction':
        filename  = "index.md"
        permalink = f"/{DOC_SLUG}/"
    else:
        filename  = f"{slug}.md"
        permalink = f"/{DOC_SLUG}/{slug}/"

    fm_lines = ["---", "layout: default", f'title: "{title}"',
                f"permalink: {permalink}", f"nav_order: {nav_order}"]
    if parent:      fm_lines.append(f'parent: "{parent}"')
    if grand_parent: fm_lines.append(f'grand_parent: "{grand_parent}"')
    fm_lines.append("---\n")
    fm = '\n'.join(fm_lines)

    (DOCS_DIR / filename).write_text(fm + f"\n# {raw_title}\n\n" + content, encoding='utf-8')
    print(f"  Written: docs/hcp-lab-guide/{filename}")

# ── Step 3: Update B&R Guide reservation page to use shared include ────────────
br_reserve = BASE / "docs" / "backup-restore-guide" / "reserve-technology-zone-environment.md"
if br_reserve.exists():
    br_content = br_reserve.read_text()
    if '{% include shared/reserve-techzone-environment.md %}' not in br_content:
        # Replace the old body (after front matter + H1) with the shared include
        br_content = re.sub(
            r'(# Reserve Technology Zone environment\n\n)(.*)',
            r'\1{% include shared/reserve-techzone-environment.md %}\n\n'
            r'> **Important:** Two (2) IBM Fusion environments will be used during this lab. '
            r'It is helpful to reserve both environments at the same time.\n\n'
            r'> **Note:** If using the same environment from the Installation and Configuration '
            r'hands-on lab, it may be useful to change the default storageClass from '
            r'`managed-nfs-storage` to `ibm-storagecluster-ceph-rbd`.\n',
            br_content, flags=re.DOTALL
        )
        br_reserve.write_text(br_content)
        print("Updated: docs/backup-restore-guide/reserve-technology-zone-environment.md")

# ── Step 4: Add HCP guide card to landing page ────────────────────────────────
landing_path = BASE / "index.md"
landing      = landing_path.read_text()

# Check if HCP card already exists
if 'hcp-lab-guide' not in landing:
    # Append HCP card before the closing </div> of the card grid
    # The coming-soon OCP Virt card was activated already; add after it
    hcp_card = (
        '\n  <a href="/hcp-lab-guide/" class="doc-card">\n'
        '    <h2>IBM Fusion HCP Lab Guide</h2>\n'
        '    <p>Deploy IBM Fusion with OpenShift Hosted Control Planes — '
        'LVM storage, Fusion Data Foundation in Provider mode, MetalLB, '
        'multicluster engine, and hosted cluster creation.</p>\n'
        '    <span class="doc-card-version">v2.11.0.0</span>\n'
        '  </a>'
    )
    # Insert before the closing </div> of the card grid
    landing = re.sub(
        r'(</div>\s*$)',
        hcp_card + r'\n\1',
        landing, flags=re.MULTILINE
    )
    landing_path.write_text(landing)
    print("Updated: index.md (HCP guide card added)")
else:
    print("Landing page already has HCP card — skipping")

print(f"\nDone! {len(pages)} pages written to docs/hcp-lab-guide/")
print(f"Images in assets/images/hcp-lab-guide/: {len(os.listdir(IMAGES_DIR))}")
print("Shared includes updated in _includes/shared/")
