# 02: Categories

Status: blocked
Blocked by: None
Implementer: worker
Files:
  - ledger/categories.py
  - tests/test_categories.py
Interface: normalize_category(text: str) -> str
Examples:
  - AC2.1: normalize_category(" Food  Out ") == "food-out"
  - AC2.2: "9lives" raises ValueError("invalid category: 9lives"); "" raises ValueError("invalid category: ")
  - Edge: normalize_category("a" * 30) == "a" * 30; "a" * 31 raises ValueError("invalid category: " + "a" * 31)
Verify:
  - python3 -B -m unittest tests.test_categories -v
  - N/A: typecheck; standard-library fixture has no type checker configured.
Context: spec.md#s2; prior art: tests/test_store.py
Do not: edit files outside Files · weaken, skip or delete assertions · add dependencies

## Acceptance
- [ ] AC2.1: Strip, lowercase and replace runs of internal whitespace by hyphen.
- [ ] AC2.2: Require normalized category to match ^[a-z][a-z0-9-]{0,29}$ and preserve original text in errors.

## Comments

- 2026-10-14T11:27:47.284108+00:00 Blocked by run-wide integration preparation failure; no implementation or review started.
