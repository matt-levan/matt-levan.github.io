#!/usr/bin/env python3
"""
Fix ordered lists in kramdown/Jekyll markdown files.

The problem: items using "1." throughout, with images/blockquotes/code blocks
between them as bare (unindented) paragraphs. Kramdown treats each break as a
new list, so every item renders as "1."

The fix: indent all continuation content (images, blockquotes, code fences,
blank lines within a list item) by 3 spaces so kramdown keeps them inside
the current list item, preserving the sequential counter.
"""
import re
import sys
from pathlib import Path


def fix_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    out = []
    in_list = False
    in_fence = False
    fence_indent = 0
    changed = False

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.rstrip("\n").rstrip("\r")

        # Detect fenced code blocks (``` or ~~~) at column 0
        fence_match = re.match(r'^(`{3,}|~{3,})', stripped)

        if in_fence:
            # Indent this fence line if we're inside a list
            if in_list and fence_indent == 0:
                out.append("   " + line)
                changed = True
            else:
                out.append(line)
            # End the fence?
            if fence_match and fence_match.group(1)[0] == in_fence[0] and len(fence_match.group(1)) >= len(in_fence):
                in_fence = False
                fence_indent = 0
            i += 1
            continue

        # List item line
        list_item = re.match(r'^(\d+)\. ', stripped)
        if list_item:
            in_list = True
            out.append(line)
            i += 1
            continue

        if in_list:
            # Blank line — keep in list context (could be lazy continuation)
            if stripped == "":
                # Peek ahead: if next non-blank is a list item or indented content, keep going
                j = i + 1
                while j < len(lines) and lines[j].rstrip("\n\r") == "":
                    j += 1
                if j < len(lines):
                    next_stripped = lines[j].rstrip("\n\r")
                    next_is_list = bool(re.match(r'^\d+\. ', next_stripped))
                    next_is_content = bool(re.match(r'^(!\[|>|\s{3}|```|~~~)', next_stripped))
                    if next_is_list or next_is_content:
                        out.append(line)
                        i += 1
                        continue
                # Otherwise end the list
                in_list = False
                out.append(line)
                i += 1
                continue

            # Heading ends the list
            if re.match(r'^#{1,6} ', stripped):
                in_list = False
                out.append(line)
                i += 1
                continue

            # Image line at column 0 → indent
            if re.match(r'^!\[', stripped):
                out.append("   " + line)
                changed = True
                i += 1
                continue

            # Blockquote at column 0 → indent
            if re.match(r'^>', stripped):
                out.append("   " + line)
                changed = True
                i += 1
                continue

            # Opening fence at column 0 inside a list → indent opening + mark fence open
            if fence_match:
                in_fence = fence_match.group(1)
                fence_indent = 0  # will be indented line by line above
                out.append("   " + line)
                changed = True
                i += 1
                continue

            # Already-indented content or other paragraph continuation — leave as-is
            out.append(line)
            i += 1
            continue

        # Outside a list
        if fence_match:
            in_fence = fence_match.group(1)
        out.append(line)
        i += 1

    if changed:
        path.write_text("".join(out), encoding="utf-8")
        return True
    return False


def main():
    root = Path(__file__).parent.parent / "docs"
    files = sorted(root.rglob("*.md"))
    fixed = []
    for f in files:
        if fix_file(f):
            fixed.append(f)
            print(f"  fixed: {f.relative_to(root.parent.parent)}")
    if fixed:
        print(f"\n{len(fixed)} file(s) updated.")
    else:
        print("Nothing to change.")


if __name__ == "__main__":
    main()
