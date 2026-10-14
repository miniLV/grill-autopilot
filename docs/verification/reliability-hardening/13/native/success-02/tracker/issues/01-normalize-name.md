# 01: Normalize surrounding name whitespace

Status: done
Blocked by: None
Files:
  - normalize.py
  - tests/test_normalize.py
Source: spec.md US1 / N1,N2,N3 -> AC1,AC2,AC3
Interface: normalize_name(value)
Examples:
  - AC1: ' Ada ' -> 'Ada'.
  - AC1: '\tAda\n' -> 'Ada'.
  - AC2: '' -> ''.
  - AC3: 'Ada' -> 'Ada'.
  - Error/non-string input class: out of scope by approved spec; empty input is the applicable boundary.
Steps:
  1. Read the frozen spec/task, confirm assigned worktree/hash/bootstrap evidence and preserve the existing baseline.
  2. For each Example, write one literal public-function unittest, observe it red where behavior is new, then implement only enough to pass before the next example.
  3. Run agreed Verify commands, preserve all assertions and commit only declared Files on the assigned ticket branch.
  4. Follow the product's worker tip-merge gate with immutable integration SHA, rerun Verify and return the clean post-tip-merge candidate SHA.
Verify:
  - python3 -B -m unittest tests.test_normalize -v
  - python3 -B -m unittest tests.test_baseline -v
  - Typecheck: N/A; plain unannotated standard-library fixture, no static checker/configuration (agreed in spec).
Baseline if new Verify file absent: python3 -B -m unittest tests.test_baseline -v
Context: spec.md#acceptance-requirements; prior art: normalize.py; tests/test_baseline.py; CODING_STANDARDS.md
Do not: edit files outside Files; weaken, skip or delete assertions; add dependencies; edit tracker/record/snapshots.

## Acceptance

- [ ] AC1: Both approved whitespace examples return 'Ada' through normalize_name.
- [ ] AC2: Empty input returns empty string.
- [ ] AC3: Existing clean input 'Ada' remains 'Ada', with baseline assertions preserved.

## Comments

- 2026-10-14T01:45:55.599698+00:00: root passedbootstrap; workerattempt planned at fixedSHA.

- 2026-10-14T01:53:05.334266+00:00: hostworkerDONEcaptured; immutablecandidateawaitsindependentreview.

- 2026-10-14T01:59:55.846550+00:00: immutablecandidate reviewedPASS, verifiedmerge 5beb2ae849c2e3059e1c4fb685d397a459152de6; noassertions weakened.
