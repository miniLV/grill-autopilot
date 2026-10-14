# 02: Atomic storage and concurrent append

**What to build:** Concurrent ledger processes retain every appended entry, while readers always see a complete JSON snapshot, including during legacy migration.

**Blocked by:** 01: Exact money and categories with v2 migration

**Status:** resolved

- [x] Implement S8 / AC8.1: two processes appending 50 entries each retain exactly 100 entries.
- [x] Implement S8 / AC8.2: lock-file flock protects read-modify-write and os.replace publishes atomic snapshots.
- [x] Keep migration backups byte-exact and preserve v2 read behavior; writes and migration share the same locking discipline.
- [x] Use TDD at the pre-approved store API, concurrent process API, and persisted-format seams; keep the full suite green.

## Comments

- Claimed by implementer 02. Confirmed branch includes integration tip `8790fdb`. Approved seams: store API, real concurrent processes, and persisted-format reader. TDD references read; no glossary or ADR present.
- TDD slice 1: synchronized two-process 50-append test failed with JSONDecodeError / worker exit 1; append flock made all six store tests pass, retaining all 100 unique notes.
- TDD slice 2: direct readers during 50 replacements observed 268 JSON decode errors before the change; same-directory temporary snapshots plus `os.replace` made all seven store tests pass.
- TDD slice 3: migration completed while a writer held the lock (red); one shared lock and unlocked internal load/save operations prevented that race without nested flock acquisition (green). Concurrent migration plus 100 appends retains all 101 entries and byte-exact backup.
- Verification: full suite `PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -s tests -v` passed all 16 tests; `git diff --check` passed. Standard library only. Status remains claimed pending integration verification.

## Answer

Implemented in 482ebb82217deebe237227eb4823c47449701658; integrated as 8062de48a55c48c5c3dc9ea72d95720fd846ae98. Final code-review fixes integrated as 5d80366b16f6341b56bce380cd8bd380a1bd5a9e. Root independently verified the final full suite: all 38 tests passed. All acceptance criteria complete; no blockers remain.
