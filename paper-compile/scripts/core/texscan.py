"""Reading the paper's .tex sources.

Part of the paper-compile state compiler (see scripts/README.md).
The .tex sources are always authoritative; this module only reads
them: comment stripping, .tex discovery (layout-agnostic, no
hardcoded file names -- roles are classified by content in
macromap), and the \\input reading order of the root tex.
"""

from __future__ import annotations

import os
import re

_INPUT_MARKER_RE = re.compile(r"\\(input|include)\{")
_LINE_COMMENT_RE = re.compile(r"[ \t]*%")


def read_lines(path: str) -> list[str]:
    with open(path, encoding="utf-8", errors="replace") as handle:
        return [line.rstrip("\n") for line in handle]


def strip_comment(line: str) -> str:
    """Drop everything from the first unescaped %.

    An odd run of backslashes before the % (\\%) marks a literal
    percent sign; an even run marks a comment.
    """
    i = line.find("%")
    while i >= 0:
        backslashes = 0
        j = i - 1
        while j >= 0 and line[j] == "\\":
            backslashes += 1
            j -= 1
        if backslashes % 2 == 0:
            return line[:i]
        i = line.find("%", i + 1)
    return line


def drop_comment_lines(lines: list[str]) -> list[str]:
    """Whole comment lines only (leading whitespace allowed)."""
    return [line for line in lines if not _LINE_COMMENT_RE.match(line)]


def discover_tex(root: str) -> list[str]:
    """Every .tex file of the paper as root-relative paths, sorted,
    except paper.tex (the root itself).

    Layout-agnostic: root-level *.tex plus a sections/ tree when
    one exists. Whether a file is a macro source or prose is
    decided later by content (macromap.scan_file), never by name.
    """
    found = set()
    for name in os.listdir(root):
        if (name.endswith(".tex") and name != "paper.tex"
                and os.path.isfile(os.path.join(root, name))):
            found.add(name)
    sections = os.path.join(root, "sections")
    if os.path.isdir(sections):
        for dirpath, _dirnames, filenames in os.walk(sections):
            for name in filenames:
                if name.endswith(".tex"):
                    rel = os.path.relpath(os.path.join(dirpath, name), root)
                    found.add(rel.replace(os.sep, "/"))
    return sorted(found)


def assembly_order(root: str, files: list[str]) -> list[tuple[str, bool]]:
    """The assembly: files as (path, mentioned) pairs.

    Order = \\input order of paper.tex (the reading order); files
    not mentioned by paper.tex append after, sorted, marked False
    -- they are work-in-progress, not yet assembled.
    """
    inputs = []
    for line in read_lines(os.path.join(root, "paper.tex")):
        if _INPUT_MARKER_RE.search(line):
            name = re.sub(r".*\\(?:input|include)\{", "", line)
            name = re.sub(r"\}.*", "", name)
            inputs.append(name)
    remaining = list(files)
    assembly: list[tuple[str, bool]] = []
    for name in inputs:
        for j, path in enumerate(remaining):
            if path == name + ".tex" or path.endswith("/" + name + ".tex"):
                assembly.append((remaining.pop(j), True))
                break
    return assembly + [(path, False) for path in remaining]


def section_base(path: str) -> str:
    """'sections/2_method/method.tex' -> 'method'."""
    base = path.rsplit("/", 1)[-1]
    return base[:-4] if base.endswith(".tex") else base
