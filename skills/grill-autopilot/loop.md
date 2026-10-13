# Implement loop

The tickets form a task graph. The **frontier** is every ticket whose status is `ready-for-agent` and whose `Blocked by` tickets are all `done`. Keep up to `concurrency` workers busy within host capacity for **all** child roles, following [runtimes.md](runtimes.md#capacity-and-release-before-review). Waiting reviews take priority over refilling workers; an agent result alone does not free its slot.

The planner keeps pointers and **verdicts** in its context; the durable run record holds identifiers and evidence paths. Diffs and test output remain in captured logs.

Before preparation/dispatch and on any error or stop, read [failures.md](failures.md). It is the single authority for logical attempts, business/infrastructure/final counters, finite exits from pending statuses, dependency blocking and result/brief rules. Adapter lifecycle facts remain in runtimes.md.

An explicit `/grill-autopilot resume <run-id>` first follows [resume.md](resume.md), including already-merged evidence checks. Re-enter this loop only at the reconciled stage; a pending status or existing branch alone never authorizes replay.

## Setup

- **Run data**: before any tracker write or packet, follow [run-record.md](run-record.md) to capture the original checkout baseline, declare owned tracker files and freeze inputs. The planner is the only tracker/record writer. Persist intended operations before host/Git calls and append observations afterward; preserve that evidence for the brief.
- **Names**: default integration branch `autopilot/<slug>/integration`; ticket branches `autopilot/<slug>/tickets/<NN>`. A unique run ID identifies this execution independently of the feature slug. Keep the chosen refs, paths and resolved base SHA with that run's details.
- **Worktree root**: `<repo-parent>/<repo-name>.autopilot-worktrees/`. Integration path `<root>/<slug>-integration`; ticket paths `<root>/<slug>-<NN>`.
- **Branch preflight** (read-only, before any branch or worktree creation):
  1. Resolve the selected base with `git rev-parse --verify --end-of-options '<base>^{commit}'`. Save its output as `<base-sha>`; stop if it fails. All creation uses the saved SHA, even if the base ref later moves.
  2. Run `git check-ref-format --branch '<actual-branch>'` for the integration branch and every ticket branch. Require success and output equal to the literal requested name; do not accept Git's previous-checkout shorthand as a branch name. Compare all planned names with each other: equal names or either name followed by `/` as a prefix of the other are conflicts, including a custom integration name.
  3. Read `git for-each-ref --format='%(refname) %(objectname)' refs/heads/` (includes packed refs) and strip the literal `refs/heads/` prefix when comparing branch names. Compare each existing branch with every planned branch: equality, an existing ancestor prefix, or an existing descendant prefix is a conflict. Also reject any residual branch at `autopilot/<slug>` or below `autopilot/<slug>/`, even if its ticket is outside the new set. For `slug=demo`, an old `autopilot/demo` blocks the entire new run.
  4. Read `git worktree list --porcelain` and inspect canonical target paths on disk. A registered target, a path already occupied by a file/directory/symlink, or residual same-slug run state is a conflict even when its branch is absent. Report the conflicting ref/path and its SHA where available.
  5. On any failure, stop before creation and preserve all refs, worktree registrations and file content. Existing state is reusable only when the user explicitly resumes the same run and ownership, active processes, worktrees and commits have been reconciled. A matching slug alone is insufficient; unresolved state stops resume. Do not reset, delete or prune the conflict.
- **Integration worktree**: after the complete preflight passes, run `git worktree add <root>/<slug>-integration -b <integration-branch> <base-sha>`. Every merge and every suite run happens here; source changes stay in dedicated worktrees, while the original checkout holds only owned run data. Recheck the target ref/path immediately before each creation; for later dispatches, check the new target's name, ref prefix conflicts and occupied path, while retaining the already recorded integration/ticket state of this run. If Git reports a race or another creation error, stop, report and retain any state already created by this run for reconciliation.
- **Ticket status**: `ready-for-agent` → `claimed` → `in-review` → `done` or `blocked`. Only the planner updates the mutable source ticket's Status/Comments and mirrors its events in the run record. The dispatched task snapshot stays fixed.

### Environment preparation gate

The planner prepares **each** newly created integration/ticket worktree before dispatching implementation; ignored dependencies in the original checkout are not inherited. In that worktree's canonical directory:

1. Save the intended initialization choice, preparation attempt identity/start/deadline and evidence destination in the run record before preparation starts, following runtimes.md. Use bounded host waits and check the remaining deadline for preparation commands too. Run the agreed initialization command(s) in order; explicit `None` skips only initialization, not baseline checks. Installing the dependencies already pinned by the existing lockfile is preparation. Changing dependency declarations or the lockfile is implementation and still requires ticket Files/scope authorization; preparation does not grant it.
2. After initialization succeeds, run the stage's baseline: integration uses the full suite and applicable typecheck; a ticket uses its agreed existing seam/Verify baseline and applicable typecheck at its starting integration SHA. A new test file that does not exist yet uses the agreed existing baseline command, recorded during grill. Preserve `N/A` and its reason for genuinely inapplicable checks; a missing tool, credential or dependency is an error. Applicable behavior checks remain mandatory.
3. Record commands, canonical cwd, starting SHA, initialization outputs/generated paths, exit codes, baseline results and log pointers through run-record.md's command/preparation fields. Only successful initialization (or explicit `None`) plus passing applicable baselines marks that worktree ready for implementation. Its worker implementation counter remains unchanged until implementation starts.
4. Initialization failure, missing credentials and pre-existing baseline failure are **environment errors**, separate from implementation `FAIL`. Preserve the worktree and command evidence and follow failures.md's environment exit; an integration preparation error stops new implementation dispatch. Do not ask a worker to repair business code or spend implementation retries on this gate. An explicit repaired continuation reruns the gate under the failure protocol; this gate adds no retry budget.

## Each dispatch

1. **Pick.** Take frontier tickets in number order. Skip a ticket whose Files overlap the Files of any `claimed` or `in-review` ticket. Prioritize queued reviews, then respect both `concurrency` running workers and confirmed free all-role host slots. Unknown capacity uses one child at a time. Capacity rejection queues the role until new availability evidence; unresolved release stops new dispatch as runtimes.md defines.
2. **Dispatch.** Recheck the new ticket's target as Setup describes, save the starting integration SHA, then create its worktree at that SHA and pass its environment gate before spawning a worker (see [runtimes.md](runtimes.md)). A retry or explicit reconciled resume uses its recorded worktree instead of creating another one; check its recorded preparation and rerun the gate if the environment changed. Save capability/route/model facts, logical attempt/budget and intended counter changes before launch and retain the attempt deadline set before preparation; a prepared worktree does not reset that deadline. Set the ticket to `claimed`. Send the worker packet below only through the permitted adapter route; capture identity, actual start/counter outcome and observations afterward. Launch errors and capacity queues follow failures.md instead of repeated spawn.
3. **Review.** When the worker or escalate role reports `DONE`, capture its full result and model status, set the ticket to `in-review`, then confirm inactivity and release/availability through runtimes.md before starting the reviewer. Save the review's own logical attempt/deadline before its call; queue it ahead of new workers and count it against host slots. A mismatch cannot pass as DONE/PASS. Apply the same bounded wait, result, stop and release semantics to reviewers, escalate roles and final-review seats. Classify `ENVIRONMENT_ERROR`, `STUCK`, reviewer timeout/invalid/unobservable result and scope expansion through failures.md; failed review infrastructure must reach a terminal exit rather than remain `in-review` or charge a business retry.
4. **On PASS**: follow [integration.md](integration.md) to qualify the fixed review base/candidate, then serialize **merge → Verify → record result**. Queue other PASS results until that transaction completes or safely rolls back; an uncertain transaction stops further integration. Only the verified current integration SHA permits `done`, followed by the separate retention/cleanup gate below. Use that reference for merge conflicts, red checks, artifact ownership and exact rollback; a mutable branch name or earlier PASS never bypasses its gate.
5. **On FAIL/error.** Apply failures.md's event decision and counter limits. For a permitted business retry, append the last reasons and preserve previous HEAD, tracked/untracked state and diagnostics in the same worktree; reconcile ownership/activity/capacity before continuing. After exhaustion, block and propagate dependencies. Environment, route and infrastructure errors use their own exits; they do not silently become implementation FAIL.
6. **Refill.** After every completed role, reconcile its activity/capacity, handle queued reviews first, then recompute the frontier and dispatch only into confirmed available capacity. Record retained identities separately from released execution slots.

The loop ends when no ticket is `ready-for-agent`, `claimed` or `in-review`, including the terminal transitions on a handled stop. When safe, run bounded full suite/typecheck checks in integration and record their results, retaining agreed `N/A` reasons. Pass those results, including red, to final review/closeout as failures.md defines; safe resource handling and the brief do not wait for green.

## Retention and cleanup gate

- **Blocked/failed handoff:** retain the entire ticket worktree and branch, including tracked, untracked and ignored files, along with attempt/log evidence. A branch contains committed objects, not the uncommitted worktree. Stop this run's still-active agents/processes that could write there using the runtime's available stop/liveness tools before handing it back. If stop/activity cannot be confirmed, retain the possibly active worktree and disclose that fact; never stop unrelated agents. The planner records the canonical path, branch/HEAD, dirty inventory, diagnostics and activity state in the run record and brief.
- **Unsafe resources:** failures.md's unconfirmed-stop exit stops all cleanup, including otherwise eligible ticket cleanup, until a later explicit reconciliation establishes safety.
- **Successful cleanup:** require all four facts immediately before deleting anything: the ticket has a recorded verified integration result and its current branch tip is merged into integration (`git merge-base --is-ancestor <ticket-branch> <integration-branch>`); its canonical worktree/branch registration matches this run's recorded ownership; every agent/process using it is inactive; and `git -C <ticket-worktree> status --porcelain --untracked-files=all` is empty. A missing/unknown fact, active agent, ownership mismatch or dirty state means skip deletion and record the reason. A retry or resumed attempt keeps its existing state; no cleanup/reset is used to manufacture a clean start.
- **Delete only the eligible ticket:** save the cleanup intent/evidence in the run record, run `git worktree remove "<canonical ticket-worktree>"`, and only after that succeeds run `git -C "<canonical integration-worktree>" branch -d "<recorded ticket-branch>"`. Use the actual recorded branch (default `autopilot/<slug>/tickets/<NN>`). Keep the integration worktree for inspection and the tracker/log evidence for the brief.
- **Cleanup failure:** save the command, exit code, retained paths/refs and diagnostic as a cleanup warning and continue to the brief. Use ordinary non-force commands; preserve a refusal instead of forcing removal/deletion or unlocking someone else's worktree. If worktree removal failed, retain the branch; if only branch deletion failed, report that remaining ref. A warning or skipped cleanup does not erase the ticket's verified result or change `done` to `blocked`.

## Worker packet

Fill the placeholders with canonical absolute paths from the run record, then send this as written. Both packets use the same frozen spec/task and saved hashes; companion and external Context pointers are expanded before dispatch.

```text
You are a worker. Implement exactly one ticket.
Task snapshot: <canonical absolute frozen ticket path>    Spec snapshot: <canonical absolute frozen spec path>
Input SHA-256: task=<hash> spec=<hash>
Mutable tracker ticket (read only): <canonical absolute source ticket path>
Run record (read only): <canonical absolute run.md path>
Companions: <canonical absolute required SKILL.md paths>
External/run Context: <canonical absolute pointers or None>
Log capture: <canonical absolute log path; planner/host writes>
Worktree: <canonical absolute path>    Branch: <ticket-branch>    Integration branch: <integration-branch>
Starting integration SHA: <integration-sha>
Preparation evidence: <canonical absolute record/log pointers for this worktree and starting SHA>
Initialization choice: <agreed commands or explicit None>
Baseline commands: <agreed existing baseline and applicable typecheck, or N/A with reason>
Attempt context: <new/retry/explicit resume>    Previous attempt evidence: <canonical pointers or None>
<Reviewer reasons from the last attempt, if any>

1. Confirm the assigned worktree/branch and this run's ownership. For a new worktree, verify its clean starting state at the recorded integration SHA. For retry/explicit resume, verify the recorded previous HEAD and tracked/untracked state and continue known prior-attempt edits; do not reset it to the current integration tip. Any unexpected state is preserved and reported STUCK for planner reconciliation.
2. Verify the snapshot hashes and read the frozen task/spec; resolve repository Files/Context under the assigned worktree. Report missing/changed inputs or scope expansion to the planner. The mutable tracker and run record are read only.
3. Confirm this worktree's initialization and applicable baseline checks passed at the recorded starting SHA before TDD. If evidence is absent/stale or an environment failure appears, preserve it and report ENVIRONMENT_ERROR; stop implementation rather than fixing business code. Once the gate is satisfied, read and follow the tdd skill at <canonical absolute tdd SKILL.md path>, at the agreed seam. The seam is already agreed; do not ask to confirm it. For each Example, write a test asserting its literal expected output, see it fail, then make it pass.
4. Edit only the paths under Files. Run applicable Verify commands until all pass; retain agreed N/A reasons. Preparation installs existing locked dependencies; dependency declaration changes still require this ticket's authorization.
5. Commit on <ticket-branch>. Follow <canonical absolute integration.md path> under “Worker tip merge”: save the exact current integration tip and your pre-merge HEAD/state before merging that SHA into this ticket; capture/abort a conflict safely and report STUCK. After a successful merge, rerun Verify, require unchanged clean HEAD/content, and return that **post-tip-merge candidate SHA**. Every changed candidate goes back through review.
6. Reply with one line only:
   DONE <commit sha> <changed paths, comma-separated>
   or ENVIRONMENT_ERROR <command and exit code/missing prerequisite reason>
   or STUCK <one-sentence reason>
```

## Reviewer packet

```text
You are a reviewer. Gate one ticket. Read; do not edit anything.
Task snapshot: <canonical absolute frozen ticket path>    Spec snapshot: <canonical absolute frozen spec path>
Input SHA-256: task=<hash> spec=<hash>
Mutable tracker ticket (read only): <canonical absolute source ticket path>
Run record (read only): <canonical absolute run.md path>
Companions: <canonical absolute required SKILL.md paths>
External/run Context: <canonical absolute pointers or None>
Log capture: <canonical absolute log path; planner/host writes>
Worktree: <canonical absolute path>
Branch: <ticket-branch>
Review base SHA: <fixed integration tip SHA from worker tip-merge evidence>
Candidate SHA: <immutable worker DONE SHA after its tip merge>
Review evidence: <canonical declared output/log path; planner/host captures>
Diff: git -C "<canonical absolute worktree path>" diff <review-base-sha>...<candidate-sha>

Verify snapshot hashes; use the frozen task/spec for requirements. Resolve repository Files/Context under the assigned worktree. Report events to the planner; tracker and record are read only.
Resolve both supplied SHAs as commits and require the base to be an ancestor of the candidate. Require worktree HEAD and branch tip equal to the candidate, clean checked content and no active/unknown writer before checks and again afterward. Use the SHA diff above, never live refs. Save exact base/candidate, commands/cwd/exits, check output, N/A reasons and before/after HEAD/status in the captured evidence. Missing evidence, movement or dirty content cannot receive PASS; preserve and report it.

Check each item:
1. Every Acceptance item is met.
2. Every changed path is listed under Files.
3. The tests assert the ticket's Examples with the same literal values. No assertion is weakened, skipped or deleted.
4. Every applicable Verify command passes when you run it in the worktree; any N/A has the reason agreed in grill.
5. Nothing outside the ticket's scope changed.

Reply with one line only:
PASS <reviewed candidate SHA> <canonical review evidence path>
or FAIL: <numbered reasons, under 120 words>
```
