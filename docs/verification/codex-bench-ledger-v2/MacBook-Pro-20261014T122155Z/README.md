# B after the Git permission fix: usage interruption and failed recovery

Ran only B with the unchanged skill and the fixed launcher at
`5f9897bd8144f92589781b9788f6d528f3a98776`:

```bash
ARMS=b BENCH_ROOT="$HOME/autopilot-bench-ledger-v2-b-fixed-20261014T120228Z" bash bench/ledger-v2/run.sh
```

The integration checkout was clean and all seven companion prerequisites passed.
A was not executed; its prior full-run results remain unchanged.

The Git permission issue is resolved: B created integration/ticket worktrees,
committed candidates, reviewed and merged tickets 01-03 in the original shared
Git metadata. No alternate Git directory or sandbox downgrade was used. Two
worker sessions recorded `gpt-6-luna / medium`; other sessions recorded
`gpt-6.1-sol / high`. No model substitution was observed.

## Execution segments

| Segment | Start (UTC) | End (UTC) | Process exit | Outcome |
| --- | --- | --- | --- | --- |
| Initial B benchmark | 2026-10-14 12:03:21 | 2026-10-14 12:21:55 | 1 | Account usage limit interrupted planner/reviews |
| User-authorized same-run resume | 2026-10-14 12:38:23.354455, observed launch intent | 2026-10-14 12:44:25.688, model task completion | 0 | Handled recovery failure; final tests unrun |

The initial script ran to completion and collected the failure. It generated no
`last.md` or brief before interruption. Its original `summary.json`, bundle and
tracker snapshot are preserved unchanged. The account later reported ordinary
usage available. The user explicitly requested continued testing, so the same
session and run were resumed once, rather than recreating tickets or resetting
attempt budgets. See [selected initial errors](initial-errors.json).

Resume qualified unchanged Git state, original-source baseline, frozen inputs
and companion fingerprints. Saved reviewers 04/05/07 were unavailable to the
restored host: interrupt calls returned `not_found`, and the live-agent query
returned only the planner. This did not establish their inactivity or resource
release. The skill's unknown-identity recovery gate therefore stopped dispatch
and all cleanup, retained commits/worktrees, and wrote a failed brief. No blind
review replay, final verification or model fallback occurred.

## Final retained outcome

- Done: tickets 01 Money, 02 Categories, 03 Date filter.
- Blocked: 04 Summary, 05 Export, 06 Import, 07 Migration, 08 Concurrency, 09 CLI.
- Candidates for 04/05/07 are committed and retained, but not qualified as done.
- Integration SHA: `d7166bf961d7bfd30d2634cbbd3d917352c6fdbe`.
- Final full suite and final Standards/Spec review: not run; testing incomplete.
- [Resumed final report](resume-01/last.md) and [failed brief](resume-01/arm-b-grill-autopilot/scratch/ledger-v2/brief.md).

The overall result is failed, even though the resumed process exited 0. This is
not a successful full ledger-v2 implementation or evidence of cost savings.

## Token usage

| Model | Input | Cached input | Output | Reasoning output |
| --- | ---: | ---: | ---: | ---: |
| gpt-6.1-sol | 10,580,289 | 10,148,992 | 74,836 | 8,277 |
| gpt-6-luna | 1,002,646 | 906,496 | 7,017 | 1,553 |

These are cumulative totals including the resumed planner, not just the initial
script segment. [combined-summary.json](combined-summary.json) separates segment
usage and timing. Do not sum cumulative totals with the original summary.
`resume-01/collector-summary.json` preserves the collector's unmodified output;
its end/exit fields still refer to the initial script, while its token totals
include later session records. The combined summary explains that distinction.

Frozen snapshots, owned tracker data, Git bundles and selected error events are
included. Full transcripts remain local. Original initial results and the
post-resume tracker snapshot are separate. No production skill was edited.

Result diff checking reports trailing display spaces in Git graph output and
extra EOF blank lines in frozen ticket snapshots. Those collected bytes remain
unchanged to preserve evidence and snapshot hashes; this check is not reported
as passed for the result commit. The launcher fix's syntax, sandbox regression
and source diff checks passed separately before this run.
