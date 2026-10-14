# ledger-v2 Git permission fix

The benchmark launcher supplied the same `workspace-write` sandbox and writable
benchmark parent to both arms. Both recorded permission profiles made the arm's
original `.git` read-only. Git branch/worktree creation therefore failed; this
was not a Unix ownership or mode difference between arms.

A copied its Git metadata to a different writable location and completed work.
B followed the skill's permission-rejection rule, preserved its inputs and
reported failure. A's workaround also meant the benchmark's original bundle
collector missed its implementation refs. The original results remain unchanged.

The launcher now explicitly adds **each arm's own `.git`** as a writable root
before starting that session. Both arms retain `workspace-write`. This provides
the shared Git metadata access needed by worktrees and commits without switching
to `danger-full-access`, changing global configuration, relocating metadata, or
weakening the skill's rejection/stop rules. No skill file was changed.

## Actual Codex CLI comparison

Two fresh `gpt-6.1-sol / high` exec sessions ran the same small Git command with
the same sandbox. Only the extra `--add-dir <repo>/.git` differed. See
[codex-exec-probes.json](codex-exec-probes.json) for selected command outcomes,
session IDs and effective permission records; full transcripts remain local.

| Case | Git command exit | Outcome |
| --- | --- | --- |
| Original launcher arguments | 255 | Cannot create `.git/refs/heads/codex/probe/integration` |
| Explicit own-Git writable root | 0 | Worktree created; commit `5d20efdb9e9b6b673608a2330b6674ceeeb4c351`; clean integration |

The restriction also reproduced twice with the installed `codex sandbox` and
the saved read-only Git rule. The host CLI is `codex-cli 0.162.1`.

## Repeatable launcher regression

```bash
python3 -B docs/verification/git-access-fix/verify.py
```

This runs the actual `run.sh` in a disposable repository with a deterministic
Codex command stub. The stub replays the observed Git protection in the actual
macOS Codex sandbox, using writable roots passed by the launcher. No models or
implementation skills run in this regression. Both arms must create integration
and ticket worktrees, commit on the ticket branch, merge into integration, and
leave clean integration content. Their collected bundles must contain both refs.
The original runner fails this check; the fixed runner passes for both arms.
Shell syntax and `git diff --check` also pass.

This verifies the permission fix, not a successful full ledger-v2 benchmark or
the skill's cost advantage. Existing benchmark measurements remain historical.

Official reference: [Codex permission profiles](https://learn.chatgpt.com/docs/permissions)
describes the workspace profile's protected Git paths and explicit path grants.
