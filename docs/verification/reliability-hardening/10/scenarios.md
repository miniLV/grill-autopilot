# Ticket 10: final-tip protocol walkthroughs

Approved seam: skill-run input → Git/worktree state, ticket state and brief. These are literal manual protocol tables, not executed review/model results or a scheduler. The 40-character SHAs below are synthetic immutable identities, not commits in this repository. In every table the saved run `base_sha` is `0000000000000000000000000000000000000000`; the base branch moving later does not change the comparison.

## RED at clean baseline `5ac4a944ffe3c04962b0e72fc516d707161afbf1`

| Ticket example | Baseline gap observed before product edits |
| --- | --- |
| Initial review has no findings, suite green | Zero-fix path exists, but no durable two-axis SHA/check fields qualify it. |
| Fix makes checks green by weakening assertions | Main step reruns checks after a fix without requiring both axes to review that new SHA. |
| Two fixes leave a finding | failures.md allows one correction; config has no final_review budget. |
| Tip moves after PASS | Current-tip result is required, but final workflow uses the moving base branch and has no requalification path for changed tip/content. |

## 1. Initial review green: zero fixes

Input: all tickets done, safe inactive writers, clean integration. Initial checks are green and neither axis has findings.

| Event / exact integration SHA | Final fix count | Suite / applicable typecheck evidence SHA | Standards verdict / SHA | Spec verdict / SHA | Decision |
| --- | --- | --- | --- | --- | --- |
| Capture tip `1111111111111111111111111111111111111111`; run checks | 0 | PASS / PASS at `1111111111111111111111111111111111111111` | pending | pending | Review this exact tip against saved base SHA. |
| Both reviews complete; recheck unchanged clean tip `1111111111111111111111111111111111111111` | 0 | PASS / PASS at `1111111111111111111111111111111111111111` | PASS `1111111111111111111111111111111111111111` | PASS `1111111111111111111111111111111111111111` | **success**, zero fixer calls; save brief. |

Unique terminal result: **success**. Zero findings plus green current evidence consumes no correction budget.

## 2. Green checks after weakened assertions

Input: all tickets done; initial Spec finding says behavior is incorrect. Fixer changes the assertion so the suite turns green while the required behavior remains wrong.

| Event / exact integration SHA | Final fix count | Suite / applicable typecheck evidence SHA | Standards verdict / SHA | Spec verdict / SHA | Decision |
| --- | --- | --- | --- | --- | --- |
| Initial tip `2222222222222222222222222222222222222222` | 0 | FAIL / PASS at `2222222222222222222222222222222222222222` | PASS `2222222222222222222222222222222222222222` | FAIL `2222222222222222222222222222222222222222`: incorrect behavior | Safe correction round 1. |
| Fix weakens assertion; tip `3333333333333333333333333333333333333333`; rerun both checks and both axes | 1 | PASS / PASS at `3333333333333333333333333333333333333333` | FAIL `3333333333333333333333333333333333333333`: weakened assertion | FAIL `3333333333333333333333333333333333333333`: behavior still wrong | Green alone cannot qualify; safe correction round 2. |
| Second fix still leaves weak assertion; tip `4444444444444444444444444444444444444444`; rerun checks and both axes | 2 | PASS / PASS at `4444444444444444444444444444444444444444` | FAIL `4444444444444444444444444444444444444444`: weakened assertion | FAIL `4444444444444444444444444444444444444444`: behavior still wrong | **failed**, budget exhausted; both remaining findings in brief; no third fix or push. |

Unique terminal result: **failed**. Each changed SHA is reviewed on both axes; earlier PASS never carries forward.

## 3. Two correction rounds still leave findings

Input: A done, B blocked for a known undelivered requirement. Initial Spec review lists B separately and finds unrelated deviation C in delivered A. The known blocked scope does not excuse C.

| Event / exact integration SHA | Final fix count | Suite / applicable typecheck evidence SHA | Standards verdict / SHA | Spec verdict / SHA | Decision |
| --- | --- | --- | --- | --- | --- |
| Initial tip `5555555555555555555555555555555555555555` | 0 | PASS / PASS at `5555555555555555555555555555555555555555` | PASS `5555555555555555555555555555555555555555` | FAIL `5555555555555555555555555555555555555555`: C; B undelivered separately | Safe correction round 1. |
| Round 1 produces `6666666666666666666666666666666666666666`; rerun checks and both axes | 1 | PASS / PASS at `6666666666666666666666666666666666666666` | PASS `6666666666666666666666666666666666666666` | FAIL `6666666666666666666666666666666666666666`: C remains | Safe correction round 2. |
| Round 2 produces `7777777777777777777777777777777777777777`; rerun checks and both axes | 2 | PASS / PASS at `7777777777777777777777777777777777777777` | PASS `7777777777777777777777777777777777777777` | FAIL `7777777777777777777777777777777777777777`: C remains | **failed**, no third correction. Brief: remaining finding C; undelivered B with blocked reason in separate fields. |

Unique terminal result: **failed**, overriding partial. A red suite at the same final SHA would independently require failed even if both axes passed. With no C and all current checks/both axes PASS, A done/B blocked would qualify partial and remain local.

## 4. Tip changes after PASS

Input: all tickets done; qualified initial PASS. An attributable committed change advances the clean tip before delivery; writers are inactive. Saved base ref later moves, but its saved SHA stays fixed.

| Event / exact integration SHA | Final fix count | Suite / applicable typecheck evidence SHA | Standards verdict / SHA | Spec verdict / SHA | Decision |
| --- | --- | --- | --- | --- | --- |
| Initial tip `8888888888888888888888888888888888888888` is checked/reviewed | 0 | PASS / PASS at `8888888888888888888888888888888888888888` | PASS `8888888888888888888888888888888888888888` | PASS `8888888888888888888888888888888888888888` | Provisionally qualified; final tip recheck required. |
| Attributable advance to `9999999999999999999999999999999999999999` | 0 | Historical at `8888888888888888888888888888888888888888`; current missing | Historical PASS `8888888888888888888888888888888888888888` | Historical PASS `8888888888888888888888888888888888888888` | Delivery refused until new exact-tip checks and both axes; no renewed fix budget. |
| Bounded checks/reviews on `9999999999999999999999999999999999999999`; compare same saved base; recheck unchanged content | 0 | PASS / PASS at `9999999999999999999999999999999999999999` | PASS `9999999999999999999999999999999999999999` | PASS `9999999999999999999999999999999999999999` | **success** on new tip; no corrective call because new evidence is green. |

Unique terminal result: **success only after requalification**. Old PASS cannot authorize delivery during the middle row. Unexplained movement/dirty content instead uses the preserved-state failed exit; repeated movement is not an unbounded re-review loop.
