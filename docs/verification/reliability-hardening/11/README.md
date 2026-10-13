# Ticket 11: source coverage and business prerequisites

Scope: approved US18/D12 ticket-preparation rules. Clean starting commit/integration: `da71bdf01c8963639606b3824cd0f3539ce9ceb4`; branch `codex/reliability-hardening/tickets/11`. Initial manual RED was recorded at `2026-10-13T17:46:31Z` (client date 2026-10-14, Asia/Shanghai). No blockers. Only tickets.md Rules/Self-check/Template, SKILL.md step-3 completion and this evidence directory changed; tracker/spec/index remain root-owned.

The agreed seam is skill inputs → observable Git/worktree, ticket and brief outputs. [scenarios.md](scenarios.md) exercises preparation readiness/reasons only. Four vertical manual RED → guidance/fixture correction → GREEN cycles were performed before final replay. Coverage/business edges were baseline gaps; vague-example and cycle rejection already existed and were retained. These decisions prove contract coverage, not runtime obedience.

## Acceptance trace

| Approved source | Evidence and manual result |
| --- | --- |
| US18: bounded task with concrete examples and independent completion | Cases 1–4 give literal inputs/results, explicit corrected readiness and frontier; unresolved design blocks preparation. |
| Ticket 11 AC1: template traces source; uncovered requirements cannot pass | Case 1: missing US2/S2 fails; Source and coverage rows map to A/AC2 to pass. Story-only, fabricated exclusions and nonexistent delivery mappings fail. Both stories **and** acceptance items are checked; only spec-approved exclusions are allowed. |
| Ticket 11 AC2: literal examples, boundaries and business edges | Cases 2/3: missing B→A fails, corrected B waits for A done; integer bounds/error strings are explicit and required. Case 4 reports A→B→A, B→missing C and A→A. |
| Ticket 11 AC3: Files isolation remains distinct | Case 2: disjoint Files still require B→A; shared Files still restrict scheduling for independent tickets. A baseline-existing prerequisite needs no fabricated delivery edge. |
| D12 / ticket 11 steps 1–3: set coverage, examples, business graph integrity | Cases 1–4: coverage ledger plus each Source/AC/example mapping; whole set fails on missing nodes, cycles or unmet prerequisites before step-3 readiness/freeze/dispatch. |
| Ticket 11 step 4: size is a heuristic, unresolved design blocks/spec | Case 4: one independently verifiable behavior across four production files stays together; required cyclic edges cannot be removed just to pass. An unsettled storage choice stops preparation under the existing scope/brief authority. |

There are no exclusions from this ticket's approved scope. Its D12 runtime success/failure/resume collection is assigned to ticket 13; these manual tables do not satisfy or drop that requirement.

## Reproduce and checks

Read each case in order, apply [tickets.md](../../../../skills/grill-autopilot/tickets.md)'s Rules/Self-check and [SKILL.md](../../../../skills/grill-autopilot/SKILL.md) step 3. Start with the incomplete input, record the reason the set cannot be ready, make its documented correction, then check its coverage, examples, graph and frontier. Follow the error/boundary variants independently. The final replay observed four rejected original inputs and four ready corrected sets, with `{A}` frontiers; B in cases 2/4 waits for A done. This is manual Verify with no shell exit code.

Actual read-only checks from the assigned worktree: `git status --short` (empty), `git branch --show-current`, `git log -1 --format='%H %s'`, and `git merge-base --is-ancestor da71bdf01c8963639606b3824cd0f3539ce9ceb4 HEAD`, all exit **0**. Integration still resolved to that SHA at `2026-10-13T17:49:15Z`. Product/new-file inspection and `git diff --check` exit **0**. Inline `python3` using `pathlib.Path.exists()` checked **17** relative Markdown link targets across these **4** changed files, exit **0**; it checks file existence only. Candidate commit, fixed integration-tip merge and post-merge check outputs are host-captured and returned in the worker handoff.

## Limits

No production test suite/typecheck, model launch, scheduler, runtime review or actual end-to-end run was performed. No prose-string tests, new executable logic or dependency was added. Manual readiness decisions and structural file checks cannot establish a real runtime's adherence; ticket 13 remains necessary. No push, PR, upstream companion, global config or plexus change.
