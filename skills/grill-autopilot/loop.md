# Implement loop

The tickets form a task graph. The **frontier** is every ticket whose status is `ready-for-agent` and whose `Blocked by` tickets are all `done`. Keep up to `concurrency` workers busy, and refill from the frontier as soon as a ticket finishes; do not wait for a whole round.

The planner keeps only pointers and **verdicts** in its context: ticket paths, branch names, `PASS`/`FAIL` lines. Diffs and test logs stay inside the subagents.

## Setup

- **Worktree root**: `<repo-parent>/<repo-name>.autopilot-worktrees/`.
- **Integration worktree**: `git worktree add <root>/<slug>-integration -b <integration-branch> <base>`. Every merge and every suite run happens here, so the user's own checkout never changes.
- **Ticket status**: `ready-for-agent` → `claimed` → `in-review` → `done` or `blocked`. Update the `Status:` line in the ticket file and append one line per event under `## Comments` (attempt, role, model, verdict).

## Each dispatch

1. **Pick.** Take frontier tickets in number order. Skip a ticket whose Files overlap the Files of any `claimed` or `in-review` ticket. Stop at `concurrency` running workers.
2. **Dispatch.** Spawn a worker in the background, in its own worktree on the integration branch tip (see the runtime section in [runtimes.md](runtimes.md)). Set the ticket to `claimed`. Send the worker packet below.
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
<Reviewer reasons from the last attempt, if any>

1. Confirm the worktree is based on <integration-branch>; if not, run `git reset --hard <integration-branch>`.
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
