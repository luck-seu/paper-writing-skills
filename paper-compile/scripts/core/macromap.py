"""The macro map: macro-source files parsed into definitions.

Part of the paper-compile state compiler (see scripts/README.md).
Macro sources are found by content, never by name (scan_file's
classification ruling below). Comment lines are excluded.
parse_commands_tex() returns every definition in document order --
callers decide last-wins vs first-wins per use; the list preserves
what the file actually says.
"""

from __future__ import annotations

import re
from typing import NamedTuple

from core import texscan
from core.copilot import note

_DEFINITION_MARKERS = (
    "newcommand{", "renewcommand{", "newcommand*{", "renewcommand*{",
    "DeclareMathOperator{", "DeclareMathOperator*{",
)
_NAME_RE = re.compile(r"\\[a-zA-Z]+\}")
_DEF_NAME_RE = re.compile(r"[a-zA-Z]+")
_N_ARGS_RE = re.compile(r"\[[0-9]+\]")
_PARAM_RE = re.compile(r"#[0-9]")


class Definition(NamedTuple):
    name: str
    takes_arg: bool
    body: str


def take_braced(text: str) -> tuple[str | None, str]:
    """text starts with '{': return (inner, remainder) at the matching '}'.

    A backslash escapes the next character (no depth change). Returns
    (None, text) when the brace never closes.
    """
    depth = 0
    k = 0
    while k < len(text):
        c = text[k]
        if c == "\\" and k + 1 < len(text):
            k += 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return text[1:k], text[k + 1:]
        k += 1
    return None, text


def _parse_definition(rest: str) -> tuple[str | None, bool | None, str | None, int]:
    """Scan rest for the earliest macro-definition marker.

    Returns (name, takes_arg, body, consumed). body is None when a name
    was recognized but no usable {body} followed (none written, or the
    brace never closes); the empty body {} is a real definition -- the
    macro expands to nothing (\\eat itself). name is None when no
    marker matched at all. consumed is how many characters of rest the
    definition spans; the caller must advance by at least one
    character regardless.
    """
    best, marker_len = -1, 0
    for marker in _DEFINITION_MARKERS:
        pos = rest.find("\\" + marker)
        if pos >= 0 and (best < 0 or pos < best):
            best, marker_len = pos, len(marker) + 1
    pos = rest.find("\\def\\")
    if pos >= 0 and (best < 0 or pos < best):
        best, marker_len = pos, len("\\def\\")
    if best < 0:
        return None, None, None, 0

    after = rest[best + marker_len:]
    if marker_len == 5:                                   # \def\name
        m = _DEF_NAME_RE.match(after)
        if not m:
            return None, None, None, best
        name, tail = m.group(), after[m.end():]
    else:                                                 # \newcommand{\name}
        m = _NAME_RE.match(after)
        if not m:
            return None, None, None, best
        name, tail = m.group()[1:-1], after[m.end():]

    n_args = 0
    if tail.startswith("["):
        m = _N_ARGS_RE.match(tail)
        if m:
            n_args, tail = int(m.group()[1:-1]), tail[m.end():]

    body = None
    if tail.startswith("{"):
        body, tail = take_braced(tail)   # None when the brace never closes

    consumed = len(rest) - len(tail)
    if body is None:
        return name, None, None, consumed
    takes_arg = n_args > 0 or bool(_PARAM_RE.search(body))
    return name, takes_arg, body, consumed


def parse_commands_tex(path: str) -> list[Definition]:
    """Macro definitions of one file, in document order."""
    lines = texscan.drop_comment_lines(texscan.read_lines(path))
    text = "".join(line + "\n" for line in lines)
    definitions = []
    rest = text
    while rest:
        name, takes_arg, body, consumed = _parse_definition(rest)
        if name and body is not None:
            definitions.append(
                Definition(name, bool(takes_arg),
                           body.replace("\t", " ").replace("\n", " "))
            )
        rest = rest[max(consumed, 1):]
    return definitions


# A line of pure LaTeX markup (never a prose sentence).
_MARKUP_LINE_RE = re.compile(r"[\\{}]")


def _brace_delta(line: str, depth: int) -> int:
    """Net brace depth change of line; a backslash escapes the next
    character (\\{ does not open a group)."""
    k = 0
    while k < len(line):
        c = line[k]
        if c == "\\":
            k += 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
        k += 1
    return depth


def swallow_names(definitions: list[Definition]) -> frozenset[str]:
    """Names whose live definition takes an argument the body never
    uses -- \\eat-style wrappers whose argument is content removed
    from the paper. Last live definition wins, as everywhere; a
    body that references any parameter (\\warn, \\revise) keeps its
    argument alive.
    """
    live: dict[str, Definition] = {}
    for definition in definitions:
        live[definition.name] = definition
    return frozenset(
        name for name, definition in live.items()
        if definition.takes_arg
        and not _PARAM_RE.search(definition.body))


def blank_swallowed(text: str, names: frozenset[str]) -> str:
    """Blank every \\name{arg} call of an argument-swallowing macro.

    The span (control sequence through the matching closing brace)
    becomes spaces; newlines survive, so line-based consumers keep
    their line structure. One braced argument only -- later
    arguments of a multi-arg swallow macro stay visible, the safe
    (under-blanking) direction. An unclosed brace is noted and left
    as-is.
    """
    if not names:
        return text
    pattern = re.compile(
        r"\\(?:" + "|".join(sorted(names)) + r")(?![a-zA-Z])\s*\{")
    out = list(text)
    for m in pattern.finditer(text):
        inner, rest = take_braced(text[m.end() - 1:])
        if inner is None:
            note("unclosed argument of a swallow macro -- left as-is")
            continue
        end = len(text) - len(rest)
        for k in range(m.start(), end):
            if out[k] != "\n":
                out[k] = " "
    return "".join(out)


def read_content(path: str, swallow: frozenset[str]) -> str:
    """A file's content text: comment-stripped, swallow-blanked.

    The single reader every prose-scanning view goes through --
    eaten content is removed once, for everyone.
    """
    text = "\n".join(
        texscan.strip_comment(line) for line in texscan.read_lines(path))
    return blank_swallowed(text, swallow)


def scan_file(path: str) -> tuple[list[Definition], bool]:
    """Definitions in file order + the macro-source verdict.

    A macro source is a preamble file by content, never by name:
    it holds at least one definition, and every non-comment line
    outside definition bodies is itself LaTeX markup (starts with
    \\, {, or }) -- a file that carries prose sentences is prose.
    The brace walk keeps multi-line definition bodies (and
    \\newenvironment blocks) off the line check.
    """
    definitions = parse_commands_tex(path)
    markup_only = bool(definitions)
    depth = 0
    for raw in texscan.read_lines(path):
        line = texscan.strip_comment(raw).strip()
        if not line:
            continue
        if depth == 0 and not _MARKUP_LINE_RE.match(line):
            markup_only = False
            break
        depth = max(_brace_delta(line, depth), 0)
    return definitions, markup_only
