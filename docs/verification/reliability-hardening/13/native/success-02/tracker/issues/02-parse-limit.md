# 02: Parse integer limits including zero and reject invalid strings

Status: done
Blocked by: None
Files:
  - limits.py
  - tests/test_limits.py
Source: spec.md US2 / L1,L2,L3,L4 -> AC1,AC2,AC3,AC4
Interface: parse_limit(value)
Examples:
  - AC1: '0' -> integer 0.
  - AC2: '2' -> integer 2.
  - AC3: 'x' -> ValueError.
  - AC3: '' -> ValueError.
  - AC4: '1' -> integer 1.
  - Non-string inputs and integer range bounds: out of scope by approved spec.
Steps:
  1. Read the frozen spec/task, confirm assigned worktree/hash/bootstrap evidence and preserve the existing baseline.
  2. For each Example, write one literal public-function unittest, observe it red where behavior is new, then implement only enough to pass before the next example.
  3. Run agreed Verify commands, preserve all assertions and commit only declared Files on the assigned ticket branch.
  4. Follow the product's worker tip-merge gate with immutable integration SHA, rerun Verify and return the clean post-tip-merge candidate SHA.
Verify:
  - python3 -B -m unittest tests.test_limits -v
  - python3 -B -m unittest tests.test_baseline -v
  - Typecheck: N/A; plain unannotated standard-library fixture, no static checker/configuration (agreed in spec).
Baseline if new Verify file absent: python3 -B -m unittest tests.test_baseline -v
Context: spec.md#acceptance-requirements; prior art: limits.py; tests/test_baseline.py; CODING_STANDARDS.md
Do not: edit files outside Files; weaken, skip or delete assertions; add dependencies; edit tracker/record/snapshots.

## Acceptance

- [ ] AC1: Zero string parses to integer 0; zero is not treated as parser rejection.
- [ ] AC2: '2' parses to integer 2.
- [ ] AC3: Each approved invalid/empty string raises ValueError, with no custom-message requirement.
- [ ] AC4: Existing '1' remains integer 1, with baseline assertions preserved.

## Comments

- 2026-10-14T02:01:24.670341+00:00: bootstrap passed, root-selected new ticket attempt planned.

- 2026-10-14T02:09:01.431705+00:00: actualworkerDONE; fixedcandidateawaitsindependentreview.

- 2026-10-14T02:16:18.964214+00:00: exact candidate PASS, serial integration merge and Verify passed at 5e6773c2771871e1acd80910fa784d186536632f.
