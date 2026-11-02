---
name: paper-scaffold
description: Reserved stub, not yet implemented — section scaffolding for a LaTeX paper. /paper-scaffold <section> lays the basic structure for writing that section under .copilot/scaffold/<section>/; the author fills the skeleton in and the content is merged into the section's .tex file, located via the file map (file_map.md) compiled by the sibling paper-compile skill. Until built, this skill does nothing.
---

# paper-scaffold

Empty placeholder. Mission: per-section scaffolding — invoked as
`/paper-scaffold <section>` (e.g. `/paper-scaffold intro`), it lays
a scaffold at `.copilot/scaffold/<section>/` describing the basic
structure for writing that section (what it must accomplish, in
what order). The author fills the skeleton in; the filled content
is then merged into the section's `.tex` file — which file that is
comes from the file map compiled by the sibling `paper-compile`
skill (`file_map.md`). The surrounding conventions (one directory per
skill, `.copilot/` state root, additive-only ledger contracts) are
recorded in the monorepo root `CLAUDE.md`.
