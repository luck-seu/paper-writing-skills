# paper-writing-skills

Claude Code skills for the academic writing loop, maintained as one
monorepo in the [luck-seu](https://github.com/orgs/luck-seu/) org.

| Skill | What it does | Status |
|---|---|---|
| `paper-compile` | Tracks a LaTeX paper's writing state — notation, terminology, labels, numbers, todos (machine views), claims and cross-section dependencies (curated ledgers), plus mechanical checks | framework stage: contracts settled, compiler pending |
| `paper-scaffold` | Section scaffolding: lays a structural skeleton per section under `.copilot/scaffold/`, filled in and merged into the section file via paper-compile's assembly map | empty stub |
| `paper-init` | Venue bootstrap: template kit, policy snapshots, policy ledger | empty stub, reserved for the graduation project |

## Install

Symlink a skill directory into `~/.claude/skills/` (personal) or
`<paper-root>/.claude/skills/` (per paper repo):

```bash
ln -s /path/to/paper-writing-skills/paper-compile ~/.claude/skills/paper-compile
```

Against a paper, state lands in that paper's `.copilot/`:
`compiled/` views (disposable, gitignore them) and `ledgers/`
(curated, keep them in the paper's own version control).

## Development

- One directory per skill; shared conventions in the root
  `CLAUDE.md` (Conventional Commits, verdict rule, additive-only
  ledger contracts).
- `test/` is a gitignored local sandbox: skills linked at
  `test/.claude/skills/` in the installed shape, `test/amdb`
  pointing at the real corpus outside the repo.
- Hermetic synthetic fixtures (tracked) live inside each skill under
  `scripts/fixtures/` once scripts exist; `test/` holds only
  machine-local links and disposable state.

## History

The full-featured predecessor (audit checks, style-guide compiler,
venue ledger, checklist) lives in the MACRO repo. This org repo is
the deliberate restart: same state-tracking core, no baggage —
nothing is ported from MACRO without a reason stated in the
committing skill's `CLAUDE.md`.
