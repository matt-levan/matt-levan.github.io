# Contributing — IBM Fusion Lab Guides

This repository hosts the source for **https://matt-levan.github.io**, a Jekyll + Just the Docs GitHub Pages site containing IBM Fusion hands-on lab guides converted from Word (`.docx`) and AsciiDoc (`.adoc`) source documents.

---

## Table of contents

- [Repository layout](#repository-layout)
- [Site architecture](#site-architecture)
- [Adding a new guide from a Word document](#adding-a-new-guide-from-a-word-document)
- [Conversion scripts reference](#conversion-scripts-reference)
- [Word style → Markdown mapping](#word-style--markdown-mapping)
- [Shared includes system](#shared-includes-system)
- [Image naming convention](#image-naming-convention)
- [Front matter conventions](#front-matter-conventions)
- [Branch and merge workflow](#branch-and-merge-workflow)
- [Running the site locally](#running-the-site-locally)
- [Known issues / backlog](#known-issues--backlog)

---

## Repository layout

```
matt-levan.github.io/          ← Jekyll site root (= git repo root)
├── _config.yml                ← remote_theme, collections, Just the Docs config
├── Gemfile
├── index.md                   ← Landing page (nav_order: 0, doc-card grid)
│
├── _includes/
│   ├── head_custom.html       ← Global CSS (2 px image border)
│   └── shared/                ← Reusable content snippets
│       ├── getting-help.md
│       ├── product-disclaimer.md
│       ├── redhat-prerequisites.md
│       ├── reserve-techzone-environment.md   ← Single-cluster TechZone steps
│       ├── install-fusion-operator.md
│       ├── openshift-project-selector.md
│       └── reserve-two-rdr-environments.md  ← Dual-cluster RDR steps
│
├── docs/
│   ├── fusion-demo-guide/     ← IBM Fusion Demo Guide (12 pages)
│   ├── backup-restore-guide/  ← Backup & Restore Lab Guide (7 pages)
│   ├── ocpv-fusion-lab/       ← OCP Virtualization with Fusion Lab (8 pages)
│   ├── hcp-lab-guide/         ← Hosted Control Plane Lab Guide (9 pages)
│   └── rdr-lab-guide/         ← Regional Disaster Recovery Lab Guide (8 pages)
│
├── assets/images/
│   ├── fusion-demo-guide/
│   ├── backup-restore-guide/
│   ├── ocpv-fusion-lab/
│   ├── hcp-lab-guide/
│   ├── rdr-lab-guide/
│   └── shared/                ← openshift-project-selector screenshots
│
└── tools/                     ← Conversion scripts (see below)
    ├── convert_docx.py        ← Demo Guide (.docx → Markdown)
    ├── convert_backup_restore.py
    ├── convert_hcp.py
    ├── convert_rdr.py
    ├── convert_adoc.py        ← OCP Virt Lab (.adoc → Markdown)
    ├── postprocess_hcp.py     ← Strip backtick artifacts from code blocks
    ├── postprocess_rdr.py
    ├── postprocess_adoc.py
    ├── rename_images.py       ← Rename imageN.png → section-slug-NN.png
    ├── restructure_multidoc.py ← One-time: moved _pages/ → docs/
    └── switch_to_just_the_docs.py ← One-time: migrated to Just the Docs theme
```

Source `.docx` and `.adoc` files live **outside** the repo in the parent workspace directory:

```
mlevan-projects/
├── matt-levan.github.io/      ← this repo
├── IBM Fusion Demo Guide v2.13.1.docx
├── IBM Fusion - Backup and Restore Lab Guide v2.12.0.0.docx
├── IBM Fusion - HCP Lab Guide v2.11.0.0.docx
├── IBM Fusion - RDR Lab Prep Guide v2.10.0.0.docx
├── IBM Fusion - RDR Lab Guide v2.11.0.0.docx
└── ocpv-rdr-setup.docx
```

All scripts must be run from `mlevan-projects/` (the parent directory), **not** from inside the repo.

---

## Site architecture

- **Theme:** `just-the-docs/just-the-docs` via `remote_theme` in `_config.yml`
- **`baseurl`:** `""` (empty) — required for a GitHub Pages user site (`username.github.io`)
- **Navigation:** Just the Docs sidebar with up to 3 levels: `parent` (H1 guide index) → page → `grand_parent` (unused currently)
- **`nav_order: 0`** on `index.md` keeps "Home" above all guide index pages (which use `nav_order: 1`)
- **Copy buttons** on code fences: built into Just the Docs v0.6+, no extra config needed
- **Global image border:** injected via `_includes/head_custom.html` → `.main-content img { border: 2px solid #e5e7eb; }`

---

## Adding a new guide from a Word document

### 1. Create a branch

```bash
git checkout main
git checkout -b my-new-guide
```

### 2. Write a conversion script

Copy `tools/convert_hcp.py` or `tools/convert_rdr.py` as a starting point. Key things to set:

```python
DOCX_PATH  = "My New Guide v1.0.docx"          # relative to mlevan-projects/
BASE       = Path("matt-levan.github.io")
DOCS_DIR   = BASE / "docs" / "my-new-guide"
IMAGES_DIR = BASE / "assets" / "images" / "my-new-guide"
DOC_SLUG   = "my-new-guide"
DOC_TITLE  = "My New Guide"
```

Set `PAGE_META` to map each H1 slug to its desired display title, `nav_order`, `parent`, and `grand_parent`.

### 3. Run the script

```bash
cd mlevan-projects/
python3 matt-levan.github.io/tools/convert_my_new_guide.py
```

### 4. Post-process code blocks

Word's run-level formatting leaks inline backtick markers into code blocks. Run the post-processor:

```bash
python3 matt-levan.github.io/tools/postprocess_hcp.py   # or write a variant for your guide
```

### 5. Add a card to the landing page

Edit [`index.md`](index.md) and add a new `<a href="/my-new-guide/" class="doc-card">` entry to the grid.

### 6. Review content manually

Check the generated Markdown for:
- Broken nested bullet lists (indentation collapsed by the converter)
- Markdown link syntax inside code blocks (`[url](url)` → plain URL)
- `mailto:` links wrapped around SSH commands
- Double-bold artifacts: `**Create an ****IBMid**` → `**Create an IBMid**`
- Duplicate raw URLs after hyperlinks: `[text](url) (url)` → `[text](url)`
- Missing `##`/`###` headings on plain-text section titles
- YAML code blocks with collapsed indentation

### 7. Commit and push

```bash
git add docs/my-new-guide/ assets/images/my-new-guide/
git commit -m "Add My New Guide"
git push origin my-new-guide
```

---

## Conversion scripts reference

| Script | Input | Output | Notes |
|---|---|---|---|
| `convert_docx.py` | `IBM Fusion Demo Guide v2.13.1.docx` | `docs/fusion-demo-guide/` | First guide; also writes `_config.yml` skeleton |
| `convert_backup_restore.py` | `IBM Fusion - Backup and Restore Lab Guide v2.12.0.0.docx` | `docs/backup-restore-guide/` | Also creates `_includes/shared/` snippets |
| `convert_hcp.py` | `IBM Fusion - HCP Lab Guide v2.11.0.0.docx` | `docs/hcp-lab-guide/` | Extracts `reserve-techzone-environment` and `install-fusion-operator` shared includes |
| `convert_rdr.py` | `IBM Fusion - RDR Lab Prep Guide v2.10.0.0.docx` + `IBM Fusion - RDR Lab Guide v2.11.0.0.docx` | `docs/rdr-lab-guide/` | Merges two source docs; image rename runs across both combined |
| `convert_adoc.py` | `.adoc` pages cloned from `jeanchlopez/txc26-ocpv-fusion-lab` | `docs/ocpv-fusion-lab/` | Run from `mlevan-projects/`; expects adoc source at `/tmp/ocpv-adoc/pages/` |
| `postprocess_hcp.py` | `docs/hcp-lab-guide/` | (in place) | Strips inline backtick markers inside fenced code blocks |
| `postprocess_rdr.py` | `docs/rdr-lab-guide/` | (in place) | Same as above for RDR |
| `postprocess_adoc.py` | `docs/ocpv-fusion-lab/` | (in place) | Fixes broken code fences, leftover AsciiDoc macros |
| `rename_images.py` | `assets/images/` | (in place) | Renames `imageN.png` → `section-slug-NN.png`; also updates Markdown refs |
| `restructure_multidoc.py` | `_pages/*.md` | `docs/fusion-demo-guide/` | **One-time migration** — already applied; do not re-run |
| `switch_to_just_the_docs.py` | site root | (in place) | **One-time migration** — already applied; do not re-run |

---

## Word style → Markdown mapping

The IBM LCD (Lab Content Developer) custom Word styles map as follows:

| Word style ID | Markdown output |
|---|---|
| `heading1` | `# ` (H1 — becomes a new page) |
| `heading2` | `## ` |
| `heading3` | `### ` |
| `heading4` | `#### ` |
| `LCD - Narration` / `lcd-narration` | `> blockquote` |
| `LCD - UI Element Bold` / `lcd-uielement-bold` | `**bold**` |
| `LCD - Code Element Mono` / `lcd-codeelement-mono` | `` `inline code` `` |
| `LCD - Code` / `lcd-code` | ```` ```code block``` ```` |
| `LCD - Bullet List Compact 1–3` | `-` bullet (indented by level) |
| `LCD - List Numbering 1–3` | `1.` ordered list (indented by level) |
| `TOC*` / `lcd-toc` / `lcd-disclaimer` | skipped |
| `lcd-doctitle` | `# ` title (skipped — replaced by front matter) |
| `lcd-caption` | `*italic caption*` |
| `lcd-graphic` / `lcd-spacer` | skipped |

Code blocks are auto-tagged with `bash` or `yaml` based on content heuristics (looks for `apiVersion:`, `kind:`, `oc `, `kubectl`, `ssh`, etc.).

---

## Shared includes system

Reusable content lives in `_includes/shared/` and is embedded with:

```liquid
{% include shared/filename.md %}
```

| File | Content | Used by |
|---|---|---|
| `getting-help.md` | Slack links, TechZone help | All guides |
| `product-disclaimer.md` | UI change disclaimer | All guides |
| `redhat-prerequisites.md` | DO080/DO180/DO280 course links | All guides |
| `reserve-techzone-environment.md` | Single-cluster TechZone reservation walkthrough | Demo Guide, HCP Guide |
| `install-fusion-operator.md` | Install + Connect to Fusion steps | HCP Lab Prerequisites |
| `openshift-project-selector.md` | OCP project selector reference screenshots | All addendum pages |
| `reserve-two-rdr-environments.md` | Dual-cluster reservation with ocp2 network CIDRs | RDR Guide only |

> **Important:** Do NOT reuse `reserve-techzone-environment.md` for RDR — the RDR guide needs two separate reservations with specific network CIDRs. Use `reserve-two-rdr-environments.md` instead.

---

## Image naming convention

Images are extracted from the `.docx` zip and renamed to:

```
<section-slug>-NN.ext
```

where `<section-slug>` is the slugified text of the H2/H3 heading the image appears under, and `NN` is a zero-padded sequential counter (01, 02, …) scoped to that heading.

Examples:
- `creating-an-ibmid-01.png`
- `openshift-web-console-03.png`
- `install-backup-restore-service-05.png`

**Known issue — RDR `lab-prerequisites.md`:** The image rename for RDR ran across the combined Prep Guide + Lab Guide elements in sequence. This caused a naming collision where some Fusion Operator install screenshots in `lab-prerequisites.md` were assigned names like `creating-an-ibmid-02.png` (from the Prep Guide IBMid section that shares the same heading counter). These images need to be manually replaced with the correct Fusion Operator screenshots.

---

## Front matter conventions

Every page requires:

```yaml
---
layout: default
title: "Page Title"
permalink: /guide-slug/page-slug/
nav_order: N
parent: "Guide Index Title"   # omit on index pages
---
```

- Guide index pages (`index.md`) have **no `parent`** and use `nav_order: 1`
- The site `index.md` (landing page) has `nav_order: 0` so it always sorts first
- Just the Docs supports a maximum of 3 navigation levels; use `grand_parent` for a third level if needed

---

## Branch and merge workflow

Each new guide is developed on its own branch, then merged into `main` in order (since each branch builds on the previous):

```
main
  └── backup-restore-guide
        └── ocpv-fusion-lab
              └── hcp-lab-guide
                    └── rdr-lab-guide
```

All four branches have been merged into `main`. For a new guide:

```bash
git checkout main
git pull origin main
git checkout -b new-guide-name
# ... do work ...
git push origin new-guide-name
# open PR → merge to main
```

---

## Running the site locally

```bash
cd matt-levan.github.io/
bundle install
bundle exec jekyll serve
# open http://localhost:4000
```

Requires Ruby + Bundler. The `Gemfile` pins `github-pages` and `just-the-docs`.

---

## Known issues / backlog

| Status | Issue |
|---|---|
| 🔲 Open | **RDR `lab-prerequisites.md` wrong images** — image rename collision means Install Fusion Operator steps show IBMid screenshots (`creating-an-ibmid-02/03/04/05.png`) instead of actual Fusion operator install screenshots. Needs manual image replacement with correct screenshots. |
| 🔲 Open | Content review of B&R Guide pages (not yet done in detail) |
| 🔲 Open | Content review of OCP Virt lab pages (not yet done in detail) |
