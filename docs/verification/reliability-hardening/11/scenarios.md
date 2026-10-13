# Ticket 11: manual ticket-readiness walkthroughs

Approved seam: skill inputs → observable Git/worktree, ticket state and brief outputs. This ticket exercises the preparation gate's ticket readiness and recorded reasons; no worker, Git merge or runtime run is simulated. These are manual protocol decisions, not automated test results. Baseline: clean `da71bdf01c8963639606b3824cd0f3539ce9ceb4` on `codex/reliability-hardening/tickets/11`.

Each case uses a tiny synthetic approved spec, complete unrelated template fields and explicit inputs below. Follow tickets.md's Rules/Self-check, then SKILL.md step 3. A red case means the required readiness decision fails; it does not imply a shell command failed. Record red before changing the relevant guidance or fixture, then walk the correction. Literal expectations come from ticket 11's Examples and D12, independently of the checklist wording.

## 1. Incomplete source coverage

Input spec: US1 = `greet a named person`; acceptance S1 = `greet("Ada") → "Hello, Ada!"`. US2 = `greet without a name`; acceptance S2 = `greet("") → "Hello, world!"`. Both are in scope; approved exclusions: none. Ticket A lists only US1/S1 → AC1, with example `greet("Ada") → "Hello, Ada!"`, edge `greet("Lin") → "Hello, Lin!"`, Files `greeting.js`, no dependencies and no unresolved choice. The agreed seam accepts strings only and all strings have greetings, so rejected-input examples are inapplicable; empty string is the boundary addressed by S2.

RED before slice 1: applying the baseline checklist to A fills every field, gives its sole acceptance a literal example and finds no graph issue. It can wrongly declare the whole set ready. Expected result is **not ready: US2/S2 uncovered**. This is a missing gate, not an executed model result.

GREEN after slice 1: unchanged A now fails the coverage check: **not ready; missing US2 and S2**. Correct A by adding US2/S2 → AC2 and `greet("") → "Hello, world!"`; coverage table rows are US1/S1 → A/AC1 and US2/S2 → A/AC2. Every source item is delivered, so **ready**, frontier `{A}`. Removing S2 while retaining a US2 label still fails: stories alone cannot stand in for acceptance coverage. Marking US2/S2 `out-of-scope` locally fails because the approved spec has no such exclusion. A distinct spec-approved exclusion (e.g. US3/S3 `Spanish greeting`, excluded at spec Out of Scope) passes only with that exact pointer recorded. Mapping S2 to absent B/AC9 fails rather than claiming coverage.

## 2. Business prerequisite across disjoint files

Input spec: US1/S1 `makeToken("Ada") → "token:Ada"`; US2/S2 `renderToken("Ada") → "<b>token:Ada</b>"`, requiring the new makeToken interface. A delivers US1/S1 → AC1 in `token.js`. B delivers US2/S2 → AC1 in `view.js`. Their literal examples also include `makeToken("") → "token:guest"` and `renderToken("") → "<b>token:guest</b>"`. Every string input has a token; errors are inapplicable at this agreed string-only seam, and empty string is the boundary. All Source/table mappings are complete. Both initially say `Blocked by: None`.

RED before slice 2: the checklist validates the empty graph; disjoint Files can be mistaken for independence, making frontier `{A, B}`. Expected result: **not ready; B requires A's unavailable interface**. File isolation cannot establish that prerequisite.

GREEN after slice 2: unchanged B fails the independent business-prerequisite check. Set B to `Blocked by: A`; A stays `None`. The set is now **ready**, but its frontier is **`{A}` only**. B enters the frontier after A is `done`; if A is blocked, B cannot dispatch. Conversely, two independent tickets both writing `shared.md` need scheduling isolation even with no business edge; disjoint independent `a.md`/`b.md` may share the frontier, subject to runtime capacity. A prerequisite already available at the agreed baseline needs no invented delivery edge.

## 3. Vague acceptance, error and boundary inputs

Input spec: US1/S1 `increment integer n in [0,9]`; acceptance requires literal results for valid, boundary and rejected inputs. A delivers it via `increment(n)` in `counter.js`, Source US1/S1 → AC1, no dependencies. AC1 says only `works normally`; example `increment(1) → correct result`. No other fields are missing.

RED before slice 3: the existing checklist already rejects this example because `correct result` is not a literal expected value. Expected result: **not ready; AC1 has no concrete observable expectation**. This protection existed at baseline; this cycle improves example linkage and error/boundary coverage rather than claiming a new vague-example detector.

GREEN after slice 3: replace AC1 with `returns n+1 for integers 0 through 9; rejects other inputs with RangeError("n must be an integer from 0 to 9")`. Examples explicitly link AC1: `increment(1) → 2`, `increment(0) → 1`, `increment(9) → 10`, `increment(-1)`, `increment(10)`, `increment(1.5)` and `increment("1")` each → `RangeError("n must be an integer from 0 to 9")`. Decision: **ready**, frontier `{A}`. Removing the error examples while retaining valid/boundary values now fails. A docs-only ticket with no parsed external input may explain why numeric/error input classes are inapplicable, while still supplying concrete observable examples for each acceptance; missing checks cannot become a claimed pass.

## 4. Cycle, missing node and bounded complete slice

Input spec: US1/S1 `produceData("Ada") → "Ada"`; US2/S2 `emitReport("Ada") → "report:Ada"` using A's data. A delivers US1/S1 → AC1 in `data.js`, B delivers US2/S2 → AC1 in `report.js`. Linked examples also cover empty data: `produceData("") → ""`, `emitReport("") → "report:"`; errors are inapplicable for these fixed local string inputs. All source items are mapped. A incorrectly lists `Blocked by: B`; B lists `Blocked by: A`.

RED before slice 4: the existing checklist rejects the graph; expected result is **not ready; cycle A → B → A**, with no dispatch. Cycle detection existed at baseline. The file-count rule still frames more tickets as preferable and says to split any judgement call, without preserving independent acceptance or an explicit unresolved-design stop.

GREEN after slice 4: the approved spec shows no prerequisite on B for A, so correct A to `Blocked by: None`, leaving B dependent on A. Decision: **ready**, frontier `{A}`. If the spec truly required both directions, keep the gate closed and settle a spec/slice change instead of dropping a real edge. Variant B → C with no ticket C: **not ready; missing C referenced by B**; correction back to the actual producer A restores readiness. A → A: **not ready; self-cycle A → A**. These checks report specific IDs/chains, independently of Files.

Size boundary: if A's same independently verifiable `produceData("Ada") → "Ada"` behavior requires four production paths (`data.js`, `parse.js`, `format.js`, `storage.js`) and its test, list all five. More than three production files alone does **not** fail or force fragments that cannot be accepted independently. An undecided choice `choose a storage format` instead makes A **not ready**, even if it touches only one file; settle the choice in the approved spec or block preparation through the existing handled-stop/brief path. The size heuristic never overrides coverage or bounded design.

## Final replay

Manually replay all four unchanged red inputs against the final guidance: each set stays **not ready** with the reasons above. Replay each corrected input: all are **ready**; frontiers are respectively `{A}`, `{A}`, `{A}`, `{A}`. In cases 2/4 B becomes eligible only after A is done. Missing coverage, vague/error-incomplete examples, absent producer edges, missing graph nodes or cycles each independently prevent the step-3 completion gate. No model was launched and no runtime result/brief was observed; a handled unresolved-design stop's brief is required by the existing failures authority, not produced by these tables.
