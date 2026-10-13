# Current host schema evidence

Recorded from the tool declarations exposed to this task; this is a schema transcription, not a call/result trace. Client date: 2026-10-14 Asia/Shanghai. Host tool version is not exposed (`unknown`). Root supplied the independent capture at `/Users/tyrion/Github/grill-autopilot.autopilot-worktrees/execution-notes/host-capabilities.md`; no secrets or global settings were read.

| Exposed tool | Declared arguments and behavior | Adapter limitation |
| --- | --- | --- |
| `collaboration.spawn_agent` | `task_name`, `message`, optional `fork_turns`, `model`, `reasoning_effort`; returns the native task identity. Full-history forks inherit routing and reject overrides. | Requested values are inputs; no trusted actual model/effort return is exposed. |
| `collaboration.list_agents` | Optional `path_prefix`; lists live agents in this root tree, optional prefix filter. | Status evidence, not a deletion or free-slot operation. |
| `collaboration.wait_agent` | Optional `timeout_ms`; default 30000, min 10000, max 3600000. Waits for mailbox update/new input and returns an update/interruption/timeout summary. Final messages are delivered separately to the parent. | Bounded notification wait is not complete result content or cancellation. |
| `collaboration.interrupt_agent` | `target`; interrupts current turn, returns previous status and leaves the agent available for follow-up. | Request/previous status is not confirmed current inactivity, capacity return or identity deletion. |
| `collaboration.send_message` | `target`, `message`; queues a message without triggering a turn. | Not a start/resume/stop primitive. |
| `collaboration.followup_task` | `target`, `message`; triggers an idle agent's turn or delivers to running one. | Reconcile prior activity and selected role/model before reuse; no silent model switch. |

No close/destroy/release-agent tool is exposed. Metadata release is **unsupported**. Runtime says to inspect host status/capacity facts after completion rather than treating retained identities as deleted. This task's declared capacity is **4 concurrent slots including root**, therefore at most **3 active children** after deducting root, before accounting for other occupants. Current free capacity and retained-identity accounting were not probed; availability is **unknown** for this evidence. No additional child was launched or interrupted to test release.

Root's supplied observation: initial saved execution route `gpt-5.6-luna/xhigh` was rejected as Unknown model; user then explicitly selected `gpt-6.1-sol/high`. No CLI bypass was attempted. The user's execution selection does not change the repository's default role table. The assigned ticket06 native child accepted the selected request; its trusted actual model/effort remain **unknown**. Child identity/self-report and accepted arguments do not establish `match`.

No Claude Agent-tool schema is exposed here, so native Agent/SendMessage/status/wait/stop support and actual model/effort remain **unverified**. [cli-help.log](cli-help.log) captures current read-only CLI versions/help: Codex CLI 0.156.0, Claude Code 2.1.292. Claude help describes agents JSON status, logs, stop (conversation retained) and rm (session/worktree deletion); none was used against a real session. Codex help describes model/effort inputs, cwd, output capture and JSON; no Codex CLI model run, liveness, cancellation or release was performed. CLI help verifies syntax only.
