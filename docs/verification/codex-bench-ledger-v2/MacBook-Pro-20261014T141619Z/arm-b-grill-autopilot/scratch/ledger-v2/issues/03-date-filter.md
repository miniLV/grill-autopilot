# 03: Date filter

Status: done
Blocked by: None
Implementer: escalate (ordering: must preserve original entry order)
Files:
  - ledger/query.py
  - tests/test_query.py
Interface: filter_entries(entries, start=None, end=None) -> list
Examples:
  - AC3.1: Entries dated 2026-01-01, 2026-01-15, 2026-02-01: start="2026-01-15" -> last two; end="2026-01-15" -> first two
  - AC3.2: start="2026-02-01", end="2026-01-15" -> ValueError("start after end")
  - Edge: both bounds "2026-01-15" -> only the middle entry; no bounds -> all entries in input order; empty input -> []. Do not validate ISO date syntax beyond this spec; compare supplied ISO strings.
Verify:
  - python3 -B -m unittest tests.test_query -v
  - N/A: standard-library fixture has no type checker
Context: spec.md#S3; prior art: ledger/models.py; tests/test_store.py
Do not: edit files outside Files · weaken, skip or delete assertions · add dependencies

## Acceptance
- [ ] AC3.1: Filter inclusive ISO date bounds and preserve original order.
- [ ] AC3.2: Reject a reversed range.

## Comments

- 2026-10-14T13:00:19.389796+00:00: Preparation passed; implementation attempt planned, not yet charged.

- 2026-10-14T13:04:39.102651+00:00: DONE check passed; planner tip merge produced 321d3b183d7a34c5ecabff61f6c14d9afe3f408f against 6380caf932906eb22e6384a0f2d6cd571547b725

- 2026-10-14T13:07:46.955461+00:00: Reviewer PASS and exact integration Verify passed at 0de76fabf581f097f0d87d547378c316929eb020
