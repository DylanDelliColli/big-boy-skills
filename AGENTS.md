```doc-meta
role: contract
lifecycle: active
```

# Skills repository — agent contract

This repository is the canonical home of the operator's post-SABLE
general-purpose agent skills. The skills under `skills/` are the
product; they are developed here and installed user-globally to run in
any repository. ABACUS incubated them; this repo owns them now.

Rules for any agent session working here:

- The backlog is this repo's own `br` store (prefix `skills-`). Never
  use `bd`, `sable-note`, or the abacus tracker for work on this repo.
- `NORTH-STAR.md` does not exist yet by design: it is produced by
  running the north-star skill's establish mode WITH the operator —
  that run is simultaneously the skill's establish-mode acceptance
  test and this repo's founding thesis. Do not write it by hand.
- Documentation is governed by `docs-corpus.json` and checked with
  docs-doctor from jot: `python3 ~/dev-environment/jot/tools/docs_doctor.py
  --repo .`. `docs-corpus.json` declares membership only — which document
  locations this repo admits, plus `conforms_to` naming the class-library
  version; the classes ship inside the tool, and
  `docs_doctor.py --classes` lists them. Run `--init` to regenerate the
  file rather than hand-authoring it.
- **Known gap from that move (operator decision, 2026-08-13):** jot's copy
  carries four structural checks. `reverse-citations` is not among them,
  and it produced every finding this repo used to get — eight as of the
  move, all against `skills-xg9`. This repo now reports clean because the
  check that found things no longer runs, not because the citations were
  fixed. They are still there. The eleven-check copy survives in the
  frozen `abacus-v1` tree if that signal is ever wanted back.
- Cross-lineage adversarial review is what produced the quality of
  everything this repo inherited — the two skills were aligned over
  four and five review rounds, and docs-doctor over ten, catching
  roughly thirty real defects. Before landing a skill change, pair
  with a reviewer of the other lineage (a Codex pane for a Claude
  session, or the reverse). **The established lane is a Codex pane
  in this repo's own herdr workspace** — recompute the live seat
  before every dispatch (`herdr agent list`): pane IDs do not survive
  repo renames or herdr restarts, so this contract names none. A
  fresh seat inherits no doctrine, and an unprimed reviewer will wave
  through a bloated artifact an experienced one would refuse: prime
  it on first dispatch with the MVP-first ruling below, the
  scale-not-shape scope guard, and the archived rounds for the skill
  under review — the root SKILL-REVIEW-* files first, whose
  verification style (hash the blobs yourself, verify claims against
  the filesystem) a new seat should match. Recovery pointers for the
  abacus-era rounds are recorded on `skills-xg9`.
- `skills/*/SKILL.md` files are deliberately outside the managed
  corpus for now: doc-meta blocks would break the skill loader's
  frontmatter. Their governance class is routed to `skills-bny` (the
  council acceptance-run subject), not decided on the extraction bead.
- Never edit `~/.claude` or other machine-global configuration from
  this repo; the user-global install (symlinks into `~/.claude/skills/`)
  is the operator's act, documented in README.md.
- The only remote is `git@github-personal:DylanDelliColli/big-boy-skills.git`
  (the `github-personal` SSH alias authenticates as DylanDelliColli;
  the machine's default key has no write access). Never add other
  remotes. Commit when a coherent unit lands; push after committing.
- Tree-residency applies here as in abacus: the tree holds current
  state, git history is the archive, `docs/history/README.md` is the
  pointer index, one review file per cycle, one shift report per lane.

## MVP first, fix as we use

**Operator ruling, 2026-08-12, binding on every build in this repo.**
Ship the braindead-simple version, dogfood it, and handle real failures
when observed evidence exists. Do not pre-build contingencies for
failure modes that have not happened.

Why it exists: a sibling spec reached v20 across ~18 adversarial review
rounds — ULID event ids, canonical digests, an fsync/`link(2)` publish
protocol, a two-observation gate, an attempt state machine — to replace
a **123-line bash script** that nobody opened across twenty spec
versions. Two mechanisms let that happen, and both are live here:

1. A ceremony rule that judges a review round by *what it caught* tests
   productivity **within a chosen scope** and is structurally blind to
   whether the artifact should have been that large. A big artifact
   always yields defects under review, so the rule never fires.
2. "Verify the seam before you draft" must be applied to the **product
   being replaced**, not only to code seams. Read what exists and name
   what is inadequate about it before designing a replacement.

Concretely for the work in flight: `skills-h1u` says to reuse the
docs-doctor fixture patterns. Reuse the *shape* — temp repos, a clean
baseline, result-bound assertions — **not the scale.** That suite is
176 cases for a 1,400-line linter that gates every documentation
change. A skill's check mode needs enough cases to make its verdict
fold trustworthy and no more. An approved design document is never a
build order.
