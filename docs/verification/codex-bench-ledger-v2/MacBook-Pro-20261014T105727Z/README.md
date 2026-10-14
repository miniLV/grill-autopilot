# ledger-v2 benchmark: fresh full rerun

This run was explicitly requested after the earlier startup-failure benchmark.
Both arms used fresh sessions and fresh clones in
`~/autopilot-bench-ledger-v2-rerun-20261014T105708Z`; the previous data was preserved.
The integration branch was clean at
`a7544fed65eac953862917407154fb486484061b` before the run. All seven required
companion skill directories and their `SKILL.md` files were present. Python and
Git were available, and the selected new benchmark root did not exist.

Command:

```bash
BENCH_ROOT=/Users/tyrion/autopilot-bench-ledger-v2-rerun-20261014T105708Z bash bench/ledger-v2/run.sh
```

| Arm | Start (UTC) | End (UTC) | Exit |
| --- | --- | --- | --- |
| arm-a-implement-spec | 2026-10-14T10:57:17Z | 2026-10-14T10:57:22Z | 1 |
| arm-b-grill-autopilot | 2026-10-14T10:57:22Z | 2026-10-14T10:57:27Z | 1 |

Both arms failed before implementation with the API response:

> The 'gpt-6.1-sol' model is not supported when using Codex with a ChatGPT account.

The script continued after A failed, ran B, collected the results, and exited 0.
Neither arm generated `last.md`, tickets, a brief, or implementation commits.
Both clones remain clean at seed commit `4cce6e7`. Each arm completed 0 tickets;
no arm-level implementation or acceptance tests ran. The three seed baseline
tests passed during script preparation, as required before starting either arm.

Both `tokens_by_model` objects are empty. No token usage was recorded; this is
not a measured token total of zero. No subagent was started and no replacement
model was executed. Startup diagnostics also reported missing model metadata
(including a `gpt-5.6-luna` metadata warning), an invalid plugin hooks configuration
with an unknown `modules` field, and WebSocket HTTP 426 followed by HTTP fallback.
Metadata fallback is not evidence of an executed model substitution.

See `summary.json`, the collected `stderr.log` files, and `startup-errors.json`
(the startup error events only, not full transcripts). No `.git` write failure
occurred, so the conditional full-access retry was not used. No session was
interrupted or manually assisted, and no skill or bench file was edited.
