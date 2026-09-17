#!/usr/bin/env python3
"""
Converts the three RDR source documents into docs/rdr-lab-guide/:

  1. IBM Fusion - RDR Lab Prep Guide v2.10.0.0.docx  → prep pages
  2. IBM Fusion - RDR Lab Guide v2.11.0.0.docx        → lab pages
  3. ocpv-rdr-setup.docx                              → techzone-workaround.md
                                                         (hand-authored, no images)

Also:
  - Creates _includes/shared/reserve-two-rdr-environments.md
    (RDR-specific dual-cluster reservation with different network CIDRs)
  - Updates landing page with RDR guide card
"""

import os
import re
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

BASE      = Path("fusion-demo-guide")
DOCS_DIR  = BASE / "docs" / "rdr-lab-guide"
IMAGES_DIR = BASE / "assets" / "images" / "rdr-lab-guide"
INCLUDES  = BASE / "_includes" / "shared"
DOC_SLUG  = "rdr-lab-guide"
DOC_TITLE = "IBM Fusion RDR Lab Guide"

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
            block = '\n'.join(code_lines)
            if re.search(r'^(apiVersion|kind|metadata|spec|name|namespace)\s*:', block, re.MULTILINE):
                lang = 'yaml'
            elif re.search(r'^(ssh|oc |kubectl|curl|sudo|lsblk|ls |chmod|tar |cat |echo |export |mkdir|cd |bash )', block, re.MULTILINE):
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
        text  = elem['text'].strip()
        images = elem.get('images', [])
        for img in images:
            flush_code()
            lines.append(f'\n![Screenshot]({{{{ site.baseurl }}}}/assets/images/{slug}/{img})\n')
        if not text:
            continue
        mapped = STYLE_MAP.get(style, 'normal')
        if mapped == 'skip':
            continue
        if mapped == 'code_block':
            code_open = True
            code_lines.append(text)
            continue
        flush_code()
        md = para_to_md(style, text, [], slug)
        lines.extend(md)

    flush_code()
    return '\n'.join(lines)


def parse_docx(path):
    """Return (elements, rel_map, hyperlinks, img_count)."""
    with zipfile.ZipFile(path) as zf:
        doc_xml  = zf.read('word/document.xml')
        rels_xml = zf.read('word/_rels/document.xml.rels')
        IMAGES_DIR.mkdir(parents=True, exist_ok=True)
        img_count = 0
        for name in zf.namelist():
            if name.startswith('word/media/'):
                fname = os.path.basename(name)
                dest  = IMAGES_DIR / fname
                if not dest.exists():
                    with zf.open(name) as src, open(dest, 'wb') as dst:
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

    root = ET.fromstring(doc_xml)
    body = root.find('.//w:body', NS)
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

    return elements, rel_map, hyperlinks, img_count


def rename_images(elements):
    """Rename images by section heading, update elements in-place. Returns rename_map."""
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

    return rename_map


def split_to_pages(elements):
    """Split by H1 headings, skipping TOC."""
    pages        = []
    current_page = None
    skip_front   = True

    for elem in elements:
        if elem['type'] == 'para':
            style = elem['style']
            text  = elem['text'].strip()
            if style in ('toc1', 'toc2', 'toc3', 'toc4', 'lcd-toc', 'tocheading'):
                continue
            if style == 'heading1' and text:
                skip_front   = False
                current_page = {'title': text, 'slug': slugify(text), 'elements': []}
                pages.append(current_page)
            elif current_page is not None and not skip_front:
                current_page['elements'].append(elem)
        elif current_page is not None and not skip_front:
            current_page['elements'].append(elem)

    return pages


def inject_shared_includes(content, slug):
    """Replace boilerplate sections with shared includes."""
    if '## Getting help' in content:
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
    return content


def write_page(filename, title, raw_title, nav_order, parent, grand_parent, content):
    fm_lines = ["---", "layout: default", f'title: "{title}"',
                f"permalink: /{DOC_SLUG}/{'' if filename == 'index.md' else filename.replace('.md', '') + '/'}",
                f"nav_order: {nav_order}"]
    if parent:       fm_lines.append(f'parent: "{parent}"')
    if grand_parent: fm_lines.append(f'grand_parent: "{grand_parent}"')
    fm_lines.append("---\n")
    fm = '\n'.join(fm_lines)
    (DOCS_DIR / filename).write_text(fm + f"\n# {raw_title}\n\n" + content, encoding='utf-8')
    print(f"  Written: docs/rdr-lab-guide/{filename}")


# ── Create dirs ────────────────────────────────────────────────────────────────
DOCS_DIR.mkdir(parents=True, exist_ok=True)
INCLUDES.mkdir(parents=True, exist_ok=True)

# ── Step 1: Parse BOTH docx files, extract images into shared IMAGES_DIR ───────
print("Parsing RDR Lab Prep Guide...")
prep_elements, _, _, prep_img_count = parse_docx("IBM Fusion - RDR Lab Prep Guide v2.10.0.0.docx")

print("Parsing RDR Lab Guide...")
lab_elements, _, _, lab_img_count = parse_docx("IBM Fusion - RDR Lab Guide v2.11.0.0.docx")

# Rename ALL images together (from both docx) before splitting into pages,
# since they share the same IMAGES_DIR and we need unique section names.
all_elements = prep_elements + lab_elements
rename_map = rename_images(all_elements)
# Split back
prep_elements = all_elements[:len(prep_elements)]
lab_elements  = all_elements[len(prep_elements):]

print(f"Renamed {len(rename_map)} images total")

# ── Step 2: Write the RDR-specific shared include ──────────────────────────────
INCLUDES.joinpath("reserve-two-rdr-environments.md").write_text("""\
This lab requires two (2) IBM Fusion environments provisioned through IBM Technology Zone. Reserve both at the same time to minimize wait time.

> **Tip:** Reserve the environments far enough in advance. Each environment can take 30–60 minutes to provision.

> **Important:** To complete the lab successfully, set **OCS/ODF size** to **None** on both environments. This disables automatic ODF/FDF deployment so you can install and configure it manually.

## Reserve cluster local-cluster

The **local-cluster** hosts your primary workloads and Red Hat ACM.

1. Open a web browser and go to the [IBM Technology Zone – IBM Fusion Collection](https://techzone.ibm.com/collection/ibm-spectrum-fusion).
1. From the product overview page, click **Environments** in the left-hand menu.
1. Click the **Reserve** button on the **Beta: Storage Fusion on OCP w/ODF and Scale** tile.
1. Select **Reserve now** or **Schedule for later**.
1. Set **Name** to `local-cluster` and select the **Education** purpose tile.
1. Enter a **Purpose description** (e.g., *Using the environment for course work*).
1. Select **Preferred Geography:** `itzvmware-spectrum – AMERICAS – us-east-region – wdc04`.
1. Configure the following options:
   - **OpenShift Version** — 4.18 (required)
   - **Worker Node Count** — 3
   - **Worker Node Flavor** — 16 vCPU x 64 GB – 300 GB ephemeral storage
   - **OCS/ODF Size** — **None** (required)
   - Leave all three **network options** at their defaults.
1. Accept the Terms and Conditions and click **Submit**.

> **Note:** If you have any difficulties, visit the [IBM Technology Zone Help page](https://techzone.ibm.com/help) or email [techzone.help@ibm.com](mailto:techzone.help@ibm.com).

## Reserve cluster ocp2

The **ocp2** cluster is the disaster recovery site. It must use **different** network CIDRs from local-cluster to allow Submariner cross-cluster connectivity.

1. Open a web browser and go to the [IBM Technology Zone – IBM Fusion Collection](https://techzone.ibm.com/collection/ibm-spectrum-fusion).
1. From the product overview page, click **Environments** in the left-hand menu.
1. Click the **Reserve** button on the **Beta: Storage Fusion on OCP w/ODF and Scale** tile.
1. Select **Reserve now** or **Schedule for later**.
1. Set **Name** to `ocp2` and select the **Education** purpose tile.
1. Enter a **Purpose description**.
1. Select **Preferred Geography:** `itzvmware-spectrum – AMERICAS – us-east-region – wdc04`.
1. Configure the following options:
   - **OpenShift Version** — 4.18 (required)
   - **Worker Node Count** — 3
   - **Worker Node Flavor** — 16 vCPU x 64 GB – 300 GB ephemeral storage
   - **OCS/ODF Size** — **None** (required)
1. Modify the **network settings** as follows:

| Setting | Value |
| --- | --- |
| Machine Network | `192.168.242.0/24` |
| OCP/Kubernetes Cluster Network | `10.132.0.0/14` |
| OCP/Kubernetes Service Network | `172.31.0.0/16` |

1. Accept the Terms and Conditions and click **Submit**.

> **Important:** The distinct network CIDRs for ocp2 are required. Submariner uses these non-overlapping networks to establish cross-cluster connectivity for disaster recovery.

## Connect to the environments

Once both environments show **Ready** status, retrieve access details from your [IBM Technology Zone reservations page](https://techzone.ibm.com/my/reservations):

- **Desktop URL** — direct browser access to the OpenShift console
- **kubeadmin** username and password
- **Bastion SSH connection** and password for CLI access

> **Note:** Connectivity to the OpenShift console may be lost during the first 30 minutes after the "Reservation Ready" email. The MachineConfigPool is still updating and rebooting worker nodes during this time.
""")
print("Written: _includes/shared/reserve-two-rdr-environments.md")

# ── Step 3: Split Prep Guide pages ────────────────────────────────────────────
prep_pages = split_to_pages(prep_elements)
print(f"Prep Guide: {len(prep_pages)} H1 sections: {[p['title'] for p in prep_pages]}")

# ── Step 4: Split Lab Guide pages ─────────────────────────────────────────────
lab_pages = split_to_pages(lab_elements)
print(f"Lab Guide: {len(lab_pages)} H1 sections: {[p['title'] for p in lab_pages]}")

# ── Step 5: Write pages ────────────────────────────────────────────────────────
#
# Final page map (nav_order, title, filename):
#  1. index.md              — Introduction (from Lab Guide)
#  2. prerequisites.md      — Prerequisites & Getting Started (from Lab Guide, shared redhat-prereqs)
#  3. reserve-two-environments.md  — Reserve Two Environments (shared RDR include)
#  4. lab-prerequisites.md  — Lab prerequisites: install Fusion + FDF + OADP on both clusters (Lab Guide)
#  5. configure-rhacm.md    — Configure RHACM: ACM, Orchestrator, Import ocp2, Submariner, DR Policy (Lab Guide)
#  6. rdr-lab.md            — RDR Lab exercises: app, DR policy, failover, failback (Lab Guide)
#  7. addendum.md           — OCP project selector (shared include)
#
# The "Reserve Two Technology Zone Environments" page from the Lab Guide
# becomes just the shared include. The Prep Guide content feeds into:
#   - prerequisites.md (IBMid creation)
#   - reserve-two-environments.md (shared include covers it)
#   - The Lab infrastructure table and access steps go into prerequisites.md

# ── index.md from Lab Guide Introduction ──────────────────────────────────────
intro_page = next((p for p in lab_pages if p['slug'] == 'introduction'), None)
if intro_page:
    content = elements_to_markdown(intro_page['elements'], DOC_SLUG)
    content = inject_shared_includes(content, 'introduction')
    write_page("index.md", DOC_TITLE, "Introduction", 1, None, None, content)

# ── prerequisites.md — combines Prep Guide content + Lab Guide prerequisites ──
# Pull "Create an account" and "Connect to the lab" and "Lab infrastructure"
# and "Access the Environment" sections from Prep Guide,
# plus "Prerequisites & Getting Started" text from Lab Guide
prereq_elements = []
for p in prep_pages:
    if p['slug'] in ('create-an-account-to-request-your-environment',
                     'connect-to-the-lab-environment',
                     'lab-infrastructure',
                     'access-the-environment'):
        prereq_elements.extend(p['elements'])

lab_prereq_page = next((p for p in lab_pages if p['slug'] == 'prerequisites-getting-started'), None)
lab_prereq_elements = lab_prereq_page['elements'] if lab_prereq_page else []

# Combine: lab guide prereq text first (IBMid + linux prereqs), then prep guide access details
combined_prereq = elements_to_markdown(lab_prereq_elements + prereq_elements, DOC_SLUG)
# Replace inline redhat course block with shared include
combined_prereq = re.sub(
    r'(In addition, you must be familiar with the Linux.*?Note: Red Hat Partner Connect Training.*?\n)',
    '\n{% include shared/redhat-prerequisites.md %}\n\n',
    combined_prereq, flags=re.DOTALL
)
write_page("prerequisites-getting-started.md",
           "Prerequisites & Getting Started", "Prerequisites & Getting Started",
           2, DOC_TITLE, None, combined_prereq)

# ── reserve-two-environments.md — shared include only ─────────────────────────
reserve_content = "{% include shared/reserve-two-rdr-environments.md %}\n"
write_page("reserve-two-environments.md",
           "Reserve Two Environments", "Reserve Two Technology Zone Environments",
           3, DOC_TITLE, None, reserve_content)

# ── lab-prerequisites.md — RDR Lab prerequisites (install Fusion, FDF, OADP on both) ──
rdr_prereq_page = next((p for p in lab_pages if p['slug'] == 'regional-disaster-recovery-lab-prerequisites'), None)
if rdr_prereq_page:
    content = elements_to_markdown(rdr_prereq_page['elements'], DOC_SLUG)
    # Note about running on both clusters
    content = ("> **Note:** The steps in this section must be performed on **both** clusters "
               "(`local-cluster` and `ocp2`). To save time, you can run them in parallel.\n\n"
               + content)
    write_page("lab-prerequisites.md",
               "Lab Prerequisites", "Regional Disaster Recovery Lab prerequisites",
               4, DOC_TITLE, None, content)

# ── configure-rhacm.md — Configure RHACM, Import, Submariner, DR Policy ───────
rhacm_page = next((p for p in lab_pages if p['slug'] == 'configure-rhacm'), None)
if rhacm_page:
    content = elements_to_markdown(rhacm_page['elements'], DOC_SLUG)
    write_page("configure-rhacm.md",
               "Configure RHACM", "Configure RHACM",
               5, DOC_TITLE, None, content)

# ── rdr-lab.md — The actual DR lab exercises ──────────────────────────────────
rdr_lab_page = next((p for p in lab_pages if p['slug'] == 'regional-disaster-recovery-lab'), None)
if rdr_lab_page:
    content = elements_to_markdown(rdr_lab_page['elements'], DOC_SLUG)
    write_page("rdr-lab.md",
               "Regional Disaster Recovery Lab", "Regional Disaster Recovery Lab",
               6, DOC_TITLE, None, content)

# ── addendum.md — shared project selector ─────────────────────────────────────
addendum_content = "## OpenShift project selector\n\n{% include shared/openshift-project-selector.md %}\n"
write_page("addendum.md", "Addendum", "Addendum", 7, DOC_TITLE, None, addendum_content)

# ── Step 6: Update landing page ───────────────────────────────────────────────
landing_path = BASE / "index.md"
landing      = landing_path.read_text()

if 'rdr-lab-guide' not in landing:
    rdr_card = (
        '\n  <a href="/rdr-lab-guide/" class="doc-card">\n'
        '    <h2>IBM Fusion RDR Lab Guide</h2>\n'
        '    <p>Implement and test Regional Disaster Recovery with IBM Fusion — '
        'two OpenShift clusters, Fusion Data Foundation, RHACM, Submariner, '
        'and OpenShift DR failover/relocate exercises.</p>\n'
        '    <span class="doc-card-version">v2.11.0.0</span>\n'
        '  </a>'
    )
    # Replace the "Coming soon" Regional DR card if present, otherwise append
    coming_soon_pattern = r'  <a href="#" class="doc-card doc-card-coming-soon">\s*<h2>Fusion Regional Disaster Recovery Guide</h2>.*?</a>'
    if re.search(coming_soon_pattern, landing, re.DOTALL):
        landing = re.sub(coming_soon_pattern, rdr_card.strip(), landing, flags=re.DOTALL)
    else:
        landing = re.sub(r'(</div>\s*$)', rdr_card + r'\n\1', landing, flags=re.MULTILINE)
    landing_path.write_text(landing)
    print("Updated: index.md (RDR guide card added / Coming soon replaced)")
else:
    print("Landing page already has RDR card — skipping")

print(f"\nDone!")
print(f"  Images extracted: {prep_img_count + lab_img_count} ({len(rename_map)} renamed)")
print(f"  Pages written to docs/rdr-lab-guide/: {len(list(DOCS_DIR.glob('*.md')))}")
