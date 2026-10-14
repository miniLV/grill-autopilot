# Approved Python standard-library smoke fixture

## Problem Statement

The fixture has passing legacy checks but does not normalize surrounding whitespace, parse general integer limits or render a composed message. Callers need concrete values and error propagation through three public functions. This tiny fixture makes each behavior independently verifiable while exercising dependency-aware skill integration.

## Solution

Normalize names, parse integer limits with Python standard-library semantics, then compose those public interfaces to return a normalized name and parsed limit separated by a colon. Preserve existing clean-name and legacy-one behavior.

## User Stories

1. US1: As a caller, I want surrounding whitespace removed while clean/empty names remain valid, so that names are consistent.
2. US2: As a caller, I want integer strings including zero parsed and invalid values rejected with ValueError, so that limits have explicit outcomes.
3. US3: As a caller, I want a composed normalized name/limit message and parsing errors propagated, so that rendering agrees with the two prerequisite interfaces.

## Implementation Decisions

- Keep public signatures normalize_name(value), parse_limit(value), render_message(name, limit).
- Name normalization uses Python str.strip semantics. Parsing uses Python int(value) semantics, with no custom error message. Rendering composes the public normalization/parsing functions; it does not duplicate their logic.
- Slice exactly three tickets: normalization and parsing are independent; rendering depends on both completed prerequisite tickets. File-isolation scheduling is separate from those business dependencies.
- Python standard library only; no new dependency, package, CLI, scheduler or production runtime.
- Preserve all existing legacy baseline assertions. Product writes occur only in assigned integration/ticket worktrees; the root planner alone publishes run tracker/snapshots/record/brief.

### Acceptance requirements

- N1 (US1): normalize_name(' Ada ') returns 'Ada'; normalize_name('\tAda\n') returns 'Ada'.
- N2 (US1): normalize_name('') returns ''.
- N3 (US1): normalize_name('Ada') remains 'Ada'.
- L1 (US2): parse_limit('0') returns integer 0.
- L2 (US2): parse_limit('2') returns integer 2.
- L3 (US2): parse_limit('x') and parse_limit('') each raise ValueError; exact message is unspecified.
- L4 (US2): parse_limit('1') remains integer 1.
- M1 (US3): render_message(' Ada ', '2') returns 'Ada:2'.
- M2 (US3): render_message('', '0') returns ':0'.
- M3 (US3): render_message('Ada', 'x') raises ValueError.

## Testing Decisions

- Agreed behavior seam: the three public functions, real standard-library calls, unittest with literal expected values and exception classes; no internal mocks.
- Existing baseline at every new ticket worktree before its new test file exists: python3 -B -m unittest tests.test_baseline -v. Preserve its existing assertions.
- Single-ticket Verify commands: python3 -B -m unittest tests.test_normalize -v; python3 -B -m unittest tests.test_limits -v; python3 -B -m unittest tests.test_message -v respectively.
- Full suite: python3 -B -m unittest discover -s tests -v. Initialization: explicit None.
- Typecheck: N/A, agreed because this plain unannotated standard-library fixture has no static checker or typecheck configuration; runtime behavior checks remain applicable.
- Worker TDD: one public-behavior example red before green at a time after bootstrap passes. Checks use -B so no bytecode artifact is created; actual file-state evidence still governs cleanliness.
- Product-validation seam outside the fixture implementation: real skill-entry inputs -> Git/worktree, ticket/run-record and brief outcomes. A passing fixture unittest baseline does not prove actual model orchestration, dirty preservation or interruption/resume.

## Out of Scope

Non-string input validation, integer range bounds, custom parsing/error text, external services, packaging, CLI, production scheduler, benchmark, other model/host substitutions, global config/auth changes, push, PR and deployment. Recovery is not simulated when controlled planner interruption/restart is unavailable.

## Further Notes

Design, seams, slicing, commands, no-push delivery and Go were explicitly preapproved for this smoke laboratory; the root records that authorization, not a renewed question. Existing legacy behavior is the agreed clean preparation baseline; new assertions must be written by each worker after its environment gate.

Runtime is the independent existing native Codex host. All four roles request gpt-6.1-sol/high, with actual model/effort unknown unless trusted host observations become available. Concurrency is 1 with sequential child roles and both final review seats if needed. Configured budgets are finite in the committed per-fixture configuration; existing approvals do not excuse a missing required capability.

The historical CLI account/model rejection remains preserved. This independent native trial is newly authorized; it is not CLI retry, route fallback around denial or model substitution. Companion collection and frozen inputs must be qualified by the actual root planner before dispatch.

### This independently authorized native trial

Run identity: native-smoke13-fault-20261014-02; slug: smoke13-native-fault-02. Base main is 9ff1817467574ba9ffdcd5699b2dd22f827e570d; no push/PR. The original fixture checkout is /Users/tyrion/Github/grill-autopilot.autopilot-worktrees/execution-notes/native-smoke13/native-fault-02. Full product entry is /Users/tyrion/Github/grill-autopilot.autopilot-worktrees/reliability-hardening-integration/skills/grill-autopilot/SKILL.md at 815767d2f8658774778e59305b161c2396f2e21d. These external drafts are not original-checkout tracker files and no worker may write them. Root will declare and publish canonical tracker resources before use.

Controlled fault instruction was explicitly authorized: the real started ticket01 worker, after its baseline gate, appends `# native-smoke13 fault: preserved tracked edit` to normalize.py, creates owned untracked fault-note.txt containing `native-smoke13 fault: preserved untracked evidence\n`, then returns STUCK controlled native smoke fault after owned tracked/untracked edits without committing/resetting/cleaning. Root captures actual output/identity/liveness/inventory; it cannot inject fake STUCK or pre-create dirt. worker extra/escalate/infrastructure/final-fix budgets are all0, attempt_seconds180. Thus the sole started attempt blocks01 and dependent03; independent02 may complete when safe. Missing normalization/rendering remain explicit undelivered requirements; actual result is qualified partial or failed, never forced.
