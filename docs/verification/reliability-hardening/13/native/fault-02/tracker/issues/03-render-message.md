# 03: Render a message using normalized name and parsed limit

Status: blocked
Blocked by: 01, 02
Files:
  - message.py
  - tests/test_message.py
Source: spec.md US3 / M1,M2,M3 -> AC1,AC2,AC3
Interface: render_message(name, limit)
Examples:
  - AC1: (' Ada ', '2') -> 'Ada:2'.
  - AC2: ('', '0') -> ':0'.
  - AC3: ('Ada', 'x') -> ValueError.
  - Non-string inputs: out of scope by approved spec; empty name/zero limit and invalid string are applicable boundary/error classes.
Steps:
  1. Confirm tickets01/02 are done and assigned worktree/hash/bootstrap evidence contains their approved public behaviors.
  2. For each Example, write one literal public-function unittest, observe it red, then compose normalize_name and parse_limit with colon formatting to pass before the next example.
  3. Run agreed Verify commands, preserve all assertions and commit only declared Files on the assigned ticket branch.
  4. Follow the product's worker tip-merge gate with immutable integration SHA, rerun Verify and return the clean post-tip-merge candidate SHA.
Verify:
  - python3 -B -m unittest tests.test_message -v
  - python3 -B -m unittest tests.test_baseline -v
  - Typecheck: N/A; plain unannotated standard-library fixture, no static checker/configuration (agreed in spec).
Baseline if new Verify file absent: python3 -B -m unittest tests.test_baseline -v
Context: spec.md#acceptance-requirements; prior art: message.py; tests/test_baseline.py; CODING_STANDARDS.md
Do not: edit files outside Files; duplicate normalization/parsing; weaken, skip or delete assertions; add dependencies; edit tracker/record/snapshots.

## Acceptance

- [ ] AC1: Composed message returns 'Ada:2' for the approved whitespace/integer inputs.
- [ ] AC2: Empty normalized name plus zero yields ':0'.
- [ ] AC3: Invalid limit propagates ValueError from the public parser.

## Comments

- 2026-10-14T01:53:05.333811+00:00: requiredrunwide freshstart route unavailable; sourcepreserved, noimplementationcountercharged.
