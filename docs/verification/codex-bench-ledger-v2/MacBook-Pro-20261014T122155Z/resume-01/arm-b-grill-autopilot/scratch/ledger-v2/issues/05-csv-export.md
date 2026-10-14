# 05: CSV export

Status: blocked
Blocked by: 01
Implementer: escalate (ordering: stable date sort)
Files:
  - ledger/csv_io.py
  - tests/test_csv_export.py
Interface: export_csv(entries) -> str
Examples:
  - AC5.1: The header is `date,amount,category,note`; amounts use `format_amount`; line endings are `\n`.
  - AC5.2: Rows are sorted by date, keeping insertion order for equal dates. Quoting follows the `csv` module default, so the note `a,"b"` is written as `"a,""b"""`.
  - Edge: empty -> "date,amount,category,note\n"; Jan1 -5 food empty note -> "date,amount,category,note\n2026-01-01,-0.05,food,\n"
Verify:
  - python3 -B -m unittest tests.test_csv_export -v
  - N/A: typecheck; standard-library fixture with no type checker configured
Context: spec.md#S5; prior art: tests/test_store.py
Do not: edit files outside Files · weaken, skip or delete assertions · add dependencies

## Acceptance
- [ ] AC5.1: The header is `date,amount,category,note`; amounts use `format_amount`; line endings are `\n`.
- [ ] AC5.2: Rows are sorted by date, keeping insertion order for equal dates. Quoting follows the `csv` module default, so the note `a,"b"` is written as `"a,""b"""`.

## Implementation context
AC5.1 Entry Jan5/1250/food/lunch -> "date,amount,category,note\n2026-01-05,12.50,food,lunch\n". AC5.2 input Feb1/90000/rent/z, Jan5/1250/food/a,"b", Jan5/250/food/later -> "date,amount,category,note\n2026-01-05,12.50,food,"a,""b"""\n2026-01-05,2.50,food,later\n2026-02-01,900.00,rent,z\n". csv.writer LF, money.format_amount; public CSV seam.

## Comments

- 2026-10-14T12:16:32.154039+00:00: Prepared at 0f82b4023d244ac39aa894683709d6c7e1936da5; initialization None, baseline PASS /Users/tyrion/autopilot-bench-ledger-v2-b-fixed-20261014T120228Z/arm-b-grill-autopilot/.scratch/ledger-v2/runs/ledger-v2-20261014T120629Z/logs/05-escalate-1-baseline.json

- 2026-10-14T12:19:35.330425+00:00: DONE check PASS, planner tip merge candidate 2827517494c0190b35a1749c30bc1e86ee974703 base d7166bf961d7bfd30d2634cbbd3d917352c6fdbe

- 2026-10-14T12:43:50.737974+00:00: unsafe recovery: saved reviewer04/05/07 identities unreachable; list_agents only root and interrupt_agent returned not_found for all three; inactivity/result/resource release cannot be confirmed; committed candidate preserved, no reviewer replay
