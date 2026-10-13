# Ticket 07: bounded failures and terminal briefs

Historical evidence (pre-D10): the one-correction walkthrough below describes ticket 07's intermediate policy at its recorded SHA. Ticket 10 supersedes that limit and final gate; see [its verification](../10/README.md). Old walkthroughs/logs are preserved and do not test the new two-round default.

Scope: D7/D8 failure accounting and closeout. This is a documentation contract walkthrough at the approved seam (skill-run input → Git/worktree state, ticket state and brief), **not** a runtime smoke run or scheduler test. Assigned branch `codex/reliability-hardening/tickets/07` started clean at integration `d195c61a44d86f2d5743a0819acc912c65894eb8`; tracker blockers 04, 05 and 06 were `done`. Client date: 2026-10-14, Asia/Shanghai.

[scenarios.md](scenarios.md) preserves the baseline RED gaps and the revised GREEN event/count/next-state/result decisions. The five ticket examples are rows 1–5, including invalid-result and unsafe-stop variants; rows 6–24 cover environment gates, launch/capability/model/capacity failures, reviewer exit/unobservable result, saved deadline, final-role/check failures, cleanup, normal success, preparation stops, pending waits and crash/configuration limits. Each row was manually followed through the product pointers and counter definitions. GREEN means the documentation now supplies the decision; it does not mean a model obeyed it.

## Acceptance evidence

| Acceptance | Walkthrough / contract evidence |
| --- | --- |
| Every listed error has a finite state exit and evidence | Rows 1–3, 5–18, 21–24. [failures.md](../../../../skills/grill-autopilot/failures.md#event--next-state) owns retry/terminal decisions, consuming [runtimes.md](../../../../skills/grill-autopilot/runtimes.md#shared-contract)'s lifecycle classifications and capability facts. Pending waits/queues retain their saved deadline; exhausted or handled stopped claimed/in-review tickets become blocked. |
| Implementation, infrastructure and final counters remain separate | Rows 1–3, 6–9, 14 and 18. Worker initial + 2 extras = 3; escalate = 1 total; same logical attempt initial + 1 infrastructure extra = 2 invocations without deadline/implementation reset. Preparation failure keeps implementation at 0. Final correction is run-level. [run-record.md](../../../../skills/grill-autopilot/run-record.md#minimum-record-template) records configured budgets, per-attempt extras, invocation identities/classifications/count changes, terminal reason and closeout evidence. |
| Terminal result is accurate; red suite does not prevent brief | Rows 4–5, 18 and 20–23. [SKILL.md](../../../../skills/grill-autopilot/SKILL.md) implement completion records red instead of requiring green; bounded final review/correction/check pass produces evidence for success/partial/failed. Every handleable stop writes/shows a brief, with a direct known-facts brief before run-data creation. Crash writing cannot be guaranteed. |
| Partial/failed never auto-push; active work is preserved | Rows 4–5, 12–19. Prior push opt-in is insufficient unless result is success. Unconfirmed stop/unknown liveness stops new dispatch and **all cleanup**, retains possibly writable work and marks failed. Safe independent tickets continue after ticket-local blocking; dependency blocking propagates. Cleanup refusal is a warning without erasing done evidence. |

The new disclosed [failures.md](../../../../skills/grill-autopilot/failures.md) is the single source for failure policy. Main steps, loop and runtime point to it rather than each carrying their own retry budgets. Configuration adds only `retry.infrastructure: 1`, clarifies worker/escalate meanings and keeps the already-added `timeouts.attempt_seconds: 1800`. The current existing final step is bounded to one correction call and accounted separately; the configured two-round final gate, final SHA/re-review workflow, resume algorithm and integration SHA rollback belong to later tickets and were not implemented here.

## Reproduce verification

From the ticket worktree/repository root, read and manually follow every scenario against the five product documents and `failures.md`. This is the ticket's Verify; it supplies the explicit inputs/counts/states/results without executing an invented scheduler.

Read-only preparation checks performed:

```sh
git status --porcelain
git rev-parse HEAD codex/reliability-hardening/integration
rg 'Status:' .scratch/reliability-hardening/issues/0{4,5,6}-*.md
```

Each returned **0**. The initial status output was empty, both SHAs were `d195c61a44d86f2d5743a0819acc912c65894eb8`, and all three blockers were done. The following structural checks also returned **0**; they supplement, rather than replace, manual behavior decisions:

```sh
git diff --check
python3 - <<'PY'
from pathlib import Path
import re
files = [Path('skills/grill-autopilot') / n for n in ['SKILL.md', 'loop.md', 'runtimes.md', 'run-record.md', 'failures.md']]
files += [Path('docs/verification/reliability-hardening/07/scenarios.md')]
checked = 0
for file in files:
    for target in re.findall(r'\[[^\]]*\]\(([^\s)]+)\)', file.read_text()):
        if '://' in target or target.startswith('#'):
            continue
        path = target.split('#', 1)[0]
        if path:
            assert (file.parent / path).exists(), (str(file), target)
            checked += 1
print(f'PASS: {checked} local Markdown link targets exist across {len(files)} files; structural check only.')
PY
```

Observed link result: **24** local targets exist across **6** files. New product/evidence files were inspected; no prose-string assertions or executable production/shadow scheduling code was added. Root reviewed the event/count/state/result table and main-step changes; its two clarity findings were resolved: the business failure row is explicitly ticket implementation/Verify failure, and success/partial require PASS for the current delivered integration commit. An older PASS after a fix cannot qualify; the re-review/SHA mechanics remain deferred.

## Limits

No role launch, cancellation, liveness, capacity release or end-to-end fixture was executed for this ticket. Actual model/effort and runtime compliance are not newly verified. No full product suite exists; no suite pass is claimed. Manual scenarios establish protocol completeness, with actual runtime evidence reserved for ticket 13. Existing integration rollback and final post-fix review weaknesses remain for tickets 09/10; this ticket does not claim to resolve them. Tracker/spec/index, global/plexus/upstream files and role defaults were untouched; no push or PR occurred.
