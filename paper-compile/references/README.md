# Skill references: artifact contracts

The references travel with the skill; the artifacts themselves land
in each paper repo that ships the `.copilot/` state layout. One
contract per artifact: machine views land under
`.copilot/compiled/` (disposable — the target repo gitignores them;
`compile.sh` regenerates them wholesale), curated ledgers under
`.copilot/ledgers/` (tracked — their author rulings exist nowhere
else). Each contract states the format, the source, and the producer
verdict — **script-perfect** (regenerate, never hand-edit) or
**LLM-curated** (a ledger the writing skill maintains with the
author; the script layer only seeds it once).

| Artifact contract | Producer | Owner of the judgment half |
|---|---|---|
| notation.md | script | meaning / notation choice (skill + author) |
| terminology.md | script | eligibility (author rules on proposals) |
| labels.md | script (from the fresh `.aux`) | — |
| todos.md | script | — |
| numbers.md | script | the abstract ↔ experiments mapping (ledger) |
| claims.md | LLM/author ledger | the whole artifact |
| dependencies.md | LLM/author ledger | the whole artifact |

These files are also the **interop API**: other skills (`paper-init`,
reviewer, supervisor) read the same views and ledgers without
coupling to this repo's internals. Changing a format here is
changing that API.

**The verdict rule** (the grammar-check lesson, standing): a script
may own an artifact only when its output is a mechanical function of
the sources — extraction, counting, lookup. Anything that needs
judgment (what a symbol means, whether a claim is load-bearing,
whether abstract and experiments agree) is a ledger: the script layer
can inventory or diff, never create.

Generated views never enter git; the ledgers are tracked because
they are curated, not derived. The `.tex` sources are always
authoritative.
