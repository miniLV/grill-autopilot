# 02: truncate public function

Status: done
Blocked by: None
Implementer: worker
Files:
  - textkit/trim.py
  - tests/test_trim.py
Interface: `textkit.trim.truncate(text: str, width: int) -> str`
Examples:
  - AC2: truncate("abcdef", 4) → "abc…" (U+2026, result length == width)
  - AC2: truncate("abc", 4) → "abc"
  - AC2: truncate("abcd", 4) → "abcd"
  - AC2 error: truncate("abc", 0) → raises ValueError("width must be >= 1")
  - AC2 edge: truncate("abcdef", 1) → "…"
Verify:
  - python3 -B -m unittest tests.test_trim -v (pre-implementation baseline: python3 -B -m unittest tests.test_core -v)
  - Typecheck: N/A (stdlib-only fixture with no type checker; agreed in grill)
Context: spec.md#Acceptance; prior art: textkit/core.py, tests/test_core.py
Do not: edit files outside Files · weaken, skip or delete assertions · add dependencies

## Acceptance
- [ ] AC2: `truncate` returns text unchanged when len(text) <= width, otherwise text[:width-1] + "…"; width < 1 raises ValueError("width must be >= 1").

## Comments
- planner: reviewer PASS; merged to integration; full suite green.
