```doc-meta
role: contract
lifecycle: active
```

# skills

Canonical home of post-SABLE general-purpose agent skills, extracted
from their incubation in the abacus repository.

| Skill | Purpose | Validation state |
|---|---|---|
| `skills/north-star` | Establish, check against, or revise a repository's declared thesis | establish mode: acceptance run pending (this repo's founding); check mode: UNTRUSTED until its fixture (`skills-` bead) |
| `skills/council` | Convert a contested plan into quantified knowledge via a recorded multi-reviewer run | first live run IS the acceptance test — pending (`skills-` bead) |

Both skills were aligned by multi-round adversarial cross-review in
abacus (north-star r4, council r5; rounds archived in abacus
`docs/history/README.md`).

Both skills are tracker-agnostic: a consuming repository declares its
work-item seam in its own workflow-contract document — the model is
market-brief's `docs/agents/issue-tracker.md` — and the skill text
defers to that contract rather than naming any concrete tracker.

## Install (operator act)

Symlink into the user-global skills directory so the skills load in
any repository:

    ln -s ~/dev-environment/bb-skills/skills/north-star ~/.claude/skills/north-star
    ln -s ~/dev-environment/bb-skills/skills/council ~/.claude/skills/council

Installed and verified 2026-08-17 (both skills load from a
non-repository cwd). The in-repo copies under abacus `.claude/skills/`
were retired once the global install was verified — two copies is a
drift defect, not redundancy.

## Working here

See `AGENTS.md`. The backlog is this repo's `br` store (`br ready`);
docs are governed by `docs-corpus.json` (checked with abacus's
docs-doctor until the tool is extracted).
