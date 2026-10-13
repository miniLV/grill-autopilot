# Runtime adapters

The steps and the loop are the same on every runtime. An adapter supplies three things: how to spawn a subagent on a role's model, how to give a worker its own worktree, and how to clean up.

**Detect**: with `runtime: auto`, you are on Claude Code when you have the Agent tool, and on Codex when you are the Codex CLI. Read only the matching section.

The planner role is this session. If the session's model differs from the planner role, note it in the role table and go on; the session's model is not switched.

## Claude Code

- **Spawn**: use the Agent tool with `model: <role alias>` and `effort: <role effort>`. Pass the alias from config as written (`opus`, `sonnet`, `haiku`); aliases follow new releases.
- **Worker**: the planner applies [loop.md Setup](loop.md#setup), then creates the named ticket worktree with `git worktree add <root>/<slug>-<NN> -b autopilot/<slug>/tickets/<NN> <integration-sha>`. Spawn with `run_in_background: true` and point the packet at that path, without `isolation` creating a second worktree. Record the actual branch and path in the ticket's Comments. If the host cannot run in the assigned worktree, stop and report the limitation before implementation.
- **Retry**: continue the same worker with SendMessage when it is still available. Otherwise spawn a new worker without `isolation` and point the packet at the existing worktree path.
- **Reviewer**: no `isolation`. Run it in the background when other workers are still running.
- **Cleanup**: `git worktree remove <path>`, then `git branch -d autopilot/<slug>/tickets/<NN>` once that recorded ticket branch is merged. A preflight conflict is preserved, never cleaned up as this run's work.

## Codex

- **Spawn**: use the multi-agent spawn tool with `model: <role slug>`, `reasoning_effort: <role effort>` and `fork_turns: "none"`, and send the packet as the whole message. The roles in config are explicit task-local seat overrides, so they win over any saved routing-policy default for executors.
- **Worktree**: Codex gives subagents no isolation, so the planner creates one per ticket:
  after [loop.md Setup](loop.md#setup), use `git worktree add <root>/<slug>-<NN> -b autopilot/<slug>/tickets/<NN> <integration-sha>`.
  The packet's Worktree line is the only place the worker may edit.
- **Fallback**: if the spawn tool is missing or rejects the model override, run each subagent as a background process:
  `codex exec -m <slug> -c model_reasoning_effort=<effort> -s workspace-write -C <worktree> --add-dir <repo>/.git -o <root>/<slug>-<NN>.out "<packet>"`.
  Read the reply from the `-o` file, because stdout truncates long output. If the sandbox blocks the child process, stop and report that the route is unavailable.
- **Retry**: dispatch again to the same worktree with the reviewer's reasons appended.
- **Cleanup**: `git worktree remove <path>`, then `git branch -d autopilot/<slug>/tickets/<NN>` once that recorded ticket branch is merged. A preflight conflict is preserved, never cleaned up as this run's work.
- **astra**: `gpt-6-astra` runs only when a role in config names it.
