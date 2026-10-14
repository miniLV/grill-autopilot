# grill-autopilot

A skill that grills a topic once with a human, then runs spec, tickets, implementation and review unattended, with models chosen per role.

## Roles

**Planner**:
The current session; it grills, writes the spec and tickets, grades tickets, schedules, merges and writes the brief.
_Avoid_: orchestrator, main agent

**Worker**:
The cheap-model role that implements one `Implementer: worker` ticket.
_Avoid_: executor, subagent

**Escalate**:
The strong-model role that implements `Implementer: escalate` tickets, retries failed worker tickets and applies final fixes.
_Avoid_: senior worker, fallback model

**Reviewer**:
The role that gates each ticket candidate and runs the final review; never weaker than worker or escalate.
_Avoid_: checker, judge

## Tickets

**Ticket**:
One worker-grade vertical slice under `.scratch/<slug>/issues/`, with every decision written down.
_Avoid_: task, issue

**Grading**:
The planner's checklist that decides a ticket's Implementer, splitting first when a ticket fails it.
_Avoid_: tiering, difficulty score

**Implementer**:
The ticket field naming the role that implements it first: `worker` or `escalate (<failed grading item>)`.
_Avoid_: Route (reserved for the host launch route), tier

**Frontier**:
Every `ready-for-agent` ticket whose blockers are all `done`.

## Checks

**Environment preparation gate**:
Initialization plus baseline checks in a new worktree before any implementation starts.
_Avoid_: setup check

**DONE check**:
The planner's Git check of an implementer's `DONE` reply: right branch, clean tree, at least one commit, paths within Files.
_Avoid_: Gate step, commit gate

**Planner tip merge**:
The planner merging the current integration tip into a ticket branch to produce the candidate.
_Avoid_: worker tip merge

**Candidate**:
The immutable post-tip-merge commit a reviewer judges and integration merges.
_Avoid_: ticket head, latest commit

**Integration transaction**:
One serialized merge → Verify → record step on the integration branch, with exact rollback.

**Retention and cleanup gate**:
The rule that keeps blocked worktrees and deletes only verified, clean, inactive ticket worktrees.

**Final review gate**:
Exact-tip suite, typecheck and both Standards and Spec reviews before delivery.

## Outputs

**Run**:
One execution with its own run ID, independent of the feature slug.

**Brief**:
The closing report at `.scratch/<slug>/brief.md`, classifying the run as `success`, `partial` or `failed`.
_Avoid_: PR brief (a PR opens only for `success` with prior opt-in)

**Route**:
The host launch path for a role: native tool, allowed CLI, or unavailable.
_Avoid_: using it for ticket assignment (that is the Implementer)
