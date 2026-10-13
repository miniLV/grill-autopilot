# Sample run record: inputs ready

Illustrative record for independent D3 field review. `/example` paths and fingerprint/hash literals describe a synthetic layout, not files or a companion installation verified on this machine. No model, initialization, review or merge has run in this sample. The real Git visibility evidence is in experiment.log.

```yaml
run_id: demo-inputs-20261013-001
slug: demo
phase: inputs-ready
result: not-final
started_at: 2026-10-13T12:00:00Z
updated_at: 2026-10-13T12:01:00Z
original_checkout: /example/repo
original_ref: refs/heads/base
base_ref: refs/heads/base
base_sha: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
integration:
  ref: autopilot/demo/integration
  worktree: /example/repo.autopilot-worktrees/demo-integration
  sha: not-recorded (creation has not run)
tracker: /example/repo/.scratch/demo
record: /example/repo/.scratch/demo/runs/demo-inputs-20261013-001/run.md
brief: /example/repo/.scratch/demo/brief.md
owned_tracker_files:
  - /example/repo/.scratch/demo/spec.md
  - /example/repo/.scratch/demo/issues/01-export.md
  - /example/repo/.scratch/demo/brief.md
  - /example/repo/.scratch/demo/runs/demo-inputs-20261013-001/run.md
  - /example/repo/.scratch/demo/runs/demo-inputs-20261013-001/baseline/unstaged.patch
  - /example/repo/.scratch/demo/runs/demo-inputs-20261013-001/baseline/staged.patch
  - /example/repo/.scratch/demo/runs/demo-inputs-20261013-001/baseline/untracked.nul
  - /example/repo/.scratch/demo/runs/demo-inputs-20261013-001/snapshots/spec.md
  - /example/repo/.scratch/demo/runs/demo-inputs-20261013-001/snapshots/tickets/01.md
  - /example/repo/.scratch/demo/runs/demo-inputs-20261013-001/logs/01-worker-001.log
baseline:
  ref: refs/heads/base
  base_sha: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
  tracked_diff: /example/repo/.scratch/demo/runs/demo-inputs-20261013-001/baseline/unstaged.patch
  staged_diff: /example/repo/.scratch/demo/runs/demo-inputs-20261013-001/baseline/staged.patch
  untracked_list: /example/repo/.scratch/demo/runs/demo-inputs-20261013-001/baseline/untracked.nul
  non_run_untracked:
    - {path: /example/repo/user-notes.bin, type: file, mode: "0644", sha256_or_target: bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb}
closeout_comparison: not-recorded (run is in progress)
companion:
  root: /example/companions
  fingerprint: commit:cccccccccccccccccccccccccccccccccccccccc
  skills:
    grilling: /example/companions/grilling/SKILL.md
    to-spec: /example/companions/to-spec/SKILL.md
    to-tickets: /example/companions/to-tickets/SKILL.md
    tdd: /example/companions/tdd/SKILL.md
    code-review: /example/companions/code-review/SKILL.md
    setup-matt-pocock-skills: /example/companions/setup-matt-pocock-skills/SKILL.md
roles:
  planner: {requested: {model: gpt-6.1-sol, effort: high}, observed: {model: unknown, effort: unknown}, evidence: "sample only; no host observation"}
  worker: {requested: {model: gpt-6-luna, effort: medium}, observed: {model: unknown, effort: unknown}, evidence: "not started"}
  reviewer: {requested: {model: gpt-6.1-sol, effort: high}, observed: {model: unknown, effort: unknown}, evidence: "not started"}
  escalate: {requested: {model: gpt-6.1-sol, effort: high}, observed: {model: unknown, effort: unknown}, evidence: "not started"}
commands:
  initialization: {command: None, cwd: /example/repo.autopilot-worktrees/demo-integration, result: "not-recorded (not started)"}
  ticket_verify:
    - {command: "python3 -m unittest", cwd: /example/repo.autopilot-worktrees/demo-01, result: "not-recorded (not started)"}
  full_suite: {command: "python3 -m unittest discover", cwd: /example/repo.autopilot-worktrees/demo-integration, result: "not-recorded (not started)"}
  typecheck: {command: "python3 check_types.py", cwd: /example/repo.autopilot-worktrees/demo-integration, result: "not-recorded (not started)"}
push_selected: false
inputs:
  spec:
    source: /example/repo/.scratch/demo/spec.md
    snapshot: /example/repo/.scratch/demo/runs/demo-inputs-20261013-001/snapshots/spec.md
    sha256: dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd
  tickets:
    "01":
      source: /example/repo/.scratch/demo/issues/01-export.md
      snapshot: /example/repo/.scratch/demo/runs/demo-inputs-20261013-001/snapshots/tickets/01.md
      sha256: eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
assumptions: []
tickets:
  "01":
    status: ready-for-agent
    branch: autopilot/demo/tickets/01
    worktree: /example/repo.autopilot-worktrees/demo-01
    starting_integration_sha: not-recorded (integration not created)
    counters: {worker: 0, escalate: 0, infrastructure: 0, reviewer: 0, final_review: 0}
    attempts:
      - attempt_id: demo-inputs-20261013-001/01/worker-001
        role: worker
        agent_id: not-recorded (not spawned)
        process_id: not-recorded (not spawned)
        requested: {model: gpt-6-luna, effort: medium}
        observed: {model: unknown, effort: unknown}
        planned_at: 2026-10-13T12:01:00Z
        started_at: not-recorded (not spawned)
        ended_at: not-recorded (not spawned)
        candidate_sha: not-recorded (no implementation)
        reviewed_sha: not-recorded (no review)
        merge_before_sha: not-recorded (no merge)
        merge_after_sha: not-recorded (no merge)
        verdict: not-recorded (no role result)
        evidence:
          - /example/repo/.scratch/demo/runs/demo-inputs-20261013-001/logs/01-worker-001.log
events:
  - {at: 2026-10-13T12:01:00Z, ticket: "01", attempt_id: demo-inputs-20261013-001/01/worker-001, operation: "planned future dispatch; identity/log destination saved before spawn", outcome: "not executed", evidence: "not-recorded (no host call)"}
```
