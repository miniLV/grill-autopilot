# 01: Exact money and categories with v2 migration

**What to build:** Users add normalized categories and exact cent amounts, list correctly formatted money, and safely upgrade existing ledgers while preserving their original bytes.

**Blocked by:** None (can start immediately)

**Status:** resolved

- [x] Implement S1 / AC1.1–AC1.3 and S2 / AC2.1–AC2.2 with original-text errors and exact integer cents.
- [x] Implement S7 / AC7.1–AC7.3: integer Entry amounts, v2 envelope, byte-exact v1 backup and migration, unchanged v2 loads.
- [x] Implement S9 / AC9.1: add validates money and categories, stderr errors and exit 2; retain list output.
- [x] Use TDD at the pre-approved money/category functions, Entry serialization, store load/save/append, and CLI seams; keep the full suite green.

## Comments

- Claimed ticket 01. Pre-approved seams: money/category functions, Entry serialization, store load/save/append, and CLI. Worktree HEAD matches ledger-v2/integration at eb5f5f5. Following the TDD skill and its tests/mocking references with one behavior per red-green cycle.
- Money parsing: RED missing ledger.money; GREEN tests.test_money passed (1 test), exact cents for the four AC1.1 inputs.
- Amount rejection: RED malformed text either leaked Decimal errors or was accepted; GREEN tests.test_money passed (2 tests), original-text ValueError for every invalid amount.
- Amount formatting: RED missing format_amount; GREEN tests.test_money passed (3 tests), including negative cents, zero and an amount beyond float precision.
- Category normalization: RED missing ledger.categories; GREEN tests.test_categories passed (1 test), Food Out normalizes to food-out.
- Category validation: RED every invalid category was accepted; GREEN tests.test_categories passed (2 tests), preserving original text in errors.
- V2 save and Entry serialization: RED saved file omitted version; GREEN tests.test_store passed (3 tests). Entry.amount is annotated int and the legacy round-trip fixture now uses cents.
- V1 migration: RED load returned 12.5 instead of 1250; GREEN tests.test_store passed (4 tests), byte-exact CRLF backup and v2 rewrite verified.
- Added passing regression coverage for existing v2 no-write behavior: exact bytes, mtime and absent backup remain unchanged (tests.test_store, 5 tests).
- CLI add/list: RED comma amount failed with float conversion; GREEN tests.test_cli passed (2 tests), grouped input, normalized category, exact cents and unchanged list layout.
- CLI invalid input: RED returned 1 with traceback; GREEN tests.test_cli passed (3 tests), exact stderr, exit 2 and no file created.
- Full-suite verification: PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -s tests -v passed all 13 tests; git diff --check passed. Status remains claimed for integration review.

## Answer

Implemented in 0c35451d57cc04f5286d4b780890c09045f9d3e2; merged as 52ede8fe0377b7375bcc5091521985c09c65e1dd. Root independently verified the full suite: 13 tests passed. Tickets 02–04 are unblocked.
