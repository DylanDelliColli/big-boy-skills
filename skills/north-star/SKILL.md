---
name: north-star
description: Pause in-flight work and test it against the repository's stated goal, or establish that goal if none exists. Use when deep in a problem, process, or debugging phase and it is unclear whether the current work still serves the mission; when asked "are we off track", "is this worth doing", "what is this repo for", or "/north-star".
---

# North Star

A repository declares one thesis by default; a genuinely multi-product
repository declares one thesis per product and every check names which one it
is testing against. Work either serves a declared thesis or it doesn't. Three
operator-facing modes: **establish** (no thesis exists), **check** (test
in-flight work), and **revise** (operator-only amendment). Invoking establish
or check pauses the work in flight — no edits, no fixes, no design
continuation until the mode resolves. The pause exempts only this skill's own
artifacts: the case, the check record, and (in establish mode) the thesis
document itself.

Resolve the goal source first: `NORTH-STAR.md` at the repository root.
Present → check mode. Absent → establish mode. Revise runs only on an
explicit operator request — file presence never routes to it.

**Storage rule (aligned with the knowledge-system decision — index, not
decompose):** the thesis stays a whole document; a knowledge store may index
its clauses by heading and cite them, but the judge always receives the
complete named snapshot, and no future migration decomposes this file into
nodes without a lossless round trip. Keep headings atomic so citations stay
stable — that is an indexing courtesy, not a decomposition plan.

## Establish mode

A short interview — one question at a time, wait for each answer. Bounds are
defaults, not laws: about nine questions, stopping when the six fields are
complete rather than when a count is hit. You are extracting a thesis the
operator already holds, not inventing one:

1. **Thesis** — one paragraph: what this repository makes true that was not
   true before it. If the operator gives a feature list, push once for the
   sentence behind the list.
2. **Beneficiary** — who concretely uses the result, and for what.
3. **Success condition** — an observable state, not a feeling.
4. **Non-goals** — explicit named exclusions; enough to cover the adjacent
   things people will otherwise assume are in scope (three is a floor that
   usually suffices, not a target).
5. **Kill criteria** — what evidence would mean the thesis is wrong and the
   work should stop or pivot.
6. **Test values** — the classes of test this repository actually uses,
   ranked. Ask the operator to name the classes (whatever taxonomy the
   repository really runs — unit, integration, end-to-end, property,
   real-process), then rank them by value. The thesis document records the
   answer as a required "Test values" section: a short ranked table with,
   per class, its value rank, why it earns that rank in this repository,
   and its cost class — effectively-free or expensive to run. Values and
   ranks only — binding numeric caps never live in the north star.
   Planning documents in consuming repositories carry any caps and cite
   this ranking.

Where the repository has normative documents (in ABACUS: `CONTEXT.md`, the
ADRs), **cite them, never duplicate them** — a duplicated invariant drifts
from its source and the fork becomes a defect. Show the draft, revise on
feedback, and stop. Establish mode never continues into other work; resuming
the paused task is a fresh decision.

## Revise mode (operator-only)

An explicit invocation ("revise the north star"), never a consequence of a
check verdict — an inconvenient verdict is a reason to dispute, not to move
the goalposts. A revision: records the prior version's blob hash, states the
evidence and rationale for the change, runs as an establish-style interview
over only the changing fields, and lands only on operator approval.

## Check mode

The agent in the weeds holds sunk cost and motivated reasoning — it does not
grade its own alignment. Check mode separates writing the case from judging
it, and fails closed when the separation cannot be guaranteed.

**1. Write the case.** Fixed form, bounded (~250 words as the default limit):

- **Doing:** what the current work is, concretely — files, change, intent.
- **Serves:** which clause of which thesis, quoted verbatim. No quotable
  clause → write "no clause"; that is itself the finding.
- **Cheapest surface:** why this work is the least expensive way to serve
  that clause.
- **Falsifier:** what observation would prove this work misdirected.

The case is a payload — hold it in memory or a uniquely named temporary
file, and copy its final text into the check record (step 4). Never depend on
a session scratch directory surviving; recycled sessions delete them.

**2. Convene the judge — adapter contract, fail-closed.** The judge is a
fresh, non-forked context whose *task payload* is exactly: the complete
thesis snapshot (with its blob hash), the case, the verdict schema below, and
the instruction *"judge only these supplied artifacts; do not inspect the
repository, use tools, or seek other context."* Honesty about the boundary:
the harness still supplies its own system prompt and policies — the caller
controls the payload, not the judge's total context, so the instruction plus
(where available) tool-disabling is the enforcement, and both are recorded.

Adapter steps, in order: (a) capability-check that a fresh-context mechanism
exists in this session — the Claude harness Agent tool, a host-provided fresh
Codex spawn, a fresh Herdr pane, or a one-shot CLI invocation; (b) start the
fresh context and pass the payload; (c) record which adapter ran, the agent
kind/model, and whether tools were disabled; (d) validate one structured
`judged` payload when the judge returns successfully; otherwise construct
one typed `unresolved` result. **If any step is unavailable or fails, the check fails
closed: report to the operator that no independent judge could be convened.
Self-grading and reusing the working context are never fallbacks.** A
malformed verdict gets one formatting-correction prompt to the *same* judge;
continued failure leaves the check unresolved — unresolved is a valid,
recorded outcome.

**3. Result — a sum type, not four labels.** A check resolves to exactly one
of two result kinds:

- **`judged`** — carries one of the four verdicts below, a `next_action`,
  and the judge's rationale with quoted clauses.
- **`unresolved`** — carries a typed reason (`capability_unavailable` |
  `adapter_failure` | `malformed_after_correction`), whatever provenance is
  available, and an operator-only next step. **Every unresolved state
  prohibits mutation of the work** — a validator never counterfeits a
  judgment to satisfy the record schema.

For `judged`, the judge applies the first rule that matches:

1. The case cites no clause (or the cited clause does not say what the case
   claims) → **orphaned**.
2. The clause is real but a different implementation surface serves it more
   cheaply → **right-goal-wrong-surface**.
3. The surface is right but can be reduced without changing accepted
   behavior → **aligned-but-oversized**.
4. Otherwise → **aligned**.

The verdict carries a `next_action`: "proceed unchanged" for aligned; a
concrete redirect otherwise, grounded in quoted clauses.

**4. Record — immutable initial record plus immutable addenda.** Write
`north-star-checks/<check-ULID>.md` (never edited after creation) containing:
check ID and timestamp; the thesis blob hash and which thesis; the full
case; the **result** (the full `judged` or `unresolved` payload from step
3); and adapter/model/tools provenance. A late fact — a dispute, the
operator's disposition — is **its own uniquely named immutable file**
`north-star-checks/<event-ULID>.md` carrying its event ULID, the `check_id`
it references, a kind (`dispute` | `disposition`), timestamp, and payload.
Replay of a check is deterministic: the initial record, then its referenced
addenda in ULID order. One file per record keeps concurrent checks and late
addenda merging as distinct paths. A summary `NORTH-STAR.log` may be
*derived* from these records as a view; it is never the authority.

**5. Act — authority follows materiality, not verdict label.**

- *aligned*: resume work.
- Any change that would alter acceptance criteria, user-visible behavior, or
  a named deliverable is a **direction decision and goes to the operator
  before action — whatever the verdict was.** Only a same-surface internal
  reduction within existing acceptance criteria may be applied directly; if
  applied, append the what-and-why to the work item with the tracker's
  append-safe operation (in ABACUS: `br comments add` — `br update --notes`
  *replaces* the field).
- *right-goal-wrong-surface* and *orphaned* always stop and go to the
  operator with the case, verdict, and redirect verbatim.
- The working agent may dispute any verdict — the dispute goes to the
  operator with both positions and lands in the check's folded history as
  an addendum record (never in the immutable initial file). Never re-run
  the judge shopping for a better verdict.

## Boundaries

- Check mode never edits `NORTH-STAR.md`; revision is its own operator-only
  mode.
- Per check: one case; **at most one** judge context (a
  `capability_unavailable` check convenes none, and there is never a
  replacement judge); exactly one initial result record; zero or more
  immutable addenda. Bigger findings go to the operator as findings, not
  into an extended session.
- This skill mints no beads. If the operator asks for one, the full bar
  applies: fingerprint, dependencies, and acceptance criteria in the
  *initial* description (stock `br create` cannot set acceptance atomically),
  preserving the provider-returned lowercase `abacus-*` ID.

## Before relying on check mode — falsification fixture

Check mode is not trusted until a small pinned fixture proves: (1) a missing
judge capability fails closed without self-grading; (2) the judge receives no
parent turns and its payload-only instruction is present; (3) seeded cases
hit all four verdicts, including an overlap case resolved by the decision
order; (4) malformed judge output causes no action; (5) a material trim
reaches the operator before mutation; (6) two concurrent worktrees produce
distinct check records with no merge conflict; (7) a stored record replays
the thesis snapshot, case, result, rationale, dispute, and disposition via
the initial-record-then-addenda-in-ULID-order rule. Fixture passage is
recorded **bound to this skill's blob hash and the exact adapter/model/
tool-policy combination tested** — an untested combination leaves check mode
untrusted for that combination, which is the default state, not an error.
Pass records live as immutable files under `north-star-checks/fixture/`
keyed by that combination; a changed skill blob, adapter, model, or tool
policy must produce a lookup miss, never a stale pass.
