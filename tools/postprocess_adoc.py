#!/usr/bin/env python3
"""
Post-process the converted Markdown files to fix remaining artifacts:
1. Broken code fence pairs (``` ... ```bash → ``` ... ```)
2. Leftover image:: macros (inline ones missed by block parser)
3. Leftover `. item` list items (AsciiDoc ordered list format)
4. Leftover `* item` list items on continuation lines
5. [window=blank] link artifacts
"""

import re
from pathlib import Path

DOCS_DIR = Path("fusion-demo-guide/docs/ocpv-fusion-lab")
DOC_SLUG = "ocpv-fusion-lab"
IMG_BASE = f"{{{{ site.baseurl }}}}/assets/images/{DOC_SLUG}"

def fix_content(text):
    # 1. Fix malformed code fences: ``` ... ```bash → ```lang\n...\n```
    #    Pattern: opening ``` without lang, content, then closing ```bash or ```something
    def fix_fences(t):
        # Replace ```\ncontent\n```bash with ```bash\ncontent\n```
        t = re.sub(
            r'```\n(.*?)```(bash|yaml|shell|sh|text)',
            lambda m: f'```{m.group(2)}\n{m.group(1).rstrip()}\n```',
            t, flags=re.DOTALL
        )
        # Replace bare ``` closing that follows a ```lang opening — already correct, skip
        return t

    text = fix_fences(text)

    # 2. Fix leftover image:: macros (inline form missed by block parser)
    def fix_image(m):
        filename = m.group(1).strip()
        attrs = m.group(2)
        title_m = re.search(r'title="([^"]+)"', attrs)
        first_attr = attrs.split(',')[0].strip() if attrs else ''
        alt = title_m.group(1) if title_m else (first_attr or filename.replace('-', ' ').replace('.png', ''))
        return f'\n![{alt}]({IMG_BASE}/{filename})\n'

    text = re.sub(r'image::([^\[]+)\[([^\]]*)\]', fix_image, text)

    # 3. Fix leftover AsciiDoc ordered list items (`. text` or `.. text`)
    text = re.sub(r'^(\. )(.+)$', r'1. \2', text, flags=re.MULTILINE)
    text = re.sub(r'^(\.\. )(.+)$', r'  1. \2', text, flags=re.MULTILINE)

    # 4. Fix leftover `* text` unordered list items (AsciiDoc style)
    text = re.sub(r'^\* (.+)$', r'- \1', text, flags=re.MULTILINE)
    text = re.sub(r'^\*\* (.+)$', r'  - \1', text, flags=re.MULTILINE)

    # 5. Remove [window=blank] artifacts left after link conversion
    text = re.sub(r'\[window=blank\]', '', text)
    text = re.sub(r'\[window=_blank\]', '', text)

    # 6. Fix the .Username / .Password block title artifacts that produced
    #    ``` **Username** **value** ```bash  →  clean credential callout
    text = re.sub(
        r'```\s*\n\*\*(Username|Password|Command)\*\*\s*\n(.+?)\n```bash',
        lambda m: f'> **{m.group(1)}:** {m.group(2).strip()}',
        text, flags=re.DOTALL | re.IGNORECASE
    )

    # 7. Clean up stray + continuation markers
    text = re.sub(r'^\+$', '', text, flags=re.MULTILINE)

    # 8. Collapse 3+ blank lines to 2
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text


changed = 0
for md_path in sorted(DOCS_DIR.glob('*.md')):
    original = md_path.read_text(encoding='utf-8')
    fixed = fix_content(original)
    if fixed != original:
        md_path.write_text(fixed, encoding='utf-8')
        changed += 1
        print(f"  Fixed: {md_path.name}")

print(f"\nPost-processing complete — {changed} files updated")
