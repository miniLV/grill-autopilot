# 05: CSV export

Status: blocked
Blocked by: 01
Implementer: worker
Files:
  - ledger/csv_io.py
  - tests/test_export.py
Interface: export_csv(entries) -> str
Examples:
  - AC5.1: export_csv([Entry("2026-01-05",1250,"food","lunch")]) == "date,amount,category,note\n2026-01-05,12.50,food,lunch\n"
  - AC5.2: Input [Entry("2026-02-01",100,"food","later"),Entry("2026-01-05",1250,"food",'a,"b"'),Entry("2026-01-05",250,"food","same")] gives rows 2026-01-05,12.50,food,"a,""b""" then 2026-01-05,2.50,food,same then 2026-02-01,1.00,food,later; each ending \n
  - Edge: export_csv([]) == "date,amount,category,note\n"
Verify:
  - python3 -B -m unittest tests.test_export -v
  - N/A: typecheck; standard-library fixture has no type checker configured.
Context: spec.md#s5; prior art: tests/test_store.py
Do not: edit files outside Files · weaken, skip or delete assertions · add dependencies

## Acceptance
- [ ] AC5.1: Use exact header, formatted cents and newline line endings.
- [ ] AC5.2: Stable sort by date and standard csv quoting.

## Comments

- 2026-10-14T11:27:47.284386+00:00 Blocked by run-wide integration preparation failure; no implementation or review started.
