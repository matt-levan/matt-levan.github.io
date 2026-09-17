#!/usr/bin/env python3
"""
Switch fusion-demo-guide to Just the Docs theme.
- Updates _config.yml and Gemfile
- Rewrites front matter on all pages with nav_order + parent hierarchy
- Cleans up inline-backtick artifacts inside code fences
- Tags code fences with correct language identifiers
- Removes custom _layouts/default.html and assets/css/style.css
"""

import os
import re
from pathlib import Path

BASE = Path("fusion-demo-guide")

# ── Page definitions: title, slug, nav_order, parent (None = top-level) ───────
PAGES = [
    # (file,                                               title,                                           nav_order, parent)
    ("index.md",                                           "Introduction",                                  1,         None),
    ("_pages/prerequisites.md",                            "Prerequisites",                                 2,         None),
    ("_pages/reserve-or-provision-your-environment.md",    "Reserve or Provision Your Environment",         3,         None),
    ("_pages/demonstration-scope.md",                      "Demonstration Scope",                           4,         None),
    ("_pages/demonstration-infrastructure.md",             "Demonstration Infrastructure",                  5,         None),
    ("_pages/demonstration-scenarios.md",                  "Demonstration Scenarios",                       6,         None),
    ("_pages/ibm-fusion.md",                               "IBM Fusion",                                    7,         None),
    ("_pages/provide-persistent-storage.md",               "Provide Persistent Storage",                    8,         None),
    ("_pages/wait-for-the-installation-to-complete.md",    "Wait for Installation to Complete",             9,         "Provide Persistent Storage"),
    ("_pages/persistent-storage-fusion-data-foundation-fdf.md", "Persistent Storage – Fusion Data Foundation", 10,    "Provide Persistent Storage"),
    ("_pages/protect-containerized-workload-backuprestore.md", "Protect Containerized Workload – Backup/Restore", 11, None),
    ("_pages/getting-help-and-troubleshooting.md",         "Getting Help and Troubleshooting",              12,        None),
]

# ── Helpers ───────────────────────────────────────────────────────────────────

def strip_backtick_artifacts(code):
    """
    Remove inline-code backtick wrapping that leaked into fenced code blocks.
    e.g.  `oc get nodes`   →  oc get nodes
    Also cleans up backtick-surrounded fragments across the whole block.
    """
    # Remove wrapping backticks around entire lines: `some command`
    code = re.sub(r'^`(.*)`\s*$', r'\1', code, flags=re.MULTILINE)
    # Remove stray backtick sequences from mid-line wrapping
    code = re.sub(r'`([^`\n]+)`', r'\1', code)
    # Clean up remaining lone backticks
    code = code.replace('`', '')
    return code

def tag_code_block(code):
    """Return the best language tag for a fenced code block."""
    c = code.strip()
    # YAML heuristics
    if re.search(r'^(apiVersion|kind|metadata|spec|name|namespace)\s*:', c, re.MULTILINE):
        return 'yaml'
    # Shell / bash heuristics
    if re.search(r'^(ssh|oc |kubectl|curl|sudo|mmlscluster|mmlsfs|/usr/lpp|oc$)', c, re.MULTILINE):
        return 'bash'
    if re.search(r'\$\s|^#\s', c, re.MULTILINE):
        return 'bash'
    if c.startswith('oc ') or c.startswith('ssh ') or c.startswith('curl ') or c.startswith('kubectl '):
        return 'bash'
    return 'bash'  # default for single-line commands

def process_code_blocks(content):
    """Clean artifacts and add language tags to all fenced code blocks."""
    def replace_block(m):
        lang = m.group(1).strip()   # existing lang tag (may be empty)
        code = m.group(2)
        code = strip_backtick_artifacts(code)
        if not lang:
            lang = tag_code_block(code)
        return f'```{lang}\n{code}\n```'

    return re.sub(r'```(\w*)\n(.*?)```', replace_block, content, flags=re.DOTALL)

def rewrite_front_matter(content, title, nav_order, parent, permalink):
    """Replace the front matter block in a page."""
    fm_lines = [
        '---',
        f'layout: default',
        f'title: "{title}"',
        f'permalink: {permalink}',
        f'nav_order: {nav_order}',
    ]
    if parent:
        fm_lines.append(f'parent: "{parent}"')
    fm_lines.append('---')
    new_fm = '\n'.join(fm_lines)

    # Replace existing front matter
    updated = re.sub(r'^---\n.*?---\n', new_fm + '\n', content, count=1, flags=re.DOTALL)
    return updated

# ── Update _config.yml ────────────────────────────────────────────────────────
config = """\
title: IBM Fusion Demo Guide
description: Platform modernization with IBM Fusion – Hands-on demo guide v2.13.1
baseurl: ""
url: "https://matt-levan.github.io"

remote_theme: just-the-docs/just-the-docs

# Just the Docs settings
color_scheme: light
search_enabled: true
heading_anchors: true
aux_links:
  "IBM Fusion Docs":
    - "https://www.ibm.com/docs/en/storage-fusion-software"

footer_content: "IBM Fusion Demo Guide v2.13.1 &mdash; Platform modernization with IBM Fusion"

# Callout colours for blockquotes used as notes/tips
callouts_level: quiet
callouts:
  note:
    title: Note
    color: blue
  tip:
    title: Tip
    color: green
  important:
    title: Important
    color: yellow
  warning:
    title: Warning
    color: red

# Build settings
markdown: kramdown
highlighter: rouge

kramdown:
  input: GFM
  syntax_highlighter: rouge

plugins:
  - jekyll-remote-theme
  - jekyll-seo-tag
"""

(BASE / "_config.yml").write_text(config)
print("Written: _config.yml")

# ── Update Gemfile ─────────────────────────────────────────────────────────────
gemfile = """\
source "https://rubygems.org"
gem "github-pages", group: :jekyll_plugins
gem "jekyll-remote-theme"
gem "jekyll-seo-tag"
"""
(BASE / "Gemfile").write_text(gemfile)
print("Written: Gemfile")

# ── Remove custom layout and CSS (Just the Docs provides its own) ─────────────
layout_path = BASE / "_layouts" / "default.html"
css_path     = BASE / "assets" / "css" / "style.css"

if layout_path.exists():
    layout_path.unlink()
    print("Removed: _layouts/default.html")

if css_path.exists():
    css_path.unlink()
    print("Removed: assets/css/style.css")

# Remove empty _layouts dir if now empty
layouts_dir = BASE / "_layouts"
if layouts_dir.exists() and not any(layouts_dir.iterdir()):
    layouts_dir.rmdir()
    print("Removed: _layouts/ (empty)")

# ── Process each page ─────────────────────────────────────────────────────────
for filename, title, nav_order, parent in PAGES:
    path = BASE / filename
    if not path.exists():
        print(f"WARNING: {path} not found, skipping")
        continue

    content = path.read_text(encoding='utf-8')

    # Determine permalink from existing front matter
    m = re.search(r'permalink:\s*(\S+)', content)
    permalink = m.group(1) if m else '/'

    # Rewrite front matter
    content = rewrite_front_matter(content, title, nav_order, parent, permalink)

    # Fix code blocks
    content = process_code_blocks(content)

    path.write_text(content, encoding='utf-8')
    print(f"Updated:  {filename}")

print("\nDone!")
