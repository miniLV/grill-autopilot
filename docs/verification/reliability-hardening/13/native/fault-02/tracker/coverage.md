# Actual planner whole-set coverage and self-check

Root manually checked all coverage rows, examples, Files and prerequisites before publication; this set is approved and ready, implementation is not yet started.

| Approved story | Requirement | Delivering ticket / acceptance | Concrete task examples |
| --- | --- | --- | --- |
| US1 | N1 | 01 / AC1 | ' Ada ' and '\tAda\n' -> 'Ada' |
| US1 | N2 | 01 / AC2 | '' -> '' |
| US1 | N3 | 01 / AC3 | 'Ada' -> 'Ada' |
| US2 | L1 | 02 / AC1 | '0' -> integer0 |
| US2 | L2 | 02 / AC2 | '2' -> integer2 |
| US2 | L3 | 02 / AC3 | 'x' and '' each -> ValueError |
| US2 | L4 | 02 / AC4 | '1' -> integer1 |
| US3 | M1 | 03 / AC1 | (' Ada ','2') -> 'Ada:2' |
| US3 | M2 | 03 / AC2 | ('','0') -> ':0' |
| US3 | M3 | 03 / AC3 | ('Ada','x') -> ValueError |

Root self-check PASS: all template fields filled; every story and acceptance requirement covered; every acceptance has concrete literal examples; each ticket has boundary examples and applicable error examples or approved out-of-scope input classes; no worker design decision; every touched path in Files; dependencies acyclic (01/02 ->03). 01/02 have independent behavior and disjoint writable Files. 03's required semantics come from business prerequisites 01/02 even though its writable Files are disjoint.

The existing signature stubs already exist at baseline. New test modules intentionally do not exist; existing tests.test_baseline supplies every preparation gate. Existing baseline tests are read-only to workers and remain mandatory Verify. Root runtime/control, record/fingerprint/ownership/cleanliness/review/brief obligations remain the product protocol, not extra implementation tickets or undocumented exclusions.
