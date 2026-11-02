"""Math-mode extraction and control-sequence tokenization.

Part of the paper-compile state compiler (see scripts/README.md).
extract_math() segments everything LaTeX treats as math -- inline
$...$ (multi-line included), \\(...\\), \\[...\\], and the interior
of display environments -- into (document_offset, segment) pairs;
iter_tokens() turns a segment into notation-grade tokens.

Offsets stay comparable across math kinds: extracted spans are
blanked with spaces, never cut, so every segment keeps its document
position and the notation table is true reading order.
"""

from __future__ import annotations

import os
import re
from typing import Iterator

from core import macromap, texscan
from core.copilot import note

DISPLAY_ENVIRONMENTS = (
    "equation", "align", "gather", "eqnarray", "displaymath", "math",
)

# A font switch takes exactly one token in LaTeX: \mathcal M and
# \mathcal{M} are the same notation, so the tokenizer normalizes the
# unbraced form to the braced one.
FONT_SWITCHES = frozenset((
    "mathcal", "mathbb", "mathrm", "mathsf", "mathit", "mathbf",
    "mathtt", "cal", "frak", "scr",
))

_CONTROL_SEQ_RE = re.compile(r"\\[a-zA-Z]+")
_BRACED_ARG_RE = re.compile(r"\{[^{}]*\}")
_UNBRACED_LETTER_RE = re.compile(r"[ ]?[A-Za-z0-9]")


def extract_math(base: str, text: str) -> list[tuple[int, str]]:
    """All math segments of one file as (document_offset, segment),
    sorted by offset (stable, so equal offsets keep emission order)."""
    segments: list[tuple[int, str]] = []

    def blank_spans(begin: str, end: str) -> None:
        nonlocal text
        while True:
            b = text.find(begin)
            if b < 0:
                return
            after = text[b + len(begin):]
            e = after.find(end)
            if e < 0:
                return
            segments.append((b, after[:e]))
            blanked = " " * (len(begin) + e + len(end))
            text = text[:b] + blanked + after[e + len(end):]

    for env in DISPLAY_ENVIRONMENTS:
        blank_spans("\\begin{" + env + "}", "\\end{" + env + "}")
        blank_spans("\\begin{" + env + "*}", "\\end{" + env + "*}")
    blank_spans("\\[", "\\]")
    blank_spans("\\(", "\\)")

    # Inline $...$: a backslash escapes the next character (so \$ never
    # toggles), and a segment may span lines (they were joined by spaces).
    piece: list[str] = []
    open_at, is_open = 0, False
    i = 0
    while i < len(text):
        c = text[i]
        if c == "\\":
            if is_open:
                piece.append(text[i:i + 2])
            i += 2
            continue
        if c == "$":
            if is_open:
                content = "".join(piece)
                if content:
                    segments.append((open_at, content))
                is_open, piece = False, []
            else:
                is_open, open_at, piece = True, i, []
            i += 1
            continue
        if is_open:
            piece.append(c)
        i += 1
    if is_open:
        note(f"unbalanced $ in {base} -- unterminated inline math dropped")

    segments.sort(key=lambda pair: pair[0])
    return segments


def iter_tokens(segment: str) -> Iterator[str]:
    """Yield control-sequence tokens left to right.

    A token swallows its own single, simple braced argument
    (\\at{Application} stays one token); a font switch additionally
    swallows one unbraced letter (\\mathcal M -> \\mathcal{M}).
    """
    s = segment
    while True:
        m = _CONTROL_SEQ_RE.search(s)
        if not m:
            return
        token = m.group()
        rest = s[m.end():]
        m2 = _BRACED_ARG_RE.match(rest)
        if m2:
            token += m2.group()
            s = rest[m2.end():]
        elif token[1:] in FONT_SWITCHES and _UNBRACED_LETTER_RE.match(rest):
            lead = 2 if rest.startswith(" ") else 1
            token = f"{token}{{{rest[lead - 1]}}}"
            s = rest[lead:]
        else:
            s = rest
        yield token


def collect_tokens(
    root: str, order: list[str], swallow: frozenset[str] = frozenset()
) -> list[tuple[str, str]]:
    """(section base, token) for every math token, in reading order.

    Files are read through macromap.read_content: comment-stripped
    and swallow-blanked, so \\eat-style removed content never
    reaches the math scan.
    """
    tokens = []
    for path in order:
        base = texscan.section_base(path)
        text = macromap.read_content(os.path.join(root, path), swallow)
        for _pos, segment in extract_math(base, text):
            for token in iter_tokens(segment):
                tokens.append((base, token))
    return tokens
