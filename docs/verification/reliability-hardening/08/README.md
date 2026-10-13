# Ticket 08 verification

Approved seam: a skill run's input → Git/worktree facts, ticket state and brief. The product is a Markdown execution protocol. [experiment.py](experiment.py) captures real Git/check facts in four fresh temporary repositories; [experiment.log](experiment.log) retains the actual commands, SHAs, exits, check output, UTC times and unchanged state observations. State/brief decisions and all host cases below are **manual protocol rehearsals**, not an executable resume engine, prose-string tests or proof that a model obeyed the protocol.

## RED before protocol edits

The assigned branch was clean at integration `1c310c40c58f392f6afb2dfb3f92c4d5447a0279`; blocker 07 was done. Reading the baseline before edits exposed these gaps: no explicit resume argument/entry, no qualification/interruption/reconciliation order, no active-vs-included-vs-missing-evidence decision, and no exact checked integration SHA/log field. Generic recovery mentions in the record/runtime/failure documents could not resolve the ticket's literal examples. This was a manual protocol RED, not a failing executable product test. The real Git fixtures independently validate the facts those decisions consume.

## GREEN decisions rehearsed

The manual reviewer followed [resume.md](../../../../skills/grill-autopilot/resume.md) in order for every row below, with [run-record.md](../../../../skills/grill-autopilot/run-record.md), [runtimes.md](../../../../skills/grill-autopilot/runtimes.md), [companions.md](../../../../skills/grill-autopilot/companions.md) and [failures.md](../../../../skills/grill-autopilot/failures.md) supplying their existing authorities.

| Input / literal facts | Observable decision from the revised protocol | Evidence level |
| --- | --- | --- |
| `resume fixture-08-matching-evidence`; in-review; candidate included; candidate/review identity equal; matching successful check/log at current integration SHA; owned inactive resources stipulated | Supplement done from evidence; no worker/reviewer/merge replay. Preserved ref/worktree/content snapshots prove the fixture was not merged/reset/cleaned again. | Real Git/check facts; done decision manual. |
| in-review; attributable merge includes candidate; no checks recorded | Keep pending until bounded Verify/applicable typecheck succeeds at unchanged current integration SHA; only then supplement done. No merge replay. | Real missing-record/check/reverification facts; decision manual. |
| in-review; checks passed at merge-after SHA; attributed later integration commit moves current HEAD | Old check remains historical; rerun checks on current SHA. Log binds exact SHA, command, cwd, exit, UTC times and clean unchanged HEAD/content. | Real older/current SHA distinction and fresh check; decision manual. |
| recorded candidate/review unchanged but ticket branch advances without attributable intent; dirty tracked and untracked files exist | Failed recovery brief; retain dirt, refs, registrations and old record; no replay, reset, clean or verification used to conceal identity mismatch. | Real branch ancestry exit 1 and preserved state/hash assertions; failed brief decision manual. |
| claimed; saved run/attempt `r/01-W1`, host identity `host-A`, same owned worktree; trusted host says active at 60 of 1800 saved seconds | Query/observe `host-A`, retain W=1 and saved deadline/slot; no worker spawn or continuation message. At deadline use existing timeout/stop rules; resume grants no new clock. | **Manual host protocol rehearsal; no actual host query/dispatch.** |
| claimed but full attributable DONE available and host inactive; candidate not included | Consume original result, release/reconcile capacity, proceed to normal review; no second implementation merely to repair claimed. | Manual host/result rehearsal. |
| recorded PID may be reused, host unreachable or liveness unknown | Stop new execution and all cleanup, block unfinished statuses through failures.md, retain possibly writable work and show failed with unconfirmed resources. | Manual host/brief rehearsal. |
| candidate included but review SHA differs/missing, or recorded integration movement cannot be explained | Failed; reverify cannot repair candidate/review/merge ownership. | Manual contradictory-record rehearsal. |
| `resume` with duplicate/missing record, path separator ID, or unqualified tracker ownership | Read-only qualification fails; preserve existing record; direct failed known-facts brief when no owned destination can be qualified. No record creation or unsafe overwrite. | Manual entry/ownership rehearsal. |
| valid original run identity but saved snapshots/source task body or companion content/target/source differs | Preserve original hashes/selection and frozen task; stop resume and report exact drift with failed brief. Evidence-only interruption appends are allowed only after record ownership qualification. | Manual fingerprint/input rehearsal. |
| ordinary topic uses an existing slug | Normal entry runs new-run conflict preflight; it never falls through to resume. | Manual entry rehearsal plus existing ticket 01 Git preflight evidence. |
| root crashed before brief; terminal saved run resumed later | No immediate/background recovery guarantee. After qualification, append observed interruption with unknown cause/time if necessary. A consistent terminal run shows existing brief without replaying delivery/cleanup. | Manual boundary rehearsal; no crash injected. |
| reverify red/unavailable/timeout or integration becomes dirty/moves during checks | Preserve evidence/state, follow bounded failure exit and failed brief; no done, duplicate merge or recovery reset. | Manual check-failure rehearsal. |

Acceptance: explicit same-run entry and qualification precede execution; all four ticket examples have decisions; current-SHA/log evidence or bounded re-verification governs included candidates; ambiguous identity/state stops safely; crash guarantee is explicitly limited. The run-data schema remains authoritative in run-record.md, runtime facts in runtimes.md, fingerprints in companions.md and budgets/results in failures.md. No second field/lifecycle/failure authority was added.

## Reproduce

From the ticket worktree/repository root:

```sh
python3 docs/verification/reliability-hardening/08/experiment.py > docs/verification/reliability-hardening/08/experiment.log
git diff --check
```

Observed exits: **0**, **0**. The experiment uses stdlib and subprocess timeouts of 30 seconds; no network, dependencies or host role launch. It embeds each temporary check log/record into its retained stdout before temporary directories are removed. The recorded candidate-content checks are real; review PASS, identity/fingerprint qualification and no-writer premises are explicitly stipulated for the rehearsal. The JSON record is a minimal scenario projection, not a full valid production run record. No mutable status or brief was automatically written; the table supplies the corresponding manual protocol output.

Supplemental local Markdown target/fragment validation passed: **41** links across the six changed skill documents and this evidence document, exit **0**. New files and patch were inspected. The same Git fixture and diff/link checks are rerun after committing and merging the integration tip into the ticket branch. There is no executable product suite/typecheck in this Markdown repository; no full-suite or end-to-end pass is claimed.

## Limits and scope

No real runtime cancellation, active-attempt query, recovered role or crash/restart was executed. Those remain ticket 13 evidence. Integration rollback and new SHA-bound review packet mechanics remain ticket 09; final-review repair rounds remain ticket 10. This ticket added the resume reference and pointers, one checked-SHA record field, and a minimal README invocation. Tracker/spec/index, global/plexus/upstream files, role defaults and other tickets were untouched. No push/PR.
