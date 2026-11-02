#!/usr/bin/env python3
"""compile.py -- the paper-compile state compiler: entry point.

Builds the machine views into $PAPER_ROOT/.copilot/compiled/.
Views this round: file_map, notation. Later build rounds add views
(terminology, labels, todos, numbers) contract-first -- the
contract lands with the artifact; the CLI knows only the built set.

The implementation lives in two packages: core/ (view-agnostic
machinery, one job per module -- texscan, mathmode, macromap,
copilot) and views/ (one module per machine view -- file_map,
notation). Bare-name scripts at this level are the only public
interfaces; core/ and views/ modules are import-only.

Pipeline (author ruling, 2026-11-02): map first -- discovery and
content classification (macro source vs prose) precede the views.
No corpus file name is hardcoded; commands.tex / keywords.tex
style names are found by scanning, never assumed.

Language ruling (author, 2026-11-02): Python, standard library
only, Python >= 3.9. Readability is part of the contract -- the
verdict rule grants a script an artifact only as a mechanical
function of its sources, and the author must be able to audit it.

Contracts: references/ (one per built view). The .tex sources are
always authoritative; views regenerate wholesale.

Usage: python3 compile.py [view ...]     (default: every view)
       PAPER_ROOT=path/to/paper python3 compile.py [view ...]
Exit:  0 ok, 1 fatal, 2 unknown view name.
"""

from __future__ import annotations

import datetime
import os
import signal
import sys

from core import macromap, mathmode, texscan
from views import file_map, notation

VIEWS = ("file_map", "notation")


def die(message: str) -> None:
    print(f"compile.py: error: {message}", file=sys.stderr)
    sys.exit(1)


def die2(message: str) -> None:
    print(f"compile.py: error: {message}", file=sys.stderr)
    sys.exit(2)


# --- hardening (carried over from the predecessor's disk-fill incident)


def limit_write_size() -> None:
    """Cap any single file this process writes; views are KB-scale."""
    cap = 4 * 1024 * 1024
    try:
        import resource
        resource.setrlimit(resource.RLIMIT_FSIZE, (cap, cap))
    except (ImportError, OSError, ValueError):
        pass


def _raise_exit(signum: int, _frame: object) -> None:
    raise SystemExit(1)


def install_signal_exits() -> None:
    """HUP/TERM unwind through the finally blocks (temp cleanup)."""
    for name in ("SIGHUP", "SIGTERM"):
        sig = getattr(signal, name, None)
        if sig is not None:
            signal.signal(sig, _raise_exit)


def resolve_root() -> str:
    """PAPER_ROOT env, else the CWD when it holds paper.tex, else die."""
    env = os.environ.get("PAPER_ROOT", "")
    if env:
        if not os.path.isfile(os.path.join(env, "paper.tex")):
            die(f"PAPER_ROOT='{env}' holds no paper.tex")
        root = env
    elif os.path.isfile("paper.tex"):
        root = "."
    else:
        die(f"no PAPER_ROOT set and no paper.tex in {os.getcwd()}")
    return os.path.abspath(root)


def parse_args(argv: list[str]) -> list[str]:
    """Requested views, first-occurrence order; default: every view."""
    want: list[str] = []
    for arg in argv:
        if arg not in VIEWS:
            die2(f"unknown view '{arg}' (known: {' '.join(VIEWS)})")
        if arg not in want:
            want.append(arg)
    return want or list(VIEWS)


def main(argv: list[str]) -> int:
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%SZ")

    limit_write_size()
    install_signal_exits()

    root = resolve_root()
    inventory = texscan.discover_tex(root)
    if not inventory:
        die(f"no .tex files found under '{root}'")
    assembly = texscan.assembly_order(root, inventory)

    # Map scan first (author ruling, 2026-11-02): discovery + content
    # classification (macro source vs prose) precede the views. Later
    # stages and the persisted file_map.md read these results; no
    # corpus file name is hardcoded anywhere.
    scans = {
        path: macromap.scan_file(os.path.join(root, path))
        for path, _mentioned in assembly
    }
    macro_files = {
        path for path, (_defs, is_macro) in scans.items() if is_macro}
    def_counts = {path: len(scans[path][0]) for path in macro_files}
    definitions = [
        definition
        for path, _mentioned in assembly
        for definition in scans[path][0]
    ]
    prose = [(path, mentioned) for path, mentioned in assembly
             if path not in macro_files]
    if not prose:
        die(f"no prose .tex files found under '{root}'")

    # \\eat-style wrappers: a declared argument the live body never
    # uses. Their calls are blanked before any prose scan, so removed
    # content is not usage, not a heading, not anything.
    swallow = macromap.swallow_names(definitions)

    order = [path for path, _mentioned in prose]
    tokens = mathmode.collect_tokens(root, order, swallow)

    for view in parse_args(argv):
        if view == "file_map":
            file_map.compile_file_map(
                root, assembly, macro_files, def_counts, swallow, stamp)
        elif view == "notation":
            notation.compile_notation(root, definitions, tokens, len(order), stamp)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
