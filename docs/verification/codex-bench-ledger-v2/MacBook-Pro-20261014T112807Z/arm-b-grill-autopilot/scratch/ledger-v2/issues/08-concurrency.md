# 08: Concurrent append

Status: blocked
Blocked by: 07
Implementer: escalate (concurrency, ordering and shared state)
Files:
  - ledger/store.py
  - tests/test_store.py
Interface: store.append(path,entry), load(path), save(path,entries); lock file with fcntl.flock and atomic os.replace
Examples:
  - AC8.1: Two processes each append Entry("2026-01-05",100,"food","a") or note "b" 50 times simultaneously; final load length == 100 and note counts == {"a":50,"b":50}
  - AC8.2: Reader repeatedly loads during concurrent writes: every observed value is a complete valid entry list, no JSONDecodeError, final count 100; implementation uses fcntl.flock on a separate lock file and os.replace
  - Edge: First append to missing path yields exactly [Entry("2026-01-05",100,"food","first")]; prior migration/load tests remain green.
Verify:
  - python3 -B -m unittest tests.test_store -v
  - N/A: typecheck; standard-library fixture has no type checker configured.
Context: spec.md#s8; prior art: ledger/store.py; tests/test_store.py
Do not: edit files outside Files · weaken, skip or delete assertions · add dependencies

## Acceptance
- [ ] AC8.1: Concurrent append preserves all entries in valid JSON.
- [ ] AC8.2: Atomic replace prevents readers seeing partially written data and lock covers read-modify-write.

## Comments

- 2026-10-14T11:27:47.284645+00:00 Blocked by run-wide integration preparation failure; no implementation or review started.
