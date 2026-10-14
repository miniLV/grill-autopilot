import datetime
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import control as c


def link(path, label):
    return f'[{label}]({path})'


s = c.read()
root = c.RUN
tip = s['closeout']['delivered_sha']
base = s['base_sha']
c.write(root / 'companion-fingerprint.json', json.dumps(s['companion']['fingerprint'], indent=2) + '\n')
c.write(root / 'companion-contract.md', s['companion']['contract_evidence'] + '\n\nCanonical root: ' + s['companion']['root'] + '\nSource fact: ' + s['companion']['source_commit'] + '\n')
s['companion']['fingerprint_manifest'] = str(root / 'companion-fingerprint.json')
s['companion']['contract_evidence_path'] = str(root / 'companion-contract.md')
s['ownership_manifest'] = str(c.TRACKER / 'ownership.json')
s['runtime']['schema_summary'] = s['runtime']['schema_help_evidence']
s['runtime']['schema_help_evidence'] = [str(root / 'runtime.json')]
s['commands']['confirmed_choices'] = dict(s['commands'])
s['commands']['initialization'] = {'command': 'None', 'result': 'skipped explicitly; every worktree baseline gate passed', 'evidence': str(c.RECORD)}
s['commands']['ticket_verify'] = [
    {'ticket': n, 'command': v['command'], 'cwd': v['cwd'], 'exit': v['exit'], 'log': v['log']}
    for n, t in s['tickets'].items() for a in t['attempts'] for v in a['integration_checks']
    if isinstance(v.get('command'), list)
]
s['commands']['ticket_baseline'] = [
    {'cwd': p['worktree'], 'starting_sha': p['starting_sha'], 'commands': p['baselines'], 'result': p['status']}
    for p in s['preparations']
]
checks = [x for x in s['closeout']['checks'] if x['qualification'] == 'current']
s['commands']['full_suite'] = {**next(x for x in checks if x['kind'] == 'suite'), 'result': 'pass, 66 tests'}
s['commands']['typecheck'].update(cwd=s['integration']['worktree'], result='N/A: standard-library fixture has no type checker configured')
c.save(s)
c.hashes()
finalstate = c.state(s['integration']['worktree'])
assert finalstate['head'] == tip and not finalstate['status'] and not finalstate['untracked_ignored'] and not finalstate['pending_merge']
stattext = c.git(s['integration']['worktree'], 'diff', base + '...' + tip, '--stat')
c.write(root / 'delivery-stat.txt', stattext + '\n')
c.write(root / 'delivery-state.json', json.dumps(finalstate, indent=2) + '\n')
rows = []
finishers = []
for n, t in s['tickets'].items():
    fin = [a for a in t['attempts'] if a['role'] in ('worker', 'escalate') and a['verdict'].startswith('DONE ')][-1]
    role = fin['role']
    req = fin['requested']
    verdict = 'FAIL -> PASS' if n == '01' else 'PASS'
    count = t['counters']['worker'] + t['counters']['escalate']
    rows.append(f"| {n} {t['title']} | {t['implementer']} | {role}: {req['model']} {req['effort']} (requested; observed unknown) | {count} | {verdict} |")
    finishers.append({'ticket': n, 'title': t['title'], 'implementer': t['implementer'], 'finisher_role': role, 'finisher_agent': fin['agent_id'], 'requested': req, 'observed': fin['observed'], 'model_status': fin['model_status'], 'counters': t['counters'], 'finished_commit': fin['verdict'].split()[1]})
c.write(root / 'finishers.json', json.dumps(finishers, indent=2) + '\n')
totals = {k: sum(t['counters'][k] for t in s['tickets'].values()) for k in ('worker', 'escalate', 'reviewer', 'infrastructure')}
brief = f'''# Ledger v2 brief

Result: **success**. All nine tickets are done; blocked or undelivered scope: **none**. Stop reason: None.

Integration branch: `{s['integration']['ref']}`  
Delivered SHA: `{tip}`  
Saved review/base SHA: `{base}`  
Retained worktree: {link(s['integration']['worktree'], 'integration worktree')}

## Done

| Ticket | Implementer and grading | Finisher | Implementation attempts | Reviewer verdicts |
| --- | --- | --- | ---: | --- |
{chr(10).join(rows)}

Worker calibration: **2 worker tickets finished on worker; 0 needed escalate**. Money used its second worker attempt to allow leading-zero thousands groups. Seven tickets went directly to escalate according to grading. Every successful candidate passed its reviewer and serialized integration Verify before done. All nine verified ticket branches/worktrees were safely removed; integration remains.

## Standards

**PASS**, base `{base}`, reviewed `{tip}`. Hard documented-standard violations: 0; material baseline-smell judgement calls: 0. No assertions weakened or removed. {link(root / 'logs/final-standards-1-result.txt', 'Full evidence')}.

## Spec

**PASS**, same base and delivered SHA. No missing, partial, wrong or unasked requirements remain in S1-S9. Initial final review found a Python 3.9 CSV carriage-return quoting issue; one escalate correction fixed it and added literal regressions. Both axes were reviewed again at the new SHA. {link(root / 'logs/final-spec-1-result.txt', 'Full evidence')}.

Final review summary: **Standards 0 findings, worst none; Spec 0 findings, worst none**. Earlier review/check entries are retained as historical and do not qualify this delivered SHA.

## Final checks

- **PASS**: `python3 -B -m unittest discover -s tests -v`, **66 tests**, exit 0, Python 3.13.3, exact delivered SHA and unchanged clean content. {link(root / 'logs/final-suite-1.json', 'Complete stdout/stderr and state')}.
- **PASS**: full suite with explicit Xcode Python 3.9.6, **66 tests**, exit 0, same SHA and clean state. {link(root / 'logs/final-suite-py39-1.json', 'Complete compatibility evidence')}. This additional check covers the final review's reproduced failure.
- **Typecheck N/A**: standard-library fixture has no type checker configured, agreed in grill. No pass invented.
- Final unchanged-tip gate: HEAD/ref/content equal both axes and current checks; no pending Git operation or active writer. {link(root / 'delivery-state.json', 'Delivery state')}.

## Budgets, attempts and errors

- Ticket implementation starts: worker **{totals['worker']}**, escalate **{totals['escalate']}**. Money spent 2/2 worker starts and succeeded; every other ticket spent 1. No worker-to-escalate transition.
- Ticket reviewer calls: **{totals['reviewer']}**. Final-axis reviewer calls: **4** (initial Standards PASS/Spec FAIL; corrected Standards PASS/Spec PASS).
- Run-level final-fix calls: **1/2**, requested gpt-6.1-sol high, finished by `/root/final_correction_1` at delivered SHA. Observed exact model/effort unknown.
- Worker/escalate/reviewer infrastructure retries: **0 per attempt, 0 aggregate**. Brief generation used **1/1** infrastructure/artifact retry after a Python SyntaxError before any writes; corrected writer succeeded. Run-level infrastructure extra invocations: **1 aggregate**. No business attempt renewed by this retry.
- Default budgets: worker initial +1 retry; direct-escalate initial +1 retry; escalate after worker exhaustion 1; infrastructure 1 extra per logical attempt; final corrections 2 total; timeout 1800 seconds including preparation. No failed exhausted budget, timeout, route rejection, unresolved environment error or unsafe rollback.
- Optional ps inventory was sandbox-denied; managed host lifecycle and clean owned worktrees supplied writer-isolation evidence. Ancillary read-only Markdown/JSON parsing errors were corrected within review attempts and changed no source or retry budget.
- Remaining findings, blocked requirements and resources not stopped: **none**. Child executions inactive and capacity returned. Native metadata deletion unsupported; identities retained in history.

## Assumptions

Approved source spec published **verbatim**; original Further Notes: **none**. Post-Go clarifications recorded in frozen tasks/run record: ASCII amount grammar with optional minus and correct comma grouping, no plus/outer whitespace; CSV four fields/canonical ISO dates, physical record-start line numbers and aggregated errors; Decimal(str(value)) HALF_UP for legacy fractional cents. New Verify modules used existing full suite baselines. Approved spec bytes were not rewritten.

## Roles and runtime

| Role | Requested | Observed model / effort | Status |
| --- | --- | --- | --- |
| Planner | gpt-6.1-sol / high | unknown / unknown; current session retained | unknown |
| Worker | gpt-6-luna / medium | unknown / unknown | unknown |
| Reviewer | gpt-6.1-sol / high | unknown / unknown | unknown |
| Escalate | gpt-6.1-sol / high | unknown / unknown | unknown |

Finishing observations are listed above and in {link(root / 'finishers.json', 'finishers')}. Accepted requests do not prove actual model matches; limitations disclosed before execution.

Native Codex start/result/status/bounded wait/cancel supported. Host advertises **4 active-execution slots including planner**, so at most **3 children** counting all roles and both final seats. Latest inventory confirms no active child. Identity destruction unsupported; recorded metadata retained. Exact host version unexposed. Planner shell resolves Python 3.13.3; children resolve Xcode 3.9.6, which prompted and now passes compatibility checks. Session-driven execution cannot guarantee continuation or immediate brief after a crash; no crash occurred.

## Record and preservation

{link(c.RECORD, 'Canonical run record')}  
{link(c.TRACKER / 'ownership.json', 'Exact ownership manifest')}  
{link(root / 'snapshots/spec.md', 'Frozen spec')} and {link(root / 'snapshots/tickets', 'frozen tasks')}  
{link(root / 'companion-fingerprint.json', 'Companion fingerprint')} and {link(root / 'companion-contract.md', 'contract evidence')}  
{link(root / 'closeout-comparison.json', 'Original-checkout comparison')}

Original checkout remains on main at saved base. Staged/unstaged tracked diffs and all non-run untracked entries match baseline, excluding **only exact manifest-owned tracker paths**; no drift. Frozen source/task and companion content hashes unchanged. Product commits stayed on assigned branches. No push or PR, as selected.

```text
{stattext}
```

Terminal brief delivered; stop here.
'''
c.write(c.TRACKER / 'brief.md', brief)
s = c.read()
s['owned_tracker_files'] = json.loads((c.TRACKER / 'ownership.json').read_text())
s['phase'] = 'terminal'
s['result'] = 'success'
s['closeout']['finishers'] = finishers
s['closeout']['total_ticket_counters'] = totals
s['closeout']['brief_saved_at'] = c.now()
s['closeout']['brief_generation']['result'] = 'completed: corrected writer saved brief, no product changes'
c.save(s)
c.event('brief saved', 'terminal success; local only; stop', evidence=str(c.TRACKER / 'brief.md'), sha=tip)
c.hashes()
assert c.state(s['integration']['worktree']) == finalstate
print(brief)
