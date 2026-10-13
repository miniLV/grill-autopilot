# Ticket 02: stable inputs and run record verification

Scope: approved D3. The seam is the run's inputs to observable Git/worktree, tracker and evidence state. This ticket supplies a Markdown contract and a real Git visibility experiment, not a production scheduler or an end-to-end model run.

## Reproduce

From the repository root:

```sh
python3 docs/verification/reliability-hardening/02/experiment.py > /tmp/grill-autopilot-02.log
git diff --check
```

The experiment returned **0** on 2026-10-13 with Python 3 and Git `2.50.1 (Apple Git-155)`. [experiment.log](experiment.log) records actual commands, working directories, exit codes, canonical input paths, literal contents, hashes and before/after original-checkout state. Temporary paths/SHAs differ each run; no network or real user files are involved.

## Observed behavior

- **Red:** before changing product docs, two newly created worktrees each failed to read the checkout-relative uncommitted spec and ticket (`cat` returned **1**, four failures total). The original checkout's tracker was never committed to base.
- **Green:** after the doc change, the full fresh experiment was rerun. Two independent reader subprocesses, with different worktree working directories, read the same canonical absolute snapshots; both returned **0**. The content and SHA-256 arrays were equal and matched the independently written literal spec/task.
- **Frozen inputs:** snapshot write permission bits were removed. Updating the source ticket's Status/Comments and adding a scope-expansion event/assumption to the run record preserved both snapshot hashes. This is an explicitly scripted planner rehearsal, not proof of model compliance. The literal snapshot excludes Status/Comments; it is not a test of a production parser.
- **Original checkout:** ref, base SHA, unstaged/staged diff and the SHA-256 hash of unrelated binary untracked data were equal before/after. Only the exact declared tracker files were excluded. Both reader worktrees remained clean.

## Field and contract review

[sample-run.md](sample-run.md) is an illustrative, inputs-ready record, with synthetic absolute paths/hash values and explicit unknown/not-recorded facts. It is for independent field review against spec D3, not observed runtime evidence. The [product record template](../../../../skills/grill-autopilot/run-record.md) is the sole authority for ownership and field meanings.

The independent reviewer should check these groups directly against D3 rather than trusting a template comparison:

| D3 group | Sample location |
| --- | --- |
| Run ID, phase/result, original checkout, base SHA, integration ref/worktree | Header fields and `integration` |
| Companion source fingerprint and canonical paths | `companion` |
| Requested/observed role model and effort, initialization/verification commands, push choice | `roles`, `commands`, `push_selected` |
| Ticket branch/worktree, agent/process and attempt identity, counters/times | `tickets.01` and its planned attempt |
| Candidate/reviewed/merge before-after SHAs, verdict and evidence locations | Attempt fields explicitly not-recorded with reasons |
| Input snapshots, exact owned tracker files, baseline and closeout comparison | `inputs`, `owned_tracker_files`, `baseline`, `closeout_comparison` |
| Save intent before operation and retain mutable events/assumptions | Planned dispatch event and `assumptions` |

Independent review: **PASS**, 2026-10-13, by the root agent (separate from this ticket's executor). It reviewed sample-run.md directly against spec D3 and the full field groups above: identity/path/config/command, ticket attempt/counter/time/SHA/verdict/evidence, ownership/baseline/input and save-before-operation. It confirmed that synthetic facts are labeled, unperformed work has not-recorded reasons and unobserved role facts are unknown. This is a field/contract review; future runtime behavior remains unverified.

Product scenarios were inspected manually: both packets use canonical frozen inputs, companion/Context and log pointers; only the planner writes mutable records; scope expansion blocks without altering a distributed task; brief preparation compares original-checkout evidence. Local pointers and diff whitespace are supplementary document checks, not behavioral tests.

## Limits

The experiment proves real Git visibility and file preservation for these fixtures. It does not prove that runtime agents obey read-only inputs, that every host exposes role/process metadata, or that recovery, initialization, retry/merge gates and final results execute correctly. This ticket defines fields for those later protocols without implementing them. Read-only mode is advisory; the contract also requires hash checks and preservation on drift.
