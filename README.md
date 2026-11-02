# paper-writing-skills

Claude Code skills for the academic writing loop, maintained as one
monorepo in the [luck-seu](https://github.com/orgs/luck-seu/) org.

| Skill | What it does | Status |
|---|---|---|
| `paper-compile` | Tracks a LaTeX paper's writing state through machine-compiled views: a file map (assembly order, file roles, headings) and math notation as used, hand-typed duplicates flagged; further views, ledgers, and checks in later rounds | first cut built: the file_map + notation views (`scripts/compile.py`) |
| `paper-scaffold` | Section scaffolding: lays a structural skeleton per section under `.copilot/scaffold/`, filled in and merged into the section file via paper-compile's file map | empty stub |
| `paper-init` | Venue bootstrap: template kit, policy snapshots, policy ledger | empty stub, reserved for the graduation project |

## Install

Symlink a skill directory into `~/.claude/skills/` (personal) or
`<paper-root>/.claude/skills/` (per paper repo):

```bash
ln -s /path/to/paper-writing-skills/paper-compile ~/.claude/skills/paper-compile
```

Against a paper, state lands in that paper's `.copilot/compiled/`
(views, disposable, gitignore them); curated ledgers arrive in a
later round and are durable by design.

## Development

- One directory per skill; shared conventions in the root
  `CLAUDE.md` (Conventional Commits, verdict rule, additive-only
  ledger contracts).
- `test/` is a gitignored local sandbox: skills linked at
  `test/.claude/skills/` in the installed shape, `test/amdb`
  pointing at the real corpus outside the repo.
- Synthetic fixtures are deliberately out of scope for the prototype
  (author ruling, 2026-11-02); `test/` holds only machine-local links
  and disposable state, and the compiler is verified against the real
  corpus plus disposable out-of-repo synthetic runs (see
  `paper-compile/scripts/README.md`).

## History

The full-featured predecessor (audit checks, style-guide compiler,
venue ledger, checklist) lives in the MACRO repo. This org repo is
the deliberate restart: same state-tracking core, no baggage —
nothing is ported from MACRO without a reason stated in the
committing skill's `CLAUDE.md`.
