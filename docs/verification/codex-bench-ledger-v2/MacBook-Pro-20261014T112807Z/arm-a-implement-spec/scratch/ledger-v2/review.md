# ledger-v2 final code review

Fixed point: main = 76dd680740e0559ef189e2a3483c615a2487f4f3.
Reviewed integration: 53a247797319c0844a87e5f2168deceffa77247e.
Diff: git diff main...HEAD. Both axes ran in parallel read-only subagents.

## Standards

Standards review of main...53a2477: no hard violations and no actionable smell findings.

- ledger and tests satisfy the spec's Python 3 standard library only / no dependencies rule.
- The feature directory, copied spec, numbered individual issues, status lines, and appended comments follow the local tracker conventions. Tickets 02–04 are claimed pending final resolution.
- Possible Duplicated Code: the short amount/category ValueError handlers retain explicit field assignment and independent error collection; extraction adds machinery without useful reduction.
- Possible Middle Man: public save delegates to the unlocked internal save while holding the shared lock. This avoids nested locking during append and migration.
- Possible Primitive Obsession: date strings, integer cents and category strings are the prescribed public representations; wrappers would change the approved interface.

No Standards fixes required.

## Spec

Findings: 2.

1. Malformed CSV is accepted and persisted. The permissive reader accepts an unterminated quoted note. Import returns an entry and CLI appends it with exit 0. S6: “all or nothing. On any error raise CsvImportError”. S9: “on CsvImportError it prints each error to stderr, adds nothing and exits 1.” Use strict CSV parsing with regression coverage.
2. Parser errors escape the required error boundary. Header and row reads do not catch csv.Error. A note above csv.field_size_limit() leaks a raw parser error, discards earlier row diagnostics, and causes a CLI traceback. S6: “On any error raise CsvImportError whose .errors lists every problem as line <n>: <message>”. Catch parser errors at both boundaries, retain earlier diagnostics and physical file line numbers.

No additional missing requirements or actionable scope creep found. Other spec behavior matches the requirements.

Standards: 0 actionable findings, no worst issue. Spec: 2 findings; worst is malformed CSV being accepted and persisted.

## Fixes

Both Spec findings are fixed by the single review-fix implementer at the already approved CSV and CLI seams. No Standards fixes were needed.

- Finding 1: `csv.reader` now uses strict parsing. Unterminated quoted notes and text after a closing quote are rejected; valid-prefix entries are never returned or appended when parsing fails.
- Finding 2: header `csv.Error` becomes `CsvImportError.errors == ["line 1: bad header"]`. Record parser errors join previously collected diagnostics, retain the physical record-start line, and allow the reader to advance to independently invalid later records. An unterminated quoted record consumes EOF and the next read ends the loop. The process-wide CSV field limit is unchanged.
- Red-green cycle 1: public `import_csv` test with a valid multiline prefix followed by an unterminated quote failed with "CsvImportError not raised". Strict parsing plus record error conversion made it pass, reporting physical line 4.
- Red-green cycle 2: mixed prior amount error, malformed multiline record, and later category error failed because only the parser diagnostic survived. Collecting parser errors and continuing made it pass with all diagnostics on physical lines 4, 5, and 7.
- Red-green cycle 3: malformed and oversized headers failed with raw `_csv.Error`. Header error conversion made both cases pass with the AC6.1 bad-header diagnostic.
- Supplemental regressions at approved seams: field-limit record errors preserve prior and later validation diagnostics; five real CLI cases (unterminated quote, malformed quote with earlier/later errors, field-limit record with earlier/later errors, malformed header, oversized header) exit 1 with exact stderr and retain only the pre-existing entry, observed through `ledger list`. These tests passed after the API fixes and required no CLI implementation change.
- Verification: `PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -s tests -v` passed all 38 tests in 1.732s; `git diff --check` passed.

## Final verification

Root read the complete review-fix diff, verified both reported failures were covered, and independently ran the full suite on integrated code at 5d80366b16f6341b56bce380cd8bd380a1bd5a9e: all 38 tests passed. git diff --check passed. Standards findings: 0. Spec findings: 2, both fixed; no remaining findings.
