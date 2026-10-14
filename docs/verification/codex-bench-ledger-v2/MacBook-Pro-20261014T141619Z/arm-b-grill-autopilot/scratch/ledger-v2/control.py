"""Planner-only evidence helpers; no autonomous scheduling or child writes."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess

TRACKER = Path(__file__).resolve().parent
RECORD = next((TRACKER / 'runs').glob('*/run.md'))
RUN = RECORD.parent
ORIGINAL = TRACKER.parent.parent

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def read():
    return json.loads(RECORD.read_text().split('```json\n', 1)[1].split('\n```', 1)[0])

def save(s):
    s['updated_at'] = now()
    temporary = own(RECORD.with_suffix('.md.tmp'))
    temporary.write_text('# Ledger v2 run record\n\n```json\n' + json.dumps(s, indent=2) + '\n```\n')
    os.replace(temporary, RECORD)

def event(op, outcome, **fields):
    s = read()
    s['events'].append({'at': now(), 'operation': op, 'outcome': outcome, **fields})
    save(s)

def own(p):
    p = Path(p).resolve()
    assert p.is_relative_to(TRACKER)
    m = TRACKER / 'ownership.json'
    paths = json.loads(m.read_text())
    if str(p) not in paths:
        assert not p.exists(), f'unowned existing path: {p}'
        paths.append(str(p))
        m.write_text(json.dumps(paths, indent=2))
    p.parent.mkdir(parents=True, exist_ok=True)
    return p

def write(p, content):
    p = own(p)
    p.write_text(content)
    return str(p)

def git(cwd, *args):
    return subprocess.check_output(['git', '-C', str(cwd), *args], text=True).strip()

def state(cwd):
    cwd = Path(cwd)
    entries = []
    raw = subprocess.check_output(['git', '-C', str(cwd), 'ls-files', '--others', '-z'])
    for name in raw.split(b'\0'):
        if not name:
            continue
        p = cwd / os.fsdecode(name)
        entries.append({'path': str(p), 'type': 'symlink' if p.is_symlink() else 'file', 'mode': stat.S_IMODE(p.lstat().st_mode), 'hash_or_target': os.readlink(p) if p.is_symlink() else hashlib.sha256(p.read_bytes()).hexdigest()})
    return {'head': git(cwd, 'rev-parse', 'HEAD'), 'ref': git(cwd, 'symbolic-ref', 'HEAD'), 'status': git(cwd, 'status', '--porcelain=v1', '--untracked-files=all'), 'unstaged': git(cwd, 'diff', '--binary'), 'staged': git(cwd, 'diff', '--cached', '--binary'), 'untracked_ignored': entries, 'pending_merge': (Path(git(cwd, 'rev-parse', '--absolute-git-dir')) / 'MERGE_HEAD').exists()}

def command(label, argv, cwd, timeout=1800):
    p = own(RUN / 'logs' / (label + '.json'))
    before = state(cwd)
    start = now()
    event('command intended', 'planned', command=argv, cwd=str(cwd), evidence=str(p), generated_artifacts=[], deadline=(datetime.datetime.now(datetime.timezone.utc)+datetime.timedelta(seconds=timeout)).isoformat())
    try:
        v = subprocess.run(argv, cwd=cwd, env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'}, capture_output=True, text=True, timeout=timeout)
        result = {'command': argv, 'cwd': str(cwd), 'started_at': start, 'ended_at': now(), 'exit': v.returncode, 'stdout': v.stdout, 'stderr': v.stderr, 'before': before, 'after': state(cwd), 'generated_artifacts': [], 'log': str(p)}
    except subprocess.TimeoutExpired as e:
        result = {'command': argv, 'cwd': str(cwd), 'started_at': start, 'ended_at': now(), 'exit': 'timeout', 'stdout': str(e.stdout), 'stderr': str(e.stderr), 'before': before, 'after': state(cwd), 'log': str(p)}
    p.write_text(json.dumps(result, indent=2))
    event('command completed', result['exit'], evidence=str(p), sha=result['after']['head'])
    return result

def hashes():
    s = read()
    for item in [s['inputs']['spec'], *s['inputs']['tickets'].values()]:
        assert hashlib.sha256(Path(item['snapshot']).read_bytes()).hexdigest() == item['sha256']
        source = Path(item['source']).read_text()
        if item is not s['inputs']['spec']:
            source = '\n'.join(line for line in source.split('## Comments', 1)[0].splitlines() if not line.startswith('Status:')) + '\n'
        assert hashlib.sha256(source.encode()).hexdigest() == item['sha256']

def status(n, value, note):
    s = read()
    item = s['tickets'][n]
    p = Path(s['inputs']['tickets'][n]['source'])
    body = p.read_text()
    body = body.replace('Status: ' + item['status'], 'Status: ' + value, 1)
    p.write_text(body + '\n- ' + now() + ': ' + note + '\n')
    item['status'] = value
    save(s)
    event('ticket status', value, ticket=n, reason=note)

def new_attempt(n, role, ident, worktree):
    s = read()
    at = now()
    a = {'attempt_id': ident, 'role': role, 'status': 'planned', 'implementation_started': False, 'infrastructure_retries': 0, 'remaining_budget': s['budgets'], 'next_state': 'claimed' if role in ('worker','escalate') else 'in-review', 'agent_id': 'not-recorded: before launch', 'process_id': 'not-applicable: native agent', 'requested': s['roles'][role]['requested'], 'observed': {'model': 'unknown', 'effort': 'unknown'}, 'model_status': 'unknown', 'lifecycle': {'launch': 'not-recorded','result':'not-recorded','activity':'inactive before start','stop':'not-requested','capacity_release':'not-recorded','identity_metadata':'not-recorded'}, 'logical_started_at': at, 'planned_at': at, 'started_at':'not-recorded','ended_at':'not-recorded','deadline':(datetime.datetime.now(datetime.timezone.utc)+datetime.timedelta(seconds=1800)).isoformat(), 'worktree':str(worktree),'output':str(own(RUN/'logs'/(ident+'-result.txt'))),'invocations':[], 'candidate_sha':'not-recorded','done_check':'not-recorded','review_base_sha':'not-recorded','reviewed_sha':'not-recorded','review_evidence':'not-recorded','merge_before_sha':'not-recorded','merge_after_sha':'not-recorded','integration_transaction':'not-applicable yet','integration_checks':[], 'verdict':'not-recorded','evidence':[]}
    (s['tickets'][n]['attempts'] if n else s['closeout']['attempts']).append(a)
    save(s)
    return a

def attempt(ident):
    s = read()
    for ticket in s['tickets'].values():
        for a in ticket['attempts']:
            if a['attempt_id'] == ident:
                return s, a, ticket
    for a in s['closeout']['attempts']:
        if a['attempt_id'] == ident:
            return s, a, None
    raise KeyError(ident)

def launched(ident, agent, host):
    s,a,t = attempt(ident)
    a.update(agent_id=agent, status='active', started_at=now())
    a['lifecycle'].update(launch='completed: accepted native request', activity='active', identity_metadata='retained')
    if a['role'] in ('worker','escalate'):
        a['implementation_started'] = True
        if t is not None:
            t['counters'][a['role']] += 1
        else:
            s['closeout']['counters']['final_fix'] += 1
    elif t is not None:
        t['counters']['reviewer'] += 1
    else:
        s['closeout']['counters']['reviewer'] += 1
    a['invocations'].append({'number':1,'planned_at':a['planned_at'],'started_at':a['started_at'],'identity':agent,'classification':'completed: accepted','counts_after':t['counters'] if t else s['closeout']['counters'],'evidence':host})
    save(s)
    event('role launched', 'accepted', attempt_id=ident, agent_id=agent, model_status='unknown', host=host)

def completed(ident, result, hosts):
    s,a,t = attempt(ident)
    output = Path(a['output'])
    output.write_text((output.read_text() + '\n\n' if output.exists() else '') + result)
    a.update(status='completed', ended_at=now(), verdict=result)
    a['lifecycle'].update(result='completed', activity='inactive', capacity_release='confirmed: host active-slot contract and terminal list_agents status', identity_metadata='retained: deletion unsupported', evidence=hosts)
    a['invocations'][-1].update(ended_at=a['ended_at'], classification='completed', evidence=hosts)
    save(s)
    event('role completed and capacity reconciled', result, attempt_id=ident, evidence=a['output'], host=hosts)

def prepare(n=None):
    s=read()
    item=s['tickets'][n] if n else s['integration']
    cwd=Path(item['worktree']); branch=item['branch'] if n else item['ref']; sha=git(s['integration']['worktree'],'rev-parse','HEAD') if n else s['base_sha']
    assert not cwd.exists() and not cwd.is_symlink()
    assert git(ORIGINAL,'check-ref-format','--branch',branch)==branch
    refs=git(ORIGINAL,'for-each-ref','--format=%(refname)','refs/heads/').splitlines()
    for ref in refs:
        ref=ref.removeprefix('refs/heads/')
        assert not (ref==branch or ref.startswith(branch+'/') or branch.startswith(ref+'/')),ref
    ident=(n+'-impl-1') if n else 'integration-preparation'
    if n:
        a=new_attempt(n,item['implementer'].split(' ',1)[0],ident,cwd)
        s=read(); s['tickets'][n]['starting_integration_sha']=sha
        save(s)
    else:
        a={'attempt_id':ident,'logical_started_at':now(),'deadline':(datetime.datetime.now(datetime.timezone.utc)+datetime.timedelta(seconds=1800)).isoformat()}
    event('worktree creation intended','preflight passed',ticket=n,ref=branch,path=str(cwd),sha=sha,attempt_id=ident)
    out=command(ident+'-create',['git','worktree','add',str(cwd),'-b',branch,sha],ORIGINAL)
    assert out['exit']==0,out
    baseline=command(ident+'-baseline',['python3','-B','-m','unittest','discover','-s','tests','-v'],cwd)
    s=read(); s['preparations'].append({'worktree':str(cwd),'attempt_id':ident,'started_at':a['logical_started_at'],'deadline':a['deadline'],'starting_sha':sha,'initialization':'skipped: explicit None','generated_paths':[],'baselines':[baseline,{'command':'N/A','reason':'standard-library fixture has no type checker'}],'status':'ready' if baseline['exit']==0 else 'environment-error'})
    if not n:s['integration']['sha']=sha
    save(s)
    assert baseline['exit']==0,baseline
    assert not state(cwd)['status'] and not state(cwd)['untracked_ignored'],state(cwd)
    if n:status(n,'claimed','Preparation passed; implementation attempt planned, not yet charged.')
    return ident

def done(n, ident, sha):
    s,a,t=attempt(ident); cwd=t['worktree']; start=t['starting_integration_sha']; b=state(cwd)
    assert b['ref']=='refs/heads/'+t['branch'] and b['head']==sha and not b['status'] and not b['untracked_ignored'] and not b['pending_merge'],b
    assert int(git(cwd,'rev-list','--count',start+'..'+sha))>=1
    files=git(cwd,'diff','--name-only',start+'...'+sha).splitlines()
    assert set(files)<=set(t['files']),(files,t['files'])
    a['done_check']={'status':'pass','state':b,'changed_files':files};a['candidate_sha']=sha;save(s)
    tip=git(s['integration']['worktree'],'rev-parse','HEAD')
    event('planner tip merge intended','planned',ticket=n,done_sha=sha,tip_sha=tip,state=b,generated_artifacts=[])
    out=command(n+'-tip-merge',['git','merge','--no-edit',tip],cwd)
    assert out['exit']==0,out
    candidate=out['after']['head'];assert not out['after']['status'] and not out['after']['untracked_ignored']
    s,a,t=attempt(ident);a['candidate_sha']=candidate;a['review_base_sha']=tip;save(s)
    status(n,'in-review','DONE check passed; planner tip merge produced '+candidate+' against '+tip)
    return tip,candidate

def integrate(n, reviewid, candidate):
    hashes();s,a,t=attempt(reviewid);cwd=Path(s['integration']['worktree']); b=state(cwd); tb=state(t['worktree'])
    assert tb['head']==candidate and not tb['status'] and not tb['untracked_ignored']
    assert not b['status'] and not b['untracked_ignored'] and not b['pending_merge'],b
    assert a['verdict'].startswith('PASS '+candidate+' '),a['verdict']
    assert git(t['worktree'],'rev-parse',t['branch'])==candidate
    assert subprocess.run(['git','-C',t['worktree'],'merge-base','--is-ancestor',a['review_base_sha'],candidate]).returncode==0
    a['integration_transaction']={'id':reviewid,'status':'merging','baseline_evidence':b,'generated_artifacts':[],'diagnostics':[],'rollback':{'operation':'not-applicable','target_sha':b['head']}}
    a['merge_before_sha']=b['head'];save(s)
    out=command(n+'-integration-merge',['git','merge','--no-ff','--no-edit',candidate],cwd);assert out['exit']==0,out
    merged=out['after']['head'];assert subprocess.run(['git','-C',str(cwd),'merge-base','--is-ancestor',candidate,merged]).returncode==0
    checks=[]
    modules=[t['test_module']] + (['test_cli'] if n=='07' else [])
    for module in modules:
        check=command(n+'-integration-verify-'+module,['python3','-B','-m','unittest','tests.'+module,'-v'],cwd)
        assert check['exit']==0 and check['before']==check['after'],check
        checks.append(check)
    s,a,t=attempt(reviewid);a.update(merge_after_sha=merged,integration_checks=checks+[{'sha':merged,'command':'N/A','reason':'standard-library fixture has no type checker'}]);a['integration_transaction'].update(status='verified',diagnostics=[out['log']]+[v['log'] for v in checks]);s['integration']['sha']=merged;save(s)
    status(n,'done','Reviewer PASS and exact integration Verify passed at '+merged)
    return merged

def cleanup(n, hosts):
    s=read();t=s['tickets'][n];cwd=Path(t['worktree'])
    assert t['status']=='done'
    b=state(cwd)
    assert b['ref']=='refs/heads/'+t['branch'] and not b['status'] and not b['untracked_ignored']
    assert all(a['lifecycle']['activity']=='inactive' for a in t['attempts'])
    assert subprocess.run(['git','-C',str(cwd),'merge-base','--is-ancestor',t['branch'],s['integration']['ref']]).returncode==0
    registrations=git(ORIGINAL,'worktree','list','--porcelain')
    assert 'worktree '+str(cwd)+'\n' in registrations and 'branch refs/heads/'+t['branch'] in registrations
    event('ticket cleanup intended','four gates passed',ticket=n,state=b,hosts=hosts)
    out=command(n+'-cleanup-worktree',['git','worktree','remove',str(cwd)],ORIGINAL)
    if out['exit']!=0:
        event('cleanup warning','retained worktree and branch',ticket=n,evidence=out['log']);return
    out=command(n+'-cleanup-branch',['git','branch','-d',t['branch']],s['integration']['worktree'])
    event('cleanup completed' if out['exit']==0 else 'cleanup warning',out['exit'],ticket=n,evidence=out['log'])
