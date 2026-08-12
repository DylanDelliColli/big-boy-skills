---
name: council
description: Convene an adversarial, evidence-adjudicated review of a materially contested plan, design, or ADR using ephemeral Herdr panes (mixed Claude and Codex). Disagreements are settled by the cheapest discriminating observation — an existing probe where one exists, a throwaway spike where none does. Use only for a material contested decision or on explicit operator request ("convene the council", "/council"); ordinary review requests take an ordinary single-reviewer pass.
---

# Council

A council converts a contested plan into quantified knowledge: recorded
observations whose results adjudicated the argument, plus the plan amendments
and defects those results license. An **experiment is the cheapest
discriminating observation** — reading a type, running an existing test, one
command — and a throwaway spike is minted only when no existing observation
discriminates. Rhetoric that survives unprobed is a failure of the council.

The invoking agent is the **Lead**: Socratic moderator, holds no position,
and owns the run's resources. A Lead that starts advocating has joined the
council and must say so to the operator.

## Preflight — refuse to start rather than start dirty

All of these before creating anything; any failure stops the run:

1. `HERDR_ENV` is `1` (the session is under Herdr control).
2. Repo root resolved: `REPO="$(git rev-parse --show-toplevel)"` — never an
   assumed variable.
3. `herdr --version` recorded verbatim into the manifest (the subcommand
   form `herdr version` does not exist); this skill is written against
   v0.8.0 semantics.
4. A short **run id** minted (e.g. `c7k2`); all agent names are
   `council-<runid>-<lens>` (Herdr names: `[a-z][a-z0-9_-]{0,31}`, unique
   among live agents — the run id prevents collision with stale panes from a
   failed prior run).
5. Run directory `docs/council/<yyyy-mm-dd>-<slug>/` absent, or explicitly
   marked resumable.
6. **The review subject is frozen**: committed material → record the exact
   commit; uncommitted plan text → copy it into the brief and record its
   content digest. Current dirty paths are captured and excluded from
   council writes. Live-state probes in the brief are labeled *live
   observations* with time and provider version — they never redefine the
   frozen snapshot.
7. The **owner ledger** is initialized: an on-disk record (in the run
   directory) that every subsequent step appends to, with **explicit
   resource state transitions**: `intended` → `created` →
   `evidence_preserved` → `tip_sealed` → `worktree_removed` →
   `branch_deleted`, with the failure branch
   `preservation_failed/retained_for_operator`. (`worktree_removed` is
   terminal for a branchless resource; the run always creates run-unique
   branches — Herdr 0.8.0 exposes no detach flag on worktree create, so no
   detached plan exists to declare.) Before *every* mutating creation,
   append and durably flush a `creation_intent` naming a run-unique
   `--path`, `--branch`, `--label`, the frozen base, and the resource
   kind; append the returned IDs as a second transition. On an ambiguous
   result (server succeeded, response lost), reconcile **only the exact
   intended path/branch/label** against `herdr worktree list` and
   `git worktree list` — adopt a uniquely matching resource into the ledger,
   or stop for operator recovery. Entries are role-discriminated: reviewer
   entries carry agent name, kind, explicit model args, and the
   `agent start` result; spike entries carry the common worktree-ownership
   fields plus `assigned_agent`/pane — **no fabricated start result**.
   Teardown trusts only this ledger; anything not in it does not get
   touched.

## Phase 0 — the brief

Reviewers are fresh contexts; the brief is their world. Its gate is
executable: *a reader given only `brief.md` can state the decision under
review, name the frozen snapshot (commit/digest), run each probe and get the
predicted result, and name the bounds.* If a probe or bound is missing, the
brief is not done. Contents: the question (stated so a measurement could
settle it); the frozen plan (inline or by digest); the authority map with
LANDED / PLANNED / PROSE kept distinct; probes with expected results; bounds
and the settled decisions that are off the table.

## Phase 1 — spawn, isolate, dispatch

**Sizing.** Two panes — one Claude (`--model claude-sonnet-5` passed
explicitly), one Codex (exact model passed explicitly) — is the default:
one owns seams + necessity, the other cheapest-alternative + falsifiability.
Four panes only when the question genuinely spans four independent seams.
Record per-pane tokens, time, and decision-changing findings; pane counts
above two must keep earning their place.

**Independence is honest about its enforcement level.** For each reviewer,
create a clean checkout of the frozen snapshot (`herdr worktree create` from
the recorded commit, `--no-focus`, full response captured into the ledger),
and **validate it before dispatch**: clean tree, `HEAD` equal to the frozen
commit, branch/detached state matching the ledger. Each reviewer writes to a
**private output path inside its own checkout** plus one disposable private
scratch/build directory (compilers and probes need one — the first run
records the actual write set), and its prompt carries an explicit
allowlist: *only your findings file and your scratch dir; no edits to
reviewed files, no commits, no tracker mutations, no reading outside your
checkout.* Linked worktrees under one Unix user do **not** enforce read
isolation — so the round is called **"independent by instruction"** and
cross-reads are audited from tool logs in the first run. It may be called
**"blind"** only when reviewers run under a tested read boundary whose
denied cross-read is itself verified at preflight. The Lead's checkout is
for assembling and committing the run artifact only; it is never the
evidence surface.

**Agents must be started — a worktree's root pane is a shell, not a
reviewer.** For each reviewer, after the worktree response is parsed into
the ledger:

```sh
herdr agent start council-<runid>-<lens> --kind <claude|codex> --pane <root-pane-id> -- <explicit model args>
```

Record the start result in the ledger; only then enter dispatch. This is
also what makes the manifest's "exact model arguments" describe the process
that actually ran.

**Dispatch is submit-all, then wait-all** — `--wait` on prompt serializes the
council and multiplies anchoring and wall-clock:

```sh
herdr agent prompt <pane-id> "<brief + lens duty + private output path>"   # NO --wait, per pane
herdr agent wait <pane-id> --timeout 1800000                               # then wait each
```

Do not pass `--until idle`: an unfocused pane finishing background work
surfaces as `done`; the default wait matches idle, done, or blocked.
`blocked` is a *request*, not completion — read the pane, answer, wait
again. Handle `agent_prompt_stalled`, timeouts, and `unknown` explicitly. A
settled pane is not a completed finding: verify the findings file exists, is
nonempty, has the required structure, and has stopped growing. One
corrective prompt on failure; after that the pane is recorded as failed —
never silently scored as "no findings."

## Phase 2 — import, then cross-examine

The Lead imports every findings file into the run directory **before any
pane sees another's output**, recording each file's hash — the independent originals (call them "blind"
only when the preflight read-denial probe passed and `blind=true` is
recorded) are preserved verbatim and are never edited afterward — a
successful import-and-hash appends `evidence_preserved` to that reviewer's
ledger entry, which is what later licenses its checkout's removal;
adjudication outcomes are appended as linked revisions, so the record shows
how contested the round actually was. Then bounded Socratic rounds: pose the
question each pane's evidence puts under tension; answers cite evidence.
When two panes disagree on a probeable claim, the Lead freezes that thread
and asks first: *what existing observation discriminates?* Only when none
does is a spike minted.

## Phase 3 — spikes (when an experiment needs new code)

A spike is the smallest throwaway program distinguishing the positions,
assigned to the pane whose position it tests, with the opposing pane
reviewing the harness before it runs — opposing review *reduces* harness
bias; record harness challenges rather than claiming the rig is canceled.
Preregister what outcome supports which position. Timebox 30 minutes; an
overrun means tool failure, a bad harness, or an oversized question —
diagnose which before extending anything.

Spike lifecycle, all steps mandatory:

1. `creation_intent` to the ledger, then `herdr worktree create` from the
   frozen base with the intended run-unique path/branch/label, `--no-focus`;
   append the returned workspace id, path, branch, tab, and root pane as the
   `created` transition (spike entries record `assigned_agent`/pane — no
   agent is started in the spike root pane).
2. Hand the exact path to the assigned pane **with a recorded, temporary
   grant extending both read and write access to that one owned spike path,
   for that experiment only** — the standing no-reading-outside-your-checkout
   rule stays active for every other path; an access expansion is explicit
   or it does not exist. The opposing reviewer inspects the harness from an
   inline copy by default; if it must inspect by path, it gets its own
   recorded read-only grant to the same spike path. Record every grant in
   the experiment file.
3. Preserve the evidence: inline the essential harness, the command, exit
   status, and raw result (hashed) into `experiments/<n>-<slug>.md` — a
   spike that isn't recorded didn't happen. Success appends
   `evidence_preserved`. **Failure appends
   `preservation_failed/retained_for_operator`: stop the spike agent if
   necessary, retain the exact checkout and branch untouched, and write
   their recovery coordinates into the incomplete run record — no removal
   of any kind, in Phase 3 or in final teardown.**
4. Seal the tip: resolve the spike branch's final ref and object id and
   append `tip_sealed`; validate the preregistered reachability rule now
   (no kept branch reaches spike commits). A branch forbidden to commit
   seals its unchanged base.
5. Remove exactly the owned workspace — **legal only from `tip_sealed`**:
   `herdr worktree remove --workspace <owned-id> --force` (spikes are dirty
   by design; unforced removal will refuse), verify it is no longer listed,
   and append `worktree_removed` — final teardown skips anything already in
   that state.

## Phase 4 — synthesis and output

`record.md` in the run directory: the question and the answer the evidence
supports, citing experiments by number; plan amendments as concrete edits;
**unresolved forks to the operator with both positions and their evidence**
— the Lead never casts a tiebreak. The committed run directory additionally
carries a **run manifest**: frozen snapshot ids, full reviewer prompts,
Herdr/Claude/Codex versions, exact model args, all ledger ids, start/end
times and terminal states, experiment commands and raw-output hashes,
findings-file hashes, and teardown outcomes.

**Tracker discipline (hard rule).** No note beads, no communication beads,
no "council says" beads. A defect mints a bead only with the full bar —
fingerprint, dependencies, acceptance — in the *initial* description (stock
`br create` cannot set acceptance atomically), preserving the returned
lowercase `abacus-*` id. On the first live run, record bead-worthy defects
in `record.md` and let the operator mint them afterward.

**The commit is the last act, not part of synthesis.** Order: import and
hash findings → synthesize → finally-style teardown (below) → append every
terminal outcome to the manifest → validate the manifest is complete → then
make the **single artifact commit** of the run directory. A commit made
before teardown cannot contain the outcomes its manifest requires. Failure
paths commit nothing complete: they leave an explicitly incomplete run
record marked for operator recovery, which may not claim council evidence.
The committed directory is the binding artifact; a future knowledge store
indexes its paths and hashes — it never decomposes or replaces it without a
lossless round trip.

## Termination and teardown

A round that produces no defect, no resolved decision, and no new experiment
**ends the council immediately** — the two-consecutive-rounds phrasing in
repo doctrine is a postmortem diagnostic, not a license to run a second
empty round. The record states whether the review completed or exhausted.

Teardown is finally-style and runs on success, timeout, failed panes, and
partial spawn alike, walking only the owner ledger's state machine, in this
order:

1. For each owned worktree workspace: destructive removal is **legal only
   from `evidence_preserved` or `tip_sealed`** (or an explicit
   operator-authorized discard). Seal the tip if not yet sealed, then
   `herdr worktree remove --workspace <id> --force` **first**, letting it
   close its own panes; verify the checkout and workspace are absent;
   append `worktree_removed`. An entry still in `created` or in
   `preservation_failed` is **retained**: no removal, recovery coordinates
   written to the incomplete run record, surfaced to the operator — a
   deliberately surviving resource is a recorded outcome, not a leak. For
   an entry already in `worktree_removed`, verify absence **without issuing
   a second remove** — already-absent is a verified terminal state, not an
   error.
2. `pane close` only owned panes **not consumed by a worktree removal**
   (never close a worktree's last pane before its removal — Herdr's
   last-pane path can collapse the workspace and strand the checkout on
   disk with an invalidated workspace id).
3. For each recorded owned ephemeral branch: prove the exact
   `refs/heads/<recorded>` was created by this run, is not checked out
   anywhere, is not shared, and still points at its **sealed** tip — Herdr's
   worktree removal deletes the checkout but *not* the ref, so "deleted"
   spike commits stay reachable until this step — then delete with one
   explicit delimiter-safe command (`git branch -D -- <recorded>`), verify
   the ref is absent, and append `branch_deleted`.
4. Verify owned tabs are gone.

**Never infer, glob, or touch an id the ledger does not contain.** Record
every teardown outcome in the manifest — the commit that needs those
outcomes happens after this, per Phase 4.

## First live run — acceptance protocol

The corrected skill's first real council doubles as its acceptance test.
Record at minimum: preflight refusal outside Herdr and on an unfrozen
subject; all prompts submitted before any wait; one `blocked` transition
answered and re-waited; one settled-without-file pane caught by the
completion gate; no writes outside allowlisted paths; no cross-reading
before import; one dirty spike force-removed by exact workspace id and
verified absent; cleanup after a partial spawn closing only owned ids;
then two cleanup subcases run and reported **separately** — *(a)
happy-path:* after teardown, both reviewer workspaces absent, every
run-created branch absent, and no pre-existing ref changed (the direct
falsifiers for the ownership lifecycle); *(b) preservation-failure:* one
forced findings-copy or hash failure, whose selected checkout and branch
are **deliberately retained** with recovery coordinates recorded — retention
here is the pass condition, not a cleanup miss; the committed run directory
complete; per-pane marginal yield (does pane three
or four earn its cost?). An ownership, isolation, dispatch, or teardown
failure aborts the run and its record may not claim council evidence; an
operational-debt failure is recorded and fixes the skill afterward.
