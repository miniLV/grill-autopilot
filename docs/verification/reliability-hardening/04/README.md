# Ticket 04: worktree preparation evidence

Scope: D5 initialization and baseline gates. This is one fresh temporary Git fixture plus real command results and labeled planner records. It does not implement a scheduler, automatic attempt accounting or the later general failure lifecycle.

## Reproduce

From the repository root:

```sh
python3 docs/verification/reliability-hardening/04/experiment.py > /tmp/grill-autopilot-04.log
git diff --check
```

Both returned **0** on 2026-10-13. The experiment was run before changing the product docs and again afterward. [experiment.log](experiment.log) records actual canonical working directories, commands, exit codes, hashes and scripted planner handoffs; temporary paths/SHAs differ per run. The fixture uses Python's standard library and an artificial local dependency module generated from a literal fixture lock pin. It neither installs network dependencies nor creates credentials.

## Actual Git and command observations

| Scenario | Observed command behavior and preservation |
| --- | --- |
| Original checkout has ignored `.deps/fixture_dep.py` | Its initialization and baseline test return **0**; `git check-ignore` confirms the module is ignored. |
| Fresh integration worktree | The module is absent. Before initialization, baseline returns **1** with ModuleNotFoundError. Initialization returns **0**, then the same behavior test returns **0**. Tracked business/init/test/lock/ignore bytes remain unchanged. |
| Fresh ticket worktree | The same absent dependency → exit **1** → initialization **0** → baseline **0** sequence occurs independently. Original checkout dependencies are not reused. |
| Initialization exits **7** | The literal failure command returns **7**. No baseline or implementation call follows; tracked bytes remain unchanged. |
| Initialization succeeds but inherited baseline is red | A deliberate fixture defect is committed **before** the preparation experiment. Initialization returns **0**; the existing behavior test returns **1** because export returns 41 instead of the independently specified 42. No business repair follows, and all tracked bytes remain equal to their pre-gate hashes. |

Original tracked content, checkout ref and base SHA were recorded before/after without change. All inspected worktree status outputs are empty after preparation; generated dependency files are ignored. The bad-baseline fixture commit is setup data, not a worker implementation.

## Planner and check-choice rehearsal

The log labels every synthetic preparation/counter record `PLANNER REHEARSAL`. The integration/ticket success records are ready for implementation but still show implementation attempts **0**, because no worker was dispatched. The exit-7 and baseline-red records are environment errors with evidence/handoff reasons and implementation attempts **0**. These exercise the prescribed classification manually; they do not prove a host scheduler applies it automatically.

The typecheck choice is **N/A**, with the explicit reason that this standard-library Python fixture has an artificial local module and no configured static-type checker/contract. Behavior tests still ran; no typecheck pass or exit code is fabricated. The initialization-None choice is a document/check-choice rehearsal only: it skips the initialization process when the environment is already runnable but never waives applicable baseline checks. This fixture actually needs its initializer, so it did not claim a successful None initialization for a missing dependency.

Product contract review found:

- Grill records initialization (including explicit None), ticket Verify, full suite and typecheck/N/A with a reason; known unavailable tools/credentials prevent readiness.
- Integration preparation precedes implementation dispatch; each ticket prepares separately before TDD. If its new test file is absent, the recorded existing seam baseline provides the pre-implementation check.
- Environment failure is distinct from implementation FAIL, and its worker reply uses the environment handoff rather than consuming implementation retries. No general failure budget or recovery engine is added here.
- Existing locked dependencies may be installed during preparation; dependency declaration/lock changes remain scoped implementation work.
- The existing run record receives stage-specific preparation evidence; packets point to it with canonical paths. Brief/typecheck wording retains an agreed N/A rather than calling it green.

Changed product/evidence files were inspected, local links resolve, and `git diff --check` passes. These document checks supplement the real fixture observations.

Independent root review, 2026-10-13: no findings against D5; the root reran the same fresh experiment (**exit 0**) and diff check and confirmed the initialization/baseline, counter and N/A contracts. This does not add runtime evidence; timeout/termination remains a later ticket.

## Limits

No real worker/runtime, credential failure, package-manager install or automatic environment-repair path was executed. None and N/A choices and zero implementation counters are explicitly rehearsed records. Initialization timeout/retry/termination handling remains for the later lifecycle tickets. Tracker/spec/index, globals and upstream companions were not edited.
