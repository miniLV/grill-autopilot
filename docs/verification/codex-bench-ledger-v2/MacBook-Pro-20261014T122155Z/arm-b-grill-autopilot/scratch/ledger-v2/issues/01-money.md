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
  - AC1.2: parse_amount("") raises ValueError("invalid amount: "); "abc", "1.234", "1,23" raise ValueError("invalid amount: <original text>")
  - AC1.3: format_amount(123456) -> "1234.56"; format_amount(-5) -> "-0.05"; format_amount(0) -> "0.00"
  - Edge: parse_amount("0") -> 0; parse_amount("1,234,567.89") -> 123456789; format_amount(-300) -> "-3.00"
Verify:
  - python3 -B -m unittest tests.test_money -v
  - N/A: typecheck; standard-library fixture with no type checker configured
Context: spec.md#S1; prior art: tests/test_store.py
Do not: edit files outside Files · weaken, skip or delete assertions · add dependencies

## Acceptance
- [ ] AC1.1: Parse exact integer cents from decimal text and correctly grouped commas.
- [ ] AC1.2: Reject the four invalid literals with exact original-text errors.
- [ ] AC1.3: Format integer cents with exactly two decimal places.

## Implementation context
Use exact decimal/integer arithmetic, never float. Standard signed decimal spellings only; grouped comma blocks have 3 digits; no whitespace/exponents. Public money seam catches parsing/formatting, misses CLI/storage wiring.

## Comments

- 2026-10-14T12:11:36.547981+00:00: Prepared at 9d5c4374ad0bc60e7bd6b09d99cf8356913d6533; initialization None, baseline PASS /Users/tyrion/autopilot-bench-ledger-v2-b-fixed-20261014T120228Z/arm-b-grill-autopilot/.scratch/ledger-v2/runs/ledger-v2-20261014T120629Z/logs/01-worker-1-baseline.json

- 2026-10-14T12:13:47.635864+00:00: DONE check PASS, planner tip merge candidate 1fb64788888563f92c2cccd2d55fb651ddfdf281 base 9d5c4374ad0bc60e7bd6b09d99cf8356913d6533

- 2026-10-14T12:16:31.429920+00:00: Reviewer PASS 1fb64788888563f92c2cccd2d55fb651ddfdf281; serialized integration Verify PASS 0f82b4023d244ac39aa894683709d6c7e1936da5
