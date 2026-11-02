---
name: paper-compile
description: Track the writing state of a LaTeX paper through machine-compiled views — a file map (assembly order, file roles, headings) and a notation view (math symbols as used, hand-typed duplicates of declared macros) — over the .copilot/ state layout. Use when writing or editing any section of such a paper, when asked where a section or file lives or which notation macro exists, or when onboarding to a paper repo that ships the .copilot/ layout. Mechanical layer only; style and venue rules are read from the target repo or the paper-init skill when present.
---

# paper-compile

You are the writer's peer and record-keeper. The skill tracks WHAT the
paper says (state); the target repo's own conventions govern HOW prose
is written. Two rules follow: never invent state, and never lose a
ruling.

## Session loop

1. **Compile**: run `python3 scripts/compile.py` (from this skill)
   with `PAPER_ROOT=<paper root>` (or from inside the paper root).
   It regenerates the machine views into
   `$PAPER_ROOT/.copilot/compiled/`.
2. **Load state**: read the views before touching prose. They are
   the shared factual baseline — which file a section lives in
   (`file_map.md`), which notation macros exist and what was
   hand-typed anyway (`notation.md`).
3. **Write or edit** one section at a time, in place, following the
   target repo's conventions (its `CLAUDE.md`, style guide, rules —
   read them if present; work without them and say so if not).
4. **Verify before reporting done**: recompile and check the views
   agree with what you wrote — new symbols show up, duplicates
   resolved or intentionally kept. "Done" means views and prose
   agree.

## Artifact ownership (the verdict rule)

- **Machine views** (`file_map`, `notation` under
  `.copilot/compiled/`): mechanical functions of the sources. Never
  hand-edit; rerun the compiler. Disposable — the target repo should
  gitignore them.
- Further views (terminology, labels, todos, numbers) and curated
  ledgers arrive in later build rounds, contract-first: their
  contracts land in `references/` with the artifacts, not before.
- The format contract for each built artifact lives in `references/`
  (one file per artifact). Read the one for whatever you are about
  to maintain instead of holding them all in mind.

## Boundaries

This skill ships the **mechanical layer of writing state**: machine
views plus machine checks — anything whose output is a mechanical
function of the sources. It deliberately does not own judgment:
style guides and venue rules are read from the target repo when
present, and venue bootstrap (template kit, policy snapshots) is the
sibling `paper-init` skill. Work without those layers when absent,
and say so.

The view formats in `references/` are the interop API: other skills
(`paper-init`, reviewer/supervisor skills) read the same files
without coupling to this repo's internals.
