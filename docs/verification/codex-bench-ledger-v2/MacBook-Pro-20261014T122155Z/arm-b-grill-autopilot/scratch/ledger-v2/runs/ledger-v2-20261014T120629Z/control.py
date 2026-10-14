import datetime
import hashlib
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys

RUN = Path(__file__).resolve().parent
RECORD = RUN / 'run.md'
S = json.loads(RECORD.read_text().split('```json\n')[1].split('\n```')[0])
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def persist():
    S['updated_at'] = now()
    RECORD.write_text('# Autopilot run record\n\n```json\n' + json.dumps(S, indent=2) + '\n```\n')

def declare(name):
    p = RUN / name
    if str(p) not in S['owned_tracker_files']:
        assert not p.exists(), p
        S['owned_tracker_files'].append(str(p))
        persist()
    p.parent.mkdir(parents=True, exist_ok=True)
    return p

def evidence(name, value):
    p = declare(name)
    p.write_text(value if isinstance(value, str) else json.dumps(value, indent=2))
    return str(p)

def event(operation, outcome='intended', ticket='run', attempt='not-applicable', pointer=None):
    S['events'].append(dict(at=now(), ticket=ticket, attempt_id=attempt, operation=operation, outcome=outcome, evidence=pointer))
    persist()

def command(argv, cwd, name):
    log = declare('logs/' + name + '.json')
    event('command ' + shlex.join(argv), pointer=str(log))
    started = now()
    r = subprocess.run(argv, cwd=cwd, env=ENV, capture_output=True, timeout=90)
    data = dict(command=shlex.join(argv), cwd=str(cwd), started_at=started, ended_at=now(), exit=r.returncode, stdout=r.stdout.decode(errors='replace'), stderr=r.stderr.decode(errors='replace'))
    log.write_text(json.dumps(data, indent=2))
    event('command ' + shlex.join(argv), str(r.returncode), pointer=str(log))
    return r, str(log)

def git(cwd, *args):
    return subprocess.check_output(['git', *args], cwd=cwd, env=ENV).decode().strip()

def state(cwd):
    data = dict(head=git(cwd, 'rev-parse', 'HEAD'), ref=git(cwd, 'symbolic-ref', 'HEAD'), status=git(cwd, 'status', '--porcelain=v1', '--untracked-files=all'), tracked_diff=git(cwd, 'diff', '--binary'), staged_diff=git(cwd, 'diff', '--cached', '--binary'), ignored=git(cwd, 'ls-files', '--others', '--ignored', '--exclude-standard'), untracked=git(cwd, 'ls-files', '--others', '--exclude-standard'), inventory=[])
    for rel in filter(None, (data['ignored']+'\n'+data['untracked']).splitlines()):
        p = Path(cwd) / rel
        data['inventory'].append(dict(path=str(p), type='symlink' if p.is_symlink() else 'file', hash_or_target=os.readlink(p) if p.is_symlink() else hashlib.sha256(p.read_bytes()).hexdigest()))
    data['branch_tip'] = git(cwd, 'rev-parse', data['ref'])
    data['pending_git'] = {x: Path(git(cwd, 'rev-parse', '--git-path', x)).exists() for x in ['MERGE_HEAD', 'CHERRY_PICK_HEAD', 'REVERT_HEAD']}
    return data

def clean(cwd):
    st = state(cwd)
    assert not st['status'] and not st['ignored'] and not any(st['pending_git'].values()), st
    assert st['head'] == st['branch_tip'], st
    return st

def hashes():
    for x in [S['inputs']['spec']] + list(S['inputs']['tickets'].values()):
        assert hashlib.sha256(Path(x['snapshot']).read_bytes()).hexdigest() == x['sha256'], x
    assert Path(S['inputs']['spec']['source']).read_bytes() == Path(S['inputs']['spec']['snapshot']).read_bytes()
    for x in S['inputs']['tickets'].values():
        text = Path(x['source']).read_text().split('\n## Comments')[0]
        import re
        body = re.sub(r'^Status:.*\n', '', text, flags=re.M) + '\n'
        assert hashlib.sha256(body.encode()).hexdigest() == x['sha256'], x

def status(nn, value, comment):
    import re
    p = Path(S['inputs']['tickets'][nn]['source'])
    body = re.sub(r'^Status:.*$', 'Status: ' + value, p.read_text(), flags=re.M)
    p.write_text(body + '\n- ' + now() + ': ' + comment + '\n')
    S['tickets'][nn]['status'] = value
    persist()

def attempt(nn, role):
    container = S['closeout'] if nn == 'run' else S['tickets'][nn]
    number = sum(a['role'] == role for a in container['attempts']) + 1
    aid = nn + '-' + role + '-' + str(number)
    started = now()
    a = dict(attempt_id=aid, role=role, status='planned', implementation_started=False, infrastructure_retries=0, remaining_budget=S['budgets'], next_state='preparation' if role in ['worker','escalate','integration-preparation'] else 'in-review', agent_id='not-recorded: not-started', process_id='not-applicable: native', requested=S['roles']['escalate' if role=='final-fix' else 'reviewer' if role.startswith('final-review') else role]['requested'] if role in S['roles'] or role.startswith('final-review') or role=='final-fix' else {'model':'not-applicable','effort':'not-applicable'}, observed={'model':'unknown','effort':'unknown'}, model_status='unknown', lifecycle=dict(launch='not-recorded',result='not-recorded',activity='not-started',stop='not-requested',capacity_release='not-applicable',identity_metadata='not-created',evidence=[]), deadline=(datetime.datetime.fromisoformat(started)+datetime.timedelta(seconds=1800)).isoformat(), logical_started_at=started, planned_at=started, started_at='not-recorded: not-started', ended_at='not-recorded: pending', invocations=[], candidate_sha='not-recorded: pending', done_check='not-recorded: pending', review_base_sha='not-recorded: pending', reviewed_sha='not-recorded: pending', review_evidence='not-recorded: pending', merge_before_sha='not-recorded: pending', merge_after_sha='not-recorded: pending', integration_transaction='not-applicable: pending', integration_checks=[], verdict='not-recorded: pending', evidence=[])
    a['output_destination'] = str(declare('logs/' + aid + '-result.txt'))
    container['attempts'].append(a)
    persist()
    return a

def prepare(nn):
    hashes()
    isrun = nn == 'run'
    t = S['integration'] if isrun else S['tickets'][nn]
    cwd = t['worktree']; branch = t['ref'] if isrun else t['branch']
    start = S['base_sha'] if isrun else git(S['integration']['worktree'], 'rev-parse', 'HEAD')
    a = attempt(nn, 'integration-preparation' if isrun else t['implementer'].split()[0])
    assert not Path(cwd).exists() and not Path(cwd).is_symlink()
    refs = git(S['original_checkout'],'for-each-ref','--format=%(refname)','refs/heads/').splitlines()
    assert all(x != 'refs/heads/'+branch and not x.startswith('refs/heads/'+branch+'/') and not ('refs/heads/'+branch).startswith(x+'/') for x in refs)
    r, log = command(['git','worktree','add',cwd,'-b',branch,start],S['original_checkout'],a['attempt_id']+'-create')
    assert r.returncode == 0, r.stderr
    assert clean(cwd)['head'] == start
    t['starting_integration_sha'] = start
    if isrun: t['sha'] = start
    baseline = 'python3 -B -m unittest discover -s tests -v' if isrun else t['baseline']
    prep = dict(worktree=cwd, attempt_id=a['attempt_id'], started_at=a['logical_started_at'], deadline=a['deadline'], starting_sha=start, initialization='skipped: explicit None', generated_paths=[], baselines=[], status='preparing')
    S['preparations'].append(prep); persist()
    before=clean(cwd); r, log=command(shlex.split(baseline),cwd,a['attempt_id']+'-baseline'); after=clean(cwd)
    assert before==after
    prep['baselines']=[dict(command=baseline,result=r.returncode,evidence=log),dict(command='N/A',reason='standard-library fixture with no type checker configured')]; prep['status']='ready' if r.returncode==0 else 'environment-error'; persist()
    assert r.returncode==0, r.stderr
    if isrun:
        a['status']='completed'; a['ended_at']=now(); a['verdict']='preparation PASS'; a['evidence'].append(log); S['commands']['full_suite']['result']=dict(exit=0,evidence=log); persist(); print('Integration environment ready',start)
    else:
        status(nn,'claimed','Prepared at '+start+'; initialization None, baseline PASS '+log)
        plan_packet(nn,a,start)

def plan_packet(nn,a,start):
    hashes(); t=S['tickets'][nn]; inp=S['inputs']['tickets'][nn]; comp=S['companion']['skills']; work=t['worktree']
    packet=f'''You are a worker. Implement exactly one ticket.
Task: {inp['snapshot']}    Spec: {S['inputs']['spec']['snapshot']}
TDD skill: {comp['tdd']}
Context: {work}/{next(p for p in t['files'] if p.startswith('tests/'))}; existing prior art under {work}/tests; run record read only {RECORD}
Worktree: {work}    Branch: {t['branch']}
Starting SHA: {start}
Attempt: new    Previous attempt evidence: None

1. Work only in the Worktree, on the Branch. HEAD must equal the Starting SHA. On retry, keep the edits already there; do not reset. If the state is different, stop and reply STUCK.
2. Read the Task and Spec. Do not edit the tracker. If a needed change is outside Files, stop and reply STUCK.
3. Follow the TDD skill at the agreed seam; do not ask to confirm it. For each Example, write a test that asserts its literal expected output, see it fail, then make it pass.
4. Edit only the paths under Files. Run every Verify command until all pass. Do not add or change dependencies unless Files lists the dependency file. If a command fails because a tool, dependency or credential is missing, stop and reply ENVIRONMENT_ERROR.
5. Commit all your changes on the Branch. Do not merge, rebase, reset or switch branches.
6. Reply with one line only:
   DONE <commit sha> <changed paths, comma-separated>
   or ENVIRONMENT_ERROR <command and exit code/missing prerequisite reason>
   or STUCK <one-sentence reason>

The user is unavailable; no questions/approval waits. Set PYTHONDONTWRITEBYTECODE=1 for all Python commands and subprocesses, keep generated artifacts outside Worktree in temporary directories. Read tdd tests.md/mocking.md. Do not spawn children. Before the final one-line reply, send root a concise EVIDENCE message recording each red/green cycle command, exit and literal observed failure/success, plus final Verify output. Root captures it in {a['output_destination']} and related logs; you must not write logs in original checkout. Read/write only this worktree and read supplied tracker/companion paths; never inspect other benchmark directories. Your role route is {a['requested']}.
'''
    a['starting_sha']=start; a['packet']=evidence('packets/'+a['attempt_id']+'.txt',packet); persist(); print(packet)

def finished(nn, result, host):
    t=S['tickets'][nn]; a=t['attempts'][-1]
    p=Path(a['output_destination']); p.write_text(result)
    a.update(status='completed', ended_at=now(), verdict=result, evidence=[str(p)])
    a['lifecycle'].update(result='completed', activity='inactive', capacity_release='confirmed: list_agents terminal execution, active-execution slots', identity_metadata='retained', evidence=[evidence('evidence/'+a['attempt_id']+'-host.json',host)])
    a['invocations'][-1].update(ended_at=now(), classification='completed')
    persist()

def launched(nn, identity):
    container=S['closeout'] if nn=='run' else S['tickets'][nn]
    a=container['attempts'][-1]; role=a['role']; before=dict(container['counters'])
    counter='reviewer' if role.startswith('final-review') else 'final_fix' if role=='final-fix' else role
    container['counters'][counter]+=1
    a.update(agent_id=identity,status='active',started_at=now(),implementation_started=role in ['worker','escalate','final-fix'])
    a['lifecycle'].update(launch='completed: native spawn accepted',activity='active',identity_metadata='retained',capacity_release='not-yet')
    a['invocations'].append(dict(number=1,planned_at=a['planned_at'],started_at=a['started_at'],ended_at='pending',identity=identity,classification='completed: launch',counts_before=before,counts_after=dict(container['counters']),remaining_seconds=1800-(datetime.datetime.now(datetime.timezone.utc)-datetime.datetime.fromisoformat(a['logical_started_at'])).total_seconds(),evidence=[a['packet']]))
    event('native spawn '+identity,'accepted',nn,a['attempt_id']); persist()

def review(nn, done_sha):
    hashes(); t=S['tickets'][nn]; work=t['worktree']; impl=t['attempts'][-1]
    assert impl['lifecycle']['activity']=='inactive'
    st=clean(work); assert st['head']==done_sha and st['ref']=='refs/heads/'+t['branch']
    assert int(git(work,'rev-list','--count',impl['starting_sha']+'..'+done_sha))>=1
    donebase=t.get('last_review_base',t['starting_integration_sha'])
    changed=git(work,'diff','--name-only',donebase+'...'+done_sha).splitlines()
    assert all(p in t['files'] for p in changed), changed
    impl['candidate_sha']=done_sha; impl['done_check']=dict(result='PASS',paths=changed,state_evidence=evidence('evidence/'+impl['attempt_id']+'-done.json',st)); persist()
    tip=clean(S['integration']['worktree'])['head']
    event('planner tip merge '+tip,ticket=nn,attempt=impl['attempt_id'],pointer=evidence('evidence/'+impl['attempt_id']+'-pre-tip.json',dict(integration_tip=tip,done_sha=done_sha,state=st)))
    r,log=command(['git','merge','--no-edit',tip],work,impl['attempt_id']+'-tip-merge'); assert r.returncode==0,r.stderr
    candidate=clean(work)['head']; assert git(work,'merge-base',tip,candidate)==tip
    t['candidate_sha']=candidate; t['last_review_base']=tip; impl['tip_merge_evidence']=log; persist()
    status(nn,'in-review','DONE check PASS, planner tip merge candidate '+candidate+' base '+tip)
    a=attempt(nn,'reviewer'); a.update(candidate_sha=candidate,reviewed_sha=candidate,review_base_sha=tip)
    log=a['output_destination']; a['review_evidence']=log
    inp=S['inputs']['tickets'][nn]; spec=S['inputs']['spec']; companion=S['companion']['skills']
    packet=f'''You are a reviewer. Gate one ticket. Read; do not edit anything.
Task snapshot: {inp['snapshot']}    Spec snapshot: {spec['snapshot']}
Input SHA-256: task={inp['sha256']} spec={spec['sha256']}
Mutable tracker ticket (read only): {inp['source']}
Run record (read only): {RECORD}
Companions: {companion['tdd']}; {companion['code-review']}
External/run Context: {impl['done_check']['state_evidence']}; {impl['tip_merge_evidence']}
Log capture: {log} (planner writes)
Worktree: {work}
Branch: {t['branch']}
Review base SHA: {tip}
Candidate SHA: {candidate}
Review evidence: {log}
Diff: git -C "{work}" diff {tip}...{candidate}

Verify snapshot hashes; use frozen requirements. Resolve repository Files/Context under Worktree. Report to root; tracker and record read only. Resolve SHAs as commits, base ancestor candidate. Require HEAD and branch tip candidate, clean content and no active/unknown writer before/after checks. Save base/candidate, commands/cwd/exits, check output, N/A reason and before/after state in EVIDENCE message to root; planner captures it in declared log. Use PYTHONDONTWRITEBYTECODE=1 for all commands/subprocesses, no artifacts in worktree. No descendants or questions. Do not write log yourself.
Check each item:
1. Every Acceptance item is met.
2. Every changed path listed under Files.
3. Tests assert literal Examples; no assertions weakened, skipped or deleted. Representation literal float->cent adjustment in07 explicitly approved; preserve original behavioral assertion.
4. Every applicable Verify passes when you run it in worktree; N/A reason no type checker configured.
5. Nothing outside scope changed.

Before final, send root EVIDENCE containing hash output, full Verify output/exits, before/after status and SHA and any findings. Then one-line only:
PASS {candidate} {log}
or FAIL: numbered reasons under120 words.
'''
    a['packet']=evidence('packets/'+a['attempt_id']+'.txt',packet); persist(); print(packet)

def integrate(nn):
    hashes(); t=S['tickets'][nn]; a=t['attempts'][-1]; work=S['integration']['worktree']; candidate=t['candidate_sha']
    assert a['role']=='reviewer' and a['verdict'].startswith('PASS '+candidate+' '+a['review_evidence'])
    assert a['lifecycle']['activity']=='inactive'; assert Path(a['review_evidence']).is_file()
    assert clean(t['worktree'])['head']==candidate
    baseline=clean(work); before=baseline['head']; assert git(work,'merge-base',a['review_base_sha'],candidate)==a['review_base_sha']
    transaction=dict(id=nn+'-'+a['attempt_id'],status='merging',baseline_evidence=evidence('evidence/'+a['attempt_id']+'-integration-before.json',baseline),generated_artifacts=[],diagnostics=[],rollback=dict(target_sha=before,operation='not-applicable',result='not-needed'))
    a.update(merge_before_sha=before,integration_transaction=transaction); persist()
    event('integration merge '+candidate,ticket=nn,attempt=a['attempt_id'])
    r,log=command(['git','merge','--no-ff','-m','Integrate ledger v2 ticket '+nn,candidate],work,a['attempt_id']+'-integrate'); transaction['diagnostics'].append(log); assert r.returncode==0,r.stderr
    after=clean(work)['head']; a['merge_after_sha']=after; transaction['status']='checking'; assert git(work,'merge-base',candidate,after)==candidate; persist()
    for n,cmd in enumerate(t['verify']):
        st=clean(work); r,log=command(shlex.split(cmd),work,a['attempt_id']+'-integration-verify-'+str(n)); ending=clean(work); assert st==ending
        a['integration_checks'].append(dict(sha=after,command=cmd,cwd=work,exit=r.returncode,log=log,state_evidence=evidence('evidence/'+a['attempt_id']+'-integration-state-'+str(n)+'.json',dict(before=st,after=ending)),qualification='current' if r.returncode==0 else 'failed')); persist(); assert r.returncode==0,r.stderr
    transaction['status']='verified'; a['integration_checks'].append(dict(sha=after,command='N/A',reason='standard-library fixture with no type checker configured')); S['integration']['sha']=after; t['finished_by']=t['attempts'][-2]['requested']; t['finished_agent']=t['attempts'][-2]['agent_id']; persist()
    status(nn,'done','Reviewer PASS '+candidate+'; serialized integration Verify PASS '+after)
    print(nn,'done',after)

def cleanup(nn):
    t=S['tickets'][nn]; work=t['worktree']; integ=S['integration']['worktree']; assert t['status']=='done'
    assert all(a['lifecycle']['activity']=='inactive' for a in t['attempts']); clean(work)
    assert git(integ,'merge-base',t['branch'],S['integration']['ref'])==git(work,'rev-parse','HEAD')
    registration=git(integ,'worktree','list','--porcelain'); assert 'worktree '+work+'\n' in registration
    event('eligible successful ticket cleanup '+work,ticket=nn)
    r,log=command(['git','worktree','remove',work],integ,nn+'-cleanup-worktree'); t['cleanup']={'worktree_exit':r.returncode,'evidence':[log]}; persist()
    if r.returncode==0:
        r,log=command(['git','branch','-d',t['branch']],integ,nn+'-cleanup-branch'); t['cleanup'].update(branch_exit=r.returncode); t['cleanup']['evidence'].append(log); persist()
    print('cleanup',nn,t['cleanup'])

def final_check():
    hashes(); work=S['integration']['worktree']; baseline=clean(work); tip=baseline['head']; assert git(work,'merge-base',S['base_sha'],tip)==S['base_sha']
    S['phase']='final-review'; a=attempt('run','final-verification'); a['candidate_sha']=tip; a['generated_artifacts']=[]; a['started_at']=now(); a['status']='active'; persist()
    cmd='python3 -B -m unittest discover -s tests -v'; r,log=command(shlex.split(cmd),work,a['attempt_id']+'-suite'); ending=clean(work); assert baseline==ending
    stlog=evidence('evidence/'+a['attempt_id']+'-state.json',dict(before=baseline,after=ending))
    check=dict(attempt_id=a['attempt_id'],sha=tip,kind='suite',command=cmd,cwd=work,started_at=a['started_at'],ended_at=now(),exit=r.returncode,log=log,state_evidence=stlog,qualification='current')
    S['closeout']['checks'].append(check); S['closeout']['checks'].append(dict(attempt_id=a['attempt_id'],sha=tip,kind='typecheck',command='N/A',reason='standard-library fixture with no type checker configured',exit='N/A',state_evidence=stlog,qualification='current'))
    a.update(status='completed',ended_at=now(),verdict='PASS' if r.returncode==0 else 'FAIL',evidence=[log,stlog]); a['lifecycle'].update(launch='completed',result='completed',activity='inactive',capacity_release='confirmed: bounded command returned',identity_metadata='not-applicable'); S['closeout']['final_suite']=dict(result='PASS' if r.returncode==0 else 'FAIL',sha=tip,evidence=log); S['closeout']['final_typecheck']='N/A: standard-library fixture with no type checker configured'; persist(); print('Final suite',r.returncode,tip,log)

def final_packet(axis):
    hashes(); work=S['integration']['worktree']; st=clean(work); tip=st['head']; base=S['base_sha']; assert git(work,'merge-base',base,tip)==base
    diff=git(work,'diff',base+'...'+tip); assert diff
    commits=git(work,'log',base+'..'+tip,'--oneline')
    a=attempt('run','final-review-'+axis.lower()); a.update(candidate_sha=tip,reviewed_sha=tip,review_base_sha=base,review_evidence=a['output_destination']); a['state_before']=evidence('evidence/'+a['attempt_id']+'-state-before.json',st)
    baseline=Path(S['companion']['skills']['code-review']).read_text().split('Each smell reads')[1].split('### 4.')[0]
    files=git(work,'ls-files').splitlines(); standards=[p for p in files if Path(p).name in ['CODING_STANDARDS.md','CONTRIBUTING.md','AGENTS.md','CLAUDE.md']]
    spec=S['inputs']['spec']; blocked=[{'ticket':n,'reason':t['blocked_reason']} for n,t in S['tickets'].items() if t['status']=='blocked']
    brief=('Report per file/hunk (a) every violation of documented standard citing file and rule; (b) every baseline smell, name and quote hunk. Distinguish hard documented breaches from judgment calls; repo overrides baseline, skip tooling-enforced. Under400 words.' if axis=='Standards' else 'Report (a) missing/partial requirements; (b) unasked behavior/scope creep; (c) implemented-but-wrong requirements. Quote relevant spec line for each finding. Known blocked requirements listed separately as undelivered scope; remaining delivered deviations still findings. Under400 words.')
    packet=f'''You are the read-only final {axis} reviewer seat, selected reviewer gpt-6.1-sol high. Do not edit files, ask questions, or create descendants.
Worktree: {work}
Integration branch: {S['integration']['ref']}
Saved review base: {base}
Exact reviewed SHA: {tip}
Diff command: git -C "{work}" diff {base}...{tip}
Commits:\n{commits}
Frozen spec: {spec['snapshot']}; SHA256 {spec['sha256']}
All frozen tasks: {RUN}/snapshots/tickets/
Run record (read only): {RECORD}
Companion code-review: {S['companion']['skills']['code-review']}
Read-only local tracker convention: {S['companion']['helpers']['setup-matt-pocock-skills/issue-tracker-local.md']}
Evidence destination planner captures: {a['output_destination']}
Current full-suite/typecheck evidence: {json.dumps(S['closeout']['final_suite'])}; typecheck N/A no configured checker.
Known undelivered scope: {json.dumps(blocked)}
Standards source files: {standards or 'none; use supplied baseline'}
Smell baseline full text (judgment calls, never mechanically hard):\nEach smell reads{baseline}

{brief}
Resolve both objects as commits and base ancestor tip; check HEAD/branch/status/diffs/full ignored/untracked inventory and pending markers before/after, require clean immutable tip. Root confirms no writer. Verify hashes. Read full connected implementation plus tests and standards/spec according to your axis. Do not weaken/delete required assertions to green checks. No artifacts in worktree: set PYTHONDONTWRITEBYTECODE=1 for any Python and subprocesses. Return full report, with explicit axis, PASS/FAIL, exact base and reviewed SHA, findings, check commands/cwd/exits, before/after state and spec hash, N/A reason and declared evidence path. Root saves entire output; no bare PASS. Send concise progress evidence to root if needed. Confine reads to assigned worktree/supplied run/companion files; do not inspect other benchmark repositories.
'''
    a['packet']=evidence('packets/'+a['attempt_id']+'.txt',packet); persist(); print(packet)

if __name__=='__main__':
    if sys.argv[1]=='prepare': prepare(sys.argv[2])
    if sys.argv[1]=='review': review(sys.argv[2],sys.argv[3])
    if sys.argv[1]=='integrate': integrate(sys.argv[2])
    if sys.argv[1]=='cleanup': cleanup(sys.argv[2])
    if sys.argv[1]=='launched': launched(sys.argv[2],sys.argv[3])
    if sys.argv[1]=='final-check': final_check()
    if sys.argv[1]=='final-packet': final_packet(sys.argv[2])
