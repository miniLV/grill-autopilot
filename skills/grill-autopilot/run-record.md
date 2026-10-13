# Run record and frozen inputs

Read this before the first tracker write, before filling a worker/reviewer packet, and when preparing the brief. This is the authority for run-data ownership, paths, snapshots and record fields. The runtime adapter supplies host facts; a saved status alone never proves that a process or Git operation completed. [resume.md](resume.md) owns explicit recovery decisions, including qualification before any record append.

## Prepare and preserve

1. Resolve the original checkout, tracker and companion paths to canonical absolute paths. The tracker stays at `<original-checkout>/.scratch/<slug>/`; this run's record is `runs/<run-id>/run.md` beneath it. For a new file, resolve its existing parent first and append the filename. Reject an intended tracker target whose existing content/ownership cannot be assigned to this run; an existing directory does not grant ownership of everything below it.
2. Before the first write, capture the original checkout's symbolic ref (or detached HEAD SHA), selected base ref and SHA, `git diff --binary`, `git diff --cached --binary`, and `git ls-files --others --exclude-standard -z`. Store the raw diff/list evidence and an inventory of non-run untracked files with file type, mode and SHA-256 content hash (or symlink target). Keep an exact manifest of run-owned tracker files; exclude only these declared paths from later comparisons, never the whole `.scratch/` directory. Unrelated untracked files may remain; preserve them. Existing source changes still require the step 0 clean-source checkpoint.
3. The planner alone writes the spec, ticket status/comments, snapshots, run record, assumptions and brief. Children read these resources; their product writes stay in their assigned worktree and declared Files. Planner/host captures child output into the run's log paths, so a child need not write into the original checkout. Declare each new tracker/log/evidence path in the ownership manifest before writing it.
4. Once the spec and ticket set pass self-check, freeze one spec snapshot and each ticket's task body at `runs/<run-id>/snapshots/spec.md` and `snapshots/tickets/<NN>.md`. Exclude the mutable Status metadata and the entire Comments section from ticket snapshots; preserve all other task sections, including Context, Files, Examples, Verify and Acceptance. After freezing, retain the source spec and source task bodies too; only Status/Comments may change in source tickets. Set snapshots read-only (remove write permissions) and save SHA-256 hashes. Keep their paths and hashes fixed for the whole run, including retries and review. Permissions are an advisory guard; verify hashes before dispatch and at closeout. A changed/missing snapshot stops dispatch and is reported with the preserved evidence.
5. Record new assumptions and events in the mutable run record, without rewriting frozen inputs or the distributed task. A material scope expansion is a blocked ticket: the child reports the reason, and the planner records it and updates mutable Status/Comments. It requires a separately agreed run; ordinary retry does not authorize changing the task.
6. Before each external operation, save its intended stage, ticket/attempt identity, refs/paths and evidence destination. Afterward record the observed identifiers, times, SHAs, verdict and command result. Use `unknown` for unobservable facts and `not-recorded` with a reason for work not yet performed; do not turn missing evidence into PASS. Keep events with timestamps instead of overwriting attempt history. Recovery must reconcile records with Git/host facts; its decision rules belong to the recovery protocol.
7. At closeout, compare the original checkout's ref, base ref SHA, both tracked diffs and all non-run untracked file entries against the baseline, excluding only manifest-owned tracker files. Report any drift and preserve the affected files. The brief links to the run record and evidence, so the user can locate both the baseline and final comparison.

## Packet paths

Fill every file/directory pointer in both packets with a canonical absolute path: frozen spec/task, mutable tracker ticket, run record, assigned worktree, required companion SKILL.md files, and log capture/evidence destinations. Paths with spaces must be quoted in commands. Children use the frozen task for requirements and the mutable tracker only for reading status; they return events to the planner instead of editing it. Repository-relative Files/Context entries inside the frozen task resolve under the explicitly assigned worktree, never the child's current directory. Run-data or external Context pointers are expanded to absolute paths by the planner and included in the packet.

## Minimum record template

The Markdown record may use this YAML block plus append-only event prose. Fill each field; retain explicit unknown/not-recorded reasons. Role observations and command results are facts recorded by the planner, not assumed from configuration. Use [runtimes.md](runtimes.md) for capability, fallback, model-status and activity/capacity semantics; distinguish released execution capacity from retained identity metadata. [failures.md](failures.md) defines when counters change, per-logical-attempt infrastructure limits, terminal transitions and result classification. Record each invocation and its old/new counts so aggregate infrastructure totals cannot renew an attempt's allowance. Companion selection, necessary reference closure and fingerprint checks are defined in [companions.md](companions.md).

```yaml
run_id: <unique execution id>
slug: <feature slug>
phase: <current phase, or terminal after closeout>
result: <success/partial/failed, or not-final while running>
stop_reason: <classification/reason or None>
resources_fully_stopped: <true/false/unknown with evidence/reason>
started_at: <UTC timestamp>
updated_at: <UTC timestamp>
original_checkout: <canonical absolute path>
original_ref: <refs/heads/name or detached SHA>
base_ref: <selected ref>
base_sha: <resolved commit SHA>
integration:
  ref: <actual integration branch>
  worktree: <canonical absolute path>
  sha: <observed SHA or not-recorded reason>
tracker: <canonical absolute directory>
record: <canonical absolute run.md>
brief: <canonical absolute brief.md>
owned_tracker_files: [<exact canonical file paths, extended before writes>]
baseline:
  ref: <saved ref or detached SHA>
  base_sha: <saved SHA>
  tracked_diff: <canonical raw unstaged diff path>
  staged_diff: <canonical raw staged diff path>
  untracked_list: <canonical NUL-separated raw list path>
  non_run_untracked: [{path: <canonical path>, type: <file/symlink>, mode: <mode>, sha256_or_target: <hash/target>}]
closeout_comparison: <evidence path or not-recorded reason>
companion:
  root: <canonical source directory>
  discovery_tier: <adjacent/project/user>
  source_commit: <commit or unavailable with reason>
  fingerprint: <canonical sorted content-hash manifest path; required even with a commit>
  skills: {<name>: <canonical SKILL.md path for each required companion>}
  helpers: {<relative name>: <canonical necessary helper path>}
  contract_evidence: <canonical semantic-check/candidate-selection evidence path>
runtime:
  host: <runtime/host name>
  version: <observed version or unknown with reason>
  schema_help_evidence: [<canonical evidence paths>]
  route: {selected: <native/CLI/unavailable>, authorization: <policy/permission evidence>, reason: <capability gap or native route; no rejection bypass>}
  capabilities: {start: <status/operation/limitation>, read_result: <status/operation/limitation>, is_alive: <status/operation/limitation>, bounded_wait: <status/operation/limitation>, cancel: <status/operation/limitation>, release: <status/operation/limitation>}
  capacity: {limit: <observed total or unknown>, includes_planner: <true/false/unknown>, basis: <active-execution/retained-identities/unknown>, active_or_reserved: [<all role identities>], available: <observed count or unknown>, evidence: <canonical path/reason>}
roles:
  planner: {requested: {model: <model>, effort: <effort>}, observed: {model: <model/unknown>, effort: <effort/unknown>}, model_status: <match/mismatch/unknown>, evidence: <path/reason>}
  worker: {requested: {model: <model>, effort: <effort>}, observed: {model: <model/unknown>, effort: <effort/unknown>}, model_status: <match/mismatch/unknown>, evidence: <path/reason>}
  reviewer: {requested: {model: <model>, effort: <effort>}, observed: {model: <model/unknown>, effort: <effort/unknown>}, model_status: <match/mismatch/unknown>, evidence: <path/reason>}
  escalate: {requested: {model: <model>, effort: <effort>}, observed: {model: <model/unknown>, effort: <effort/unknown>}, model_status: <match/mismatch/unknown>, evidence: <path/reason>}
commands:
  initialization: {command: <agreed command(s) or explicit None>, cwd: <canonical path>, result: <exit/evidence, skipped for explicit None, or not-recorded reason>}
  ticket_verify: [{command: <exact command>, cwd: <canonical path>, result: <exit/evidence or not-recorded reason>}]
  ticket_baseline: [{command: <agreed existing baseline if the new Verify file is absent>, cwd: <canonical path>, result: <exit/evidence or not-recorded reason>}]
  full_suite: {command: <exact command>, cwd: <canonical path>, result: <exit/evidence or not-recorded reason>}
  typecheck: {command: <exact command or agreed N/A>, reason: <agreed N/A reason; otherwise None>, cwd: <canonical path>, result: <exit/evidence, N/A with reason, or not-recorded reason>}
preparations:
  - worktree: <canonical integration/ticket path>
    attempt_id: <preparation/role attempt identity; integration preparation included>
    started_at: <UTC timestamp saved before initialization>
    deadline: <UTC timestamp from attempt_seconds; retained through role launch>
    starting_sha: <SHA checked before implementation>
    initialization: <command result/log path, or skipped for explicit None>
    generated_paths: [<canonical expected preparation output paths>]
    baselines: [{command: <exact stage baseline/check>, result: <exit and evidence path or agreed N/A with reason>}]
    status: <ready/environment-error/not-recorded reason>
push_selected: <true/false from grill>
budgets: {worker_extra: <configured retry.worker>, escalate_total: <configured retry.escalate>, infrastructure_extra_per_attempt: <configured retry.infrastructure>, attempt_seconds: <configured timeouts.attempt_seconds>, final_fix_limit: <limit from final-review protocol>}
closeout:
  counters: {reviewer: <logical final-review calls>, infrastructure: <extra final-stage invocations>, final_fix: <final correction calls>}
  final_suite: <pass/fail/unavailable/N/A with agreed reason and evidence>
  final_typecheck: <pass/fail/unavailable/N/A with agreed reason and evidence>
  final_review: <PASS/FAIL/unavailable with evidence>
  remaining_findings: [<unresolved findings>]
  undelivered_requirements: [<blocked ticket/scope/reason>]
  attempts: [<same attempt/invocation fields below, role final-review/final-fix/final-verification/integration-preparation>]
inputs:
  spec: {source: <canonical path>, snapshot: <canonical path>, sha256: <hash>}
  tickets: {<NN>: {source: <canonical mutable tracker path>, snapshot: <canonical frozen task path>, sha256: <hash>}}
assumptions: [<new assumption, timestamp and reason; original assumptions stay in frozen spec>]
tickets:
  <NN>:
    status: <mirrors mutable ticket Status>
    branch: <actual branch>
    worktree: <canonical absolute path>
    starting_integration_sha: <saved SHA>
    counters: {worker: <logical implementation starts>, escalate: <logical implementation starts>, infrastructure: <aggregate extra invocations>, reviewer: <logical review calls>}
    blocked_reason: <last classification/reason or None>
    blocked_by: [<upstream blocked ticket IDs>]
    attempts:
      - attempt_id: <unique id within run>
        role: <worker/reviewer/escalate/preparation>
        status: <planned/active/completed/terminated>
        implementation_started: <true/false/unknown with evidence>
        infrastructure_retries: <extra invocations used for this logical attempt>
        remaining_budget: <recorded business/infrastructure allowance at decision>
        next_state: <claimed/in-review/done/blocked or final stage/brief>
        agent_id: <host id or unknown/not-recorded reason>
        process_id: <PID or unknown/not-recorded reason>
        requested: {model: <model>, effort: <effort>}
        observed: {model: <model/unknown>, effort: <effort/unknown>}
        model_status: <match/mismatch/unknown; with trusted evidence/reason>
        lifecycle: {launch: <classification>, result: <classification>, activity: <active/inactive/unknown>, stop: <confirmed/unsupported/not-requested/unknown>, capacity_release: <confirmed/unsupported/unknown>, identity_metadata: <retained/deleted/unknown>, evidence: [<canonical paths/reasons>]}
        deadline: <UTC timestamp from attempt_seconds; preparation included>
        logical_started_at: <UTC timestamp saved before preparation/first call>
        planned_at: <UTC timestamp>
        started_at: <UTC timestamp or not-recorded reason>
        ended_at: <UTC timestamp or not-recorded reason>
        invocations:
          - {number: <initial 1 or infrastructure retry 2>, planned_at: <UTC timestamp>, started_at: <timestamp/not-started/unknown>, ended_at: <timestamp/unknown>, identity: <agent/session/PID or reason>, classification: <runtime classification>, reason: <detail>, counts_before: <relevant counters>, counts_after: <reconciled counters>, remaining_seconds: <at decision>, evidence: [<canonical paths>]}
        candidate_sha: <SHA or not-recorded reason>
        reviewed_sha: <SHA or not-recorded reason>
        merge_before_sha: <SHA or not-recorded reason>
        merge_after_sha: <SHA or not-recorded reason>
        integration_checks: [{sha: <exact checked integration commit>, command: <exact applicable Verify/typecheck command or agreed N/A>, cwd: <canonical integration worktree>, started_at: <UTC>, ended_at: <UTC>, exit: <code or N/A with agreed reason>, log: <canonical captured output path>}]
        verdict: <observed verdict or not-recorded reason>
        evidence: [<canonical log/check/result paths>]
events:
  - {at: <UTC timestamp>, ticket: <NN/run>, attempt_id: <id/not-applicable>, operation: <intended/completed action>, outcome: <observed result>, evidence: <canonical path/reason>}
```
