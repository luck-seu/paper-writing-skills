# Template: dependencies.md (curated ledger)

Cross-section dependencies: the spine and the number-sync invariants.

**Verdict: NOT script-perfect — LLM/author ledger.** Which paragraph
in the intro corresponds to which contribution, and which abstract
number must equal which table cell, is a semantic mapping over the
prose. The machine layer feeds it (`numbers.md` inventories the
literals; `labels.md` locates the sections) but cannot create the
mapping. Seeded once by compile.sh; never overwritten by scripts.

## Format

```markdown
<!-- CURATED LEDGER -- maintained by the writing skill + author.
     Seeded once by compile.sh; scripts never overwrite this file.
     Format contract: references/dependencies.md in the
     paper-compile skill -->

# Cross-section dependencies

## Spine (challenge ↔ section ↔ contribution ↔ conclusion)

| Challenge | Section | Contribution | Conclusion slot |
|---|---|---|---|
| ... rows added once intro challenges + contributions exist ... | | | |

The four cells of a row must stay in 1:1:1:1 alignment (AIDB's
problem-spine rule).

## Number-sync invariants

| Invariant | Must appear in | Current |
|---|---|---|
| headline accuracy = table 2, row MACRO | 0_abs, 4_exp | ✓ / ✗ / — |

Before reporting an edit done: re-verify each row against
compiled/numbers.md (the machine inventory) and the actual tables.
```

## Maintenance (the skill's job)

- Fill the spine once the intro's challenge list and contributions
  exist; keep rows aligned through section restructuring.
- Add a number-sync row for every headline number the moment it
  appears in the abstract or a table; resolve drift by fixing the
  prose, never by editing the ledger to match the typo.
- Move resolved items out; add new invariants as the paper grows
  (running-example numbers, complexity claims the experiments test).
