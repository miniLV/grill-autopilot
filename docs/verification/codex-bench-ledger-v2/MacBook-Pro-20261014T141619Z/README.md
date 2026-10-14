# Fresh B run: success

Ran only B from the clean integration checkout at
`a6553820d658bb2533a9211e8c4490d10d738a24`, using the fixed launcher:

```bash
ARMS=b BENCH_ROOT="$HOME/autopilot-bench-ledger-v2-b-fresh-20261014T125159Z" bash bench/ledger-v2/run.sh
```

All seven companion skill directories and `SKILL.md` prerequisites passed. The
new root did not exist. No A session ran; previous A and failed B results remain
unchanged. No skill or bench file was modified during this run. The sandbox
remained `workspace-write` with explicit access to this arm's own `.git`.

## Outcome

- Start: **2026-10-14 12:52:27 UTC / 20:52:27 Asia/Shanghai**.
- End: **2026-10-14 14:16:19 UTC / 22:16:19 Asia/Shanghai**.
- Elapsed: **83 minutes 52 seconds**; process and script exit **0**.
- Brief: **success**; **9/9 tickets done, none blocked**.
- Delivered integration SHA: `7b0a2d8365c6ae9ea5f7030760f0c8acab94d3f2`.
- Final full suite: **66 tests passed on Python 3.9.6 and 3.13.3**, both exit 0.
- Final Standards **PASS**, final Spec **PASS**, no remaining findings, same SHA.
- Typecheck: agreed **N/A**, no checker configured.

[Final report](arm-b-grill-autopilot/last.md),
[brief](arm-b-grill-autopilot/scratch/ledger-v2/brief.md), and
[run record](arm-b-grill-autopilot/scratch/ledger-v2/runs/20261014T125545Z-ledger-v2/run.md)
contain the scoped delivery and evidence pointers. The collected bundle includes
the actual integration ref at the delivered SHA. Integration is retained clean;
all nine verified ticket worktrees/branches were removed by the run. Original
checkout and source/base state match their recorded baseline.

## Token usage from summary.json

| Rollout model label | Input | Cached input | Output | Reasoning output |
| --- | ---: | ---: | ---: | ---: |
| gpt-6.1-sol | 32,511,962 | 31,480,448 | 200,678 | 31,185 |
| gpt-6-luna | 1,492,066 | 1,413,376 | 12,281 | 2,567 |

26 collected sessions: planner, 3 worker starts, 7 ticket escalate starts, 10
ticket reviews, 4 final-axis reviews and 1 final correction. Rollouts label Sol
as high and Luna as medium. The protocol's independently observed model/effort
metadata remains unknown; labels are not proof of the provider's executed
model. No unexpected role-model substitution or model rejection was recorded.
Cached input is included in input. Do not blindly add reasoning output to output.

## Findings, corrections and runtime diagnostics

- Money's first worker candidate rejected valid leading-zero thousands groups.
  The second worker attempt fixed it and passed review; no worker escalation.
- Initial final Spec review found a CSV carriage-return quoting difference
  between Python 3.9 and 3.13. One final correction added regressions and fixed
  row-ending handling without changing embedded line endings. Both final axes
  were rerun and passed at the new SHA. Final-fix usage: 1 of 2 allowed rounds.
- Three automatic reconnect messages occurred, including one request-processing
  error. The process stayed running; no manual restart or session assistance.
- Optional `ps` inventory was sandbox-denied. Host lifecycle observations and
  clean owned worktrees supplied the isolation evidence recorded by reviewers.
- Brief generation hit a Python SyntaxError before writes and succeeded on its
  one recorded artifact/infrastructure retry. No extra implementation attempt.
- Startup reported an invalid plugin hooks configuration (`modules` field) and
  unstable-feature warnings. Model metadata warnings in stderr do not establish
  model substitutions. See [selected diagnostics](diagnostic-events.json).
- No account usage-limit interruption, Git permission failure, unsafe recovery,
  unresolved final finding or test failure remains in this completed run.

Full raw transcripts remain local; selected diagnostics, tracker snapshots,
check/review logs and Git bundle are collected. Logs are evidence, not runnable
instructions. Absolute evidence links inside the brief refer to the retained
local fixture; equivalent copies are under this result directory.

Result `git diff --check` reports display spaces in the generated Git graph and
blank lines/line breaks in captured evidence. Those bytes are preserved rather
than changing the frozen snapshots or raw reports. The result-data whitespace
check is not claimed as passed; the fixture's code/test/check/review outcomes
are recorded separately above.

## Comparison with existing A data

| Measure | Existing A | Fresh B | B / A |
| --- | ---: | ---: | ---: |
| Elapsed | 20m 56s | 83m 52s | 4.01 |
| Input tokens, all labels | 7,694,390 | 34,004,028 | 4.42 |
| Noncached input tokens | 333,366 | 1,110,204 | 3.33 |
| Output tokens | 58,327 | 212,959 | 3.65 |
| Sessions | 9 | 26 | 2.89 |

This sample shows **no time or token savings**. It provides per-ticket review,
retained evidence, and concrete corrections, but does not establish superior
quality: A and B used different ticket granularity and test suites (38 vs 66).
No common hidden acceptance suite or bill/price data was supplied. Run times
include service stalls, reviews, fixes and report generation; single runs cannot
establish universal performance. Failed/interrupted B costs are excluded here.

[comparison-with-a.json](comparison-with-a.json) records the arithmetic and
limitations. Seed Git trees and approved spec bytes match exactly, and skill,
seed and prompt files are unchanged between the tested versions. A used its own
Git metadata workaround; B used the corrected explicit Git authorization.
