# Runtime adapters

Read this before Go and before starting, waiting on or releasing any role. The planner interprets this contract using the host's existing tools; it does not create a scheduler/service. Detect `runtime: auto` from the exposed host tools, not the product name alone. Read the matching adapter and inspect its current schema or CLI help. An unrecognized host is unavailable, not an assumed Codex/Claude route.

## Shared contract

On explicit resume, use [resume.md](resume.md) before any start/continuation: query the saved identities through this contract and observe a still-active attempt within its saved deadline.

Record the host/version, schema/help evidence, route authorization and **each** capability below as `supported`, `unsupported` or `unknown`, with its operation and limitations. Tool names are examples only when that schema is actually exposed. Before Go, disclose missing/unknown capabilities and any model/capacity uncertainty; missing required start/result/liveness/bounded-wait support blocks readiness unless an allowed fallback supplies it.

| Operation | Completion criterion and unsupported exit |
| --- | --- |
| `start` | Save role/attempt, requested model/effort, assigned canonical worktree and output destination before the call; record returned agent/session/PID and launch outcome afterward. Acceptance is not proof of actual model. Missing capability may use the fallback gate below; policy/model/permission rejection stops the route. |
| `read-result` | Capture complete output and host completion/exit evidence, not just a notification. Record `completed` only with an attributable result; classify a missing/unreadable result as `unobservable-result`, invalid packet as `invalid-result`, and exit without a result as `abnormal-exit`. Preserve logs/state and report the limitation. |
| `is-alive` | Query this run's recorded identity using trusted host status or its owned process handle; record `active`, `inactive` or `unknown`. A DONE/PASS message alone is not inactivity. Unknown identity/activity stops dispatch into that worktree and prevents cleanup. |
| bounded wait | Use bounded host waits and check wall-clock time against the recorded attempt deadline (`timeouts.attempt_seconds`, including preparation and role execution). A wait timeout is pending unless the deadline expired. At expiry record `timeout`, request cancel and reconcile activity/release; an unconfirmed stop follows the preservation/reporting exit below. If the host cannot yield control in a bounded interval, use an allowed fallback or report unsupported before dispatch. |
| `cancel` | Request stop of only this run's identity, then query activity; request acceptance alone does not prove it stopped. On unsupported cancel or unconfirmed stop, stop new dispatch, retain every possibly writable worktree and report resources not fully stopped in the brief. |
| `release` | After confirmed inactivity, release an owned execution slot using a supported safe host operation, or record host evidence that terminal execution returned its capacity. Record capacity availability separately from retained agent/session metadata. If deletion/release is unsupported, retain that metadata and report the limitation; completion/interruption alone does not prove identity deletion or slot availability. If required capacity remains unknown/unavailable, queue or stop with that reason, preserving work. |

Launch/result classifications are shared: `capability-missing`, `policy-rejected`, `model-unavailable`, `permission-denied`, `capacity-rejected`, `environment-error`, `timeout`, `abnormal-exit`, `invalid-result`, `unobservable-result`, and `completed`. A completed result retains its worker `DONE`/`STUCK` or reviewer `PASS`/`FAIL` separately; implementation FAIL is not an infrastructure failure. Save command/tool outcomes and evidence via [run-record.md](run-record.md). For each error, queue or unconfirmed stop, use [failures.md](failures.md)'s retry/terminal-state/brief rules; adapter capability facts do not grant extra attempts. Recovery requires its own reconciliation before reuse.

### Requested and observed models

For every role and attempt, keep requested model/effort separate from trusted host-observed values, with evidence and `model_status`:

- `match`: both actual model and effort are known and match the selected route. For an alias, use trusted alias-resolution evidence to compare the resolved model, not raw alias vs full name.
- `mismatch`: any known actual value differs. Stop that child role, confirm activity/release as above and retain work; its result cannot pass the gate. Report requested/observed values; do not substitute another model.
- `unknown`: one or both actual values cannot be observed, or alias resolution is unavailable. Save those values as `unknown`, disclose before Go, and retain that limitation in the brief. An accepted request, CLI flag, configuration value or child's self-report does not prove a match. Recheck available host metadata on launch/completion; do not fill gaps from config.

The planner is the current session and stays on its current model. Record its requested/observed values and status too; disclose a difference without attempting a session switch. Child values not yet observed stay unknown at preflight and are updated per attempt when trustworthy evidence becomes available.

### Fallback gate

CLI fallback is eligible **only** when an exposed tool lacks a required capability and the CLI route itself is allowed by the host's routing policy, user authorization and permissions. Record that decision and current help evidence before launching. A routing/model/permission rejection (including rejected overrides), or a rejection whose cause is unclear, is not missing capability: report unavailable and stop that role. Never use CLI to bypass it. Keep the same selected model/effort, worktree, snapshots and safety boundaries; unavailable CLI support is an explicit unavailable exit, not a reason to change models or permissions.

### Capacity and release before review

`concurrency` limits workers, not total children. Count **all** active/reserved child roles: worker, reviewer, escalate and both final-review seats. Deduct the planner and unrelated host occupants when the host's limit includes them. Save whether capacity counts active execution, retained identities or an unknown resource; derive free slots only from host-observable facts. Unknown capacity starts with one child at a time, and still requires its activity/capacity reconciliation before the next start.

A finished worker first yields its result, then passes inactivity/release reconciliation; only then can its confirmed available slot start the waiting reviewer. Prioritize waiting reviews over new workers. Complete/release reviewers and escalate roles by the same rule. A capacity rejection queues the role and records the rejection; retry start only after new host evidence of available capacity, never a repeated spawn loop. If no child can release capacity, or release/availability cannot be established, stop new dispatch and report the unsupported route with retained identities/worktrees. Final review can run its two seats sequentially when only one slot is available.

## Claude Code

Inspect the Agent/SendMessage/status/wait/stop schema actually exposed by the current host. Do not infer it from Claude CLI help. If Agent accepts `model`, `effort` and `run_in_background`, use the configured alias/effort and background execution; otherwise apply the fallback gate rather than inventing parameters.

- **Worktree/start**: after [loop.md Setup](loop.md#setup), the planner creates the named ticket worktree at the recorded integration SHA. Point the packet at that canonical path; do not request `isolation` that creates a second worktree. Reviewers use the same assigned path read-only. A host unable to honor that path is unavailable before implementation.
- **Result/liveness/wait**: use the exposed result and status tools with bounded waits. Capture the full attributable output and terminal status. If the host exposes only messages but no activity/complete-result query, record the unsupported capability and use an eligible route or stop.
- **Cancel/release**: use exposed stop/liveness tools for the owned identity and confirm inactivity. Use a safe release tool only if its schema proves execution-resource release without destroying retained work/session evidence. Without one, record retained metadata and require host capacity evidence before another launch.
- **Continuation**: after reconciling the recorded previous attempt/activity, use SendMessage only if its schema resumes the available worker; otherwise start a permitted new attempt in the retained worktree. A queued message alone is not a resumed attempt. Preserve prior tracked/untracked changes.
- **Allowed CLI route**: current `claude --help` may expose `--background`, `agents`, `logs`, `stop` and `rm`; inspect each used command's help before launch. Record returned session/PID, cwd, output and status. `logs` alone is not a final verdict and `stop` needs liveness confirmation. `rm` deletes a session and may delete its worktree: it is not a harmless release operation and is excluded from routine slot release. If CLI cannot provide bounded result/status/stop while preserving work and evidence, report unavailable. CLI help does not verify Agent-tool capabilities or actual selected model.

## Codex

Inspect the current multi-agent schema; an app/CLI label does not guarantee the tools or model route.

- **Worktree/start**: the planner creates the ticket worktree after [loop.md Setup](loop.md#setup). Use `spawn_agent` with the selected `model`, `reasoning_effort`, `fork_turns: "none"` and the complete packet only if those arguments are supported and permitted. Honor task-local choices within host policy; an incompatible policy is an unavailable route, not an automatic override. The packet's canonical Worktree is the only editable location; native agents have no automatic isolation.
- **Result/liveness/wait**: where exposed, `list_agents` supplies statuses and `wait_agent` supplies a bounded notification wait; capture the actual delivered final message separately. `send_message` alone queues a message; `followup_task` can trigger an idle agent's next turn. Neither proves completion. Record missing trusted model/effort metadata as unknown.
- **Cancel/release**: where exposed, `interrupt_agent` interrupts a turn but leaves the agent available. Query status afterward. It is not agent destruction. If no close/destroy tool exists, explicitly record metadata release unsupported and identity retained; only documented/observed active-capacity return permits a next child. Unknown capacity after interruption or completion is not a freed slot.
- **Allowed CLI route**: inspect `codex exec --help`, then launch the same selected model/effort only after the fallback gate passes. Use `-m <slug> -c model_reasoning_effort=<effort> -C <canonical-worktree> -o <canonical-output-path>` with the complete packet through a safely quoted argument or supported stdin. Choose the sandbox/access flags allowed by this host and least necessary for the assigned worktree/shared Git metadata; verify support in help. Do not weaken permissions on rejection. Capture an owned process handle/PID, exit status and complete output (`-o`/supported JSON), check liveness through the process host, wait in bounded intervals, stop only the owned process/group and verify exit before releasing its handle. If any required operation is unavailable, report unsupported; CLI flags do not prove observed model. No detached process without an observable owned handle.
- **Continuation**: reconcile previous attempt/activity before continuing an idle permitted native identity or starting a new permitted attempt in the retained path. Preserve prior tracked/untracked changes; never silently change its role/model.

## Worktree cleanup and handoff

Both adapters apply [loop.md's retention and cleanup gate](loop.md#retention-and-cleanup-gate) after activity reconciliation. Execution-slot release is separate from Git/session deletion. Blocked branches/worktrees and evidence remain intact; verified merged ticket worktrees still require ownership, inactivity and clean-state checks. Retain integration, disclose unknown activity/resources, and capture cleanup refusals as warnings.
