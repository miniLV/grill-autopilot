# 01: slugify public function

Status: done
Blocked by: None
Implementer: worker
Files:
  - textkit/slug.py
  - tests/test_slug.py
Interface: `textkit.slug.slugify(text: str) -> str`
Examples:
  - AC1: slugify("Hello, World!") → "hello-world"
  - AC1: slugify("a  --  b") → "a-b" (run of non-alphanumerics becomes one "-")
  - AC1: slugify("--Hi--") → "hi" (leading/trailing "-" removed)
  - AC1 edge: slugify("   ") → ""
Verify:
  - python3 -B -m unittest tests.test_slug -v (pre-implementation baseline: python3 -B -m unittest tests.test_core -v)
  - Typecheck: N/A (stdlib-only fixture with no type checker; agreed in grill)
Context: spec.md#Acceptance; prior art: textkit/core.py (call textkit.core.normalize first), tests/test_core.py
Do not: edit files outside Files · weaken, skip or delete assertions · add dependencies

## Acceptance
- [ ] AC1: `slugify` lowercases via `textkit.core.normalize`, collapses each run of non-alphanumeric characters to one `-`, strips leading/trailing `-`, and returns "" for whitespace-only input.

## Comments
- planner: reviewer PASS; merged to integration; full suite green.
