# 09: CLI commands

Status: blocked
Blocked by: 02, 03, 04, 05, 06, 07, 08
Implementer: escalate (cross-module state and CLI integration)
Files:
  - ledger/cli.py
  - tests/test_cli.py
Interface: python3 -m ledger [--file PATH] add DATE AMOUNT CATEGORY [NOTE] | list | summary [--start D] [--end D] | export | import CSV_PATH
Examples:
  - AC9.1: add 2026-01-05 12.50 " Food  Out " lunch stores amount 1250, category food-out; amount abc gives stderr "error: invalid amount: abc\n", exit 2; category 9lives gives "error: invalid category: 9lives\n", exit 2
  - AC9.2: food 1250 and food 250 in January, rent 90000 in February -> stdout "2026-01 food 15.00\n2026-02 rent 900.00\n"; --start 2026-02-01 -> "2026-02 rent 900.00\n"; --end 2026-01-31 -> "2026-01 food 15.00\n"
  - AC9.3: One lunch entry exports "date,amount,category,note\n2026-01-05,12.50,food,lunch\n". Import one valid 2026-01-06,2.50,food,snack row exits 0 and store contains both. Import bad amounts abc on line 2 and 1.234 on line 4 -> stderr "line 2: invalid amount: abc\nline 4: invalid amount: 1.234\n", exit 1 and unchanged entries
  - Edge: Empty summary stdout == ""; reversed summary range emits "error: start after end\n", exit 2; bad import header -> stderr "line 1: bad header\n", exit 1 and no entries.
Verify:
  - python3 -B -m unittest tests.test_cli -v
  - N/A: typecheck; standard-library fixture has no type checker configured.
Context: spec.md#s9; prior art: ledger/cli.py; tests/test_cli.py
Do not: edit files outside Files · weaken, skip or delete assertions · add dependencies

## Acceptance
- [ ] AC9.1: Add uses money/category public functions; invalid input prints error and exits 2.
- [ ] AC9.2: Summary filters inclusive dates and prints sorted month/category totals.
- [ ] AC9.3: Export prints exact CSV; import appends every valid entry or prints all errors, exits 1 and adds none.

## Comments

- 2026-10-14T11:27:47.284723+00:00 Blocked by run-wide integration preparation failure; no implementation or review started.
