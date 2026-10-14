# 04: Validated CSV import and stable export

**What to build:** Users export correctly quoted, date-sorted CSV and import valid entries; an invalid CSV reports every row problem and adds nothing.

**Blocked by:** 01: Exact money and categories with v2 migration

**Status:** resolved

- [x] Implement S5 / AC5.1–AC5.2: exact header, LF endings, formatted amounts, stable date sorting, and csv default quoting.
- [x] Implement S6 / AC6.1–AC6.2: exact header validation, CsvImportError.errors with physical file line numbers, all-or-nothing parsing, money/category validation.
- [x] Implement S9 / AC9.3: export stdout; import appends all valid entries and exits 0, errors go to stderr with exit 1 and no writes.
- [x] Use TDD at the pre-approved export_csv, import_csv, CsvImportError, store API, and CLI seams; keep the full suite green.

## Comments

- Implementer claimed ticket 04. Pre-approved seams: export_csv/import_csv/CsvImportError for CSV behavior; CLI plus public store load/append for persistent all-or-nothing import. HEAD matches integration 8790fdb. No GLOSSARY or ADR files exist.
- Cycle 1: export formats cents, sorts dates stably, uses LF/default quoting. Red: public csv_io import raised ModuleNotFoundError. Green: tests.test_csv_io passed 1 test.
- Cycle 2: reject empty/wrong CSV headers with CsvImportError.errors. Red: missing CsvImportError public import. Green: 2 CSV tests passed.
- Cycle 3: valid import parses grouped amount and normalizes category. Red: empty import list differed from expected Entry. Green: 3 CSV tests passed.
- Cycle 4: aggregate every amount/category failure, including two fields in each bad row. Red: raw ValueError stopped on first amount. Green: 4 CSV tests passed; no partial list returned.
- Cycle 5: report physical record-start lines after/within multiline notes. Red: error was on line 5 instead of line 4. Green: 5 CSV tests passed.
- Cycle 6: collect wrong-width/blank records and invalid date together with amount/category errors. Red: short record raised IndexError. Green: 6 CSV tests passed.
- Supplement: empty/multiline CSV notes roundtrip passed at existing public seams (7 CSV tests).
- Cycle 7: CLI export prints exact CSV without extra newline. Red: argparse rejected export (exit 2). Green: focused CLI test passed.
- Cycle 8: CLI valid import appends to existing entries and preserves empty/multiline notes. Red: argparse rejected import (exit 2). Green: focused CLI test passed.
- Cycle 9: invalid CLI import prints every CSV error, exits 1, and appends no valid-prefix records. Red: stderr contained traceback instead of the exact three errors. Green: focused CLI test passed; public store.load retained only original entry.
- Validation: full suite passed 23 tests (0.329s); git diff --check passed. Ticket stays claimed pending orchestrator integration/review.
- Final code-review fixes: strict CSV parsing rejects unterminated quoted notes and malformed closing quotes; header parser errors become `line 1: bad header`, and record parser errors retain earlier diagnostics plus physical record-start lines while collecting later row errors. CSV field limits remain unchanged. Three red-green cycles and supplementary field-limit/CLI all-or-nothing regressions are recorded in [review.md](../review.md). Five real CLI parser-error cases exit 1 with exact diagnostics, no traceback, and no appended prefix entries. Full suite passed all 38 tests (1.732s); `git diff --check` passed. Ticket remains claimed for orchestrator resolution.

## Answer

Implemented in 2fe5bc6a4d7e316b10ac68b17816404546cd3b4f; review fixes 7d0b34a309d5591ef8faf1d49a5d67527a793ed0; integrated as 53a247797319c0844a87e5f2168deceffa77247e. Final code-review fixes integrated as 5d80366b16f6341b56bce380cd8bd380a1bd5a9e. Root independently verified the final full suite: all 38 tests passed. All acceptance criteria complete; no blockers remain.
