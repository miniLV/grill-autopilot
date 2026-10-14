# 07: Storage format v2

Status: in-review
Blocked by: 01, 02
Implementer: escalate (data migration and state shared across models/store/CLI)
Files:
  - ledger/models.py
  - ledger/store.py
  - ledger/cli.py
  - tests/test_store.py
  - tests/test_cli.py
Interface: Entry.amount: int; load(path), save(path,entries), append(path,entry); add/list integer storage
Examples:
  - AC7.1: Loading a v1 file (no `version`, float amounts such as `12.5`) converts amounts to cents (`1250`), writes the original bytes unchanged to `<file>.v1.bak`, and rewrites the file as v2.
  - AC7.2: Loading a v2 file changes nothing and writes no backup.
  - AC7.3: `ledger list` still prints `2026-01-05 12.50 food lunch` for an entry of 1250 cents.
  - Edge: missing path -> []; save [] -> {"version":2,"entries":[]}; v1 amount -0.05 -> -5
Verify:
  - python3 -B -m unittest tests.test_store -v
  - python3 -B -m unittest tests.test_cli -v
  - N/A: typecheck; standard-library fixture with no type checker configured
Context: spec.md#S7; prior art: tests/test_store.py
Do not: edit files outside Files · weaken, skip or delete assertions · add dependencies

## Acceptance
- [ ] AC7.1: Loading a v1 file (no `version`, float amounts such as `12.5`) converts amounts to cents (`1250`), writes the original bytes unchanged to `<file>.v1.bak`, and rewrites the file as v2.
- [ ] AC7.2: Loading a v2 file changes nothing and writes no backup.
- [ ] AC7.3: `ledger list` still prints `2026-01-05 12.50 food lunch` for an entry of 1250 cents.

## Implementation context
AC7.1 v1 bytes {"entries":[{"date":"2026-01-05","amount":12.5,"category":"food","note":"lunch"}]} -> Entry amount1250, byte-exact original .v1.bak, rewritten {"version":2,"entries":[...amount1250...]}. AC7.2 v2 input remains byte-identical and no backup. AC7.3 CLI add then list -> "2026-01-05 12.50 food lunch\n", stored1250. Existing store test literal amount changes12.5->1250 for new representation, preserving round-trip assertion and strengthening coverage. CLI add now uses money/category functions; list format_amount so integration remains green. Atomic locking ticket08, new CLI commands09. Public store and CLI seams.

## Comments

- 2026-10-14T12:17:08.985783+00:00: Prepared at 35bda48aa7c00edfc4edbff3075a498fb7f2f8e1; initialization None, baseline PASS /Users/tyrion/autopilot-bench-ledger-v2-b-fixed-20261014T120228Z/arm-b-grill-autopilot/.scratch/ledger-v2/runs/ledger-v2-20261014T120629Z/logs/07-escalate-1-baseline.json

- 2026-10-14T12:20:47.964036+00:00: DONE check PASS, planner tip merge candidate e3b5ba6ba21b25f9281ec84e39f3d4fd41bd2fa1 base d7166bf961d7bfd30d2634cbbd3d917352c6fdbe
