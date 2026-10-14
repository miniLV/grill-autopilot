# 08: Concurrent append

Status: done
Blocked by: 07
Implementer: escalate (concurrency and atomic shared storage)
Files:
  - ledger/store.py
  - tests/test_store.py
Interface: store.append(path, entry); public store.load/save remain usable
Examples:
  - AC8.1: Two simultaneous independent processes append 50 entries each -> store.load returns exactly 100 entries and 50 notes from each process
  - AC8.2: Repeated store.load from a reader during append/save writes -> no JSONDecodeError and final 100 entries; source uses fcntl.flock and os.replace
  - Edge: simultaneous first append on nonexistent ledger leaves both entries; migrations and save/load should share lock protocol without nested-lock deadlock; cleanup temporary files after errors. Lock sidecar persists. Keep v1 exact backup and v2 no-change load guarantees.
Verify:
  - python3 -B -m unittest tests.test_store -v
  - N/A: standard-library fixture has no type checker
Context: spec.md#S8; prior art: ledger/store.py; tests/test_store.py
Do not: edit files outside Files · weaken, skip or delete assertions · add dependencies

## Acceptance
- [ ] AC8.1: Serialize whole append read-modify-write using stable lock file and fcntl.flock.
- [ ] AC8.2: Write atomically with same-directory temporary file and os.replace; readers never see partial JSON.

## Comments

- 2026-10-14T13:22:23.571804+00:00: Preparation passed; implementation attempt planned, not yet charged.

- 2026-10-14T13:28:09.180926+00:00: DONE check passed; planner tip merge produced 98ac0481a10845fc3a9ee2ed5ac99526e661e211 against ba80142544092242b75bd0dc187805121093f8fb

- 2026-10-14T13:34:20.377296+00:00: Reviewer PASS and exact integration Verify passed at 0c70269e6be88a7c1be6bcb4ebcb8ec88b496262
