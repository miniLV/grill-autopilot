# 04: Monthly summary

Status: blocked
Blocked by: 03
Implementer: escalate (ordering: sorted months and categories)
Files:
  - ledger/query.py
  - tests/test_query_summary.py
Interface: summarize(entries) -> dict
Examples:
  - AC4.1: Two `food` entries in 2026-01 of 1250 and 250 plus one `rent` entry in 2026-02 of 90000 give `{"2026-01": {"food": 1500}, "2026-02": {"rent": 90000}}`.
  - AC4.2: Months and categories iterate in sorted order.
  - Edge: summarize([]) == {}; Jan food amounts100,-100 -> {"2026-01":{"food":0}}
Verify:
  - python3 -B -m unittest tests.test_query_summary -v
  - N/A: typecheck; standard-library fixture with no type checker configured
Context: spec.md#S4; prior art: ledger/query.py
Do not: edit files outside Files · weaken, skip or delete assertions · add dependencies

## Acceptance
- [ ] AC4.1: Two `food` entries in 2026-01 of 1250 and 250 plus one `rent` entry in 2026-02 of 90000 give `{"2026-01": {"food": 1500}, "2026-02": {"rent": 90000}}`.
- [ ] AC4.2: Months and categories iterate in sorted order.

## Implementation context
Preserve filter_entries. Input Feb rent90000, Jan rent100, Jan food50 -> months ["2026-01","2026-02"], Jan categories ["food","rent"]. Public query seam.

## Comments

- 2026-10-14T12:17:44.184689+00:00: Prepared at d7166bf961d7bfd30d2634cbbd3d917352c6fdbe; initialization None, baseline PASS /Users/tyrion/autopilot-bench-ledger-v2-b-fixed-20261014T120228Z/arm-b-grill-autopilot/.scratch/ledger-v2/runs/ledger-v2-20261014T120629Z/logs/04-escalate-1-baseline.json

- 2026-10-14T12:20:11.988847+00:00: DONE check PASS, planner tip merge candidate 971bb373a3b98ac6f89a7857cc44e21d1712b55d base d7166bf961d7bfd30d2634cbbd3d917352c6fdbe

- 2026-10-14T12:43:50.737463+00:00: unsafe recovery: saved reviewer04/05/07 identities unreachable; list_agents only root and interrupt_agent returned not_found for all three; inactivity/result/resource release cannot be confirmed; committed candidate preserved, no reviewer replay
