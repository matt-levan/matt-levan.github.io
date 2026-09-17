#!/usr/bin/env python3
"""
Bold the UI element label immediately preceding a callout marker like (A), (B), etc.

The pattern in these lab guides is:
  click the Save (A) button
  clicking on the Services (A) menu item
  selecting the Nodes (B) sub-item
  the Copy raw file (A) button
  Enter filebrowser in the Name (A) text entry field
  the local-cluster drop-down list (A)

The label is the UI name between the last verb/connector and the callout.

Strategy: for each (X) callout, grab the preceding text, then find the
label by walking backward from the callout, stopping as soon as we hit:
  - a hard stop character (comma, period, semicolon, colon, open paren)
  - a verb that introduces an instruction
  - a mid-phrase preposition (into, with, from, of, through, …)
    that signals a phrase boundary between a generic noun and the label

We then trim leading stopwords (articles, articles + prepositions) from
the front of the collected span.

Lines that are part of a markdown table (contain |) are skipped entirely.
"""
import re
from pathlib import Path

CALLOUT = re.compile(r'\(([A-Z])\)')

# Action verbs that precede a UI label — stop collecting when hit
VERB_STOPS = {
    'click', 'clicks', 'clicked', 'clicking',
    'select', 'selects', 'selected', 'selecting',
    'navigate', 'navigating',
    'enter', 'entering', 'entered',
    'type', 'types', 'typed', 'typing',
    'choose', 'choosing',
    'open', 'opens', 'opening',
    'close', 'closing',
    'check', 'checking',
    'uncheck', 'unchecking',
    'enable', 'enabling',
    'disable', 'disabling',
    'assign', 'assigning',
    'expand', 'expanding',
    'collapse', 'collapsing',
    'verify', 'verifying',
    'use', 'using',
    'set', 'sets', 'setting',
    'leave', 'leaving',
    'wait', 'waiting',
    'scroll', 'scrolling',
    'paste', 'pasting',
    'copy', 'copying',
    'delete', 'deleting',
    'create', 'creating',
    'reveal', 'revealing',
    'repeat',
}

# Prepositions and conjunctions that signal a phrase boundary when encountered
# mid-walk.  We stop collecting and keep whatever was already collected.
BOUNDARY_PREPS = {
    'into', 'onto', 'with', 'from', 'of', 'in', 'through', 'between',
    'against', 'within', 'throughout', 'beyond', 'past', 'toward',
    'inside', 'outside', 'along', 'upon', 'across', 'after', 'before',
    'under', 'below', 'above', 'over', 'around', 'near', 'beside',
    'except', 'despite', 'regarding', 'concerning',
    # Conjunctions — stop at "and"/"or" mid-label to avoid grabbing both sides
    'and', 'or',
}

# Leading-word stopwords: trimmed from the front of the collected label
LEADING_STOPS = {
    'the', 'a', 'an', 'on', 'by', 'for', 'as', 'at',
    'that', 'this', 'which', 'each',
    'also', 'then', 'next', 'finally', 'to',
}

# Hard-stop characters — stop collection immediately
HARD_STOP_CHARS = set('.,;:\n(|')

# Generic contextual nouns that are never part of a UI label.
# When the walk reaches one of these, stop and discard it.
# Keep this narrow: only words that are clearly never a UI element name.
GENERIC_NOUNS = {
    'contents', 'content', 'section', 'pane', 'window', 'page',
    'area', 'view', 'screen',
    'item', 'items', 'text', 'information', 'info',
    'summary', 'table', 'row', 'column',
    'step', 'steps', 'process', 'procedure',
    # "the value X" — word "value" here is generic context, not a UI label
    'value',
}


def extract_label(text_before: str) -> tuple[str, int] | tuple[None, None]:
    """
    Walk backwards through text_before to find the label phrase before a callout.
    Returns (label_string, start_pos_in_text_before) or (None, None).
    """
    s = text_before.rstrip()
    if not s:
        return None, None

    word_tokens = []
    for m in re.finditer(r'\S+', s):
        word_tokens.append((m.group(), m.start(), m.end()))

    if not word_tokens:
        return None, None

    label_tokens = []

    for tok, tok_start, tok_end in reversed(word_tokens):
        core = tok.rstrip('.,;:')
        core_lower = core.lower()

        # Hard-stop character or stray symbol at the START of this token
        if tok[0] in HARD_STOP_CHARS or tok[0] == '>':
            break

        # Verb stop
        if core_lower in VERB_STOPS:
            break

        # Boundary preposition — stop and keep what we have
        if core_lower in BOUNDARY_PREPS:
            break

        # Generic contextual noun — stop and discard
        if core_lower in GENERIC_NOUNS:
            break

        # Hard-stop character anywhere in the token body
        if any(c in HARD_STOP_CHARS for c in tok[1:]):
            break

        # Already bolded
        if tok.startswith('**'):
            break

        # Stop at bare markdown symbols
        if tok in ('*', '_', '__'):
            break

        label_tokens.insert(0, (tok, tok_start, tok_end))

        if len(label_tokens) >= 5:
            break

    if not label_tokens:
        return None, None

    # Trim leading stopwords
    while label_tokens and label_tokens[0][0].lower().rstrip('.,;:') in LEADING_STOPS:
        label_tokens.pop(0)

    if not label_tokens:
        return None, None

    # Build the label
    label_start = label_tokens[0][1]
    label_end = label_tokens[-1][2]
    label = s[label_start:label_end].rstrip('.,;:')

    if not label:
        return None, None

    return label, label_start


def bold_callouts_in_line(line: str) -> str:
    result = []
    prev_end = 0
    for m in CALLOUT.finditer(line):
        start = m.start()
        before = line[prev_end:start]

        label, label_start_in_before = extract_label(before)

        if label and label_start_in_before is not None:
            existing = before[label_start_in_before:label_start_in_before + len(label)]
            if not existing.startswith('**'):
                bolded_before = (
                    before[:label_start_in_before]
                    + '**' + label + '**'
                    + before[label_start_in_before + len(label):]
                )
                result.append(bolded_before)
            else:
                result.append(before)
        else:
            result.append(before)

        result.append(m.group(0))
        prev_end = m.end()

    result.append(line[prev_end:])
    return ''.join(result)


def fix_file(path: Path) -> bool:
    text = path.read_text(encoding='utf-8')
    lines = text.splitlines(keepends=True)
    out = []
    in_frontmatter = False
    in_fence = False
    changed = False

    for i, line in enumerate(lines):
        stripped = line.rstrip('\n').rstrip('\r')

        # Front-matter
        if i == 0 and stripped == '---':
            in_frontmatter = True
            out.append(line)
            continue
        if in_frontmatter:
            out.append(line)
            if stripped == '---':
                in_frontmatter = False
            continue

        # Fenced code blocks
        if re.match(r'^\s{0,3}(`{3,}|~{3,})', stripped):
            in_fence = not in_fence
            out.append(line)
            continue
        if in_fence:
            out.append(line)
            continue

        # Skip table lines entirely
        if '|' in line:
            out.append(line)
            continue

        # Only touch lines containing a callout
        if not CALLOUT.search(line):
            out.append(line)
            continue

        new_line = bold_callouts_in_line(line)
        if new_line != line:
            changed = True
        out.append(new_line)

    if changed:
        path.write_text(''.join(out), encoding='utf-8')
        return True
    return False


def main():
    root = Path(__file__).parent.parent / 'docs'
    files = sorted(root.rglob('*.md'))
    includes = Path(__file__).parent.parent / '_includes'
    files += sorted(includes.rglob('*.md'))

    fixed = []
    for f in files:
        if fix_file(f):
            fixed.append(f)
            print(f'  fixed: {f.relative_to(root.parent.parent)}')
    if fixed:
        print(f'\n{len(fixed)} file(s) updated.')
    else:
        print('Nothing to change.')


if __name__ == '__main__':
    main()
