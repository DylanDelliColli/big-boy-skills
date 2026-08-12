#!/usr/bin/env python3
"""PreToolUse gate: creating a design document invokes the review discipline.

Fires only on ADR/PRD/PROPOSAL markdown and only on CREATION, so editing an
existing decision (marking it superseded, fixing prose) stays silent. Never
blocks — it injects context and lets the turn continue.

Why this trigger: our observed pathology is document-first development. A
spec reached v20 across eighteen adversarial review rounds to replace a
123-line bash script, and an ADR was corrected seven times by the code it
described. Every instance began with someone opening a design document, so
that is the moment worth interrupting.

Why a hook rather than a skill: a skill must be invoked, and invoking it
requires noticing you are over-scoping — which is the faculty that fails.
A hook fires whether or not anyone is paying attention.
"""

import json
import os
import re
import sys

TRIGGER = re.compile(r"(^|[^a-z])(adr|prd)([^a-z]|$)|^proposal", re.IGNORECASE)

GUIDANCE = """You are creating a design document. Before treating it as final, \
run the adversarial review pair — they are provider-neutral role cards, and \
the reviewer must be a FRESH context of a different lineage (a Codex herdr \
pane), never this session, which holds the sunk cost.

1. ~/dev-environment/skills/agents/bloat-reviewer.md — runs FIRST and may only \
propose cuts. It reads this document plus the repository's NORTH-STAR.md.
2. ~/dev-environment/skills/agents/spec-validator.md — runs after, on whatever \
survives, and may not add requirements.

If this repository has no NORTH-STAR.md, say so plainly: without one the bloat \
review has no clause to quote and degrades to taste. Establishing it is the \
north-star skill's establish mode, run once with the operator.

Answer these in the document itself, or reconsider writing it: what runs today \
that made this necessary, what is the smallest version, and which north-star \
clause does it serve."""


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except Exception:
        return 0

    path = (event.get("tool_input") or {}).get("file_path") or ""
    if not path.endswith(".md"):
        return 0

    base = os.path.basename(path)
    in_adr_dir = "/docs/adr/" in path.replace(os.sep, "/")
    if not (in_adr_dir or TRIGGER.search(base)):
        return 0

    # Creation only. An existing file is being amended, not proposed.
    if os.path.exists(path):
        return 0

    json.dump(
        {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "additionalContext": GUIDANCE,
            }
        },
        sys.stdout,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
