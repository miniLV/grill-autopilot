---
name: grill-autopilot
description: Grill a new topic once, then run spec, tickets and a parallel implement loop on autopilot, with models chosen per role.
disable-model-invocation: true
argument-hint: "A new topic or requirement, or resume <run-id>"
---

One human checkpoint, then **autopilot**. The grill is the only conversation; after the user confirms it, continue to the **PR brief** without asking anything. Handleable failures also end with a brief under [failures.md](failures.md), with bounded attempts and preserved work.

Work is split by **role**, never by hard-coded model:

- **planner**: this session. Grills, writes the spec and tickets, schedules the loop.
- **worker**: implements one ticket in its own worktree.
- **reviewer**: gates each ticket before merge, and runs the final code-review.
- **escalate**: retries a ticket the worker failed and performs bounded final corrections.

The tracker is always local markdown under the original checkout's `.scratch/<slug>/` (conventions in the `issue-tracker-local.md` file of the companion `setup-matt-pocock-skills`), whatever `docs/agents/` says. Before the first tracker write and before filling any child packet, read [run-record.md](run-record.md): it defines planner ownership, canonical paths, frozen inputs and the minimum run record.

**Companion skills** come from [mattpocock/skills](https://github.com/mattpocock/skills): `grilling`, `to-spec`, `to-tickets`, `tdd`, `code-review` and `setup-matt-pocock-skills`. Some of them are user-invoked, so read each one's `SKILL.md` and follow it rather than calling it by name.

## Steps

### Entry: new run or explicit resume

`/grill-autopilot resume <run-id>` enters [resume.md](resume.md) before step 0. Locate and qualify the original run record, then reconcile its saved inputs, companion fingerprint, host identities and Git facts before continuing at its recorded stage. Resume keeps the original run identity and approvals; it does not repeat grill, regenerate inputs or run new-run setup. An ordinary topic enters step 0; same-slug leftovers remain a new-run conflict, never implicit resume authorization.

### 0. Resolve roles and companions

Read [companions.md](companions.md) and select one complete collection: adjacent skills, then project skills/plugins, then user skills/plugins. Check all six skills, local-tracker helpers, necessary relative references and the current semantic contracts before Go. Record canonical paths, source facts and content hashes; resolve same-tier fingerprint ambiguity with the user before Go. An explicit resume checks the saved fingerprint and preserves the run on drift.

Read [config.yaml](config.yaml), then `.grill-autopilot.yaml` at the repo root if it exists (its keys win). Read [runtimes.md](runtimes.md)'s shared contract and matching adapter. Inspect current host schema/help and record capability, authorization and capacity evidence. Resolve every role's requested model/effort separately from trusted observations (`match`, `mismatch`, `unknown`); the planner keeps its current session model. Unsupported required capabilities or a rejected route stop preparation.

Read [failures.md](failures.md) before preparation/dispatch. Apply its single logical-attempt, retry and terminal-result authority to all roles and commands; on a handled preparation stop, use its brief exit even if no run data exists yet.

Done when: one complete contract-eligible companion collection is selected with fingerprint/contract evidence ready to record once the run ID is known, you have shown the user the requested/observed model and effort plus status for all four roles, disclosed unknown model/capacity and lifecycle limitations before Go, established a permitted route for required capabilities, and the repo's tracked source state is clean. If source changes are present, ask the user to commit or stash before you go on. Run-owned tracker data is the documented write exception; preserve and inventory unrelated untracked files as run-record.md requires.

### 1. Grill: the only checkpoint

Read and follow the companion `grilling` skill on the user's topic. Add these branches to the design tree; they belong to the last round because they hang off the design:

- **Seams**: the public interfaces to test at, each with what it catches and misses. This replaces the seam check in to-spec and tdd.
- **Slicing**: what may run in parallel, how small tickets should be, and which areas are off-limits.
- **Commands**: initialization command(s) for each new worktree, or explicit `None`; the single-ticket Verify command, full suite, and typecheck. Record an inapplicable check as `N/A` with a reason agreed here, rather than an invented pass; applicable behavior checks must still run. Choose an existing baseline check at the agreed seam if a ticket's new test file will not exist yet. Record these choices in run-record.md. Known missing tools/credentials are preparation blockers before Go; a failed or unavailable check is not `N/A`.
- **Delivery**: the feature slug, the base branch, and the integration branch (recommend `autopilot/<slug>/integration`; tickets use `autopilot/<slug>/tickets/<NN>`). Assign a unique run ID separately from the slug. Apply the read-only branch preflight in [loop.md](loop.md#setup) to the known refs and paths before Go; report any invalid base/name or existing-run conflict. Ask whether to push and open a draft PR at the end (recommend: no, local branch only).

Close with one question: "Shared understanding reached. From here I run unattended until the PR brief. Go?"

Done when: the user says yes. From this point on, ask nothing. An open question becomes a recorded assumption in the spec's Further Notes before freezing inputs, then in the run record afterward, or a blocked ticket.

### 2. Spec

Read and follow the companion `to-spec` skill with these overrides:

- Use the seams confirmed in step 1; skip asking the user about them.
- The planner writes the spec to the original checkout's canonical `.scratch/<slug>/spec.md` path, after recording its baseline and owned paths as run-record.md requires. Do not apply a triage label.
- List every autopilot assumption under Further Notes.

Done when: `spec.md` exists with every template section filled.

### 3. Tickets

Read and follow the companion `to-tickets` skill with these overrides:

- Write **worker-grade** tickets as [tickets.md](tickets.md) defines. Its template replaces the local ticket template, and its path rule replaces the "avoid file paths" rule.
- Replace the human approval of ticket granularity and blocking edges, located by meaning as companions.md describes, with the self-check in [tickets.md](tickets.md).
- The planner publishes to the original checkout's canonical `.scratch/<slug>/issues/<NN>-<slug>.md` paths. Freeze the spec and ticket task bodies using run-record.md before dispatch; mutable Status/Comments stay in these source ticket files.

Done when: every ticket file exists and the recorded whole-set self-check passes [tickets.md](tickets.md), including coverage of every approved story and acceptance item (only spec-approved exclusions), concrete examples and business dependencies independently of Files isolation. Until then the set is not ready for dispatch. The record points to the coverage table and read-only spec/task snapshots with saved hashes.

### 4. Implement loop

Once the ticket set is known, complete the branch preflight in [loop.md](loop.md#setup) for every planned ref and worktree path before creating any of them. Save the resolved base SHA, create the integration worktree from that SHA, and pass its environment preparation gate before dispatching implementation. Each ticket worktree passes its own gate. A new run stops on existing state; only an explicit resume of the same run may reconcile and reuse it.

Done when: every ticket is `done` or `blocked`, and integration suite/typecheck results are recorded, including red or an agreed `N/A` reason. Safe runs proceed to final review with those results; handled unsafe stops go directly to the brief under failures.md.

### 5. Final review

Read [final-review.md](final-review.md) and follow its exact-tip check, two-axis review and bounded correction gate. It uses the run's saved base SHA and frozen spec, qualifies both Standards and Spec verdicts, and rechecks each corrected SHA before delivery. Known blocked requirements are undelivered scope; remaining findings still gate delivery.

Done when: final-review.md's current-tip qualification or finite failed stop is recorded, with both-axis verdicts, check evidence and remaining findings ready for result classification. Every handled stop proceeds to the brief.

### 6. PR brief

The planner compares the original checkout with its baseline using run-record.md, records the evidence, writes the original checkout's canonical `.scratch/<slug>/brief.md`, and shows it to the user:

- **Result**: `success`, `partial` or `failed` under failures.md, stop reason if any, integration branch and delivered SHA, `git diff <saved-base-sha>...<delivered-sha> --stat`, both Standards/Spec verdicts with reviewed/base SHAs and evidence, and suite/typecheck statuses with checked SHAs/evidence (including an agreed N/A reason or unavailable evidence). Apply final-review.md's unchanged-tip gate before delivery.
- **Done**: each done ticket by title, with its attempts and the model that finished it.
- **Blocked**: each blocked ticket with its last classified reason and available reviewer findings. Write "none" if empty.
- **Assumptions**: assumptions from the frozen spec plus later run-record entries.
- **Roles and runtime**: requested/observed model and effort plus match/mismatch/unknown for each role and finishing attempt; capability/capacity evidence and any retained identities or unconfirmed stop/resource release. Unknown values remain unknown.
- **Record and preservation**: canonical run-record path, snapshot and check evidence, and original-checkout comparison (including any drift).
- **Budgets and errors**: separate worker/escalate, per-attempt infrastructure retries/aggregate, reviewer and run-level final-fix counts; exhausted budgets, last findings and resources not fully stopped. List missing blocked requirements explicitly for partial delivery.

Push and open a draft PR only for `success` if the user chose that in step 1. `partial`/`failed` stay local.

Done when: the terminal phase/result and brief are saved and shown, including on every handleable stop. For pre-record preparation stops, follow failures.md's direct brief exception. Stop here; the user decides what happens next.

## Guardrails

- Commit product changes only to integration/ticket branches in their assigned worktrees. The planner may write only this run's manifest-owned tracker resources in the original checkout; preserve its source, branch, base ref and unrelated files, and compare them at closeout as run-record.md requires.
- Apply failures.md's result/delivery gate before push. Never force-push.
- Follow runtimes.md for capability/fallback, model observations and all-role capacity. A rejected route or observed child model/effort mismatch stops that role and preserves its work; missing actual metadata remains disclosed unknown. Keep the planner's current session model.
