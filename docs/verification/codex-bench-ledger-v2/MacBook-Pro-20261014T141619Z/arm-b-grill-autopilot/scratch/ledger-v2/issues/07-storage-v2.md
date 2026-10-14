# 07: Storage format v2

Status: done
Blocked by: 01
Implementer: escalate (data migration and shared representation across modules)
Files:
  - ledger/models.py
  - ledger/store.py
  - ledger/cli.py
  - tests/test_store.py
  - tests/test_cli.py
Interface: Entry.amount: int cents; store.load(path), store.save(path, entries), store.append(path, entry); CLI add/list compatible
Examples:
  - AC7.1: Raw b'{"entries": [{"date":"2026-01-05","amount":12.5,"category":"food","note":"lunch"}]}' -> Entry amount 1250, backup bytes exactly original, file {"version":2,"entries":[...amount 1250...]}
  - AC7.2: Existing {"version":2,"entries":[{"date":"2026-01-05","amount":1250,"category":"food","note":"lunch"}]} -> same bytes after load; no .v1.bak
  - AC7.3: CLI add 2026-01-05 12.5 food lunch followed by list -> "2026-01-05 12.50 food lunch\n"
  - Edge: missing file -> []; save/reload Entry amount -5 -> -5 and display -0.05. Convert legacy amounts from decimal string using Decimal to cents with ROUND_HALF_UP; update existing float round-trip assertions to literal cents as required by S7. For this story use parse_amount in add and format_amount in list; category errors and new commands remain S9. Also run python3 -B -m unittest tests.test_cli -v.
Verify:
  - python3 -B -m unittest tests.test_store -v
  - python3 -B -m unittest tests.test_cli -v
  - N/A: standard-library fixture has no type checker
Context: spec.md#S7; prior art: ledger/store.py; ledger/cli.py; tests/test_store.py; tests/test_cli.py
Do not: edit files outside Files · weaken, skip or delete assertions · add dependencies

## Acceptance
- [ ] AC7.1: Migrate missing-version v1 float amounts to integer cents, back up exact original bytes, rewrite version 2.
- [ ] AC7.2: A v2 load makes no file changes and creates no backup.
- [ ] AC7.3: Keep CLI money display consistent after migrating Entry to cents.

## Comments

- 2026-10-14T13:13:24.893276+00:00: Preparation passed; implementation attempt planned, not yet charged.

- 2026-10-14T13:18:09.806642+00:00: DONE check passed; planner tip merge produced df02c7c071649144c23cbcab357527849d2cb08c against 5e768749ba71bb6289746020d47f63ba44dde258

- 2026-10-14T13:22:21.626654+00:00: Reviewer PASS and exact integration Verify passed at ba80142544092242b75bd0dc187805121093f8fb
