# Ticket 01: branch naming verification

Scope: approved D2 only, at the real Git branch/worktree boundary. The product is a Markdown protocol, so this experiment checks Git's behavior and rehearses its read-only rejection steps. It does not execute a scheduler or test whether a model follows the skill.

## Reproduce

From the repository root, run:

```sh
python3 docs/verification/reliability-hardening/01/experiment.py > /tmp/grill-autopilot-01.log
git diff --check
```

Both commands returned **0** on 2026-10-13 with Python 3 and Git `2.50.1 (Apple Git-155)`. The committed [experiment.log](experiment.log) contains each actual command, output, exit code, ref/worktree inventory and before/after state. Temporary repository paths and commit SHAs will differ on another run. The script creates and deletes only its own temporary fixtures, with no network calls.

## Red and green

Before changing the product docs, the experiment reproduced the original default: `git worktree add ... -b autopilot/demo <base-sha>` succeeded, but creating `autopilot/demo/01` returned **255** with a ref-prefix conflict. Its before/after snapshots were equal.

After changing the docs, the full experiment was rerun. `git check-ref-format --branch` accepted all three literal defaults, and these creation commands each returned **0**:

```sh
git worktree add <temp>/demo-integration -b autopilot/demo/integration <base-sha>
git worktree add <temp>/demo-01 -b autopilot/demo/tickets/01 <integration-sha>
git worktree add <temp>/demo-02 -b autopilot/demo/tickets/02 <integration-sha>
```

The fixture has no implementation commits, so its integration SHA equals its saved base SHA. The observed branch list was exactly `autopilot/demo/integration`, `autopilot/demo/tickets/01`, `autopilot/demo/tickets/02`, and `base`. The base SHA, original `HEAD` ref and payload stayed unchanged. The documented ticket cleanup commands returned **0**, removed only the two merged ticket refs/worktrees, and retained integration and base.

## Rejections

Each rehearsal stops before any creation command. The state comparison covers base SHA, checkout ref, every local branch SHA, worktree registrations and SHA-256 hashes of fixture files, including dirty tracked and untracked files.

| Situation | Observed read-only evidence and decision |
| --- | --- |
| Old `autopilot/demo`, packed ref, dirty attached worktree | Git inventory includes the ancestor ref and registered path. Report conflict; snapshots equal, including unfinished files. |
| Missing base | `git rev-parse --verify --end-of-options 'missing^{commit}'` returns **128**. Stop; no new refs/worktrees and snapshots equal. |
| Invalid slug `bad:slug` | `git check-ref-format --branch 'autopilot/bad:slug/integration'` returns **128**. Stop; no new refs/worktrees and snapshots equal. |
| Existing `autopilot/demo/tickets/01` | Inventory includes the exact planned ref. Report conflict; snapshots equal. |
| Existing `autopilot/demo/integration/leftover` | Inventory includes a descendant of the planned integration ref. Report conflict; snapshots equal. |
| Existing `autopilot/demo/tickets/99` | Inventory includes same-slug residue outside the new ticket set. Report conflict; snapshots equal. |
| Occupied unregistered `demo-01` path | Disk inspection finds the path and file although Git registers only the original checkout. Report conflict before creating integration; snapshots equal. |

## Scope and limits

The changed examples in `SKILL.md`, `loop.md`, `runtimes.md` and the root README were read in full. Default creation and cleanup names agree; initial preflight checks all planned refs/paths, and later dispatch checks only its new target. The worker packet preserves unexpected state instead of resetting it. `git diff --check` passes, and every added file was inspected.

These are real Git experiments plus protocol rehearsals. They establish name compatibility and preservation when the prescribed read-only checks stop creation. They do not prove agent obedience, Claude/Codex host worktree targeting, explicit resume reconciliation, concurrent-creator recovery or end-to-end runtime success. Those require their own runtime evidence; this ticket makes no such claim.
