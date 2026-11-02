# scripts/ — the state compiler

`compile.py` is the entry point — the only public interface. The
implementation lives in two packages, one job per module:

| Path | Job |
|---|---|
| `compile.py` | CLI contract (views, exit codes), root resolution, hardening, dispatch |
| `core/texscan.py` | reading the .tex sources: comment stripping, .tex discovery, assembly order |
| `core/mathmode.py` | math segmentation ($...$, \(...\), \[...\], display envs) + tokenization |
| `core/macromap.py` | macro-source files → definitions + macro-source classification |
| `core/copilot.py` | .copilot/ output: atomic view writes + diagnostics |
| `views/file_map.py` | the file-map view: assembly order, roles, heading scan |
| `views/notation.py` | the notation view: policy lists, normalization, folding, rendering |

Structure rules (author ruling, 2026-11-02): `core/` is
view-agnostic machinery; `views/` holds one module per machine
view. Bare-name scripts at this level are the only public
interfaces — everything under `core/` and `views/` is import-only.
Views take their inputs from compile.py and core/, never from each
other's output. The skill directory is symlinked as a whole, so the
packages resolve from any installed location.

**Map-first pipeline, no hardcoded file names** (author ruling,
2026-11-02): discovery and content classification run before any
view. `commands.tex` / `keywords.tex` style names are corpus
conventions, not contracts — a file is a macro source iff it holds
definitions and no prose sentences (the walk in `macromap.scan_file`);
everything else is prose. `paper.tex` stays the one name the skill
assumes: it is the documented anchor of the paper root.

**Swallow blanking** (author ruling, 2026-11-02): a macro whose
live definition takes an argument the body never references
(`\eat`-style; `\warn`/`\revise` reference `#1` and keep content)
has its `\name{...}` calls blanked — spaces, newlines preserved —
in `macromap.read_content`, the single content reader every prose
scan goes through. Removed content is not usage, not a heading,
not anything. One braced argument only (a multi-arg swallow macro's
later arguments stay visible: under-blanking is the safe
direction); an unclosed argument is noted and left as-is. Empty
definition bodies `{}` are real definitions (the macro expands to
nothing) — a walker bug that silently dropped them (falsy-body
check) was fixed with this ruling; AMDB recovered `\eat` and
`\copyrightspace` (610 → 612 definitions).

Machine views land in `$PAPER_ROOT/.copilot/compiled/`. Machine-check
scripts arrive here when built.

**Status: first cut built** (2026-11-01; split into modules and
focused on notation, map-first, then trimmed to the simplest set —
all 2026-11-02). `compile.py` builds the `file_map` and `notation`
views; the CLI knows only the built set. Later build rounds
(terminology, labels, todos, numbers, curated ledgers) land
contract-first: the contract arrives with the artifact
(`references/` holds built contracts only; the earlier spec drafts
live in git history). Verified against the AMDB corpus
(`test/amdb` sandbox): CLI contract (unknown view exits 2), all
invocation paths (PAPER_ROOT env, CWD with paper.tex, symlinked
install), a row-by-row review of the AMDB notation table after the
exclusion rules landed (53 rows → 17, all 12 duplicate signals
kept), a byte-differential of the notation view across the
map-first rework (rows and duplicates identical; only the view's
own source description changed), and a synthetic corpus exercising
swallow blanking (eaten math, eaten heading, keep-macro contrast).
Written fresh: the global skills and their Supervisor-Skills
upstream hold nothing reusable (checked 2026-11-02); the MACRO
predecessor stays consultable-but-uncopied without a stated reason.

**Language ruling** (author, 2026-11-02): Python, standard library
only, Python >= 3.9, split into single-job modules — the entry
point stays small. Readability is part of the contract: the verdict
rule grants a script an artifact only as a mechanical function of
its sources, and the author must be able to audit that.

**Notation content ruling** (author, 2026-11-02): three classes are
not the paper's notation and never become table rows — standard
math symbols (`STANDARD_SYMBOLS` in `views/notation.py`: operators,
relations, arrows, dots, delimiters, log-like names, named
constants), a font switch applied to two or more letters
(`\mathit{type}` — prose emphasis), and `\kw{...}` carrier macros
(reserved for a future terminology view). A hand-typed standard
symbol still reaches the duplicate section when a declared macro
expands to it: that is a typing-consistency signal, independent of
notation-hood.

Contract (all subject to the verdict rule):

- `python3 scripts/compile.py [view ...]` — views: `file_map`,
  `notation` (default: both). Unknown view → exit 2.
- Paper-root resolution: `PAPER_ROOT` env, else the CWD when it
  holds `paper.tex`, else die. The skill is a standalone package —
  no repo-relative derivation.
- File scope is layout-agnostic and name-free: root-level `*.tex`
  plus a `sections/` tree when one exists (the two layouts of the
  AMDB development corpus, linked as `test/amdb` in the sandbox),
  except `paper.tex` (the root anchor). Roles are classified by
  content: macro source (definitions, no prose sentences) vs prose
  — see the map-first ruling above and `references/file_map.md`.
- Missing sources are notes in the report, not errors; the `.tex`
  sources are always authoritative.
- Hardening carried over from the predecessor (proven by its
  disk-fill incident): an `RLIMIT_FSIZE` write cap, atomic
  same-directory temp writes cleaned up on error/interrupt, and one
  coordinate space for all math spans (blanked, never cut) so the
  notation table is true reading order.
