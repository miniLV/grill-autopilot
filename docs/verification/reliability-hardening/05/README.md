# Ticket 05: retained work and guarded cleanup

Scope: D6 blocked-state preservation and successful cleanup. This is real Git evidence plus labeled ownership/activity/warning rehearsals, not a scheduler or host-liveness test. Exact integration rollback and bounded failure/stop behavior remain separate tickets.

## Reproduce

From the repository root:

```sh
python3 docs/verification/reliability-hardening/05/experiment.py > /tmp/grill-autopilot-05.log
git diff --check
```

Both returned **0**. The fixture ran before and after the product change. [experiment.py](experiment.py) creates a fresh temporary repository; [experiment.log](experiment.log) contains actual command cwd, UTC timestamp, output, exit code, refs and file hashes. The supplied client date is **2026-10-14 Asia/Shanghai**; the retained capture actually ran from **2026-10-13T16:43:06.344931+00:00** to **2026-10-13T16:43:06.813792+00:00**. These UTC timestamps correspond to October 14 locally; the client date is labeled separately and is not substituted for command time. Temporary paths/commit SHAs vary per reproduction.

## Actual observations and protocol decisions

| Case | Git/file observation | Labeled planner decision |
| --- | --- | --- |
| Dirty blocked ticket | Worktree payload contains `unfinished tracked change`; notes contain `unfinished untracked notes`. `git show <branch>:payload.txt` still returns `base content`; `git cat-file -e <branch>:notes.txt` returns **128**. | Retain the whole path and branch, plus dirty inventory/logs. Branch retention alone does not contain these edits. |
| Original blocked-removal instruction | Ordinary `git worktree remove <dirty-path>` returns **128**. Before/after branch SHA, status and both file hashes match. | The old removal instruction is unsuitable; preserve explicitly and report the handoff path rather than forcing cleanup. |
| Clean merged ticket | Actual commit, merge and literal integration-content check return **0**. Ancestry and clean status pass. Non-force worktree removal and `branch -d` from integration return **0**; absence check for the removed ref returns the expected **128**. Integration path/SHA remains. | Record verified done before cleanup. Ownership/inactivity are stipulated fixture inputs; no host observation is claimed. |
| Active-agent flag | A clean merged fixture path/ref remains unchanged; no delete command is issued. | Rehearse skip because activity is stipulated active. No process is spawned or queried. |
| Unestablished ownership | A clean merged fixture path/ref remains unchanged; no delete command is issued. | Rehearse skip because ownership is unknown, despite the other facts being favorable. |
| Cleanup refusal | A clean merged fixture is locked. Ordinary removal returns **128**, retaining its path, ref and file hash. Verified integration SHA remains unchanged, as does the earlier dirty blocked state. | Record cleanup warning, keep the prior verified result and remaining branch; no force, unlock or branch deletion follows. |

All commands use ordinary Git flags. Temporary fixture teardown occurs only after the observations are recorded; it is test-harness disposal, not a product cleanup decision or destruction of user state.

## Contract review

The product's single retention/cleanup gate is in [loop.md](../../../../skills/grill-autopilot/loop.md#retention-and-cleanup-gate); both runtime adapters point to it. It requires recorded verified integration/merged ancestry, current-run ownership, inactivity and clean state before ticket deletion. Blocked/failed handoff retains tracked/untracked/ignored files and stops only this run's remaining writers; unresolved activity is disclosed while the worktree stays intact. The brief must include the canonical path/ref, dirty inventory, diagnostics and activity state.

Retry/new-start instructions distinguish new clean starting state from recorded prior-attempt continuation, so known dirty retry work is preserved. The existing integration rollback example now has a clean-state guard; it was not redesigned around exact SHAs in this ticket. Successful integration sets done before cleanup; any deletion failure or skipped cleanup is recorded separately and cannot erase the verified result or suppress the brief. Integration and run evidence remain available.

Independent root review: no findings against D6. The root inspected the product diff and full evidence, independently reran the same fresh experiment (**exit 0**) and diff check, and confirmed dirty retention, retry continuation, clean merged cleanup and non-force warning behavior. The review used the supplied October 14 client date; command times remain in UTC as captured above.

Changed product/evidence files were inspected, local links resolve, and diff checks pass. These document checks supplement the actual Git behavior; they do not test agent obedience.

## Limits

Agent ownership, active/inactive state, stopping agents, done/warning bookkeeping and brief output were rehearsed, not run through a host adapter. No runtime model/kill/recovery operation was performed. This ticket does not implement general stop budgets or exact-SHA rollback. Tracker/spec/index, globals, plexus, upstream companions and unrelated files were not edited; no push occurred.
