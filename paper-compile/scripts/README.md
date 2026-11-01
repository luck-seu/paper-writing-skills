# scripts/ — the state compiler (not yet built)

This directory will hold the skill's machinery: `compile.sh`, the
state compiler that regenerates the machine views into
`$PAPER_ROOT/.copilot/compiled/` and seeds the curated ledgers into
`$PAPER_ROOT/.copilot/ledgers/` (once, never overwritten), the
mechanical check scripts, and a self-test fixture suite under
`fixtures/`.

**Status: deliberately empty** (author instruction, 2026-11-01): the
framework — skill definition, artifact contracts, development
corpus — is being settled first; the compiler is derived from it
afterwards, not ported blindly. The references/ contracts define its
required behavior; the predecessor implementation lives in the MACRO repo
(`~/Workspace/research/MACRO`, `.claude/skills/academic-writing-copilot/
scripts/compile.sh`) and is consultable, but nothing is copied without
a stated reason (see the History section of the repo CLAUDE.md).

Planned shape (contract-first; all subject to the verdict rule):

- `compile.sh [view ...]` — views: notation, terminology, labels,
  todos, numbers; default all + ledger seeding. Unknown view →
  exit 2.
- Paper-root resolution: `PAPER_ROOT` env, else the CWD when it holds
  `paper.tex`, else die. The skill is a standalone package — no
  repo-relative derivation.
- Prose scope is layout-agnostic: `sections/**/*.tex` when a
  `sections/` dir exists, else flat root `*.tex` (the layout of the
  AMDB development corpus, linked as `test/amdb` in the sandbox),
  excluding `paper.tex` / `commands.tex` / `keywords.tex`.
- Missing sources are notes in the report, not errors; the `.tex`
  sources are always authoritative.
- Hardening carried over from the predecessor (proven by its disk-fill
  incident): `ulimit -f` write cap, temp-file registry with
  EXIT/HUP/INT/TERM traps, and the awk RSTART/RLENGTH snapshot
  discipline in every scan loop.
