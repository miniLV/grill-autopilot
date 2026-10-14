# ledger-v2 benchmark: startup failures

Ran `bash bench/ledger-v2/run.sh` once from the clean integration branch at
`ae824f3c6e07370db5c2b3c43aede89eb6fe5a32`, with the script's default settings.
All seven required companion skill directories and their `SKILL.md` files were
present; the benchmark root did not exist, and Python and Git were available.

| Arm | Start (UTC) | End (UTC) | Exit |
| --- | --- | --- | --- |
| A: implement-spec | 2026-10-14 09:29:39 | 2026-10-14 09:29:44 | 1 |
| B: grill-autopilot | 2026-10-14 09:29:44 | 2026-10-14 09:29:49 | 1 |

Both sessions failed before implementation with this API response:

> The 'gpt-6.1-sol' model is not supported when using Codex with a ChatGPT account.

The script continued after A failed, ran B, collected both results, and exited 0.
Neither arm generated `last.md`, tickets, a brief, or implementation commits.
Both clones remain clean at the same seed commit. Completed tickets: 0 in each
arm. No arm-level implementation or acceptance tests ran. The three seed baseline
tests passed during script preparation; the script would have stopped otherwise.

`summary.json` records `tokens_by_model: {}` for both arms. This means no token
usage was recorded, rather than a measured token total of zero. No subagent was
started and no replacement model was executed.

Other startup diagnostics included missing model metadata (including a
`gpt-5.6-luna` metadata warning), an invalid plugin hooks configuration with an
unknown `modules` field, and WebSocket HTTP 426 followed by HTTP fallback.
The metadata fallback warning does not establish a model substitution.
See the collected `stderr.log` files and `startup-errors.json`, which contains
only the startup error events extracted from the local event logs, not the full
transcripts.

No `.git` write failure occurred, so the permitted sandbox retry was not used.
No session was interrupted or manually assisted, and no skill or bench file was
edited. The original benchmark data remains in `~/autopilot-bench-ledger-v2`.
