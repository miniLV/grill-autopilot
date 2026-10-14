# 04: Monthly summary

Status: done
Blocked by: None
Implementer: escalate (ordering: sorted months and categories)
Files:
  - ledger/query.py
  - tests/test_query.py
Interface: summarize(entries) -> dict[str, dict[str, int]]
Examples:
  - AC4.1: food 1250 and 250 in 2026-01, rent 90000 in 2026-02 -> {"2026-01": {"food": 1500}, "2026-02": {"rent": 90000}}
  - AC4.2: Input 2026-02 rent 90000, 2026-01 rent 200, 2026-01 food 1500 -> months ["2026-01","2026-02"], January categories ["food","rent"]
  - Edge: food -250 and 250 in 2026-01 -> {"2026-01":{"food":0}}; empty input -> {}. Preserve filter_entries if already integrated.
Verify:
  - python3 -B -m unittest tests.test_query -v
  - N/A: standard-library fixture has no type checker
Context: spec.md#S4; prior art: ledger/models.py; tests/test_store.py
Do not: edit files outside Files · weaken, skip or delete assertions · add dependencies

## Acceptance
- [ ] AC4.1: Group exact cent totals by YYYY-MM and category.
- [ ] AC4.2: Return months and categories in sorted iteration order.

## Comments

- 2026-10-14T13:07:48.118769+00:00: Preparation passed; implementation attempt planned, not yet charged.

- 2026-10-14T13:11:52.816332+00:00: DONE check passed; planner tip merge produced 70283febaa458112fff9f2297a1b35d19630cd12 against 0de76fabf581f097f0d87d547378c316929eb020

- 2026-10-14T13:16:07.770572+00:00: Reviewer PASS and exact integration Verify passed at 5e768749ba71bb6289746020d47f63ba44dde258
