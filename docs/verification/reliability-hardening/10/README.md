# Ticket 10: final SHA decides delivery

Scope: approved D10 final review/correction gate. Branch `codex/reliability-hardening/tickets/10` started clean at integration `5ac4a944ffe3c04962b0e72fc516d707161afbf1`; blocker 09 was done. Client date: 2026-10-14, Asia/Shanghai. Baseline inspection timestamp: `2026-10-13T17:35:11Z` (actual UTC).

The approved seam is skill-run input → Git/worktree state, ticket state and brief. [scenarios.md](scenarios.md) was written with the baseline RED gaps before product edits, then manually walked against the revised contract. Its four tables use literal synthetic SHA identities and observed-by-protocol counts, check bindings, both-axis verdicts and one terminal result each. They are **manual protocol evidence**, not executed model reviews or a full-suite pass.

## Acceptance evidence

| Acceptance | Manual verification result |
| --- | --- |
| Every final correction is reviewed again | Table 2: green suite after weakened assertions still gets Standards/Spec FAIL at the new SHA. Both rounds rerun full suite/applicable typecheck and both axes. Table 3 also reviews both changed SHAs. |
| Budget is two correction rounds, accurately counted | Tables 2/3: initial review F=0, round 1 F=1, round 2 F=2, no third call; failed with remaining findings. Table 1: no findings/green checks, F=0. Started correction charges are separate from ticket escalate and same-attempt infrastructure extras. |
| Current tip equals review and check identities | Table 4: old evidence becomes historical when tip advances; delivery requires checks and both axes on the new exact SHA against the same saved base. SHA/content rechecks also reject dirty or unexplained movement. |
| Remaining findings and blocked scope are distinct | Table 3: B's known blocked requirement stays undelivered; unrelated C remains a finding and makes the result failed. With C absent and current checks/both axes PASS, A done/B blocked qualifies partial under failures.md. |

Manual GREEN results: table 1 **success/0 fixes**; table 2 **failed/2 fixes**; table 3 **failed/2 fixes**; table 4 **success/0 fixes after new-tip requalification**. Intermediate stale evidence never authorizes delivery. The final-red variant in table 3 independently closes failed. Agreed typecheck N/A retains its reason; unavailable checks/review never become PASS. Unsafe/unknown resources stop further roles and retain work through the existing authority.

[final-review.md](../../../../skills/grill-autopilot/final-review.md) is the single sequence authority. The main skill points to it; failures owns counters/results, runtime owns lifecycle, integration owns check-artifact safety, resume preserves counts/deadlines and run-record stores exact check/axis histories plus invalidations. Config adds `retry.final_review: 2`. Ticket 07 evidence has a brief historical note; its original one-fix observations/logs remain intact.

## Reproduce verification

From this worktree, manually follow each scenario's successive rows through final-review.md, failures.md's counters/result table and run-record.md's closeout fields. Check the SHA/base in each command/review, current versus historical evidence, spent round count, remaining findings and blocked requirements before choosing the result. This is the ticket Verify; no shadow scheduler or prose-string test framework was added.

Read-only initial commands (each exit 0):

```sh
git status --short
git branch --show-current
git rev-parse HEAD
git rev-parse codex/reliability-hardening/integration
cat .scratch/reliability-hardening/issues/09-sha-bound-integration.md
date -u +%Y-%m-%dT%H:%M:%SZ
```

Status was empty; both HEAD and integration resolved to the baseline above; 09's Status was done. After edits, run `git diff --check` and a local Markdown link-target existence check, inspect all new files, commit the product/evidence changes, merge the resolved integration tip into the ticket branch and repeat the manual Verify/diff check on that candidate. These structural checks supplement the manual decisions.

Observed pre-commit verification at `2026-10-13T17:38:38Z`: all four tables manually followed to the unique results above; `git diff --check` exit **0**. Inline `python3` using `pathlib.Path.exists()` for relative Markdown link targets exit **0**: **57** targets across **11** product/evidence files. The script checks file existence only, not protocol wording or scheduler behavior. New files and the complete diff were inspected; old one-correction statements remain only in historical ticket 07 evidence.

## Limits

No production suite/typecheck, role launch, cancellation or real two-axis model review was run. Runtime obedience, model/effort facts, capacity release and actual success/failed/resume outcomes await ticket 13; these four tables do not claim end-to-end verification. Tracker/spec/index, global/plexus/upstream files and role defaults are untouched; no push or PR.
