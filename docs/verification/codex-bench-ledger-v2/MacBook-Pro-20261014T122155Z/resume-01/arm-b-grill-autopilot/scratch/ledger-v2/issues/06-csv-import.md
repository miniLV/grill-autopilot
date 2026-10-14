# 06: CSV import

Status: blocked
Blocked by: 01, 02, 05
Implementer: escalate (state shared across parsing/category/model modules)
Files:
  - ledger/csv_io.py
  - tests/test_csv_import.py
Interface: import_csv(text) -> list[Entry]; CsvImportError.errors -> list[str]
Examples:
  - AC6.1: A header other than `date,amount,category,note` gives `["line 1: bad header"]`.
  - AC6.2: Amounts go through `parse_amount` and categories through `normalize_category`; their `ValueError` messages become the error message. Two bad rows on lines 2 and 4 give two errors, and no entries are returned.
  - Edge: header-only -> []; row Jan5,12.50, Food  Out ,lunch -> [Entry("2026-01-05",1250,"food-out","lunch")]
Verify:
  - python3 -B -m unittest tests.test_csv_import -v
  - N/A: typecheck; standard-library fixture with no type checker configured
Context: spec.md#S6; prior art: ledger/csv_io.py
Do not: edit files outside Files · weaken, skip or delete assertions · add dependencies

## Acceptance
- [ ] AC6.1: A header other than `date,amount,category,note` gives `["line 1: bad header"]`.
- [ ] AC6.2: Amounts go through `parse_amount` and categories through `normalize_category`; their `ValueError` messages become the error message. Two bad rows on lines 2 and 4 give two errors, and no entries are returned.

## Implementation context
Preserve export. AC6.1 wrong header -> ["line 1: bad header"]. AC6.2 header then Jan1,abc,food,x (line2), Jan2,1.00,food,ok (line3), Jan3,2.00,9lives,y (line4) -> ["line 2: invalid amount: abc","line 4: invalid category: 9lives"], no partial entries. Quoted multiline note on lines2-3 then bad next row -> line4 error. Validate ISO date and four fields, diagnostics "invalid date: <date>" and "bad row". Physical record-start line numbering. Public CSV seam.

## Comments

- 2026-10-14T12:43:50.738982+00:00: upstream 05 blocked; run-wide unsafe recovery stop; never dispatched
