#!/usr/bin/env python3
"""Post-process docs/rdr-lab-guide/ — strip inline backtick markers inside fenced code blocks."""
import re
from pathlib import Path

DOCS_DIR = Path("fusion-demo-guide/docs/rdr-lab-guide")

def clean_code_block_line(line):
    while '`' in line:
        new = re.sub(r'`([^`]*)`', r'\1', line)
        if new == line:
            break
        line = new
    line = line.replace('`', '')
    return line

def process_file(path):
    text = path.read_text(encoding='utf-8')
    lines = text.splitlines(keepends=True)
    result = []
    in_code = False
    lang_fence = None
    changed = False

    for line in lines:
        stripped = line.rstrip('\n')
        if not in_code:
            m = re.match(r'^(```+)(\w*)$', stripped)
            if m:
                in_code = True
                lang_fence = m.group(1)
                result.append(line)
            else:
                result.append(line)
        else:
            if stripped == lang_fence:
                in_code = False
                lang_fence = None
                result.append(line)
            else:
                cleaned = clean_code_block_line(stripped)
                if cleaned != stripped:
                    changed = True
                result.append(cleaned + '\n')

    if changed:
        path.write_text(''.join(result), encoding='utf-8')
        print(f"  Cleaned: {path.name}")
    else:
        print(f"  OK:      {path.name}")

for md in sorted(DOCS_DIR.glob("*.md")):
    process_file(md)
print("Done.")
