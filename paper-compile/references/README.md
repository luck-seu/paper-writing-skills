# Skill references: artifact contracts

The references travel with the skill; the artifacts themselves land
in each paper repo that ships the `.copilot/` state layout. One
contract per **built** artifact: machine views under
`.copilot/compiled/` (disposable — the target repo gitignores them;
`compile.py` regenerates them wholesale). Each contract states the
format, the source, and the producer verdict — **script-perfect**
(regenerate, never hand-edit). Curated ledgers and the remaining
views (terminology, labels, todos, numbers) arrive in later build
rounds, contract-first: the contract lands with the artifact, not
before (the earlier spec drafts live in git history).

| Artifact contract | Producer | Owner of the judgment half |
|---|---|---|
| file_map.md | script | — |
| notation.md | script | meaning / notation choice (skill + author) |

These files are also the **interop API**: other skills
(`paper-scaffold`, reviewer, supervisor) read the same views without
coupling to this repo's internals. Changing a format here is
changing that API.

**The verdict rule** (the grammar-check lesson, standing): a script
may own an artifact only when its output is a mechanical function of
the sources — extraction, counting, lookup. Anything that needs
judgment (what a symbol means, whether a claim is load-bearing,
whether abstract and experiments agree) belongs to a ledger the
writing skill maintains with the author: the script layer can
inventory or diff, never create.

Generated views never enter git. The `.tex` sources are always
authoritative.
