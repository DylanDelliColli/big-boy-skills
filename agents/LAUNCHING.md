# Launching reviewers

Operator protocol (rulings 2026-08-17): an adversarial reviewer runs as a
**fresh context of a different lineage** from the authoring session, in its
**own detached pane** — never headless from inside the authoring session, and
never a split attached to the active orchestrator pane. The operator vets the
output live and can interrogate the reviewer.

The choreography, from any orchestrating session:

```bash
# 1. A dedicated workspace of its own — never a split off an existing pane
#    (pane-management hygiene; see gotchas for what splits do and do not break)
herdr workspace create <review-name>   # note the returned pane_id

# 2. A fresh named agent of the OTHER lineage in it — verify the kind in the response
herdr agent start <review-name> --kind codex --pane <pane_id>

# 3. Hand it the role card by file, not inline (shell-quoting-safe, guard-safe)
#    Write role card + assignment to an IGNORED path (e.g. repo tmp/), then:
herdr agent prompt <review-name> "Read tmp/<assignment>.md in this repository and execute the review it specifies, exactly as written. Make no edits to any file. Print the review and stop." --wait
#    If the brief mandates posting a verdict (gh pr comment), authorize that
#    single write explicitly or codex's authorization layer refuses it
#    (observed PR 35): "... execute the review it specifies, exactly as
#    written, including posting the verdict comment it mandates — that
#    single write is authorized. Make no other change of any kind. Then
#    stop."

# 4. Read (if you did not use --wait above: herdr agent wait <review-name> --until done)
herdr pane read <pane_id> --source recent-unwrapped --lines 400
```

Gotchas learned the hard way:

- **Never wait on `--until idle` for a codex agent.** Codex settles at `done`
  and never re-enters `idle`, so an untimed `herdr agent wait --until idle`
  never fires — in ANY pane topology (measured 2026-08-18 by abacus-02; the
  earlier split-pane hypothesis was refuted). Working forms:
  `herdr agent prompt ... --wait`, or `herdr agent wait --until done`. The
  workspace-per-agent standard above stands as pane-management hygiene, not
  as a monitoring requirement.
- A fresh codex session may stop at a **hook-trust dialog** before accepting
  any prompt. That decision is the operator's — never key through it.
- `herdr pane read` default snapshot loses long output; use
  `--source recent-unwrapped --lines 400`.
- Pane ids are not stable across operator rearrangement; resolve by agent
  name, not remembered pane number.
- Bloat reviewer runs FIRST (cuts only), spec validator after, on what
  survives — see the role cards in this directory.
