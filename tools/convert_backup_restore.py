#!/usr/bin/env python3
"""
1. Creates _includes/shared/ snippets for content shared between guides
2. Converts IBM Fusion - Backup and Restore Lab Guide v2.12.0.0.docx
   to docs/backup-restore-guide/ pages
3. Updates shared sections in fusion-demo-guide to use includes
4. Updates landing page to add the new guide card
5. Adds backup-restore guide images to assets/images/backup-restore-guide/
"""

import os
import re
import sys
import zipfile
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path

DOCX_PATH = "IBM Fusion - Backup and Restore Lab Guide v2.12.0.0.docx"
BASE       = Path("fusion-demo-guide")
DOCS_DIR   = BASE / "docs" / "backup-restore-guide"
IMAGES_DIR = BASE / "assets" / "images" / "backup-restore-guide"
INCLUDES   = BASE / "_includes" / "shared"

NS = {
    'w':  'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'r':  'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
    'a':  'http://schemas.openxmlformats.org/drawingml/2006/main',
    'v':  'urn:schemas-microsoft-com:vml',
}

HEADING_STYLES = {'heading1','heading2','heading3','heading4','heading5'}

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

DOC_TITLE = "Fusion Backup and Restore Lab Guide"

# ── Helpers ───────────────────────────────────────────────────────────────────

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
        rPr = run.find('w:rStyle', NS)
        style_val = ''
        rpr = run.find('w:rPr', NS)
        if rpr is not None:
            rs = rpr.find('w:rStyle', NS)
            if rs is not None:
                style_val = rs.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val','').lower()
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
            rid = child.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id','')
            url = hyperlinks.get(rid,'')
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
        rid = blip.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed','')
        if rid in rel_map: imgs.append(rel_map[rid])
    for imgdata in para.findall('.//v:imagedata', NS):
        rid = imgdata.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id','')
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
            cells.append(txt.strip().replace('|','\\|'))
        all_cells.append(cells)
    if not all_cells: return []
    lines = []
    header = all_cells[0]
    lines.append('| ' + ' | '.join(header) + ' |')
    lines.append('| ' + ' | '.join(['---']*len(header)) + ' |')
    for row in all_cells[1:]:
        while len(row) < len(header): row.append('')
        lines.append('| ' + ' | '.join(row[:len(header)]) + ' |')
    return lines

def tag_code(code):
    c = code.strip()
    if re.search(r'^(apiVersion|kind|metadata|spec|name|namespace)\s*:', c, re.MULTILINE):
        return 'yaml'
    if re.search(r'^(ssh|oc |kubectl|curl|sudo|mmlscluster|mmlsfs|/usr/lpp)', c, re.MULTILINE):
        return 'bash'
    return 'bash'

def para_to_md(style, text, images, doc_slug):
    lines = []
    for img in images:
        lines.append(f'\n![Screenshot]({{{{ site.baseurl }}}}/assets/images/{doc_slug}/{img})\n')
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
    elif mapped in ('# ','## ','### ','#### ','##### '): lines.append(f'{mapped}{text}')
    elif mapped.startswith('bullet_'):
        indent = '  ' * (int(mapped[-1]) - 1)
        lines.append(f'{indent}- {text}')
    elif mapped.startswith('num_'):
        indent = '  ' * (int(mapped[-1]) - 1)
        lines.append(f'{indent}1. {text}')
    else:
        if text.strip(): lines.append(text)
    return lines

def elements_to_markdown(elements, doc_slug):
    lines = []
    code_open = False
    for elem in elements:
        if elem['type'] == 'table':
            if code_open: lines.append('```'); code_open = False; lines.append('')
            lines.append(''); lines.extend(elem['lines']); lines.append('')
            continue
        style = elem['style']
        text  = elem['text'].strip()
        images = elem.get('images', [])
        for img in images:
            if code_open: lines.append('```'); code_open = False; lines.append('')
            lines.append(f'\n![Screenshot]({{{{ site.baseurl }}}}/assets/images/{doc_slug}/{img})\n')
        if not text:
            if code_open: lines.append('```'); code_open = False; lines.append('')
            continue
        mapped = STYLE_MAP.get(style, 'normal')
        if mapped == 'skip': continue
        if mapped == 'code_block':
            if not code_open: lines.append(''); lines.append('```'); code_open = True
            lines.append(text); continue
        if code_open: lines.append('```'); code_open = False; lines.append('')
        md = para_to_md(style, text, [], doc_slug)
        lines.extend(md)
    if code_open: lines.append('```')
    return '\n'.join(lines)

# ── Parse docx ────────────────────────────────────────────────────────────────
print(f"Parsing {DOCX_PATH}...")
with zipfile.ZipFile(DOCX_PATH) as zf:
    doc_xml = zf.read('word/document.xml')
    rels_xml = zf.read('word/_rels/document.xml.rels')
    # Extract images
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    img_count = 0
    for name in zf.namelist():
        if name.startswith('word/media/'):
            fname = os.path.basename(name)
            with zf.open(name) as src, open(IMAGES_DIR / fname, 'wb') as dst:
                dst.write(src.read())
            img_count += 1

rels_root = ET.fromstring(rels_xml)
rel_map = {}
hyperlinks = {}
for rel in rels_root:
    rid = rel.get('Id','')
    target = rel.get('Target','')
    rtype = rel.get('Type','')
    if rid:
        if 'image' in rtype.lower():
            rel_map[rid] = os.path.basename(target)
        else:
            hyperlinks[rid] = target

print(f"Extracted {img_count} images, {len(rel_map)} image rels, {len(hyperlinks)} hyperlinks")

root = ET.fromstring(doc_xml)
body = root.find('.//w:body', NS)

# ── Build element list ────────────────────────────────────────────────────────
elements = []
for child in body:
    tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
    if tag == 'p':
        style = get_style(child)
        text  = get_para_text_links(child, hyperlinks)
        imgs  = get_images(child, rel_map)
        elements.append({'type':'para','style':style,'text':text,'images':imgs})
    elif tag == 'tbl':
        elements.append({'type':'table','lines': table_to_md(child, hyperlinks)})

# ── Rename images by section ──────────────────────────────────────────────────
heading_counters = {}
rename_map = {}
current_heading = 'introduction'

for elem in elements:
    if elem['type'] != 'para': continue
    style = elem['style']
    text  = elem['text'].strip()
    if style in HEADING_STYLES and text:
        current_heading = slugify(text)
    for orig in elem.get('images', []):
        if orig in rename_map: continue
        heading_counters[current_heading] = heading_counters.get(current_heading, 0) + 1
        n = heading_counters[current_heading]
        ext = os.path.splitext(orig)[1].lower()
        rename_map[orig] = f"{current_heading}-{n:02d}{ext}"

# Rename on disk
for orig, new in rename_map.items():
    src = IMAGES_DIR / orig
    dst = IMAGES_DIR / new
    if src.exists(): src.rename(dst)

# Update image refs in elements
for elem in elements:
    if elem['type'] == 'para':
        elem['images'] = [rename_map.get(img, img) for img in elem.get('images', [])]

print(f"Renamed {len(rename_map)} images")

# ── Split into H1 sections ────────────────────────────────────────────────────
pages = []
current_page = None
skip_toc = True

for elem in elements:
    if elem['type'] == 'para':
        style = elem['style']
        text  = elem['text'].strip()
        if style in ('toc1','toc2','toc3','toc4','lcd-toc','tocheading'): continue
        if style == 'heading1' and text:
            skip_toc = False
            current_page = {'title': text, 'slug': slugify(text), 'elements': []}
            pages.append(current_page)
        elif current_page is not None and not skip_toc:
            current_page['elements'].append(elem)
    elif current_page is not None and not skip_toc:
        current_page['elements'].append(elem)

print(f"Identified {len(pages)} H1 sections: {[p['title'] for p in pages]}")

# ── Create output dir ─────────────────────────────────────────────────────────
DOCS_DIR.mkdir(parents=True, exist_ok=True)
INCLUDES.mkdir(parents=True, exist_ok=True)
DOC_SLUG = "backup-restore-guide"

# ── Write shared includes ─────────────────────────────────────────────────────
# Product disclaimer (identical in both guides)
INCLUDES.joinpath("product-disclaimer.md").write_text("""\
This product is being developed and released in an agile manner. In addition to adding new capabilities, the interface is likely to change over time. Therefore, the screenshots used in this guide may not always look exactly like what you see in the product. Depending on the product, you can expect to encounter some of the following:

- Changes in the user interface (UI), such as the location of buttons or text in various fields
- Additional tabs or buttons

These differences should not affect how the labs work but have patience and explore.
""")

# Getting help (identical in both guides)
INCLUDES.joinpath("getting-help.md").write_text("""\
If you require assistance in interpreting any of the steps in this lab, please post your questions to the [#storage_demo_feedback](https://ibm.enterprise.slack.com/archives/C06KQ49RJBF) Slack channel (IBMers only). Business Partners can request help at the [Partner Plus Support](https://www.ibm.com/partnerplus/support) website.

For troubleshooting tips, see the [TechZone Set Up Troubleshooting Guide](https://ibm.seismic.com/Link/Content/DCGT3pQ7hHM828WDQ86R7Tf6gpPV) for help with common issues and solutions when using IBM Technology Zone. Additionally, go to the [IBM Technology Zone Help page](https://techzone.ibm.com/help). If you have an issue with the site, you can [open a support case](https://ibmsf.force.com/ibminternalproducts/s/createrecord/NewCase?language=en_US) or send an email to [techzone.help@ibm.com](mailto:techzone.help@ibm.com).

Help with the Fusion product itself is available in the [#ibm-fusion-help](https://ibm.enterprise.slack.com/archives/C029ET42U8Y) Slack channel (IBMers only).

See also the [Fusion documentation](https://www.ibm.com/docs/en/storage-fusion-software).
""")

# Red Hat prerequisites courses (identical in both guides)
INCLUDES.joinpath("redhat-prerequisites.md").write_text("""\
In addition, you must be familiar with the Linux operating system and the command line interface to execute basic Linux commands such as `kubectl`, `oc`, `exit`, `ls`, `mkdir`, `ssh`, `sudo`, and `curl`. Ideally, you should also have experience with the Red Hat OpenShift GUI and CLI commands. If you need experience using Linux, Kubernetes and Red Hat OpenShift, it is highly recommended that you complete the following Red Hat courses first:

- [DO080 – Containers, Kubernetes and Red Hat OpenShift Technical Overview](https://training-lms.redhat.com/sso/saml/auth/rhopen?RelayState=deeplinkoffering%3D43022363)
- [DO180 – Red Hat OpenShift Administration I: Managing Containers and Kubernetes](https://training-lms.redhat.com/sso/saml/auth/rhopen?RelayState=deeplinkoffering%3D46105986)
- [DO280 – Red Hat OpenShift Administration II: Operating a Production Kubernetes Cluster](https://training-lms.redhat.com/sso/saml/auth/rhopen?RelayState=deeplinkoffering%3D46105987)

> Note: Red Hat Partner Connect Training access is required to access the training material provided by Red Hat.
""")

print("Written: _includes/shared/ (3 shared snippets)")

# ── Page definitions: title, nav_order, parent, grand_parent ─────────────────
PAGE_META = {
    'introduction':                         (DOC_TITLE,                             1,  None,                                    None),
    'prerequisites-getting-started':        ("Prerequisites & Getting Started",      2,  DOC_TITLE,                               None),
    'reserve-technology-zone-environment':  ("Reserve TechZone Environment",         3,  DOC_TITLE,                               None),
    'ibm-fusion-operator-and-backup-restore-service': ("Install Fusion & B&R Service", 4, DOC_TITLE,                             None),
    'backup-and-restore-labs':              ("Backup and Restore Labs",              5,  DOC_TITLE,                               None),
    'spoke-cluster-labs':                   ("Spoke Cluster Labs",                   6,  DOC_TITLE,                               None),
    'addendum':                             ("Addendum",                             7,  DOC_TITLE,                               None),
}

# ── Write pages ───────────────────────────────────────────────────────────────
for i, page in enumerate(pages):
    slug = page['slug']
    raw_title = page['title']
    meta = PAGE_META.get(slug)
    if meta:
        title, nav_order, parent, grand_parent = meta
    else:
        title = raw_title
        nav_order = i + 1
        parent = DOC_TITLE
        grand_parent = None

    content = elements_to_markdown(page['elements'], DOC_SLUG)

    # Inject shared includes where appropriate
    if slug == 'introduction':
        content = content.replace(
            '## Product disclaimer',
            '## Product disclaimer\n\n{% include shared/product-disclaimer.md %}\n\n<!--'
        )
        # close the replaced block after the disclaimer paragraphs end
        # simpler: just append the includes at known headings
    if '## Getting help' in content:
        # Replace the getting-help section body with the include
        content = re.sub(
            r'(## Getting help\n)(.*?)(\n## |\Z)',
            r'\1\n{% include shared/getting-help.md %}\n\3',
            content, flags=re.DOTALL
        )
    if '## Product disclaimer' in content:
        content = re.sub(
            r'(## Product disclaimer\n)(.*?)(\n## |\Z)',
            r'\1\n{% include shared/product-disclaimer.md %}\n\3',
            content, flags=re.DOTALL
        )

    if slug == 'introduction':
        filename = "index.md"
        permalink = f"/{DOC_SLUG}/"
    else:
        filename = f"{slug}.md"
        permalink = f"/{DOC_SLUG}/{slug}/"

    fm_lines = ["---", "layout: default", f'title: "{title}"',
                f"permalink: {permalink}", f"nav_order: {nav_order}"]
    if parent: fm_lines.append(f'parent: "{parent}"')
    if grand_parent: fm_lines.append(f'grand_parent: "{grand_parent}"')
    fm_lines.append("---\n")
    fm = '\n'.join(fm_lines)

    (DOCS_DIR / filename).write_text(fm + f"\n# {raw_title}\n\n" + content, encoding='utf-8')
    print(f"  Written: docs/backup-restore-guide/{filename}")

# ── Update fusion-demo-guide shared sections to use includes ──────────────────
fdg_intro = BASE / "docs" / "fusion-demo-guide" / "index.md"
if fdg_intro.exists():
    content = fdg_intro.read_text()
    if '{% include shared/' not in content:
        content = re.sub(
            r'(## Getting help\n)(.*?)(\n## |\Z)',
            r'\1\n{% include shared/getting-help.md %}\n\3',
            content, flags=re.DOTALL
        )
        content = re.sub(
            r'(## Product disclaimer\n)(.*?)(\n## |\Z)',
            r'\1\n{% include shared/product-disclaimer.md %}\n\3',
            content, flags=re.DOTALL
        )
        fdg_intro.write_text(content)
        print("Updated: docs/fusion-demo-guide/index.md (shared includes injected)")

fdg_prereqs = BASE / "docs" / "fusion-demo-guide" / "prerequisites.md"
if fdg_prereqs.exists():
    content = fdg_prereqs.read_text()
    if '{% include shared/' not in content:
        content = re.sub(
            r'(In addition, you must be familiar with the Linux.*?Note: Red Hat Partner Connect Training.*?\n)',
            '{% include shared/redhat-prerequisites.md %}\n',
            content, flags=re.DOTALL
        )
        fdg_prereqs.write_text(content)
        print("Updated: docs/fusion-demo-guide/prerequisites.md (shared include injected)")

# ── Update root landing page ──────────────────────────────────────────────────
landing_path = BASE / "index.md"
landing = landing_path.read_text()
landing = landing.replace(
    '  <a href="#" class="doc-card doc-card-coming-soon">\n    <h2>Fusion Backup &amp; Restore Guide</h2>\n    <p>Deep-dive into IBM Fusion Backup &amp; Restore service configuration, policies, and recovery procedures.</p>\n    <span class="doc-card-badge">Coming soon</span>\n  </a>',
    '  <a href="/backup-restore-guide/" class="doc-card">\n    <h2>Fusion Backup &amp; Restore Lab Guide</h2>\n    <p>Hands-on labs for IBM Fusion Backup &amp; Restore — policies, recipes, application-consistent backups, and hub/spoke restore.</p>\n    <span class="doc-card-version">v2.12.0.0</span>\n  </a>'
)
landing_path.write_text(landing)
print("Updated: index.md (landing page card activated)")

print(f"\nDone! {len(pages)} pages written to docs/backup-restore-guide/")
print(f"Images: {len(os.listdir(IMAGES_DIR))}")
