# paper-compile

A Claude Code skill that tracks the **writing state** of a LaTeX
paper through machine-compiled views — this round: the file map
(assembly order, file roles, headings) and the math notation as
actually used. Further views and curated ledgers arrive in later
build rounds, contract-first.

This directory **is** the skill package (`SKILL.md` at its root),
living in the `paper-writing-skills` monorepo beside its siblings
`paper-scaffold/` (section scaffolding, an empty stub) and
`paper-init/` (venue bootstrap, an empty stub reserved for the
graduation-project student). It is the starting prototype of an
undergraduate graduation project (毕业设计); the plan is to extend
it, not to preserve it.

## What it does

While a paper is being written, facts drift: a section moved to
another file, a file written but not yet `\input`, a symbol typed by
hand though a macro exists. The skill's whole job is to make that
drift visible:

- **Machine views** (regenerated wholesale by the compiler,
  gitignored in the paper repo):
  - `file_map.md` — file map: assembly order, file roles (classified
    by content, not name), headings per file, prose not yet included
    (the artifact other skills reference)
  - `notation.md` — math notation actually used; hand-typed
    duplicates of declared macros flagged

Further views (terminology, labels, todos, numbers) and curated
ledgers are planned; their contracts land with the artifacts, not
before.

Against a paper repo, state lands in `$PAPER_ROOT/.copilot/compiled/`
(views).

## Design principles

1. **Minimality — the mechanical layer of writing state.** Machine
   views and machine checks in the core; judgment (style, venue,
   claim-hood) lives with the author, the ledgers, or the sibling
   `paper-init` skill.
2. **Pull-to-upgrade.** The skill is a self-contained package with
   no target-repo-specific content; consumers upgrade by pulling
   this repo (symlinked installs track the working tree live).
3. **The verdict rule.** A script may own an artifact only when its
   output is a mechanical function of its sources (extract, count,
   look up). Judgment belongs to ledgers maintained with the author.
4. **Views are disposable.** Views regenerate wholesale; curated
   ledgers, when they arrive, are seeded once and never overwritten.

See the skill `CLAUDE.md` for the extension roadmap and history, and
the monorepo root `CLAUDE.md` for repo-wide conventions.

## Status

Framework stage: the skill definition (`SKILL.md`), the artifact
contracts (`references/`), and the conventions (`CLAUDE.md`) are in
place, beside the `paper-scaffold/` and reserved `paper-init/`
stubs. The development
corpus is a real paper kept outside this repo (an svn-severed AMDB
copy, reachable in the gitignored `test/` sandbox). The state
compiler's first cut (`scripts/compile.py`, an entry point over
`core/` machinery and `views/` modules, Python standard library
only) is built and trimmed to the simplest set: the `file_map` and
`notation` views, verified against the corpus; the remaining views
and ledger seeding are deferred contract-first (see
`scripts/README.md`). A
full-featured predecessor lives in the MACRO repo; nothing is
ported from it without a stated reason.

## Layout

- `SKILL.md` — the skill: session loop + artifact ownership
- `references/` — one format contract per artifact (the interop API)
- `scripts/` — the state compiler: `compile.py` (entry) +
  `core/` + `views/` modules
- `../paper-scaffold/` — the sibling section-scaffolding skill
  (empty stub)
- `../paper-init/` — the sibling venue-bootstrap skill (empty stub)
- `../test/` — gitignored local sandbox (installed-shape skill links
  + corpus pointer); development corpus itself lives outside the
  repo at `~/Workspace/program/AMDB`
