Non-interactive benchmark run. The user is unavailable: never ask questions and never wait for approval; every approval below is already granted. Cost and time are being measured, so follow each skill fully as written: do not skip, merge or shortcut steps to save tokens.

Work only in this repository ({{BENCH}}/arm-a-implement-spec) and its worktree root. Do not read other directories under {{BENCH}}. Issue tracker: local markdown, see docs/agents/issue-tracker.md. Feature slug: ledger-v2.

Runtime notes for Codex:
- Where a skill says "call the Skill tool with <name>", read ~/.codex/skills/<name>/SKILL.md and follow it.
- Where a skill says "subagent", use your native subagent tool. Keep every subagent on this session's model and reasoning effort.
- Create each implementer worktree yourself with `git worktree add` under {{BENCH}}/arm-a-implement-spec.worktrees/.

Steps:
1. Read and follow ~/.codex/skills/to-tickets/SKILL.md on the approved spec docs/specs/ledger.md. The user pre-approved your breakdown: skip the quiz and publish the tickets.
2. Read and follow ~/.codex/skills/implement-spec/SKILL.md for that spec and its tickets, including the final code-review and its fixes. Integration branch: ledger-v2/integration, created from main. Do not push or open a PR.

Finish with a short report: integration branch and final SHA, tickets done/blocked, commits per ticket, subagents used (role and count), code-review findings and fixes, and the final full-suite result.
