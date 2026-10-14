# 06: CSV import

Status: done
Blocked by: 01, 02, 05
Implementer: escalate (cross-module validation and all-or-nothing aggregate errors)
Files:
  - ledger/csv_io.py
  - tests/test_csv_io.py
Interface: import_csv(text) -> list[Entry]; CsvImportError(Exception) with .errors: list[str]
Examples:
  - AC6.1: "wrong,amount,category,note\n" -> CsvImportError.errors == ["line 1: bad header"]
  - AC6.2: Valid CSV "date,amount,category,note\n2026-01-05,12.50, Food  Out ,lunch\n" -> [Entry("2026-01-05",1250,"food-out","lunch")]; rows lines 2 amount abc, line 3 valid, line 4 category 9lives -> errors ["line 2: invalid amount: abc", "line 4: invalid category: 9lives"]
  - Edge: header-only -> []; empty input -> ["line 1: bad header"]. Each record must have four fields (error "expected 4 fields"); dates must be valid YYYY-MM-DD (error "invalid date: <text>"). Aggregate both amount/category problems in a row. Physical CSV record start line is used, including multiline quoted notes; preserve export_csv.
Verify:
  - python3 -B -m unittest tests.test_csv_io -v
  - N/A: standard-library fixture has no type checker
Context: spec.md#S6; prior art: ledger/csv_io.py; tests/test_store.py
Do not: edit files outside Files · weaken, skip or delete assertions · add dependencies

## Acceptance
- [ ] AC6.1: Reject a nonmatching header.
- [ ] AC6.2: Parse cents and normalize categories; collect every row error, returning no partial list.

## Comments

- 2026-10-14T13:22:22.838386+00:00: Preparation passed; implementation attempt planned, not yet charged.

- 2026-10-14T13:30:39.182924+00:00: DONE check passed; planner tip merge produced 4dc048d94e21e0b748255a2779ef192dd411fe36 against ba80142544092242b75bd0dc187805121093f8fb

- 2026-10-14T13:35:05.813805+00:00: Reviewer PASS and exact integration Verify passed at 1dfb77139d4933cf25e173b156f4f3d79752bf37
