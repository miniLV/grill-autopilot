# Ticket 06: runtime lifecycle, model facts and capacity

Scope: D7 adapter capability/lifecycle, model observations, permitted fallback and all-role capacity. This is a document contract review plus actual read-only schema/help evidence, **not** a runtime/model smoke run or scheduler test. Initial worktree/branch was clean at `b7efe1c` on `codex/reliability-hardening/tickets/06`.

## Reproduce the read-only checks

From the repository root:

```sh
python3 docs/verification/reliability-hardening/06/capture.py > /tmp/grill-autopilot-06-help.log
git diff --check
```

Both returned **0**. [capture.py](capture.py) runs only version/help commands with 30-second subprocess bounds. [cli-help.log](cli-help.log) retains exact cwd, UTC times, commands, outputs (trailing whitespace normalized only) and exits: `codex --version`, `codex exec --help`, `codex exec resume --help`, `claude --version`, `claude --help`, `claude agents --help`, `claude logs --help`, `claude stop --help`, `claude rm --help`; all nine exited **0**. Versions observed: Codex CLI **0.156.0**, Claude Code **2.1.292**. Capture times are actual UTC; client date is separately labeled October 14 in Asia/Shanghai.

Inspect current exposed tool declarations and compare with [host-schema.md](host-schema.md) when reproducing native capability checks; those declarations are host context, not automatically fetched by capture.py. Native schema is transcribed and root's prior route observation is explicitly attributed. No tool/CLI was invoked to launch, stop or delete a model session during these checks. Claude `rm --help` explicitly describes session/worktree deletion; routine release does not use `rm`.

## Four protocol walkthroughs and acceptance

[protocol-examples.md](protocol-examples.md) records each literal input/expected output, the baseline RED gap and the revised GREEN decision. They are manual protocol walkthroughs, not executable doc-string assertions or evidence of agent obedience.

| Acceptance | Contract outcome / evidence |
| --- | --- |
| Both runtimes share capability/result semantics | [runtimes.md](../../../../skills/grill-autopilot/runtimes.md#shared-contract) defines start/result/liveness/wait/cancel/release and normalized launch/result classifications, with host-specific operations conditioned on exposed schema. Missing Claude Agent tools remain unverified, not invented. |
| Bounded wait, unsupported cancel and resource release have exits | Attempt deadline is saved **before** integration/ticket preparation, bounds preparation waits and carries through launch. Expiry requests stop/reconciliation; unsupported/unconfirmed stop halts new dispatch, preserves possibly writable work and reports incomplete stop. Slot availability and retained metadata are separate facts. Native metadata deletion is unsupported here. |
| Capacity covers reviewer/escalate; refusal has no spawn loop | Walkthrough 1 releases/observes W1 capacity before R1, ahead of W4; all child seats count. Unknown capacity begins one child at a time; capacity rejection waits for new availability evidence, or exits unavailable when safe release cannot be established. Final-review seats can be sequential. |
| Model mismatches and unknowns remain visible | Walkthroughs 3/4 retain requested vs actual and match/mismatch/unknown per role/attempt, stop mismatched children, and disclose unknown before Go. Planner stays on current model. Accepted flags/requests/self-report cannot establish a match. Walkthrough 2 rejects policy/ambiguous-rejection CLI bypass. |

The main skill and loop consume the shared adapter contract. [run-record.md](../../../../skills/grill-autopilot/run-record.md) records host evidence, capabilities, authorization, capacity, preparation identity/deadline and per-role/per-attempt observations/lifecycle. [config.yaml](../../../../skills/grill-autopilot/config.yaml) keeps the existing role defaults and worker ceiling; it adds the approved **1800-second** attempt deadline. Infrastructure retry, resume reconciliation and final acceptance gates remain later tickets.

All changed/new product and evidence files were inspected; relative Markdown file links resolve and diff checks pass. These structural checks supplement the walkthroughs and help capture; they do not establish runtime behavior. Root's draft review found the preparation deadline originally too late; it was corrected before verification, including integration preparation identity/deadline fields. Root rechecked all four GREEN walkthroughs and reported no remaining D7 findings.

## Limits

Trusted actual native model/effort is **unknown**. Current free-slot/release behavior was not experimentally probed. Native completion/interruption does not prove identity deletion; no destroy/close tool is exposed. Claude native schema and both CLI model dispatch/liveness/cancellation/release remain unverified. No additional model call, Git runtime fixture, full skill run or end-to-end pass is claimed. No production engine, shadow scheduler or prose-string test was added. Tracker/spec/index, global/plexus/upstream files and role model defaults were not changed; no push or PR occurred.
