# ledger-v2: fresh full run

Repository commit: `418f94a87c8f733503814b62358b59566dafd608`.
Ran both arms once, in fresh sessions and clones, using the unchanged benchmark
script with `BENCH_ROOT=$HOME/autopilot-bench-ledger-v2-rerun-20261014T105939Z`.
All seven companion skill directories and their `SKILL.md` files were present,
the new root was absent, and the integration checkout was clean. Model, effort,
and sandbox used the script defaults: `gpt-6.1-sol`, `high`, `workspace-write`.

| Arm | Start (UTC) | End (UTC) | Process exit | Outcome |
| --- | --- | --- | --- | --- |
| A: implement-spec | 2026-10-14 10:59:52 | 2026-10-14 11:20:48 | 0 | Reports 4/4 tickets resolved; 38 tests passed |
| B: grill-autopilot | 2026-10-14 11:20:48 | 2026-10-14 11:28:07 | 0 | Brief result `failed`; 0/9 done, all blocked |

The script itself exited 0 and collected both arms. No session was interrupted or
manually assisted. Skill and bench files were not edited.

## Tokens recorded in summary.json

| Arm | Model | Input | Cached input | Output | Reasoning output |
| --- | --- | ---: | ---: | ---: | ---: |
| A | gpt-6.1-sol | 7,694,390 | 7,361,024 | 58,327 | 7,934 |
| B | gpt-6.1-sol | 924,460 | 828,160 | 18,743 | 2,937 |

A has nine collected sessions (root plus eight subagents), all recorded as
`gpt-6.1-sol / high`. B has one session and dispatched no children. No model
rejection or executed model substitution is recorded. Startup metadata warnings
mention `gpt-5.6-luna`; those warnings do not establish model execution.

## Final reports and limitations

A's [last.md](arm-a-implement-spec/last.md) reports 4 resolved tickets, 0 blocked,
38 passing tests, and two Spec review findings fixed. Final implementation SHA:
`99329f2926da08187b81df4b8c0cd3083efbb787`. Its original `.git` was read-only, so
the session chose a separate Git metadata directory. Consequently, the original
script-collected `repo.bundle` and `git-graph.txt` contain only the seed, not the
implementation. They are preserved unchanged. A supplemental
[repo-separate-git.bundle](arm-a-implement-spec/repo-separate-git.bundle) and
[git graph](arm-a-implement-spec/git-graph-separate-git.txt) preserve the actual
implementation refs; bundle verification and provenance are included. This
supplement is read-only collection after the sessions ended, not a rerun.

B's [last.md](arm-b-grill-autopilot/last.md) and
[brief](arm-b-grill-autopilot/scratch/ledger-v2/brief.md) report failure before
dispatch: integration branch/worktree creation could not write
`.git/refs/heads/autopilot/ledger-v2/integration`. The process exit of 0 reflects
a handled failure, not completed work. All nine tickets are blocked; final
review and integration verification did not run. Its unchanged source passed
the three baseline tests. This is not validation of an implementation.

No commit failure was recorded: B stopped at branch/worktree creation, and A
committed with its alternate metadata. The specified exception allowed a
sandbox retry only for a commit failure caused by an unwritable `.git`, so no
`danger-full-access` retry was performed.

Other diagnostics include an invalid plugin hooks configuration (`modules` is
unknown), missing model metadata, and WebSocket HTTP 426 followed by HTTP
fallback. See each `stderr.log` and [selected error events](diagnostic-events.json).
Full transcripts remain local and are not included. Generated `summary.json`
and original collected evidence are unchanged.
