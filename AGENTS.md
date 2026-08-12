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
  ABACUS's docs-doctor until the tool itself is extracted:
  `python3 ~/dev-environment/abacus/tools/docs_doctor.py --repo .`
- `skills/*/SKILL.md` files are deliberately outside the managed
  corpus for now: doc-meta blocks would break the skill loader's
  frontmatter. Their governance class is an open decision on the
  extraction bead.
- Never edit `~/.claude` or other machine-global configuration from
  this repo; the user-global install (symlinks into `~/.claude/skills/`)
  is the operator's act, documented in README.md.
- No remote is configured yet; the operator sets it. Until then,
  commit locally and say so in handoffs — do not invent a remote.
- Tree-residency applies here as in abacus: the tree holds current
  state, git history is the archive, `docs/history/README.md` is the
  pointer index, one review file per cycle, one shift report per lane.
