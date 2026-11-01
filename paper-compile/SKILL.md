---
name: paper-compile
description: Track the writing state of a LaTeX paper — claims, notation/symbols, terminology, labels, numbers, todo markers — through a machine-compiled view set plus curated ledgers, with mechanical checks over the sources. Use when writing or editing any section of such a paper, when asked what a symbol/term/number is or where a claim lives, or when onboarding to a paper repo that ships the .copilot/ state layout. Mechanical layer only; style and venue rules are read from the target repo or the paper-init skill when present.
---

# paper-compile

You are the writer's peer and record-keeper. The skill tracks WHAT the
paper says (state); the target repo's own conventions govern HOW prose
is written. Two rules follow: never invent state, and never lose a
ruling.

## Session loop

1. **Compile**: run `scripts/compile.sh` (from this skill) with
   `PAPER_ROOT=<paper root>` (or from inside the paper root). It
   regenerates the machine views into
   `$PAPER_ROOT/.copilot/compiled/` and seeds the ledgers into
   `$PAPER_ROOT/.copilot/ledgers/` on first run only.
2. **Load state**: read every view plus every ledger before touching
   prose. The views are the shared factual baseline (which symbol
   macro exists, how often a term is used, where a number first
   appears, which labels resolve). If `labels.md` stamps STALE,
   rebuild the paper and recompile before trusting page numbers.
3. **Write or edit** one section at a time, in place, following the
   target repo's conventions (its `CLAUDE.md`, style guide, rules —
   read them if present; work without them and say so if not).
4. **Update the ledgers as you write** — a claim row the moment a
   claim is stated, a dependency row the moment a cross-section
   invariant lands. Never batch this to "later".
5. **Verify before reporting done**: recompile and check every ledger
   row against the fresh views (numbers vs `numbers.md`, sections vs
   `labels.md`). "Done" means views and ledgers agree.

## Artifact ownership (the verdict rule)

- **Machine views** (`notation`, `terminology`, `labels`, `numbers`,
  `todos` under `.copilot/compiled/`): mechanical functions of the
  sources. Never hand-edit; rerun the compiler. Disposable — the
  target repo should gitignore them.
- **Curated ledgers** (`claims.md`, `dependencies.md` under
  `.copilot/ledgers/`): judgment artifacts YOU maintain with the
  author. Seeded once, never overwritten by scripts. Weakening or
  deleting a claim row is an author-level decision: propose, never
  apply. Durable — the target repo tracks them in git.
- The format contract for each artifact lives in `references/` (one
  file per artifact). Read the one for whatever you are about to
  maintain instead of holding them all in mind.

## Boundaries

This skill ships the **mechanical layer of writing state**: machine
views plus machine checks — anything whose output is a mechanical
function of the sources. It deliberately does not own judgment:
style guides and venue rules are read from the target repo when
present, and venue bootstrap (template kit, policy snapshots) is the
sibling `paper-init` skill. Work without those layers when absent,
and say so.

The view/ledger formats in `references/` are the interop API: other
skills (`paper-init`, reviewer/supervisor skills) read the same
files without coupling to this repo's internals.
