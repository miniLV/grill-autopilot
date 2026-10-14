# 03: python3 -m textkit CLI

Status: blocked
Blocked by: 01, 02
Implementer: worker
Files:
  - textkit/__main__.py
  - tests/test_cli.py
Interface: `python3 -m textkit slug <text>` | `python3 -m textkit trim <width> <text>`; result + newline on stdout, exit 0; unknown command → `unknown command: <cmd>` + newline on stderr, exit 2
Examples:
  - AC3: python3 -m textkit slug "Hello World" → stdout "hello-world\n", exit 0
  - AC3: python3 -m textkit trim 4 abcdef → stdout "abc…\n", exit 0
  - AC3 error: python3 -m textkit x → stderr "unknown command: x\n", exit 2
  - AC3 edge: python3 -m textkit trim 4 abc → stdout "abc\n", exit 0
Verify:
  - python3 -B -m unittest tests.test_cli -v (pre-implementation baseline: python3 -B -m unittest tests.test_core -v)
  - Typecheck: N/A (stdlib-only fixture with no type checker; agreed in grill)
Context: spec.md#Acceptance; prior art: textkit/slug.py, textkit/trim.py (from tickets 01/02), tests/test_core.py; tests run the CLI via subprocess with sys.executable, cwd = repo root, encoding utf-8
Do not: edit files outside Files · weaken, skip or delete assertions · add dependencies

## Acceptance
- [ ] AC3: CLI dispatches `slug` to `textkit.slug.slugify` and `trim` to `textkit.trim.truncate(text, int(width))`, prints the result to stdout and exits 0; an unknown command prints `unknown command: <cmd>` to stderr and exits 2. Tests use subprocess.

## Comments
- planner: blocked before dispatch — run USD budget exhausted ($0.46 left after the 01/02 review) before a worker+reviewer+final review could run. Unblocked by 01/02; ready for a new run.
