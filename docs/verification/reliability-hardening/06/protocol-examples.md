# Ticket 06 protocol examples

These are manual protocol walkthroughs against literal ticket examples, not an executable scheduler, live model test, or assertions about agent obedience. Initial RED records the missing decisions at base `b7efe1c` before editing the adapter. Final GREEN will record the decisions after editing. Host/tool facts are separate in [host-schema.md](host-schema.md) and [cli-help.log](cli-help.log).

## 1. Three child slots: complete worker before reviewer

Input: a stipulated host has three child slots; workers W1/W2/W3 run; W1 reports DONE; a reviewer is waiting.
Literal expected output: confirm W1 inactive and its slot available, then start reviewer R1; do not refill W4 first. Reviewer/escalate/final-review children count against slots. If inactive metadata is retained and availability is not confirmed, do not claim release; preserve/queue and report unavailable if no safe release route exists.
RED: existing loop starts review immediately on DONE and refills workers; adapter has no slot-release/capacity contract.
GREEN: runtimes.md Capacity and release before review requires inactivity plus observed release/available capacity before review; loop.md Pick/Review/Refill now prioritize queued R1. In the stipulated active-slot host, inactive W1 plus observed free capacity yields R1, with W2/W3/R1 occupying the three child slots. In the retained/unknown variant there is no R1/W4 launch until evidence changes; absent a safe release route, stop dispatch with that limitation. No host slot-release experiment was performed.

## 2. Routing policy rejection

Input: spawn is rejected by upper routing policy.
Literal expected output: route unavailable with rejection evidence; zero CLI dispatches. CLI is eligible only for missing capability plus explicit policy/permission allowance; an ambiguous rejection stops too.
RED: Codex adapter explicitly permits CLI fallback when model override is rejected.
GREEN: runtimes.md Fallback gate classifies policy/model/permission rejection separately from capability absence and explicitly stops ambiguous rejection too. The Codex adapter removed rejected-override fallback. Rehearsed output: policy-rejected; route unavailable; CLI dispatch count 0. The prior root route-rejection observation is separately attributed in host-schema.md; this walkthrough issued no spawn or CLI model call.

## 3. Observed model differs

Input: child requests gpt-6-luna/medium; trusted host reports gpt-6.1-sol/high.
Literal expected output: model_status=mismatch; record both values, stop this role, confirm activity, preserve its worktree; no accepted DONE/PASS and no substitution. Planner requests gpt-6.1-sol/high but trusted current session is different: keep the current session and disclose its mismatch.
RED: main skill only stops unavailable models; runtime/record have no mismatch comparison or child stop rule.
GREEN: runtimes.md Requested and observed models records the literal requested/observed values as mismatch; it stops the child, checks stop/release and preserves work without accepting DONE/PASS. SKILL.md preflight/guardrail and run-record.md role/attempt fields carry that status. The planner variant keeps its current model and displays the difference. This uses stipulated trusted metadata; no mismatched model was launched.

## 4. Model cannot be observed

Input: spawn accepts requested gpt-6-luna/medium, returns an identity but no trusted actual model/effort.
Literal expected output: model_status=unknown; actual model=unknown, actual effort=unknown; disclose before Go. Acceptance of requested fields and child self-report do not verify the route. An allowed run may proceed with this limitation; it must retain unknown in the record/brief.
RED: requested role table is presented before Go without a required observation status or unknown disclosure.
GREEN: runtimes.md preflight/model rules plus SKILL.md step 0 require pre-Go unknown disclosure; run-record.md retains requested vs observed and model_status. Rehearsed output: requested gpt-6-luna/medium, observed unknown/unknown, model_status unknown; permitted run only with disclosed limitation. The current host schema separately confirms actual metadata is not exposed here; CLI flags/accepted spawn are not a substitute. No actual-match claim or model dispatch test.
