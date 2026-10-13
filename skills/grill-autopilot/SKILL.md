---
name: grill-autopilot
description: Grill a new topic once, then run spec, tickets and a parallel implement loop on autopilot, with models chosen per role.
disable-model-invocation: true
argument-hint: "A new topic or requirement"
---

One human checkpoint, then **autopilot**. The grill is the only conversation; after the user confirms it, every step runs to the **PR brief** without asking anything.

Work is split by **role**, never by hard-coded model:

- **planner**: this session. Grills, writes the spec and tickets, schedules the loop.
- **worker**: implements one ticket in its own worktree.
- **reviewer**: gates each ticket before merge, and runs the final code-review.
- **escalate**: retries a ticket the worker failed.

The tracker is always local markdown under `.scratch/<slug>/` (conventions in the `issue-tracker-local.md` file of the companion `setup-matt-pocock-skills`), whatever `docs/agents/` says.

**Companion skills** come from [mattpocock/skills](https://github.com/mattpocock/skills): `grilling`, `to-spec`, `to-tickets`, `tdd`, `code-review` and `setup-matt-pocock-skills`. Some of them are user-invoked, so read each one's `SKILL.md` and follow it rather than calling it by name.

## Steps

### 0. Resolve roles and companions

Locate every companion skill's `SKILL.md`. Look first in this skill's parent directory (`../<name>/SKILL.md`), then search the agent's skill and plugin directories (for example `~/.claude/skills`, `~/.claude/plugins`, `~/.codex/skills`, `~/.codex/plugins`, `.claude/skills`, `.agents/skills`) for a `<name>/SKILL.md`. If one is missing, stop and tell the user to install mattpocock/skills.

Read [config.yaml](config.yaml), then `.grill-autopilot.yaml` at the repo root if it exists (its keys win). Detect the runtime as [runtimes.md](runtimes.md) describes and read that runtime's section. Resolve every role to a model and effort.

Done when: every companion path is known, you have shown the user a one-line role table (`planner=… worker=… reviewer=… escalate=…`) and the repo is a git repo with a clean working tree. If the tree is dirty, ask the user to commit or stash before you go on.

### 1. Grill: the only checkpoint

Read and follow the companion `grilling` skill on the user's topic. Add these branches to the design tree; they belong to the last round because they hang off the design:

- **Seams**: the public interfaces to test at, each with what it catches and misses. This replaces the seam check in to-spec and tdd.
- **Slicing**: what may run in parallel, how small tickets should be, and which areas are off-limits.
- **Commands**: the single-test-file command, the full test suite, and typecheck.
- **Delivery**: the feature slug, the base branch, and the integration branch (recommend `autopilot/<slug>/integration`; tickets use `autopilot/<slug>/tickets/<NN>`). Assign a unique run ID separately from the slug. Apply the read-only branch preflight in [loop.md](loop.md#setup) to the known refs and paths before Go; report any invalid base/name or existing-run conflict. Ask whether to push and open a draft PR at the end (recommend: no, local branch only).

Close with one question: "Shared understanding reached. From here I run unattended until the PR brief. Go?"

Done when: the user says yes. From this point on, ask nothing. An open question becomes a recorded assumption in the spec's Further Notes, or a blocked ticket.

### 2. Spec

Read and follow the companion `to-spec` skill with these overrides:

- Use the seams confirmed in step 1; skip asking the user about them.
- Write the spec to `.scratch/<slug>/spec.md`. Do not apply a triage label.
- List every autopilot assumption under Further Notes.

Done when: `spec.md` exists with every template section filled.

### 3. Tickets

Read and follow the companion `to-tickets` skill with these overrides:

- Write **worker-grade** tickets as [tickets.md](tickets.md) defines. Its template replaces the local ticket template, and its path rule replaces the "avoid file paths" rule.
- Replace step 4 (quiz the user) with the self-check in [tickets.md](tickets.md).
- Publish to `.scratch/<slug>/issues/<NN>-<slug>.md`.

Done when: every ticket file exists and the whole set passes the self-check.

### 4. Implement loop

Once the ticket set is known, complete the branch preflight in [loop.md](loop.md#setup) for every planned ref and worktree path before creating any of them. Save the resolved base SHA and create the integration worktree from that SHA, then run the loop. A new run stops on existing state; only an explicit resume of the same run may reconcile and reuse it.

Done when: every ticket is `done` or `blocked`, and the full test suite and typecheck pass on the integration branch.

### 5. Final review

Read and follow the companion `code-review` skill, and spawn its two review sub-agents on the reviewer role. Use the base branch as the fixed point and `.scratch/<slug>/spec.md` as the spec. Send all findings to one escalate-role subagent to fix on the integration branch, then rerun the full suite and typecheck.

Done when: the review has run, its fixes are committed, and the suite is green. If the suite stays red after the fix, record the failure in the brief.

### 6. PR brief

Write `.scratch/<slug>/brief.md` and show it to the user:

- **Result**: integration branch, `git diff <base>...<integration> --stat`, suite status.
- **Done**: each done ticket by title, with its attempts and the model that finished it.
- **Blocked**: each blocked ticket with the reviewer's last reasons. Write "none" if empty.
- **Assumptions**: every autopilot assumption from the spec.
- **Roles**: the role table from step 0.

Push and open a draft PR only if the user chose that in step 1.

Done when: the brief is shown. Stop here; the user decides what happens next.

## Guardrails

- Commit only to the integration branch and the ticket branches. Leave the base branch and the user's working tree untouched.
- Push only when the user chose that in step 1. Never force-push.
- If a role's model is unavailable, stop and report it. Never run that role's work on another model.
