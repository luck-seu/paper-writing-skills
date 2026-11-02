"""The notation machine view: math notation as actually used.

Part of the paper-compile state compiler (see scripts/README.md).
Rows are what the prose consumes, not what the macro sources
declare: the macro sources are a shared macro library inherited
across papers, so unused declarations are expected and never
listed.

Three classes never become rows -- they are not the paper's
notation:

- standard math symbols (STANDARD_SYMBOLS below: operators,
  relations, arrows, dots, delimiters, log-like names, named
  constants -- symbols whose meaning does not vary across papers);
- a font switch applied to two or more letters (\\mathit{type} --
  prose emphasis, not notation);
- \\kw{...} carrier macros -- terminology, the deferred sibling
  view.

A hand-typed standard symbol still reaches the duplicate section
when a declared macro expands to it: that is a typing-consistency
signal, independent of notation-hood.
"""

from __future__ import annotations

import collections
import os
import re
from typing import NamedTuple

from core import copilot, macromap
from core.mathmode import FONT_SWITCHES

# Control sequences that are structural LaTeX (or table/line noise)
# rather than notation of a mathematical object.
IGNORED_COMMANDS = frozenset((
    "begin", "end", "label", "ref", "eqref", "cite", "citep", "citet",
    "text", "textrm", "textsf", "texttt", "textbf", "textit", "textsc",
    "textnormal", "mbox", "ensuremath", "protect", "displaystyle",
    "xspace", "frac", "dfrac", "tfrac", "quad", "qquad", "hspace",
    "hskip", "vspace", "phantom", "hphantom", "vphantom", "left",
    "right", "big", "Big", "bigg", "Bigg", "bigl", "bigr", "nonumber",
    "notag", "hfill", "kw", "hline", "allowbreak",
))

STANDARD_SYMBOLS = frozenset((
    # relations
    "leq", "le", "geq", "ge", "neq", "ne", "equiv", "approx", "sim",
    "simeq", "cong", "propto", "prec", "preceq", "succ", "succeq",
    "ll", "gg", "subset", "subseteq", "supset", "supseteq",
    "sqsubset", "sqsubseteq", "in", "notin", "ni", "mid", "parallel",
    "perp", "models", "asymp", "doteq",
    # binary operators
    "pm", "mp", "times", "div", "cdot", "ast", "star", "circ",
    "bullet", "oplus", "ominus", "otimes", "oslash", "odot", "wedge",
    "vee", "land", "lor", "setminus", "cup", "cap", "sqcup", "sqcap",
    "uplus", "triangleleft", "triangleright",
    # big operators
    "sum", "prod", "coprod", "int", "iint", "iiint", "oint",
    "bigcup", "bigcap", "bigvee", "bigwedge", "bigoplus", "bigotimes",
    "bigodot", "bigsqcup",
    # arrows
    "to", "gets", "leftarrow", "rightarrow", "leftrightarrow",
    "Leftarrow", "Rightarrow", "Leftrightarrow", "longleftarrow",
    "longrightarrow", "longleftrightarrow", "mapsto", "longmapsto",
    "hookrightarrow", "hookleftarrow", "uparrow", "downarrow",
    "updownarrow", "Uparrow", "Downarrow", "Updownarrow",
    "rightleftharpoons", "rightharpoonup", "rightharpoondown",
    "leftharpoonup", "leftharpoondown", "leadsto", "nearrow",
    "searrow", "swarrow", "nwarrow",
    # dots and punctuation
    "ldots", "cdots", "vdots", "ddots", "dots", "dotsb", "dotsc",
    "dotsi", "dotsm", "dotso", "colon",
    # delimiters
    "langle", "rangle", "lceil", "rceil", "lfloor", "rfloor", "vert",
    "Vert", "lvert", "rvert", "lVert", "rVert",
    # log-like operator names
    "log", "ln", "lg", "exp", "sin", "cos", "tan", "cot", "sec",
    "csc", "arcsin", "arccos", "arctan", "sinh", "cosh", "tanh",
    "coth", "arg", "det", "dim", "ker", "deg", "gcd", "hom", "Pr",
    "sup", "inf", "max", "min", "lim", "liminf", "limsup",
    # named constants
    "infty", "aleph", "hbar", "ell", "emptyset", "varnothing",
    "partial", "nabla", "angle", "prime", "top", "bot",
))

_DECORATION_RE = re.compile(r"\\protect|\\xspace|\\ensuremath|\\displaystyle")
_FILLER_RE = re.compile(r"[{} \t]")
_CONTROL_SEQ_RE = re.compile(r"\\[a-zA-Z]+")
_FONT_ONE_LETTER_RE = re.compile(r"\\[a-zA-Z]+[ ]?[A-Za-z0-9]$")

# A font switch applied to a word: prose emphasis (or a term), not a
# notation symbol. Single letters (\mathcal{M}) stay notation.
_FONT_WORD_RE = re.compile(
    r"\\(?:" + "|".join(sorted(FONT_SWITCHES)) + r")\{[A-Za-z]{2,}\}"
)


def norm_key(s: str) -> str:
    """Comparison key: decorations stripped, braces and spaces erased."""
    return _FILLER_RE.sub("", _DECORATION_RE.sub("", s))


def display_norm(s: str) -> str:
    """Display form: unwrap one outer brace pair; brace a font switch's
    single letter so \\mathcal M and \\mathcal{M} render identically."""
    t = _DECORATION_RE.sub("", s).strip(" \t")
    if t.startswith("{") and t.endswith("}"):
        depth = 0
        k = 0
        unwrapped = False
        while k < len(t):
            c = t[k]
            if c == "\\" and k + 1 < len(t):
                k += 2
                continue
            if c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    unwrapped = k == len(t) - 1
                    break
            k += 1
        if unwrapped:
            t = t[1:-1].strip(" \t")
    if "{" not in t and "}" not in t and _FONT_ONE_LETTER_RE.match(t):
        command = re.sub(r"[ ]?[A-Za-z0-9]$", "", t)
        if command[1:] in FONT_SWITCHES:
            t = f"{command}{{{t[-1]}}}"
    return t


class Row(NamedTuple):
    display: str
    form: str
    first: str


def build_notation_rows(
    definitions: list[macromap.Definition],
    tokens: list[tuple[str, str]],
) -> tuple[dict[tuple[str, str], Row], collections.Counter]:
    """Fold the token stream into table rows, keyed for the row
    classes (dict insertion order == first-appearance order):

    - macro-arg: a used macro that takes arguments        (main table)
    - expansion: a used zero-arg macro, keyed by body     (main table)
    - duplicate: hand-typed token a declared macro already covers
    - hand-typed: everything else                          (main table)
    """
    body_of = {d.name: d.body for d in definitions}       # last def wins
    arg_of = {d.name: d.takes_arg for d in definitions}
    expansion_owner: dict[str, str] = {}                  # first def wins
    for d in definitions:
        if not d.takes_arg and d.body:
            key = norm_key(d.body)
            if key and key not in expansion_owner:
                expansion_owner[key] = d.name

    rows: dict[tuple[str, str], Row] = {}
    counts: collections.Counter = collections.Counter()

    for base, token in tokens:
        m = _CONTROL_SEQ_RE.match(token)
        if not m:
            continue
        cs = m.group()[1:]
        if cs in IGNORED_COMMANDS:
            continue
        if _FONT_WORD_RE.fullmatch(token):
            continue                      # \mathit{type}: prose emphasis
        key = None
        if cs in STANDARD_SYMBOLS:
            # Not this paper's notation -- but a hand-typed standard
            # symbol that a declared macro already prints is still a
            # typing-consistency signal.
            token_key = norm_key(token)
            if token_key in expansion_owner:
                key = ("duplicate", token_key)
                if key not in rows:
                    rows[key] = Row(token, expansion_owner[token_key], "")
        elif body_of.get(cs):
            if "\\kw{" in body_of[cs]:
                continue                  # terminology carrier, not notation
            if arg_of[cs]:
                key = ("macro-arg", cs)
                if key not in rows:
                    rows[key] = Row(token, f"macro \\{cs}", base)
            else:
                lead = _CONTROL_SEQ_RE.match(body_of[cs])
                if lead and lead.group()[1:] in STANDARD_SYMBOLS:
                    continue              # e.g. \ra -> \rightarrow
                key = ("expansion", norm_key(body_of[cs]))
                if key not in rows:
                    rows[key] = Row(display_norm(body_of[cs]), f"macro \\{cs}", base)
        else:
            token_key = norm_key(token)
            if token_key in expansion_owner:
                key = ("duplicate", token_key)
                if key not in rows:
                    rows[key] = Row(token, expansion_owner[token_key], "")
            else:
                key = ("hand-typed", token_key)
                if key not in rows:
                    rows[key] = Row(token, "hand-typed", base)
        if key is not None:
            counts[key] += 1
    return rows, counts


def render_notation(
    rows: dict[tuple[str, str], Row],
    counts: collections.Counter,
    prose_count: int,
    stamp: str,
) -> list[str]:
    lines = [
        f"<!-- Machine view. Generated by compile.py at {stamp} from a scan",
        "     of math-mode notation actually used in the prose files (inline",
        "     $...$, \\(...\\), \\[...\\], display environments; comments stripped),",
        "     mapped against the macro sources (files the map classifies",
        "     as macros). A declared macro that is never used",
        "     does not reach the main table. REGENERATE: python3 scripts/compile.py.",
        "     The .tex sources are authoritative. -->",
        "",
        "# Notation (as used in the paper)",
        "",
    ]
    if not rows:
        lines.append(f"(no math-mode tokens found in {prose_count} prose files)")
        lines.append("")
    else:
        lines.append("| Notation | Form | Uses | First used in |")
        lines.append("|---|---|---|---|")
        for key, row in rows.items():
            if key[0] == "duplicate":
                continue
            lines.append(
                f"| `{row.display}` | {row.form} | {counts[key]} | {row.first} |"
            )
        lines.append("")
        duplicates = [(k, r) for k, r in rows.items() if k[0] == "duplicate"]
        if duplicates:
            lines.append("## Hand-typed duplicates of declared macros")
            lines.append("")
            for key, row in duplicates:
                lines.append(
                    f"- `{row.display}` hand-typed {counts[key]}x; macro"
                    f" `\\{row.form}` already declares it -- use the macro"
                )
            lines.append("")
    lines += [
        "## Scan limits",
        "",
        "- Bare letters (variables with no control sequence) are not tokenized.",
        "- A token swallows its own single, simple braced argument; a font",
        "  switch (\\mathcal etc.) additionally swallows one unbraced letter.",
        "- Not notation, never tabled: standard math symbols (operators,",
        "  relations, arrows, dots, delimiters, log-like names, named",
        "  constants -- the fixed list in the script); a font switch applied",
        "  to two or more letters (\\mathit{type}, prose emphasis); and",
        "  \\kw{...} carrier macros (terminology, a deferred view). A",
        "  hand-typed standard symbol still reaches the duplicate section",
        "  when a macro declares it.",
        "- begin/end lines inside a display environment are approximations.",
        "- Argument-swallowing macros (\\eat-style: a declared argument",
        "  the body never uses) are blanked before scanning -- eaten",
        "  content is not usage.",
        "- Comment lines are excluded; escaped-\\% parity and trailing comments",
        "  are heuristics.",
        "- The macro map is every macro-source file (content-classified;",
        "  see file_map.md), comment lines excluded, last live",
        "  definition wins.",
    ]
    return lines


def compile_notation(
    root: str,
    definitions: list[macromap.Definition],
    tokens: list[tuple[str, str]],
    prose_count: int,
    stamp: str,
) -> None:
    rows, counts = build_notation_rows(definitions, tokens)
    copilot.write_view(
        root, "notation", render_notation(rows, counts, prose_count, stamp)
    )
