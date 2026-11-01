# paper-writing-skills

Claude Code skills for academic paper writing, maintained as one
monorepo: **one directory per skill, one repository for all**. Home
of the graduation-project ("毕设") prototypes — the plan is to extend
them, not to preserve them.

- `paper-compile/` — writing-state tracking: machine views,
  curated ledgers, machine checks
- `paper-scaffold/` — section scaffolding: per-section structural
  skeletons under `.copilot/scaffold/`, merged into the section
  file via the compile map (empty stub)
- `paper-init/` — venue bootstrap (empty stub, reserved for the
  graduation-project student to design and build)

## Git conventions

Every commit message follows [Conventional Commits 1.0.0](
https://www.conventionalcommits.org/en/v1.0.0/):

    <type>(<scope>): <short imperative summary>

    [optional body: motivation and what changed, wrapped at ~72]

- Types: `feat` `fix` `docs` `style` `refactor` `perf` `test` `build`
  `ci` `chore`. Scope names the skill touched (`paper-compile`,
  `paper-scaffold`, `paper-init`) or `repo` for shared files; omit
  when unclear.
- Summary: imperative mood, lowercase, no trailing period, under ~50
  characters when possible.
- Commit only when the author asks; split into small logical units.
- End every commit message created by Claude Code with:

      Co-Authored-By: Claude Code <noreply@anthropic.com>

- PR descriptions end with:

      🤖 Generated with [Claude Code](https://claude.com/claude-code)

The GitHub remote is `luck-seu/paper-writing-skills` (public);
commit and push only when the author asks.

## Layout & install

- Each top-level directory is one skill (`SKILL.md` at its root).
  Install = symlink the skill directory into `~/.claude/skills/<name>`
  (personal, all projects) or `<paper-root>/.claude/skills/<name>`
  (per paper repo; takes precedence over the personal level).
- `test/` — **gitignored local sandbox**: links the skills at
  `test/.claude/skills/` in the installed shape and points
  `test/amdb -> ../../AMDB` at the real development corpus, so basic
  tests run without touching the corpus or the global config.
- The development corpus lives OUTSIDE this repo at
  `~/Workspace/program/AMDB` — an svn-severed copy of a real paper;
  it must never interact with its upstream repo, and it never enters
  version control here. Skill state output lands in the target
  paper's `.copilot/` (views disposable, ledgers durable).

## Standing rules (all skills)

1. **The verdict rule.** A script may own an artifact only when its
   output is a mechanical function of its sources. Judgment belongs
   to ledgers maintained with the author.
2. **Ledger contracts only extend, never break.** Skills are
   consumed via live symlinks into the dev clone; a format change
   that renames/removes fields breaks every existing paper repo's
   ledgers. Additive changes only; breaking moves require a
   with-the-author migration.
3. **One interface: the documented `.copilot/` layout.** No
   target-repo-specific content may live in this repo; skills
   upgrade by pulling it.
