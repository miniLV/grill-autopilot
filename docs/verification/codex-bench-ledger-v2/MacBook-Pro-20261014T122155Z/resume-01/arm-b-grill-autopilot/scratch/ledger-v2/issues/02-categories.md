# 02: Categories

Status: done
Blocked by: None
Implementer: worker
Files:
  - ledger/categories.py
  - tests/test_categories.py
Interface: normalize_category(text: str) -> str
Examples:
  - AC2.1: Strip, lowercase, and replace each run of internal whitespace with `-`: `" Food  Out "` → `"food-out"`.
  - AC2.2: The result must match `^[a-z][a-z0-9-]{0,29}$`; otherwise raise `ValueError("invalid category: <text>")` with the original text. `"9lives"` and `""` are invalid.
  - Edge: normalize_category("Food\tOut") == "food-out"; 30-letter category accepted; 31 letters rejected with original-text error
Verify:
  - python3 -B -m unittest tests.test_categories -v
  - N/A: typecheck; standard-library fixture with no type checker configured
Context: spec.md#S2; prior art: tests/test_store.py
Do not: edit files outside Files · weaken, skip or delete assertions · add dependencies

## Acceptance
- [ ] AC2.1: Strip, lowercase, and replace each run of internal whitespace with `-`: `" Food  Out "` → `"food-out"`.
- [ ] AC2.2: The result must match `^[a-z][a-z0-9-]{0,29}$`; otherwise raise `ValueError("invalid category: <text>")` with the original text. `"9lives"` and `""` are invalid.

## Implementation context
Agreed seam public category function.

## Comments

- 2026-10-14T12:11:37.179805+00:00: Prepared at 9d5c4374ad0bc60e7bd6b09d99cf8356913d6533; initialization None, baseline PASS /Users/tyrion/autopilot-bench-ledger-v2-b-fixed-20261014T120228Z/arm-b-grill-autopilot/.scratch/ledger-v2/runs/ledger-v2-20261014T120629Z/logs/02-worker-1-baseline.json

- 2026-10-14T12:14:08.150554+00:00: DONE check PASS, planner tip merge candidate 4bc063608ea85d70e2692db75b1fb739700d00ce base 9d5c4374ad0bc60e7bd6b09d99cf8356913d6533

- 2026-10-14T12:17:08.247978+00:00: Reviewer PASS 4bc063608ea85d70e2692db75b1fb739700d00ce; serialized integration Verify PASS 35bda48aa7c00edfc4edbff3075a498fb7f2f8e1
