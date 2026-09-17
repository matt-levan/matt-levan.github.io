#!/usr/bin/env python3
"""
Convert jeanchlopez/txc26-ocpv-fusion-lab .adoc pages to Jekyll/Just the Docs Markdown.
Handles: headings, images, code blocks, callouts (NOTE/TIP/IMPORTANT/WARNING),
         ordered/unordered lists, bold/italic, xrefs, attribute substitution,
         source blocks with role=execute (copy button via bash tag),
         table blocks, and Antora-specific macros.
"""

import re
from pathlib import Path

ADOC_DIR  = Path("/tmp/ocpv-adoc/pages")
OUT_DIR   = Path("fusion-demo-guide/docs/ocpv-fusion-lab")
DOC_SLUG  = "ocpv-fusion-lab"
DOC_TITLE = "OCP Virtualization with IBM Fusion Lab"
IMG_BASE  = f"{{{{ site.baseurl }}}}/assets/images/{DOC_SLUG}"

OUT_DIR.mkdir(parents=True, exist_ok=True)

# ── Known attribute values (replaces Antora runtime substitutions) ────────────
ATTRS = {
    "ocp_version":              "4.20",
    "ocpvirt_version":          "4.20",
    "fusion_version":           "2.12",
    "openshift_console_url":    "*your OpenShift Console URL (from TechZone reservation)*",
    "openshift_api_url":        "*your OpenShift API URL (from TechZone reservation)*",
    "admin_user":               "*your kubeadmin username (from TechZone reservation)*",
    "admin_password":           "*your kubeadmin password (from TechZone reservation)*",
    "openshift_cluster_console_url": "*your OpenShift Console URL (from TechZone reservation)*",
    "openshift_cluster_api_url":     "*your OpenShift API URL (from TechZone reservation)*",
    "openshift_cluster_admin_username": "kubeadmin",
    "openshift_cluster_admin_password": "*your kubeadmin password (from TechZone reservation)*",
    "lab_name":                 "ocpv-fusion-lab",
}

# ── Page definitions ──────────────────────────────────────────────────────────
PAGES = [
    # (adoc_file,          out_file,            title,                                    nav_order, parent)
    ("index.adoc",         "index.md",           DOC_TITLE,                                1,         None),
    ("01-overview.adoc",   "overview.md",        "Workshop Overview",                      2,         DOC_TITLE),
    ("02-details.adoc",    "details.md",         "Workshop Details",                       3,         DOC_TITLE),
    ("03-module-01.adoc",  "module-01.md",       "Module 1: Exploring the Environment",    4,         DOC_TITLE),
    ("04-module-02.adoc",  "module-02.md",       "Module 2: VM Lifecycle Management",      5,         DOC_TITLE),
    ("05-module-03.adoc",  "module-03.md",       "Module 3: Workload Migration",           6,         DOC_TITLE),
    ("06-module-04.adoc",  "module-04.md",       "Module 4: Backup and Restore",           7,         DOC_TITLE),
    ("07-conclusion.adoc", "conclusion.md",      "Workshop Conclusion",                    8,         DOC_TITLE),
]

# ── Conversion helpers ────────────────────────────────────────────────────────

def substitute_attrs(text):
    """Replace {attr_name} references with known values."""
    def replacer(m):
        key = m.group(1)
        return ATTRS.get(key, f"`{{{key}}}`")
    return re.sub(r'\{([a-zA-Z0-9_]+)\}', replacer, text)

def convert_adoc(text):
    """Convert AsciiDoc markup to Markdown line by line with block awareness."""
    lines = text.split('\n')
    out = []
    i = 0
    in_source_block = False
    source_lang = 'bash'
    in_listing_block = False
    in_table = False
    skip_next = False
    block_title = None

    while i < len(lines):
        line = lines[i]

        # Skip include directives for attributes partial
        if line.startswith('include::'):
            i += 1
            continue

        # Skip AsciiDoc header directives (:toc:, :source-highlighter:, etc.)
        if re.match(r'^:[a-zA-Z][a-zA-Z0-9_-]*:.*$', line) and not line.startswith('::'):
            i += 1
            continue

        # Block title (.Some title)
        if re.match(r'^\.[A-Z]', line) and not line.startswith('..'):
            block_title = line[1:]
            i += 1
            continue

        # Source block delimiter ----
        if line.strip() == '----':
            if in_source_block or in_listing_block:
                out.append('```')
                in_source_block = False
                in_listing_block = False
                source_lang = 'bash'
            else:
                # Look back for [source,...] or just treat as code
                in_listing_block = True
                if block_title:
                    out.append(f'**{block_title}**')
                    block_title = None
                out.append(f'```{source_lang}')
            i += 1
            continue

        # Source block annotation [source,lang,role=execute] etc.
        if re.match(r'^\[source', line):
            # extract language
            m = re.search(r'\[source[,\s]*([a-zA-Z0-9_+-]*)', line)
            source_lang = m.group(1).strip() if m and m.group(1).strip() else 'bash'
            if not source_lang or source_lang in ('subs=attributes', 'subs', 'subs=attributes,'):
                source_lang = 'bash'
            # Next line should be ---- delimiter — set flag so we open block when we hit it
            in_source_block = True
            i += 1
            continue

        # Block title (.Username / .Password / .Command etc.)
        if re.match(r'^\.[A-Za-z]', line) and not line.startswith('..'):
            block_title = line[1:].strip()
            i += 1
            continue

        # Inside code block — emit raw (after attr substitution)
        if in_source_block or in_listing_block:
            out.append(substitute_attrs(line))
            i += 1
            continue

        # ==== example block (used for "Verify" sections) — treat as blockquote header
        if line.strip() == '====':
            i += 1
            continue

        # [NOTE], [TIP], [IMPORTANT], [WARNING] blocks
        if line.strip() in ('[NOTE]', '[TIP]', '[IMPORTANT]', '[WARNING]'):
            label = line.strip()[1:-1].title()
            # Next line might be ==== or just text
            i += 1
            if i < len(lines) and lines[i].strip() == '====':
                i += 1  # skip opening ====
                callout_lines = []
                while i < len(lines) and lines[i].strip() != '====':
                    callout_lines.append(lines[i])
                    i += 1
                i += 1  # skip closing ====
                body = convert_adoc('\n'.join(callout_lines)).strip()
                out.append(f'> **{label}:** {body}')
                out.append('')
                continue
            else:
                # inline adoc NOTE: style handled below
                continue

        # Inline NOTE:/TIP:/IMPORTANT:/WARNING: callouts
        m = re.match(r'^(NOTE|TIP|IMPORTANT|WARNING):\s*(.*)', line)
        if m:
            label, body = m.group(1).title(), m.group(2)
            body = convert_inline(body)
            out.append(f'> **{label}:** {body}')
            out.append('')
            i += 1
            continue

        # AsciiDoc document title (= Title) → H1 (skip — we add it via front matter)
        if re.match(r'^= [^=]', line):
            i += 1
            continue

        # Section headings == → ##, === → ###, etc.
        m = re.match(r'^(={2,6})\s+(.*)', line)
        if m:
            level = len(m.group(1))   # 2=##, 3=###, 4=####
            hashes = '#' * level
            title_text = convert_inline(m.group(2))
            # Strip anchor IDs from heading text
            title_text = re.sub(r'\[\[.*?\]\]', '', title_text).strip()
            out.append(f'{hashes} {title_text}')
            out.append('')
            i += 1
            continue

        # Anchor [[id]] — skip (Just the Docs generates heading anchors)
        if re.match(r'^\[\[.*\]\]$', line):
            i += 1
            continue

        # Image macro: image::file.png[alt,...] — may appear anywhere in line
        # First check as standalone block macro
        m = re.match(r'^image::([^\[]+)\[([^\]]*)\]', line)
        if m:
            filename = m.group(1).strip()
            attrs_str = m.group(2)
            title_m = re.search(r'title="([^"]+)"', attrs_str)
            # Fall back to first positional attr before comma
            first_attr = attrs_str.split(',')[0].strip() if attrs_str else ''
            alt = title_m.group(1) if title_m else (first_attr or filename.replace('-',' ').replace('.png',''))
            if block_title:
                alt = block_title
                block_title = None
            out.append(f'![{alt}]({IMG_BASE}/{filename})')
            out.append('')
            i += 1
            continue

        # Ordered list (. item) — but not .. (second level) which use different indent
        m = re.match(r'^(\.*)\. (.+)', line)
        if m:
            dots = m.group(1)
            text = convert_inline(m.group(2))
            indent = '  ' * len(dots)
            out.append(f'{indent}1. {text}')
            i += 1
            continue

        # Unordered list (* item or ** item)
        m = re.match(r'^(\*+) (.+)', line)
        if m:
            stars = m.group(1)
            text = convert_inline(m.group(2))
            indent = '  ' * (len(stars) - 1)
            out.append(f'{indent}- {text}')
            i += 1
            continue

        # Continuation + (attach next block to list item)
        if line.strip() == '+':
            i += 1
            continue

        # Horizontal rule '''
        if line.strip() == "'''":
            out.append('---')
            i += 1
            continue

        # Table block |=== 
        if line.strip() == '|===':
            in_table = not in_table
            if not in_table:
                out.append('')
            i += 1
            continue

        if in_table:
            # Simple table row conversion
            cells = [c.strip() for c in line.split('|') if c.strip()]
            if cells:
                out.append('| ' + ' | '.join(convert_inline(c) for c in cells) + ' |')
                # Add separator after first row
                if len(out) >= 2 and out[-2].startswith('|') and not out[-2].startswith('| ---'):
                    # Check if prev line was first header row
                    prev = out[-2] if len(out) >= 2 else ''
                    if prev.startswith('|') and '---' not in prev:
                        # peek: is this the second row? insert separator
                        pass
            i += 1
            continue

        # Blank line
        if not line.strip():
            out.append('')
            i += 1
            continue

        # Regular paragraph text
        converted = convert_inline(line)
        if block_title and converted.strip():
            out.append(f'**{block_title}**')
            block_title = None
        out.append(converted)
        i += 1

    return '\n'.join(out)


def convert_inline(text):
    """Convert inline AsciiDoc markup to Markdown."""
    # Attribute substitution
    text = substitute_attrs(text)

    # xref:file.adoc#anchor[label] → [label](#anchor) or just label
    def xref_replace(m):
        target = m.group(1)   # e.g. "03-module-01.adoc#exercise-1"
        label  = m.group(2)
        if '#' in target:
            anchor = target.split('#')[1]
            return f'[{label}](#{anchor})'
        return label
    text = re.sub(r'xref:([^\[]+)\[([^\]]*)\]', xref_replace, text)

    # link:url[label] or url[label, window=blank]
    def link_replace(m):
        url   = m.group(1)
        label = m.group(2).split(',')[0].strip()
        return f'[{label}]({url})'
    text = re.sub(r'link:([^\[]+)\[([^\]]+)\]', link_replace, text)

    # Bare URL[label]
    text = re.sub(r'(https?://[^\[]+)\[([^\]]+)\]', lambda m: f'[{m.group(2).split(",")[0].strip()}]({m.group(1)})', text)

    # Bold **text** (AsciiDoc *text* or **text**)
    text = re.sub(r'\*\*(.+?)\*\*', r'**\1**', text)
    text = re.sub(r'\*([^*\s][^*]*[^*\s])\*', r'**\1**', text)

    # Italic __text__ or _text_
    text = re.sub(r'__(.+?)__', r'*\1*', text)
    text = re.sub(r'_([^_\s][^_]*[^_\s])_', r'*\1*', text)

    # Inline code `text` (AsciiDoc uses backtick too)
    text = re.sub(r'`([^`]+)`', r'`\1`', text)

    # Monospace +text+
    text = re.sub(r'\+([^+]+)\+', r'`\1`', text)

    # Superscript ^text^
    text = re.sub(r'\^([^^]+)\^', r'<sup>\1</sup>', text)

    # Remove AsciiDoc passthrough $$...$$ and +++...+++
    text = re.sub(r'\$\$(.+?)\$\$', r'\1', text)
    text = re.sub(r'\+\+\+(.+?)\+\+\+', r'\1', text)

    # image:file.png[alt] inline image
    text = re.sub(r'image:([^\[]+)\[([^\]]*)\]',
                  lambda m: f'![{m.group(2)}]({{{{ site.baseurl }}}}/assets/images/{DOC_SLUG}/{m.group(1)})',
                  text)

    return text


def build_front_matter(title, nav_order, parent, permalink):
    lines = ["---", "layout: default", f'title: "{title}"',
             f"permalink: {permalink}", f"nav_order: {nav_order}"]
    if parent:
        lines.append(f'parent: "{parent}"')
    lines.append("---\n")
    return '\n'.join(lines)


# ── Process each page ─────────────────────────────────────────────────────────
for adoc_file, out_file, title, nav_order, parent in PAGES:
    src = ADOC_DIR / adoc_file
    if not src.exists():
        print(f"WARNING: {src} not found, skipping")
        continue

    raw = src.read_text(encoding='utf-8')

    # Build permalink
    if out_file == "index.md":
        permalink = f"/{DOC_SLUG}/"
    else:
        slug = out_file.replace('.md', '')
        permalink = f"/{DOC_SLUG}/{slug}/"

    # Convert content
    body = convert_adoc(raw)

    # Clean up excessive blank lines
    body = re.sub(r'\n{3,}', '\n\n', body)

    # Fix table separators — insert after header row
    def fix_table(text):
        lines = text.split('\n')
        result = []
        for idx, l in enumerate(lines):
            result.append(l)
            if l.startswith('|') and idx + 1 < len(lines) and lines[idx+1].startswith('|') and '---' not in l:
                # Check if previous line was not already a separator
                prev = result[-2] if len(result) >= 2 else ''
                if '---' not in prev and idx == next((j for j, x in enumerate(lines) if x.startswith('|')), -1):
                    cols = l.count('|') - 1
                    result.append('| ' + ' | '.join(['---'] * max(cols, 1)) + ' |')
        return '\n'.join(result)

    fm = build_front_matter(title, nav_order, parent, permalink)
    dest = OUT_DIR / out_file
    dest.write_text(fm + body, encoding='utf-8')
    print(f"  Written: docs/ocpv-fusion-lab/{out_file}")

print(f"\nDone! {len(PAGES)} pages written")
