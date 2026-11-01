# Template: claims.md (curated ledger)

The claims-that-must-survive ledger.

**Verdict: NOT script-perfect — LLM/author ledger.** Recognizing a
load-bearing claim (vs a routine sentence), capturing it verbatim,
and judging whether an edit weakens it are exactly the judgment a
keyword script cannot fake (the grammar-check lesson). The script
layer's only role: seed this file once, never overwrite it.

## Format

```markdown
<!-- CURATED LEDGER -- maintained by the writing skill + author.
     Seeded once by compile.sh; scripts never overwrite this file.
     Format contract: references/claims.md in the
     paper-compile skill -->

# Claims that must survive

| Claim (verbatim) | Source | Status |
|---|---|---|
| ... one line per load-bearing claim ... | file:line | proven |

Any edit that weakens a row is an author-level decision: propose,
never apply. The author is the sole approver of claim changes.
Status: proven (theorem/experiment) | built | planned | placeholder
(placeholder claims must never be written as fact).
```

## Maintenance (the skill's job)

- Add rows when the contributions paragraph, theorem/proposition
  statements, or headline experimental claims land — verbatim, with
  source locations.
- Re-verify source locations after structural edits (a moved
  paragraph changes file:line).
- Never delete a row silently: flag it to the author, who decides.
- Cross-check: conclusions must not outrun experiments — this ledger
  is where that discipline is enforced (the target repo's style guide
  may sharpen it).
