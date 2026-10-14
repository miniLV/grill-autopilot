# 09: CLI ledger v2

Status: done
Blocked by: 01, 02, 03, 04, 05, 06, 07, 08
Implementer: escalate (cross-module integration and transactional validation)
Files:
  - ledger/cli.py
  - tests/test_cli.py
Interface: python3 -m ledger --file PATH add DATE AMOUNT CATEGORY [NOTE] | list | summary [--start D] [--end D] | export | import CSV_PATH
Examples:
  - AC9.1: add 2026-01-05 12.50 " Food  Out " lunch -> stored/displayed food-out and 12.50; add ... abc food -> stderr "error: invalid amount: abc\n", exit 2; add ... 1 9lives -> "error: invalid category: 9lives\n", exit 2, adds nothing
  - AC9.2: food 1250 and 250 in January, rent 90000 in February -> "2026-01 food 15.00\n2026-02 rent 900.00\n"; --start 2026-02-01 -> only "2026-02 rent 900.00\n"
  - AC9.3: export one lunch entry -> "date,amount,category,note\n2026-01-05,12.50,food,lunch\n"; valid import exits 0 and appends all; invalid lines 2 abc and 4 9lives -> stderr "line 2: invalid amount: abc\nline 4: invalid category: 9lives\n", exit 1, ledger unchanged
  - Edge: --start 2026-02-01 --end 2026-01-15 -> stderr "error: start after end\n", exit 2; empty export is header-only; summary on empty ledger prints nothing. Tests invoke the CLI through subprocess; do not require atomicity across concurrent import batches beyond validation before append.
Verify:
  - python3 -B -m unittest tests.test_cli -v
  - N/A: standard-library fixture has no type checker
Context: spec.md#S9; prior art: ledger/cli.py; tests/test_cli.py
Do not: edit files outside Files · weaken, skip or delete assertions · add dependencies

## Acceptance
- [ ] AC9.1: Add uses public amount/category parsers; invalid inputs stderr error and exit 2.
- [ ] AC9.2: Summary supports inclusive date bounds and sorted output.
- [ ] AC9.3: Export exact CSV to stdout; import validates every row before appending any entries.

## Comments

- 2026-10-14T13:35:07.262622+00:00: Preparation passed; implementation attempt planned, not yet charged.

- 2026-10-14T13:41:56.292929+00:00: DONE check passed; planner tip merge produced b88b1a975693991c39d91d2c52856035bc8437f5 against 1dfb77139d4933cf25e173b156f4f3d79752bf37

- 2026-10-14T13:47:14.923841+00:00: Reviewer PASS and exact integration Verify passed at 62f80af6537254af2b34f44b47bc099b56d582d9
