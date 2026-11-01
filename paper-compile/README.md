# paper-compile

A Claude Code skill that tracks the **writing state** of a LaTeX
paper: its claims, notation, terminology, labels, numbers, and open
to-dos — through a small set of machine-compiled views plus curated
ledgers that the writing agent maintains together with the author.

This directory **is** the skill package (`SKILL.md` at its root),
living in the `paper-writing-skills` monorepo beside its siblings
`paper-scaffold/` (section scaffolding, an empty stub) and
`paper-init/` (venue bootstrap, an empty stub reserved for the
graduation-project student). It is the starting prototype of an
undergraduate graduation project (毕业设计); the plan is to extend
it, not to preserve it.

## What it does

While a paper is being written, facts drift: a symbol typed by hand
though a macro exists, a term spelled two ways, a headline number in
the abstract that no longer matches the table, a claim quietly
weakened by an edit. The skill's whole job is to make that drift
visible:

- **Machine views** (regenerated wholesale by the compiler,
  gitignored in the paper repo):
  - `notation.md` — math notation actually used; hand-typed
    duplicates of declared macros flagged
  - `terminology.md` — declared term macros and their use counts
  - `labels.md` — label/number/page index from the `.aux`, the
    assembly map, and a STALE stamp when sources are newer
  - `todos.md` — line-leading `TODO` / `! ` census
  - `numbers.md` — numeric-literal inventory with first-seen context
- **Curated ledgers** (seeded once, then maintained by the writing
  agent WITH the author; tracked in the paper repo):
  - `claims.md` — the claims that must survive; weakening one is an
    author-only decision
  - `dependencies.md` — the challenge ↔ section ↔ contribution ↔
    conclusion spine and number-sync invariants

Against a paper repo, state lands in `$PAPER_ROOT/.copilot/compiled/`
(views) and `$PAPER_ROOT/.copilot/ledgers/` (ledgers).

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
4. **Views are disposable, ledgers are durable.** Views regenerate
   wholesale; ledgers are seeded once and never overwritten.

See the skill `CLAUDE.md` for the extension roadmap and history, and
the monorepo root `CLAUDE.md` for repo-wide conventions.

## Status

Framework stage: the skill definition (`SKILL.md`), the artifact
contracts (`references/`), and the conventions (`CLAUDE.md`) are in
place, beside the `paper-scaffold/` and reserved `paper-init/`
stubs. The development
corpus is a real paper kept outside this repo (an svn-severed AMDB
copy, reachable in the gitignored `test/` sandbox). The state
compiler (`scripts/compile.sh`) is deliberately **not built yet** —
the framework is being settled first. A full-featured predecessor
lives in the MACRO repo; nothing is ported from it without a stated
reason.

## Layout

- `SKILL.md` — the skill: session loop + artifact ownership
- `references/` — one format contract per artifact (the interop API)
- `scripts/` — future home of the state compiler (README placeholder)
- `../paper-scaffold/` — the sibling section-scaffolding skill
  (empty stub)
- `../paper-init/` — the sibling venue-bootstrap skill (empty stub)
- `../test/` — gitignored local sandbox (installed-shape skill links
  + corpus pointer); development corpus itself lives outside the
  repo at `~/Workspace/program/AMDB`
