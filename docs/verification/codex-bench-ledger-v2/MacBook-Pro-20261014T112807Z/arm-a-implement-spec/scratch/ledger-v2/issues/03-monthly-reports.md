# 03: Date-filtered monthly summaries

**What to build:** Users request inclusive date-filtered monthly totals by category, printed as exact money in deterministic order.

**Blocked by:** 01: Exact money and categories with v2 migration

**Status:** resolved

- [x] Implement S3 / AC3.1–AC3.2: inclusive optional bounds, retained entry order, and start-after-end error.
- [x] Implement S4 / AC4.1–AC4.2: exact cent totals and sorted month/category iteration.
- [x] Implement S9 / AC9.2: summary with optional start/end prints sorted month/category totals.
- [x] Use TDD at the pre-approved filter_entries, summarize, and CLI seams; keep the full suite green.

## Comments

- Implementer claimed this ticket. Pre-approved public seams: `filter_entries` catches inclusive bounds, invalid ranges and preserved order; `summarize` catches exact totals and sorted iteration; CLI subprocess tests catch argument parsing, printed totals and errors. No internal mocks.
- TDD cycle 1: inclusive optional-bound/order test failed with missing `ledger.query`, then passed after the minimal filter implementation (1 test).
- TDD cycle 2: reversed-range test failed because no ValueError was raised, then passed with the exact `start after end` validation (1 test).
- TDD cycle 3: exact monthly/category total test failed with missing `summarize`, then passed after integer-cent accumulation, including a negative amount (1 test).
- TDD cycle 4: iteration test failed with months/categories in input order, then passed after sorting both levels (1 test).
- TDD cycle 5: CLI summary test failed with argparse rejecting the missing subcommand, then passed with sorted totals formatted as money (1 test).
- TDD cycle 6: CLI optional-bound test failed with unrecognized `--start`/`--end`, then passed for either and both inclusive bounds (1 test, 3 subcases).
- TDD cycle 7: reversed-range CLI test failed with traceback/exit 1, then passed with `error: start after end` on stderr and exit 2 (1 test).
- Full suite: `PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -s tests -v` passed all 20 tests. `git diff --check` passed. No dependencies or internal mocks added.
- Merged the current `ledger-v2/integration` tip, including ticket 02, without conflicts. The same full-suite command then passed all 23 tests; `git diff --check` passed. Ticket remains claimed pending orchestrator review and resolution.

## Answer

Implemented in c5c95f6; verification 1b89d25a8831039a5ddb72211febe60927389d33; integrated as bb9b0602968dabb12d9e72a72752efc3bbb0d086. Final code-review fixes integrated as 5d80366b16f6341b56bce380cd8bd380a1bd5a9e. Root independently verified the final full suite: all 38 tests passed. All acceptance criteria complete; no blockers remain.
