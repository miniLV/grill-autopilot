# 02: Categories

Status: done
Blocked by: None
Implementer: worker
Files:
  - ledger/categories.py
  - tests/test_categories.py
Interface: normalize_category(text: str) -> str
Examples:
  - AC2.1: normalize_category(" Food  Out ") -> "food-out"
  - AC2.2: "9lives" -> ValueError("invalid category: 9lives"); "" -> ValueError("invalid category: ")
  - Edge: "A\tB" -> "a-b"; "a" repeated 30 times stays valid; repeated 31 times raises ValueError with the original text.
Verify:
  - python3 -B -m unittest tests.test_categories -v
  - N/A: standard-library fixture has no type checker
Context: spec.md#S2; prior art: tests/test_store.py; ledger/models.py
Do not: edit files outside Files · weaken, skip or delete assertions · add dependencies

## Acceptance
- [ ] AC2.1: Strip, lowercase and collapse internal whitespace to a hyphen.
- [ ] AC2.2: Require normalized result to match ^[a-z][a-z0-9-]{0,29}$ and retain original text in errors.

## Comments

- 2026-10-14T13:00:18.694419+00:00: Preparation passed; implementation attempt planned, not yet charged.

- 2026-10-14T13:02:40.386684+00:00: DONE check passed; planner tip merge produced 25a4700ba35d0fe48b22d78ad5ff8a4d47b35c36 against 6380caf932906eb22e6384a0f2d6cd571547b725

- 2026-10-14T13:06:11.838510+00:00: Reviewer PASS and exact integration Verify passed at d30d78b3a13b12e4afd987511e6df9b2892a80f6
