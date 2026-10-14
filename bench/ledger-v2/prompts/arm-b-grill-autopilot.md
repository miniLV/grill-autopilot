Non-interactive benchmark run. The user is unavailable: never ask questions and never wait for approval; every approval below is already granted. Cost and time are being measured, so follow the skill fully as written: do not skip, merge or shortcut steps to save tokens.

Work only in this repository ({{BENCH}}/arm-b-grill-autopilot) and its autopilot worktree root. Do not read other directories under {{BENCH}}.

Read and follow {{SKILL_MD}} (this exact path; do not use any other installed copy of grill-autopilot) for the topic "ledger v2" in this repository. Companion skills are in ~/.codex/skills/.

The grill (step 1) is already complete. The user's agreed answers:
- Spec: the approved spec is docs/specs/ledger.md. In step 2, publish it verbatim as the run's spec.md instead of re-running to-spec; Further Notes: none.
- Seams: the public functions in ledger.money, ledger.categories, ledger.query, ledger.csv_io and ledger.store; the CLI through subprocess (`python3 -m ledger`).
- Slicing: one ticket per user story unless grading says to split; independent stories may run in parallel; nothing is off-limits.
- Commands: initialization None; single-ticket Verify `python3 -B -m unittest tests.<module> -v`; full suite `python3 -B -m unittest discover -s tests -v`; typecheck N/A because this standard-library fixture has no type checker.
- Delivery: slug ledger-v2, base branch main, integration branch autopilot/ledger-v2/integration, no push, no PR.
- Roles and limits: config.yaml defaults (Codex: planner, reviewer and escalate gpt-6.1-sol high; worker gpt-6-luna medium; concurrency 3).
The user answered Go. In step 0, show the disclosures in your output but do not wait for confirmation.

Run to the brief, then stop. Finish with a short report: result, integration SHA, each ticket's Implementer and who finished it, attempts and escalations, reviewer verdicts, final review, and the final full-suite result.
