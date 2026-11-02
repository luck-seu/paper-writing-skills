"""The .copilot/ output side of the compiler plus shared diagnostics.

Part of the paper-compile state compiler (see scripts/README.md).
Views land in $PAPER_ROOT/.copilot/compiled/<name>.md, written via a
same-directory temp file renamed into place so an interrupted run
never leaves a half-written view behind.
"""

from __future__ import annotations

import contextlib
import os
import sys
import tempfile
from typing import Iterator


def note(message: str) -> None:
    print(f"compile.py: note: {message}", file=sys.stderr)


@contextlib.contextmanager
def atomic_write(path: str) -> Iterator[object]:
    """Write path via a same-directory temp file renamed into place."""
    directory = os.path.dirname(path)
    os.makedirs(directory, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=directory, prefix=".compile-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            yield handle
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def write_view(root: str, name: str, lines: list[str]) -> None:
    """Write one machine view and report it on stdout."""
    path = os.path.join(root, ".copilot", "compiled", name + ".md")
    with atomic_write(path) as out:
        out.write("\n".join(lines) + "\n")            # type: ignore[attr-defined]
    print(f"[compile] {name} -> .copilot/compiled/{name}.md ({len(lines)} lines)")
