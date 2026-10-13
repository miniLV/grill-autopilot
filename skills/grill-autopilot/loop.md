# Implement loop

The tickets form a task graph. The **frontier** is every ticket whose status is `ready-for-agent` and whose `Blocked by` tickets are all `done`. Keep up to `concurrency` workers busy, and refill from the frontier as soon as a ticket finishes; do not wait for a whole round.

The planner keeps only pointers and **verdicts** in its context: ticket paths, branch names, `PASS`/`FAIL` lines. Diffs and test logs stay inside the subagents.

## Setup

- **Names**: default integration branch `autopilot/<slug>/integration`; ticket branches `autopilot/<slug>/tickets/<NN>`. A unique run ID identifies this execution independently of the feature slug. Keep the chosen refs, paths and resolved base SHA with that run's details.
- **Worktree root**: `<repo-parent>/<repo-name>.autopilot-worktrees/`. Integration path `<root>/<slug>-integration`; ticket paths `<root>/<slug>-<NN>`.
- **Branch preflight** (read-only, before any branch or worktree creation):
  1. Resolve the selected base with `git rev-parse --verify --end-of-options '<base>^{commit}'`. Save its output as `<base-sha>`; stop if it fails. All creation uses the saved SHA, even if the base ref later moves.
  2. Run `git check-ref-format --branch '<actual-branch>'` for the integration branch and every ticket branch. Require success and output equal to the literal requested name; do not accept Git's previous-checkout shorthand as a branch name. Compare all planned names with each other: equal names or either name followed by `/` as a prefix of the other are conflicts, including a custom integration name.
  3. Read `git for-each-ref --format='%(refname) %(objectname)' refs/heads/` (includes packed refs) and strip the literal `refs/heads/` prefix when comparing branch names. Compare each existing branch with every planned branch: equality, an existing ancestor prefix, or an existing descendant prefix is a conflict. Also reject any residual branch at `autopilot/<slug>` or below `autopilot/<slug>/`, even if its ticket is outside the new set. For `slug=demo`, an old `autopilot/demo` blocks the entire new run.
  4. Read `git worktree list --porcelain` and inspect canonical target paths on disk. A registered target, a path already occupied by a file/directory/symlink, or residual same-slug run state is a conflict even when its branch is absent. Report the conflicting ref/path and its SHA where available.
  5. On any failure, stop before creation and preserve all refs, worktree registrations and file content. Existing state is reusable only when the user explicitly resumes the same run and ownership, active processes, worktrees and commits have been reconciled. A matching slug alone is insufficient; unresolved state stops resume. Do not reset, delete or prune the conflict.
- **Integration worktree**: after the complete preflight passes, run `git worktree add <root>/<slug>-integration -b <integration-branch> <base-sha>`. Every merge and every suite run happens here. Recheck the target ref/path immediately before each creation; for later dispatches, check the new target's name, ref prefix conflicts and occupied path, while retaining the already recorded integration/ticket state of this run. If Git reports a race or another creation error, stop, report and retain any state already created by this run for reconciliation.
- **Ticket status**: `ready-for-agent` → `claimed` → `in-review` → `done` or `blocked`. Update the `Status:` line in the ticket file and append one line per event under `## Comments` (attempt, role, model, verdict).

## Each dispatch

1. **Pick.** Take frontier tickets in number order. Skip a ticket whose Files overlap the Files of any `claimed` or `in-review` ticket. Stop at `concurrency` running workers.
2. **Dispatch.** Recheck the new ticket's target as Setup describes, save the starting integration SHA, then create its worktree at that SHA and spawn a worker in the background (see [runtimes.md](runtimes.md)). A retry or explicit reconciled resume uses its recorded worktree instead of creating another one. Set the ticket to `claimed`. Send the worker packet below.
3. **Review.** When the worker reports `DONE`, set the ticket to `in-review` and spawn a reviewer with the reviewer packet below. When it reports `STUCK`, treat that as a `FAIL` with its reason.
4. **On PASS**:
   - In the integration worktree, run `git merge --no-ff <ticket-branch>`, then the ticket's Verify commands and typecheck.
   - If the merge conflicts or a check goes red, run `git merge --abort` (or `git reset --hard ORIG_HEAD` after a red check) and treat it as a `FAIL` with that reason.
   - Otherwise remove the ticket worktree, delete the merged branch, and set the ticket to `done`.
5. **On FAIL**, count the ticket's attempts:
   - While attempts ≤ `retry.worker`, send a worker back to the same worktree with the reviewer's reasons appended to the packet.
   - Then, for up to `retry.escalate` more attempts, use the escalate role instead.
   - After that, set the ticket to `blocked` with the last reasons. Remove its worktree but keep its branch for the human.
   - Every ticket that is blocked by a blocked ticket, directly or not, also becomes `blocked`, with the reason "upstream <NN> blocked".
6. **Refill.** After every `done` or `blocked`, recompute the frontier and dispatch again.

The loop ends when no ticket is `ready-for-agent`, `claimed` or `in-review`. Then run the full suite and typecheck in the integration worktree.

## Worker packet

Fill the placeholders and send this as written:

```text
You are a worker. Implement exactly one ticket.
Ticket: <ticket path>    Spec: <spec path>
Worktree: <path>    Branch: <ticket-branch>    Integration branch: <integration-branch>
Starting integration SHA: <integration-sha>
<Reviewer reasons from the last attempt, if any>

1. Confirm the assigned branch, worktree and starting integration SHA match the planner's recorded state. If they differ or unexpected edits are present, preserve the worktree and report STUCK; the planner reconciles it before retrying.
2. Read the ticket and the files under Context.
3. Read and follow the tdd skill at <tdd SKILL.md path>, at the ticket's seam. The seam is already agreed, so do not ask the user to confirm it. For each Example, write a test asserting its literal expected output, see it fail, then make it pass.
4. Edit only the paths under Files. Run every Verify command until all pass.
5. Commit on <ticket-branch>, then merge the <integration-branch> tip into it and rerun Verify.
6. Reply with one line only:
   DONE <commit sha> <changed paths, comma-separated>
   or STUCK <one-sentence reason>
```

## Reviewer packet

```text
You are a reviewer. Gate one ticket. Read; do not edit anything.
Ticket: <ticket path>    Worktree: <path>
Diff: git -C <path> diff <integration-branch>...<ticket-branch>

Check each item:
1. Every Acceptance item is met.
2. Every changed path is listed under Files.
3. The tests assert the ticket's Examples with the same literal values. No assertion is weakened, skipped or deleted.
4. Every Verify command passes when you run it in the worktree.
5. Nothing outside the ticket's scope changed.

Reply with one line only:
PASS
or FAIL: <numbered reasons, under 120 words>
```
