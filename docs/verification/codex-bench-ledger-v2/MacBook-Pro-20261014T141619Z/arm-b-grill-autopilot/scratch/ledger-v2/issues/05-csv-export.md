# 05: CSV export

Status: done
Blocked by: 01
Implementer: escalate (ordering: stable date sort)
Files:
  - ledger/csv_io.py
  - tests/test_csv_io.py
Interface: export_csv(entries) -> str
Examples:
  - AC5.1: One Entry("2026-01-05",1250,"food","lunch") -> "date,amount,category,note\n2026-01-05,12.50,food,lunch\n"
  - AC5.2: Input 2026-02-01 note late, 2026-01-05 note a,"b", 2026-01-05 note second -> rows Jan a,"b", Jan second, Feb late; quoted note field exactly "a,""b"""
  - Edge: empty input -> "date,amount,category,note\n"; cents -5 -> amount field -0.05; do not mutate the input list.
Verify:
  - python3 -B -m unittest tests.test_csv_io -v
  - N/A: standard-library fixture has no type checker
Context: spec.md#S5; prior art: ledger/models.py; tests/test_store.py
Do not: edit files outside Files · weaken, skip or delete assertions · add dependencies

## Acceptance
- [ ] AC5.1: Use exact header, formatted cents and LF line endings.
- [ ] AC5.2: Stable date ordering and default CSV quoting.

## Comments

- 2026-10-14T13:13:24.213944+00:00: Preparation passed; implementation attempt planned, not yet charged.

- 2026-10-14T13:18:09.493296+00:00: DONE check passed; planner tip merge produced 0778eb9e6ae72b2c398ff01354ef36b76a8eac15 against 5e768749ba71bb6289746020d47f63ba44dde258

- 2026-10-14T13:22:20.250529+00:00: Reviewer PASS and exact integration Verify passed at f0f079d479be622a83e1312b7f152a6dd916a124
