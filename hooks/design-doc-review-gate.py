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

TWO PAYLOAD SHAPES, both observed live rather than assumed:

  Claude Code  tool_name Write/Edit, tool_input.file_path
  Codex        tool_name apply_patch, tool_input.command holding a patch
               whose "*** Add File: <path>" lines name what is created

Codex never uses Write/Edit, so a hook keyed only to file_path fires and
silently finds nothing — it looks installed while doing nothing.
"*** Add File:" is also a better creation signal than probing the
filesystem: it states intent instead of racing the write.
"""

import json
import os
import re
import sys

TRIGGER = re.compile(r"(^|[^a-z])(adr|prd)([^a-z]|$)|^proposal", re.IGNORECASE)
ADD_FILE = re.compile(r"^\*\*\* Add File:\s*(.+?)\s*$", re.MULTILINE)

GUIDANCE = """You are creating a design document. Before treating it as final, \
run the adversarial review pair — they are provider-neutral role cards, and \
the reviewer must be a FRESH context of a different lineage (a Codex herdr \
pane for a Claude session, or the reverse), never this session, which holds \
the sunk cost.

1. ~/dev-environment/bb-skills/agents/bloat-reviewer.md — runs FIRST and may only \
propose cuts. It reads this document plus the repository's NORTH-STAR.md.
2. ~/dev-environment/bb-skills/agents/spec-validator.md — runs after, on whatever \
survives, and may not add requirements.

If this repository has no NORTH-STAR.md, say so plainly: without one the bloat \
review has no clause to quote and degrades to taste. Establishing it is the \
north-star skill's establish mode, run once with the operator.

Answer these in the document itself, or reconsider writing it: what runs today \
that made this necessary, what is the smallest version, and which north-star \
clause does it serve."""


def created_paths(tool_input: dict) -> list:
    """Paths this call CREATES, across both agent shapes."""
    paths = []

    # Codex: a patch that declares what it adds.
    command = tool_input.get("command")
    if isinstance(command, str):
        paths.extend(ADD_FILE.findall(command))

    # Claude Code: a direct path. A pre-existing file is an amendment.
    file_path = tool_input.get("file_path")
    if isinstance(file_path, str) and not os.path.exists(file_path):
        paths.append(file_path)

    return paths


def is_design_doc(path: str) -> bool:
    if not path.endswith(".md"):
        return False
    normalized = path.replace(os.sep, "/")
    return "/docs/adr/" in normalized or bool(TRIGGER.search(os.path.basename(path)))


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except Exception:
        return 0

    tool_input = event.get("tool_input")
    if not isinstance(tool_input, dict):
        return 0

    if not any(is_design_doc(p) for p in created_paths(tool_input)):
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
