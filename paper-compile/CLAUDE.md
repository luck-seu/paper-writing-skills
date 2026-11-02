# paper-compile (prototype)

A Claude Code skill that tracks the **writing state** of a LaTeX
paper — this round: the file map (assembly order, file roles,
headings) and the math notation as actually used. This directory IS
the skill package
(SKILL.md at its root), living in the `paper-writing-skills`
monorepo beside its siblings `paper-scaffold/` (section
scaffolding — an empty stub) and `paper-init/` (venue bootstrap —
an empty stub reserved for the graduation-project student). It is the
starting prototype for an undergraduate graduation project ("毕设")
that will extend it.

Repo-wide conventions — Conventional Commits, scopes, the verdict
rule, additive-only ledger contracts, the `test/` sandbox — live in
the monorepo root `../CLAUDE.md`. Only skill-specific rulings live
here.

## Design principles (standing rulings)

1. **Minimality — the mechanical layer of writing state.** The
   skill owns machine views (file_map, notation; later build rounds
   extend the set) and machine checks (any mechanical function of
   the sources: typography, citation hygiene, dangling labels).
   Judgment — style, venue policy, claim-hood — belongs to the
   author and, in later rounds, curated ledgers maintained with the
   author; venue bootstrap is the sibling `paper-init/` skill;
   repo-side style guides are read as ground truth, never shipped
   here.
2. **Pull-to-upgrade.** The skill is a self-contained package: no
   target-repo-specific content may live here. Consumers upgrade by
   pulling this repo; symlinked installs track the working tree
   live. The only interface is the documented `.copilot/` layout
   the skill reads/writes in the target repo.
3. **The verdict rule.** A script may own an artifact only when its
   output is a mechanical function of its sources (extraction,
   counting, lookup). Judgment (meaning, claim-hood, cross-section
   mapping) belongs to ledgers, maintained by the writing skill
   WITH the author. Weakening a claim row is an author-only
   decision.
4. **Views are disposable.** Views regenerate wholesale
   (`compile.py`). Curated ledgers, when they arrive in a later
   round, are durable by design: seeded once, never overwritten —
   their author rulings exist nowhere else.

## Layout

- `SKILL.md` — the skill: session loop + artifact ownership.
- `references/` — one format contract per artifact (read on demand).
- `scripts/` — home of the state compiler: `compile.py` (the entry
  point, the only public interface) over `core/` (view-agnostic
  machinery: `texscan`, `mathmode`, `macromap`, `copilot`) and
  `views/` (one module per machine view: `file_map`, `notation`;
  Python, standard library only). The file_map and notation views
  are built; further views land contract-first. See
  `scripts/README.md`.
- Development corpus, OUTSIDE this repo: `~/Workspace/program/AMDB`
  — an svn-severed copy of a real paper (acmart, flat `sec-*.tex`
  layout); it must never interact with its upstream repo and never
  enters version control. The repo's gitignored `test/` sandbox
  links it as `test/amdb` and links the skills in the installed
  shape under `test/.claude/skills/`.

## Using the skill against a paper

From inside the paper root, via any installed location
(`~/.claude/skills/`, a paper's `.claude/skills/`, or the repo's
`test/.claude/skills/` sandbox):

    python3 <skills-location>/paper-compile/scripts/compile.py

or from anywhere: `PAPER_ROOT=path/to/paper python3 .../compile.py`.
State lands in `$PAPER_ROOT/.copilot/compiled/` (views, disposable).

The first cut (the file_map and notation views) is built; later
build rounds are marked in `scripts/README.md`.

## Extension points (the 毕设 roadmap)

- **Venue plug-in — reserved for the sibling `paper-init/` skill**
  (empty stub; the graduation-project student designs and builds
  it): fetch the venue kit in-tree, snapshot policy sources into
  `.copilot/policy/sources/` (disposable), seed the durable
  `submission-policy.md` ledger. This skill would read that ledger
  as ground truth when checking venue rules.
- **Style plug-in**: the target repo ships a style guide; the skill
  reads it as ground truth when present, stays style-agnostic
  itself.
- **Skill interop**: the artifact contracts in `references/` are
  the stable API — other skills (e.g. supervisor/reviewer skills)
  read the same files without coupling to this repo's internals.

## History

The full-featured predecessor (audit checks, style guide compiler,
venue ledger, submission checklist) lives in the MACRO repo
(`~/Workspace/research/MACRO`, `.claude/skills/` + `paper/copilot/`).
This project is the deliberate restart: same state-tracking core,
no baggage. Do not port from MACRO without a reason stated here.
