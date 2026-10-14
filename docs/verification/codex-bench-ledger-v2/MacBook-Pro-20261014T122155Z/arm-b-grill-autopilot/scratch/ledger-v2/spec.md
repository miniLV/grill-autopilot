# Spec: ledger v2 — money, categories, reports, CSV, safe storage

## Problem

`ledger` stores amounts as floats, accepts any category text, has no reports, cannot exchange data, and loses entries when two processes write at once. This spec fixes all five.

## User stories and acceptance

Amounts below are integer cents unless written as text.

### S1 Money parsing — `ledger/money.py`

`parse_amount(text: str) -> int` returns cents; `format_amount(cents: int) -> str` returns text.

- AC1.1 `parse_amount("12.50") == 1250`, `parse_amount("-3") == -300`, `parse_amount("1,234.56") == 123456`, `parse_amount("0.1") == 10`.
- AC1.2 `""`, `"abc"`, `"1.234"`, `"1,23"` raise `ValueError("invalid amount: <text>")` with the original text.
- AC1.3 `format_amount(123456) == "1234.56"`, `format_amount(-5) == "-0.05"`, `format_amount(0) == "0.00"`.

### S2 Categories — `ledger/categories.py`

`normalize_category(text: str) -> str`.

- AC2.1 Strip, lowercase, and replace each run of internal whitespace with `-`: `" Food  Out "` → `"food-out"`.
- AC2.2 The result must match `^[a-z][a-z0-9-]{0,29}$`; otherwise raise `ValueError("invalid category: <text>")` with the original text. `"9lives"` and `""` are invalid.

### S3 Date filter — `ledger/query.py`

`filter_entries(entries, start=None, end=None) -> list` keeps entries whose ISO date is within `[start, end]`, inclusive, in the original order.

- AC3.1 With entries dated 2026-01-01, 2026-01-15 and 2026-02-01, `start="2026-01-15"` keeps the last two; `end="2026-01-15"` keeps the first two.
- AC3.2 `start > end` raises `ValueError("start after end")`.

### S4 Monthly summary — `ledger/query.py`

`summarize(entries) -> dict` returns `{ "YYYY-MM": { category: total_cents } }`.

- AC4.1 Two `food` entries in 2026-01 of 1250 and 250 plus one `rent` entry in 2026-02 of 90000 give `{"2026-01": {"food": 1500}, "2026-02": {"rent": 90000}}`.
- AC4.2 Months and categories iterate in sorted order.

### S5 CSV export — `ledger/csv_io.py`

`export_csv(entries) -> str`.

- AC5.1 The header is `date,amount,category,note`; amounts use `format_amount`; line endings are `\n`.
- AC5.2 Rows are sorted by date, keeping insertion order for equal dates. Quoting follows the `csv` module default, so the note `a,"b"` is written as `"a,""b"""`.

### S6 CSV import — `ledger/csv_io.py`

`import_csv(text) -> list[Entry]`, all or nothing. On any error raise `CsvImportError` whose `.errors` lists every problem as `line <n>: <message>`, where `n` is the file line number and the header is line 1.

- AC6.1 A header other than `date,amount,category,note` gives `["line 1: bad header"]`.
- AC6.2 Amounts go through `parse_amount` and categories through `normalize_category`; their `ValueError` messages become the error message. Two bad rows on lines 2 and 4 give two errors, and no entries are returned.

### S7 Storage format v2 — `ledger/models.py`, `ledger/store.py`

`Entry.amount` becomes integer cents everywhere. The file format becomes `{"version": 2, "entries": [...]}`.

- AC7.1 Loading a v1 file (no `version`, float amounts such as `12.5`) converts amounts to cents (`1250`), writes the original bytes unchanged to `<file>.v1.bak`, and rewrites the file as v2.
- AC7.2 Loading a v2 file changes nothing and writes no backup.
- AC7.3 `ledger list` still prints `2026-01-05 12.50 food lunch` for an entry of 1250 cents.

### S8 Concurrent append — `ledger/store.py`

- AC8.1 Two processes that each call `append` 50 times at the same time leave exactly 100 entries in a valid JSON file.
- AC8.2 Writes are atomic: a reader never sees a partly written file. Use a lock file with `fcntl.flock` and replace the file with `os.replace`.

### S9 CLI — `ledger/cli.py`

- AC9.1 `add` parses the amount with `parse_amount` and the category with `normalize_category`. Invalid input prints `error: <message>` to stderr and exits 2.
- AC9.2 `summary [--start D] [--end D]` prints one line per month and category, such as `2026-01 food 15.00`, in sorted order.
- AC9.3 `export` prints the CSV to stdout. `import <csv-path>` appends all imported entries and exits 0; on `CsvImportError` it prints each error to stderr, adds nothing and exits 1.

## Commands

- Initialization: None. Python 3 standard library only; no dependencies.
- Single test file: `python3 -B -m unittest tests.<module> -v`
- Full suite: `python3 -B -m unittest discover -s tests -v`
- Typecheck: N/A (standard-library fixture with no type checker configured).

## Out of scope

Currencies other than one decimal currency, multi-user access, packaging, and Windows file locking.
