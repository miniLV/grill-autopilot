# Cost comparison: direct implementation vs grill-autopilot (2026-10-14)

One small, real Claude Code run per arm, capped to keep the whole test under $3. Both arms got the same approved [spec](spec.md) (3 stories: `slugify`, `truncate`, a CLI that wires both) and skipped grill and to-spec. Main model: `opus` for both. Host: Claude Code 2.1.296, `claude -p --permission-mode auto --max-budget-usd <cap> --output-format json`.

| | Baseline: to-tickets → implement-spec, which ran inline (see Caveats) | grill-autopilot (this repo) |
| --- | --- | --- |
| Budget cap | $1.00 | $1.80 |
| **Actual cost** | **$0.47** (Opus $0.466) | **$1.51** (Opus $1.49, Haiku $0.02) |
| Delivered | 3/3 tickets, 10 tests pass | 2/3 tickets, 7 tests pass; result `partial` |
| Cost per delivered ticket | $0.16 | $0.76 |
| Wall time | 1.9 min | 2.7 min |
| Commits | 1 commit per ticket, linear | 1 commit per ticket + one `--no-ff` merge each |
| Independent review | none | one Opus review call covering 01 and 02, both PASS |
| Worker tickets on Haiku | n/a | 2/2 passed first try, 0 escalated |
| Main window context | 50.8K → 62.4K, 352K input sent | 51.0K → 94.1K, 1,382K input sent |
| Subagents | 0 | 3 (2 Haiku workers, 1 Opus reviewer), each started at about 51K context |

Sources: [baseline result](baseline/result.json), [autopilot result](autopilot/result.json) (`total_cost_usd`, `modelUsage`), [autopilot brief](autopilot/brief.md), context reports and git logs in each folder.

## What this shows

- **The cheap worker works for worker-grade tickets.** Haiku finished both graded tickets on the first try for $0.02 in total, and the Opus reviewer passed both. `modelUsage` shows Haiku actually ran, although the run record kept the observed model as unknown.
- **Main-window cost split** (from transcripts, scaled to the reported total): autopilot main window ≈ $1.19 over 18 calls with 15K output tokens; Opus reviewer ≈ $0.30; two Haiku workers ≈ $0.015. The baseline main window did tickets and code in 6 calls with 4K output tokens.
- **Fixed overhead dominates on small tasks.** Of $1.51, about $1.49 was Opus: the planner reading the ~700-line protocol, keeping the run record and doing Git bookkeeping, plus the reviewer (the run estimated $0.39 for the review). The implementation work itself was about 1% of the cost.
- **Cost savings are not shown.** On this task grill-autopilot cost about 3× the baseline in total and about 5× per delivered ticket. Savings would need implementation output that is much larger than the fixed planner and reviewer cost; that is untested.
- **Each agent starts at about 51K tokens of context** in this environment (global instructions, skill list, tool definitions). That is host-specific, but it is paid by every subagent.

## Caveats

- Both sessions could see their budget cap and changed their behaviour. The baseline did all tickets inline in one session: no implementer or merger subagents, no worktrees and no code-review. A faithful implement-spec run would cost more than $0.47. grill-autopilot merged the two ticket reviews into one call, then blocked ticket 03 and skipped the final review when the budget ran low.
- Grading put all three tickets on `worker`, so the escalate path did not run.
- One tiny Python fixture, one run per arm, Claude Code only. Codex was not run.
