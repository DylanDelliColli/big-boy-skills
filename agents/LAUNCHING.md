# Launching reviewers

Operator protocol (rulings 2026-08-17): an adversarial reviewer runs as a
**fresh context of a different lineage** from the authoring session, in its
**own detached pane** — never headless from inside the authoring session, and
never a split attached to the active orchestrator pane. The operator vets the
output live and can interrogate the reviewer.

The choreography, from any orchestrating session:

```bash
# 1. A detached pane of its own (split from any non-orchestrator workspace pane)
herdr pane split <workspace-pane> --direction right --ratio 0.4   # note the returned pane_id

# 2. A fresh named agent of the OTHER lineage in it — verify the kind in the response
herdr agent start <review-name> --kind codex --pane <pane_id>

# 3. Hand it the role card by file, not inline (shell-quoting-safe, guard-safe)
#    Write role card + assignment to an IGNORED path (e.g. repo tmp/), then:
herdr agent prompt <review-name> "Read tmp/<assignment>.md in this repository and execute the review it specifies, exactly as written. Make no edits to any file. Print the review and stop."

# 4. Wait and read
herdr agent wait <review-name> --until idle
herdr pane read <pane_id> --source recent-unwrapped --lines 400
```

Gotchas learned the hard way:

- A fresh codex session may stop at a **hook-trust dialog** before accepting
  any prompt. That decision is the operator's — never key through it.
- `herdr pane read` default snapshot loses long output; use
  `--source recent-unwrapped --lines 400`.
- Pane ids are not stable across operator rearrangement; resolve by agent
  name, not remembered pane number.
- Bloat reviewer runs FIRST (cuts only), spec validator after, on what
  survives — see the role cards in this directory.
