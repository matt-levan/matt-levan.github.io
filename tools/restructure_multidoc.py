#!/usr/bin/env python3
"""
Restructure the site for multi-doc support:
 - Moves _pages/*.md  → docs/fusion-demo-guide/*.md
 - Moves assets/images/* → assets/images/fusion-demo-guide/*
 - Fixes all image paths in markdown files
 - Rewrites front matter for 3-level Just the Docs hierarchy
 - Writes new _config.yml, root index.md, and per-doc index.md
"""

import os
import re
import shutil
from pathlib import Path

BASE = Path("fusion-demo-guide")

# ── Page definitions ──────────────────────────────────────────────────────────
# (old filename under _pages/, new filename under docs/fusion-demo-guide/,
#  title, nav_order, parent, grand_parent)
# grand_parent = the top-level doc title (shows in 3rd level nesting)
DOC_TITLE = "IBM Fusion Demo Guide"

PAGES = [
    # old_name,                                       new_name,                                           title,                                           nav_order, parent,                        grand_parent
    ("index.md",                                      "index.md",                                         "IBM Fusion Demo Guide",                          1,         None,                          None),
    ("_pages/prerequisites.md",                       "prerequisites.md",                                 "Prerequisites",                                  2,         DOC_TITLE,                     None),
    ("_pages/reserve-or-provision-your-environment.md","reserve-or-provision.md",                         "Reserve or Provision Environment",               3,         DOC_TITLE,                     None),
    ("_pages/demonstration-scope.md",                 "demonstration-scope.md",                           "Demonstration Scope",                            4,         DOC_TITLE,                     None),
    ("_pages/demonstration-infrastructure.md",        "demonstration-infrastructure.md",                  "Demonstration Infrastructure",                   5,         DOC_TITLE,                     None),
    ("_pages/demonstration-scenarios.md",             "demonstration-scenarios.md",                       "Demonstration Scenarios",                        6,         DOC_TITLE,                     None),
    ("_pages/ibm-fusion.md",                          "ibm-fusion.md",                                    "IBM Fusion",                                     7,         DOC_TITLE,                     None),
    ("_pages/provide-persistent-storage.md",          "provide-persistent-storage.md",                    "Provide Persistent Storage",                     8,         DOC_TITLE,                     None),
    ("_pages/wait-for-the-installation-to-complete.md","wait-for-installation.md",                        "Wait for Installation to Complete",              1,         "Provide Persistent Storage",  DOC_TITLE),
    ("_pages/persistent-storage-fusion-data-foundation-fdf.md","persistent-storage-fdf.md",               "Persistent Storage – FDF",                       2,         "Provide Persistent Storage",  DOC_TITLE),
    ("_pages/protect-containerized-workload-backuprestore.md","backup-restore.md",                        "Protect Workload – Backup/Restore",              9,         DOC_TITLE,                     None),
    ("_pages/getting-help-and-troubleshooting.md",    "getting-help.md",                                  "Getting Help and Troubleshooting",               10,        DOC_TITLE,                     None),
]

DOCS_DIR   = BASE / "docs" / "fusion-demo-guide"
NEW_IMAGES = BASE / "assets" / "images" / "fusion-demo-guide"
OLD_IMAGES = BASE / "assets" / "images"

# ── Step 1: Create new directories ───────────────────────────────────────────
DOCS_DIR.mkdir(parents=True, exist_ok=True)
NEW_IMAGES.mkdir(parents=True, exist_ok=True)
print("Created docs/fusion-demo-guide/ and assets/images/fusion-demo-guide/")

# ── Step 2: Move images into subfolder ───────────────────────────────────────
moved_images = 0
for img in OLD_IMAGES.iterdir():
    if img.is_file():
        shutil.move(str(img), str(NEW_IMAGES / img.name))
        moved_images += 1
print(f"Moved {moved_images} images → assets/images/fusion-demo-guide/")

# ── Step 3: Copy & rewrite each page ─────────────────────────────────────────
def build_front_matter(title, nav_order, parent, grand_parent, permalink):
    lines = ["---", "layout: default", f'title: "{title}"',
             f"permalink: {permalink}", f"nav_order: {nav_order}"]
    if parent:
        lines.append(f'parent: "{parent}"')
    if grand_parent:
        lines.append(f'grand_parent: "{grand_parent}"')
    lines.append("---")
    return "\n".join(lines)

def fix_image_paths(content):
    # /assets/images/foo.png → /assets/images/fusion-demo-guide/foo.png
    return re.sub(
        r'(/assets/images/)(?!fusion-demo-guide/)([^\)]+)',
        r'\1fusion-demo-guide/\2',
        content
    )

def fix_permalinks(content, new_permalink):
    return re.sub(r'permalink:.*', f'permalink: {new_permalink}', content)

for old_rel, new_name, title, nav_order, parent, grand_parent in PAGES:
    old_path = BASE / old_rel
    new_path = DOCS_DIR / new_name

    if not old_path.exists():
        print(f"  WARNING: {old_path} not found, skipping")
        continue

    content = old_path.read_text(encoding="utf-8")

    # Build new permalink
    if new_name == "index.md":
        permalink = "/fusion-demo-guide/"
    else:
        slug = new_name.replace(".md", "")
        permalink = f"/fusion-demo-guide/{slug}/"

    # Strip existing front matter
    content = re.sub(r'^---\n.*?---\n', '', content, count=1, flags=re.DOTALL)

    # Fix image paths
    content = fix_image_paths(content)

    # Build new front matter
    fm = build_front_matter(title, nav_order, parent, grand_parent, permalink)
    content = fm + "\n\n" + content.lstrip()

    new_path.write_text(content, encoding="utf-8")
    print(f"  Written: docs/fusion-demo-guide/{new_name}")

# ── Step 4: Remove old _pages dir and old root index ─────────────────────────
old_pages = BASE / "_pages"
if old_pages.exists():
    shutil.rmtree(str(old_pages))
    print("Removed _pages/")

old_index = BASE / "index.md"
if old_index.exists():
    old_index.unlink()
    print("Removed root index.md (will be replaced)")

# ── Step 5: Write new root index.md (landing page) ───────────────────────────
landing = """\
---
layout: home
title: Home
permalink: /
nav_order: 1
---

# IBM Storage Technical Library

Welcome to the IBM Storage technical documentation library. Select a guide below to get started.

<div class="doc-cards">

  <a href="/fusion-demo-guide/" class="doc-card">
    <h2>IBM Fusion Demo Guide</h2>
    <p>Hands-on demo guide for platform modernization with IBM Fusion. Covers installation, storage, backup, and restore on OpenShift.</p>
    <span class="doc-card-version">v2.13.1</span>
  </a>

  <a href="#" class="doc-card doc-card-coming-soon">
    <h2>Fusion Backup &amp; Restore Guide</h2>
    <p>Deep-dive into IBM Fusion Backup &amp; Restore service configuration, policies, and recovery procedures.</p>
    <span class="doc-card-badge">Coming soon</span>
  </a>

  <a href="#" class="doc-card doc-card-coming-soon">
    <h2>Fusion Regional Disaster Recovery Guide</h2>
    <p>Configure and test regional disaster recovery with IBM Fusion hub-and-spoke architecture.</p>
    <span class="doc-card-badge">Coming soon</span>
  </a>

</div>

<style>
.doc-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 1.25rem;
  margin-top: 2rem;
}
.doc-card {
  display: block;
  padding: 1.25rem 1.5rem;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  text-decoration: none;
  color: inherit;
  transition: border-color 0.15s, box-shadow 0.15s;
}
.doc-card:hover {
  border-color: #2c84fa;
  box-shadow: 0 2px 8px rgba(44,132,250,0.12);
  text-decoration: none;
}
.doc-card h2 {
  margin: 0 0 0.5rem;
  font-size: 1.05rem;
  color: #2c84fa;
  border: none;
}
.doc-card p {
  margin: 0 0 0.75rem;
  font-size: 0.9rem;
  color: #57606a;
  line-height: 1.5;
}
.doc-card-version {
  font-size: 0.78rem;
  color: #57606a;
  background: #f0f4ff;
  padding: 0.15em 0.5em;
  border-radius: 3px;
}
.doc-card-coming-soon {
  opacity: 0.6;
  cursor: default;
  pointer-events: none;
}
.doc-card-badge {
  font-size: 0.78rem;
  color: #ffffff;
  background: #57606a;
  padding: 0.15em 0.5em;
  border-radius: 3px;
}
</style>
"""
(BASE / "index.md").write_text(landing, encoding="utf-8")
print("Written: index.md (landing page)")

# ── Step 6: Write _config.yml ─────────────────────────────────────────────────
config = """\
title: IBM Storage Technical Library
description: Technical guides for IBM Storage — Fusion, Backup & Restore, Disaster Recovery
baseurl: ""
url: "https://matt-levan.github.io"

remote_theme: just-the-docs/just-the-docs

# Just the Docs settings
color_scheme: light
search_enabled: true
heading_anchors: true

aux_links:
  "IBM Storage Docs":
    - "https://www.ibm.com/docs/en/storage-fusion-software"

footer_content: "IBM Storage Technical Library &mdash; matt-levan.github.io"

# Collections — one per document
collections:
  docs:
    output: true
    permalink: /:path/

just_the_docs:
  collections:
    docs:
      name: "Documents"

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
(BASE / "_config.yml").write_text(config, encoding="utf-8")
print("Written: _config.yml")

# ── Step 7: Clean up old _data/navigation.yml (not needed by Just the Docs) ──
old_nav = BASE / "_data" / "navigation.yml"
if old_nav.exists():
    old_nav.unlink()
    print("Removed _data/navigation.yml (not needed)")
old_data = BASE / "_data"
if old_data.exists() and not any(old_data.iterdir()):
    old_data.rmdir()
    print("Removed _data/ (empty)")

print("\nDone!")
