# Ticket 09 verification

Approved seam: one skill run's input → Git/worktree facts, ticket status and brief. This repository delivers a Markdown protocol. [experiment.py](experiment.py) performs fresh real Git/check experiments with stdlib, temporary repositories and 30-second subprocess bounds. [experiment.log](experiment.log) retains literal commands, canonical cwd, actual UTC timestamps, SHAs, exits, contents/hashes, conflict output and state observations. PASS/done/reject/queue/failed/STUCK decisions are **manual protocol rehearsals**, not a production executor or actual model verdicts.

## RED before edits

Assigned ticket branch was clean at `bf59249a6a74f2191890ecad5245eb2cefea6445`; blockers 05/07 were complete in the supplied approved packet. Baseline loop.md accepted bare PASS, diffed live integration/ticket refs, merged the ticket branch and used `git reset --hard ORIG_HEAD` after a red check. The literal stale-PASS and precise-rollback examples therefore had no valid protocol gate. This is a **manual protocol RED**, not a failing executable product test. Each experiment independently asserts Git facts consumed by the revised protocol, without matching prose strings.

## Rehearsed acceptance

The manual planner follows [integration.md](../../../../skills/grill-autopilot/integration.md), with packets in [loop.md](../../../../skills/grill-autopilot/loop.md), fields in [run-record.md](../../../../skills/grill-autopilot/run-record.md) and existing failure/runtime/recovery authorities.

| Literal input / actual Git facts | Manual protocol output | Evidence |
| --- | --- | --- |
| A qualified PASS; merge includes A; Verify checks literal `A accepted` and exits 0 at unchanged clean SHA | Record checks/result, then A done; release transaction afterward | Real merge, ancestry, command exit and before/after state; PASS/done manual |
| A already done; B merge includes `B rejected`; Verify exits 1; ORIG_HEAD deliberately points to original base rather than B pre-merge SHA | B never done; reset only to recorded pre-B SHA | Exact SHA/ref/status/content equality to accepted A state; A ancestry passes, B inclusion exits 1; B worktree and failed merge commit remain |
| Failed B check produces predeclared absent `known-output.txt` with literal owned content | Capture hash/state, remove only that exact artifact, qualify clean state and roll back B | Actual targeted unlink plus exact restored A state; ownership/no-writer premise manual |
| Same known output plus unrecorded `user-notes.txt` containing `unknown user work` | Clean only qualified known output; failed brief; preserve unknown file and merged HEAD; no reset/clean | Unknown literal content and full retained state equality; decision manual |
| Same known output plus `shared.txt` changed to `unknown tracked user work` | Failed; retain tracked edit, merged HEAD and diagnostics | Actual tracked diff/hash/content preserved; no reset |
| PASS for A; same ticket branch advances to B | Reject stale PASS; B needs review before merge | Real unequal commits; fixed SHA diff still shows A; integration state unchanged |
| Candidate HEAD unchanged but uncommitted content moves | Reject PASS, preserve dirt | Real unchanged HEAD plus dirty diff; integration unchanged |
| A/C PASS at same fixed base; independent candidates | A merge → Verify → record done, then C uses current post-A SHA as pre-merge base | Real sequential merges, checks and ancestor proof for both; queue/order/done are manual, not a scheduler test |
| Worker merges independently advanced fixed integration SHA successfully | Return new post-tip-merge candidate; review base is that saved merged tip, excluding already integrated paths | Real changed candidate SHA, tip/base ancestry and fresh successful Verify; fixed-tip diff lists only `a.txt`; review mandate manual |
| Integration merge conflict; separately worker tip merge conflict | Capture diagnostics, qualified abort restores exact baseline, then FAIL/STUCK; no blind continuation | Real merge exit 1, MERGE_HEAD, unmerged index, conflict content, abort exit 0, exact state equality and absent MERGE_HEAD |
| Missing SHA/evidence/base, branch movement during review/checks, outside writer, ambiguous artifact, changed HEAD, abort/reset failure | No done; preserve, stop affected integration, apply bounded failure exit/brief | Manual protocol review only; these host/race/failure-injection cases were not executed |

Acceptance: immutable candidate/fixed-base evidence gates PASS; stale verdict/content cannot authorize merge; checks precede done; recorded SHA governs rollback and preserves earlier A; one transaction at a time uses updated pre-merge SHA; conflict evidence precedes abort. Ordinary merge commits receive integration verification; unchanged candidates receive no redundant per-ticket review.

## Reproduce

From repository root:

```sh
python3 docs/verification/reliability-hardening/09/experiment.py > docs/verification/reliability-hardening/09/experiment.log
git diff --check
```

Observed exits: **0**, **0**. Every Python assertion passed; expected red Verify exits **1**, conflicting merges **1**, absent MERGE_HEAD resolution **128** are intentional and checked. Actual timestamps use UTC; `2026-10-14 Asia/Shanghai` is the supplied client date. Temporary fixtures are removed only by the experiment after stdout captures their facts. No network, external dependencies, host role dispatch or original-checkout writes occur in the experiments. The executable fixture is a reproducer, not a new engine/transaction helper.

Supplemental local Markdown target/fragment validation: **21** links across loop.md, run-record.md, integration.md and this document, exit **0**. New files and patch inspected; this does not replace behavior evidence.

Before handoff, commit ticket changes, merge the integration tip into this ticket branch, rerun the experiment into an external log and run diff/link checks again. Report those commands/paths separately so a committed evidence log is not silently replaced by a later run.

## Limits and scope

This does not prove a real model obeyed serialization, review qualification, artifact ownership, cancellation or brief writing. Runtime smoke remains ticket 13; final-review repair remains ticket 10 and recovery policy remains resume.md. There is no executable product suite or typecheck in this Markdown repository; no full-suite/end-to-end pass is claimed. Changed only loop.md/run-record.md, the disclosed integration reference and these verification files. Tracker/spec/index/global/plexus/upstream files, other tickets and role defaults remain outside this executor's writes; no push/PR.
