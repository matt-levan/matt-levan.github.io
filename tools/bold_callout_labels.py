#!/usr/bin/env python3
"""
Bold the UI element label associated with each callout marker like (A), (B), etc.

Two sentence patterns exist in these lab guides:

BACKWARD pattern — label precedes callout:
  click the Quick create (A) (the icon…)
  clicking on the Services (A) menu item
  selecting the Installed Operators (B) sub-item
  click the Create StorageSystem (A) button
  click on the Next (B) button
  the local-cluster drop-down list (A)
  with Username (A): admin

FORWARD pattern — callout leads the sentence fragment:
  (C) Next, type the word Fusion Data Foundation in the Search field
  (A) Enter ibm-spectrum-fusion-local in the LocalVolumeSet name field
  (B) Enter filebrowser in the Name text entry field

For the forward pattern, the label is the first proper-noun/name phrase
immediately after the callout (before the verb that follows it).

Lines inside fenced code blocks, front-matter, or markdown tables are skipped.
Already-bolded spans are not re-processed.
"""
import re
from pathlib import Path

CALLOUT = re.compile(r'\(([A-Z])\)')

# ── BACKWARD WALK ─────────────────────────────────────────────────────────────

# Action verbs that PRECEDE a UI label in the backward walk.
# NOTE: "create", "expand", "enable", "disable", "assign", "install",
# "configure", "import", "export" are intentionally NOT here because they
# appear as button/tile names that need bolding.
VERB_STOPS_BACK = {
    'click', 'clicks', 'clicked', 'clicking',
    'select', 'selects', 'selected', 'selecting',
    'navigate', 'navigating',
    'enter', 'entering', 'entered',
    'type', 'types', 'typed', 'typing',
    'choose', 'choosing',
    'close', 'closing',
    'check', 'checking',
    'uncheck', 'unchecking',
    'verify', 'verifying',
    'use', 'using',
    'set', 'sets', 'setting',
    'leave', 'leaving',
    'wait', 'waiting',
    'scroll', 'scrolling',
    'paste', 'pasting',
    'copy', 'copying',
    'delete', 'deleting',
    'repeat',
}

# Prepositions / conjunctions that signal a phrase boundary mid-walk.
BOUNDARY_PREPS_BACK = {
    'into', 'onto', 'with', 'from', 'of', 'in', 'through', 'between',
    'against', 'within', 'throughout', 'beyond', 'past', 'toward',
    'inside', 'outside', 'along', 'upon', 'across', 'after', 'before',
    'under', 'below', 'above', 'over', 'around', 'near', 'beside',
    'except', 'despite', 'regarding', 'concerning',
    'and', 'or',
}

# Leading stopwords trimmed from the FRONT of the collected label.
LEADING_STOPS = {
    'the', 'a', 'an', 'on', 'by', 'for', 'as', 'at',
    'that', 'this', 'which', 'each',
    'also', 'finally', 'to',
}

# Hard-stop characters — stop collection immediately.
HARD_STOP_CHARS = set('.,;:\n(|')

# Generic context nouns — never a UI element name by themselves.
GENERIC_NOUNS = {
    'contents', 'content', 'section', 'pane', 'window', 'page',
    'area', 'view', 'screen',
    'item', 'items', 'text', 'information', 'info',
    'summary', 'table', 'row', 'column',
    'step', 'steps', 'process', 'procedure',
}


def extract_label_backward(text_before: str) -> tuple[str, int] | tuple[None, None]:
    """
    Walk backwards from the callout to find the UI label that precedes it.
    Returns (label_string, start_pos_in_text_before) or (None, None).
    """
    s = text_before.rstrip()
    if not s:
        return None, None

    word_tokens = [(m.group(), m.start(), m.end()) for m in re.finditer(r'\S+', s)]
    if not word_tokens:
        return None, None

    label_tokens: list[tuple[str, int, int]] = []

    for tok, tok_start, tok_end in reversed(word_tokens):
        core = tok.rstrip('.,;:')
        core_lower = core.lower()

        # Hard-stop char at token start
        if tok[0] in HARD_STOP_CHARS or tok[0] == '>':
            break
        # Verb stop
        if core_lower in VERB_STOPS_BACK:
            break
        # Boundary preposition
        if core_lower in BOUNDARY_PREPS_BACK:
            break
        # Generic noun
        if core_lower in GENERIC_NOUNS:
            break
        # Hard-stop char in token body
        if any(c in HARD_STOP_CHARS for c in tok[1:]):
            break
        # Already bolded
        if tok.startswith('**') or tok.endswith('**'):
            break
        # Bare markdown symbols
        if tok in ('*', '_', '__', '***'):
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

    label_start = label_tokens[0][1]
    label_end   = label_tokens[-1][2]
    label = s[label_start:label_end].rstrip('.,;:')
    if not label:
        return None, None

    return label, label_start


# ── FORWARD WALK ──────────────────────────────────────────────────────────────

# After a sentence-start callout like "(C) Next, type the word FOO in the …"
# we bold the name FOO.  The label starts after the first verb that follows the
# callout and ends before a preposition/article/verb.

# Verbs that come right after the callout in the forward direction.
INTRO_VERBS_FWD = {
    'enter', 'type', 'click', 'select', 'navigate',
    'paste', 'copy', 'use', 'next', 'then',
}

# Words that end the forward label scan.
BOUNDARY_FWD = {
    'in', 'into', 'on', 'at', 'to', 'from', 'of', 'for', 'with',
    'and', 'or', 'the', 'a', 'an',
    'text', 'field', 'box', 'button', 'menu', 'tab', 'tile',
    'item', 'pane', 'page', 'screen', 'entry', 'window',
}


def extract_label_forward(text_after: str) -> str | None:
    """
    From text that follows a sentence-start callout, extract the label.
    E.g. " Next, type the word Fusion Data Foundation in the Search field"
    → "Fusion Data Foundation"
    """
    # Strip leading space/comma
    s = text_after.lstrip(' ,')
    if not s:
        return None

    words = re.findall(r'\S+', s)
    if not words:
        return None

    # Skip the intro verb(s) at the start
    i = 0
    while i < len(words):
        w = words[i].lower().rstrip('.,;:')
        if w in INTRO_VERBS_FWD:
            i += 1
        else:
            break

    # Skip filler phrases like "the word", "the value"
    FILLERS = {'the', 'a', 'an', 'word', 'value', 'following', 'text'}
    while i < len(words) and words[i].lower().rstrip('.,;:') in FILLERS:
        i += 1

    if i >= len(words):
        return None

    # Collect the label: stop at boundary words, punctuation, or 5 words
    label_words = []
    while i < len(words) and len(label_words) < 5:
        w = words[i]
        core = w.rstrip('.,;:')
        if core.lower() in BOUNDARY_FWD:
            break
        if w[0] in '.,;:(':
            break
        # Stop if we hit an already-bolded span or a pure function word
        if w.startswith('**'):
            break
        label_words.append(core)
        i += 1

    if not label_words:
        return None

    return ' '.join(label_words)


# ── LINE PROCESSOR ────────────────────────────────────────────────────────────

def bold_callouts_in_line(line: str) -> str:
    """
    Process all callouts in a line left-to-right.

    For each (X) callout:
    - Try backward: bold the label preceding it.
    - Else if it starts the sentence/list-item, try forward: bold the label
      following it, then recurse on the rest of the line so remaining callouts
      (e.g. a (B) later on the same line) are also processed.
    """
    result: list[str] = []
    prev_end = 0

    for m in CALLOUT.finditer(line):
        start = m.start()
        before = line[prev_end:start]
        after  = line[m.end():]

        # ── Backward pattern ──────────────────────────────────────────────
        label, label_start = extract_label_backward(before)

        if label and label_start is not None:
            existing = before[label_start:label_start + len(label)]
            if not existing.startswith('**'):
                bolded_before = (
                    before[:label_start]
                    + '**' + label + '**'
                    + before[label_start + len(label):]
                )
                result.append(bolded_before)
            else:
                result.append(before)
        else:
            # ── Forward pattern ───────────────────────────────────────────
            stripped_before = before.strip().rstrip('1234567890. ').strip()
            is_sentence_start = (stripped_before == '' or stripped_before == '(')

            if is_sentence_start:
                fwd_label = extract_label_forward(after)
                if fwd_label and fwd_label.strip():
                    escaped = re.escape(fwd_label)
                    new_after, n = re.subn(
                        r'(?<!\*\*)(?<!\*)(' + escaped + r')(?!\*)(?!\*\*)',
                        r'**\1**',
                        after,
                        count=1,
                    )
                    # Emit prefix + callout, then recurse on the rest
                    result.append(before)
                    result.append(m.group(0))
                    result.append(bold_callouts_in_line(new_after))
                    return ''.join(result)
                else:
                    result.append(before)
            else:
                result.append(before)

        result.append(m.group(0))
        prev_end = m.end()

    result.append(line[prev_end:])
    return ''.join(result)


# ── FILE PROCESSOR ────────────────────────────────────────────────────────────

def fix_file(path: Path) -> bool:
    text = path.read_text(encoding='utf-8')
    lines = text.splitlines(keepends=True)
    out: list[str] = []
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

        # Table rows
        if '|' in line:
            out.append(line)
            continue

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
