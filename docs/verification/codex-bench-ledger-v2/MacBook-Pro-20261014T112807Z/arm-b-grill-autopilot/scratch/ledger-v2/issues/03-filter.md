# 03: Date filter

Status: blocked
Blocked by: None
Implementer: worker
Files:
  - ledger/query.py
  - tests/test_filter.py
Interface: filter_entries(entries, start=None, end=None) -> list
Examples:
  - AC3.1: For entries a=2026-01-01, b=2026-01-15, c=2026-02-01: start="2026-01-15" gives [b,c]; end="2026-01-15" gives [a,b]
  - AC3.2: start="2026-02-01", end="2026-01-15" raises ValueError("start after end")
  - Edge: filter_entries([]) == []; start=end="2026-01-15" for [a,b,c] gives [b]
Verify:
  - python3 -B -m unittest tests.test_filter -v
  - N/A: typecheck; standard-library fixture has no type checker configured.
Context: spec.md#s3; prior art: tests/test_store.py
Do not: edit files outside Files · weaken, skip or delete assertions · add dependencies

## Acceptance
- [ ] AC3.1: Inclusive ISO bounds preserve original entry order.
- [ ] AC3.2: Reversed bounds fail.

## Comments

- 2026-10-14T11:27:47.284202+00:00 Blocked by run-wide integration preparation failure; no implementation or review started.
