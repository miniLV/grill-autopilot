# 01: Money parsing

Status: done
Blocked by: None
Implementer: worker
Files:
  - ledger/money.py
  - tests/test_money.py
Interface: parse_amount(text: str) -> int; format_amount(cents: int) -> str
Examples:
  - AC1.1: parse_amount("12.50") -> 1250; parse_amount("-3") -> -300; parse_amount("1,234.56") -> 123456; parse_amount("0.1") -> 10
  - AC1.2: "", "abc", "1.234", "1,23" -> ValueError("invalid amount: <original text>")
  - AC1.3: format_amount(123456) -> "1234.56"; format_amount(-5) -> "-0.05"; format_amount(0) -> "0.00"
  - Edge: parse_amount("-0.05") -> -5; parse_amount("+1") -> ValueError("invalid amount: +1"). Amount grammar is optional minus, ASCII digits, optional correctly grouped comma thousands, optional decimal with one or two digits; no surrounding whitespace.
Verify:
  - python3 -B -m unittest tests.test_money -v
  - N/A: standard-library fixture has no type checker
Context: spec.md#S1; prior art: tests/test_store.py; ledger/models.py
Do not: edit files outside Files · weaken, skip or delete assertions · add dependencies

## Acceptance
- [ ] AC1.1: Parse decimal amounts and correctly grouped thousands into exact integer cents.
- [ ] AC1.2: Reject malformed amount text with the original text in the ValueError.
- [ ] AC1.3: Format cents with two digits and no grouping.

## Comments

- 2026-10-14T13:00:18.015677+00:00: Preparation passed; implementation attempt planned, not yet charged.

- 2026-10-14T13:03:38.590103+00:00: DONE check passed; planner tip merge produced 324dc670df89951d42e7780e5d63c2f494e5f688 against 6380caf932906eb22e6384a0f2d6cd571547b725

- 2026-10-14T13:07:46.255324+00:00: Business retry allowed: worker count 1 < 2; reviewer leading-zero grouping finding. Same clean worktree retained.

- 2026-10-14T13:09:28.088860+00:00: DONE check passed; planner tip merge produced d78da4bbe443e1249acb161777bacbdd26e47769 against 0de76fabf581f097f0d87d547378c316929eb020

- 2026-10-14T13:13:23.012713+00:00: Reviewer PASS and exact integration Verify passed at 245c5cc6333bdd01e2946d79389b55ad034db1b4
