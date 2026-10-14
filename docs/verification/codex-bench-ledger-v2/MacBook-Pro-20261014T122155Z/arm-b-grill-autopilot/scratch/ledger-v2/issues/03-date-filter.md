# 03: Date filter

Status: done
Blocked by: None
Implementer: escalate (ordering: original entry order must be preserved)
Files:
  - ledger/query.py
  - tests/test_query_filter.py
Interface: filter_entries(entries, start=None, end=None) -> list
Examples:
  - AC3.1: With entries dated 2026-01-01, 2026-01-15 and 2026-02-01, `start="2026-01-15"` keeps the last two; `end="2026-01-15"` keeps the first two.
  - AC3.2: `start > end` raises `ValueError("start after end")`.
  - Edge: empty input -> []; entries C,A,B with no bounds -> [C,A,B]; both bounds 2026-01-15 -> [B]
Verify:
  - python3 -B -m unittest tests.test_query_filter -v
  - N/A: typecheck; standard-library fixture with no type checker configured
Context: spec.md#S3; prior art: tests/test_store.py
Do not: edit files outside Files · weaken, skip or delete assertions · add dependencies

## Acceptance
- [ ] AC3.1: With entries dated 2026-01-01, 2026-01-15 and 2026-02-01, `start="2026-01-15"` keeps the last two; `end="2026-01-15"` keeps the first two.
- [ ] AC3.2: `start > end` raises `ValueError("start after end")`.

## Implementation context
Use Entry cents A=100/B=200/C=300 with dates stated in AC3.1. Public query seam. Reversed bounds reject even empty entries.

## Comments

- 2026-10-14T12:11:37.799005+00:00: Prepared at 9d5c4374ad0bc60e7bd6b09d99cf8356913d6533; initialization None, baseline PASS /Users/tyrion/autopilot-bench-ledger-v2-b-fixed-20261014T120228Z/arm-b-grill-autopilot/.scratch/ledger-v2/runs/ledger-v2-20261014T120629Z/logs/03-escalate-1-baseline.json

- 2026-10-14T12:15:06.186968+00:00: DONE check PASS, planner tip merge candidate b49ad7acb7c9a24f8ebd9f8dbc9f04f6c320b01f base 9d5c4374ad0bc60e7bd6b09d99cf8356913d6533

- 2026-10-14T12:17:43.430511+00:00: Reviewer PASS b49ad7acb7c9a24f8ebd9f8dbc9f04f6c320b01f; serialized integration Verify PASS d7166bf961d7bfd30d2634cbbd3d917352c6fdbe
