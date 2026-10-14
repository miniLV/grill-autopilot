from pathlib import Path
import subprocess,json,hashlib,datetime,os,sys
R=Path(__file__).resolve().parents[4];T=R/'.scratch/ledger-v2';D=Path(__file__).resolve().parent;P=D/'run.md'
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def read():return json.loads(P.read_text().split('```json\n')[1].split('\n```')[0])
s=read()
def save():
 s['updated_at']=now();P.write_text('# ledger v2 run record\n\n```json\n'+json.dumps(s,indent=2)+'\n```\n');(D/'owned.json').write_text(json.dumps(s['owned_tracker_files'],indent=2))
def own(p):
 p=Path(p)
 if str(p) not in s['owned_tracker_files']:s['owned_tracker_files'].append(str(p));save()
 p.parent.mkdir(parents=True,exist_ok=True);return p
def put(p,data):own(p).write_text(data)
def event(op,**kw):s['events'].append({'at':now(),'operation':op,**kw});save()
def raw(cwd,*a):
 p=subprocess.run(list(a),cwd=cwd,capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'},timeout=120);return p

def git(cwd,*a):
 p=raw(cwd,'git',*a);assert p.returncode==0,(a,p.stderr);return p.stdout.strip()
def state(w):
 return {'head':git(w,'rev-parse','HEAD'),'ref':git(w,'symbolic-ref','HEAD'),'status':git(w,'status','--porcelain=v1','--untracked-files=all'),'ignored':git(w,'ls-files','--others','--ignored','--exclude-standard'),'diff':git(w,'diff','--binary'),'cached_diff':git(w,'diff','--cached','--binary'),'files':git(w,'ls-files','--stage')}
def command(label,w,argv):
 pth=own(D/f'logs/{label}.json');before=state(w);event('command-intent',label=label,cwd=str(w),argv=argv,evidence=str(pth),deadline=(datetime.datetime.now(datetime.timezone.utc)+datetime.timedelta(seconds=1800)).isoformat(),generated_artifacts=[],environment={'PYTHONDONTWRITEBYTECODE':'1'})
 started=now();p=raw(w,*argv);after=state(w);data={'command':argv,'cwd':str(w),'started_at':started,'ended_at':now(),'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'before':before,'after':after,'generated_artifacts':[]};pth.write_text(json.dumps(data,indent=2));event('command-result',label=label,exit=p.returncode,evidence=str(pth),sha=after['head']);assert p.returncode==0,(label,p.stdout,p.stderr);return data

def verify_inputs():
 for v in [s['inputs']['spec'],*s['inputs']['tickets'].values()]:assert hashlib.sha256(Path(v['snapshot']).read_bytes()).hexdigest()==v['sha256']

def begin(role,nn,worktree,label):
 a={'attempt_id':label,'ticket':nn,'role':role,'status':'planned','implementation_started':False,'infrastructure_retries':0,'logical_started_at':now(),'planned_at':now(),'deadline':(datetime.datetime.now(datetime.timezone.utc)+datetime.timedelta(seconds=1800)).isoformat(),'worktree':str(worktree),'requested':s['roles'].get(role,{}).get('requested',{}),'observed':{'model':'unknown','effort':'unknown'},'model_status':'unknown','agent_id':'not-started','lifecycle':{'launch':'not-started','result':'not-recorded','activity':'inactive','capacity_release':'not-used','identity_metadata':'not-created'},'output':str(own(D/f'logs/{label}-result.txt')),'remaining_budget':s['budgets'],'invocations':[]};s['attempts'].append(a)
 if nn in s['tickets']:s['tickets'][nn]['attempts'].append(label)
 save();return a

def status(nn,value,comment=''):
 t=s['tickets'][nn];t['status']=value;p=Path(s['inputs']['tickets'][nn]['source']);text=p.read_text();text='\n'.join('Status: '+value if line.startswith('Status:') else line for line in text.split('\n'));p.write_text(text+(f'\n- {now()} {comment}\n' if comment else ''));save()

def worker_packet(nn,a):
 t=s['tickets'][nn];inp=s['inputs']['tickets'][nn];sp=s['inputs']['spec'];w=Path(t['worktree']);head=git(w,'rev-parse','HEAD');a['starting_sha']=head
 return f'''You are a worker. Implement exactly one ticket.
Task: {inp['snapshot']}    Spec: {sp['snapshot']}
TDD skill: {s['companion']['skills']['tdd']}
Context: {w}/tests/test_store.py; {w}/tests/test_cli.py
Worktree: {w}    Branch: {t['branch']}
Starting SHA: {head}
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

Agreed seams are public functions in ledger.money, ledger.categories, ledger.query, ledger.csv_io and ledger.store; CLI via subprocess python3 -m ledger. Never ask questions; all approvals already granted. No descendants. Use PYTHONDONTWRITEBYTECODE=1 in the environment of every Python/check command, inherited by subprocesses, so no bytecode artifacts are written. Literal \\n in ticket examples denotes newline. Record red/green commands and failures per example in commit-message body for review evidence. Deadline: {a['deadline']}. Only worktree Files are writable; do not read other benchmark directories. TDD skill helpers may be read from same canonical companion collection.
'''

if __name__=='__main__':
 action=sys.argv[1];nn=sys.argv[2] if len(sys.argv)>2 else ''
 if action=='prepare':
  verify_inputs();item=s['integration'] if nn=='integration' else s['tickets'][nn];w=Path(item['worktree']);branch=item.get('ref',item.get('branch'));start=s['base_sha'] if nn=='integration' else git(s['integration']['worktree'],'rev-parse','HEAD');a=begin('preparation',nn,w,nn+'-preparation');assert not w.exists();assert not raw(R,'git','show-ref','--verify','--quiet','refs/heads/'+branch).returncode==0;event('worktree-create-intent',branch=branch,path=str(w),base_sha=start);w.parent.mkdir(parents=True,exist_ok=True);p=raw(R,'git','worktree','add',str(w),'-b',branch,start);put(D/f'logs/{nn}-worktree.txt',p.stdout+p.stderr);assert p.returncode==0,p.stderr
  item['starting_integration_sha']=start;item['sha']=start;save();argv=['python3','-B','-m','unittest','discover','-s','tests','-v'] if nn=='integration' else (item['verify'] if (w/(item['verify'][4].replace('.','/')+'.py')).exists() else ['python3','-B','-m','unittest','tests.test_store','-v']);data=command(nn+'-baseline',w,argv);assert data['before']==data['after'];assert not data['after']['status'] and not data['after']['ignored'];a['status']='completed';a['ended_at']=now();a['verdict']='initialization None; baseline pass; typecheck N/A (no configured checker)';save();print('PREPARED',nn,start)
 elif action=='launch':
  role=sys.argv[3];verify_inputs();t=s['tickets'][nn];w=Path(t['worktree']);count=t['counters'].get(role,0)+1;label=f'{nn}-{role}-{count}';a=begin(role,nn,w,label);status(nn,'claimed');packet=worker_packet(nn,a);path=D/f'packets/{label}.txt';put(path,packet);a['packet']=str(path);a['counts_before']=dict(t['counters']);a['intended_counters']={**t['counters'],role:count};save();print(packet)
 elif action=='attach':
  a=next(x for x in s['attempts'] if x['attempt_id']==nn);a['agent_id']=sys.argv[3];a['status']='active';a['started_at']=now();a['lifecycle']={'launch':'completed: native spawn accepted','result':'pending','activity':'active','capacity_release':'not-yet','identity_metadata':'retained'};a['invocations'].append({'number':1,'started_at':now(),'identity':sys.argv[3],'classification':'completed: launch accepted','actual_model_metadata':'unknown'});role=a['role'];ticket=a['ticket'];
  if role in ['worker','escalate','reviewer']:
   s['counters'][role]+=1
   if ticket in s['tickets']:s['tickets'][ticket]['counters'][role]+=1
  a['implementation_started']=role in ['worker','escalate'];save();print('ATTACHED',nn,sys.argv[3])
 elif action=='finish':
  a=next(x for x in s['attempts'] if x['attempt_id']==nn);result=sys.argv[3];put(Path(a['output']),result+'\n');a['status']='completed';a['ended_at']=now();a['verdict']=result;a['lifecycle'].update({'result':'completed','activity':'inactive','capacity_release':'confirmed: host list_agents idle and active-capacity contract','identity_metadata':'retained; deletion unsupported'});a['lifecycle']['evidence']='Root queried list_agents after complete final result; no active turn for this identity.';save();print('RECORDED',nn)
 elif action=='candidate':
  verify_inputs();t=s['tickets'][nn];w=Path(t['worktree']);sha=sys.argv[3];a=next(x for x in reversed(s['attempts']) if x['ticket']==nn and x['role'] in ['worker','escalate']);before=state(w);assert before['head']==sha and before['ref']=='refs/heads/'+t['branch'] and not before['status'] and not before['ignored'];assert int(git(w,'rev-list','--count',a['starting_sha']+'..'+sha))>=1;changed=git(w,'diff','--name-only',t['starting_integration_sha']+'...'+sha).splitlines();assert set(changed)<=set(t['files']),(changed,t['files']);a['done_check']={'status':'pass','state':before,'paths':changed};tip=git(s['integration']['worktree'],'rev-parse','HEAD');event('planner-tip-merge-intent',ticket=nn,done_sha=sha,review_base_sha=tip,before=before);command(nn+'-tip-merge',w,['git','merge','--no-edit',tip]);candidate=git(w,'rev-parse','HEAD');t['review_base_sha']=tip;t['candidate_sha']=candidate;a['candidate_sha']=candidate;a['review_base_sha']=tip;status(nn,'in-review');save();print('CANDIDATE',nn,tip,candidate)
 elif action=='review-packet':
  verify_inputs();t=s['tickets'][nn];w=Path(t['worktree']);a=begin('reviewer',nn,w,f"{nn}-reviewer-{t['counters']['reviewer']+1}");a['review_base_sha']=t['review_base_sha'];a['candidate_sha']=t['candidate_sha'];inp=s['inputs']['tickets'][nn];sp=s['inputs']['spec'];ev=own(D/f"logs/{a['attempt_id']}-evidence.txt");a['review_evidence']=str(ev)
  packet=f'''You are a reviewer. Gate one ticket. Read; do not edit anything.
Task snapshot: {inp['snapshot']}    Spec snapshot: {sp['snapshot']}
Input SHA-256: task={inp['sha256']} spec={sp['sha256']}
Mutable tracker ticket (read only): {inp['source']}
Run record (read only): {P}
Companions: {s['companion']['skills']['tdd']}
External/run Context: {w}/tests/test_store.py; {w}/tests/test_cli.py
Log capture: {ev}; planner/host writes
Worktree: {w}
Branch: {t['branch']}
Review base SHA: {t['review_base_sha']}
Candidate SHA: {t['candidate_sha']}
Review evidence: {ev}
Diff: git -C "{w}" diff {t['review_base_sha']}...{t['candidate_sha']}

Verify snapshot hashes; use frozen task/spec for requirements. Resolve repository Files/Context under assigned worktree. Report events to planner; tracker/record are read only.
Resolve supplied SHAs as commits and require base ancestor candidate. Require HEAD and branch tip equal candidate, clean checked content and no active/unknown writer before checks and again afterward. Planner confirms implementer inactive; this is sole active reviewer in this worktree. Use SHA diff above, never live refs. Save exact base/candidate, commands/cwd/exits, check output, N/A reasons and before/after HEAD/status in captured evidence. Missing evidence/movement/dirty content cannot PASS.
Check: 1. Every Acceptance met. 2. Every changed path in Files. 3. Tests assert literal Examples, no weakened/skipped/deleted assertion. 4. Run every applicable Verify; typecheck N/A because standard-library fixture with no checker. 5. Nothing outside scope changed.

Set PYTHONDONTWRITEBYTECODE=1 for all check commands (including child subprocesses). Read only: do not write logs/tracker or modify files. Before final reply send root via collaboration.send_message a REVIEW_EVIDENCE message containing exact base/candidate, hashes, before/after git state, commands, exits, complete check outputs, TDD commit evidence and findings. Planner captures that message in {ev}. Deadline {a['deadline']}. No descendants; no other benchmark directories.
Reply with one line only:
PASS <reviewed candidate SHA> {ev}
or FAIL: <numbered reasons, under 120 words>
''';path=D/f"packets/{a['attempt_id']}.txt";put(path,packet);a['packet']=str(path);save();print(packet)
 elif action=='integrate':
  verify_inputs();t=s['tickets'][nn];w=Path(s['integration']['worktree']);tw=Path(t['worktree']);candidate=t['candidate_sha'];a=next(x for x in reversed(s['attempts']) if x['ticket']==nn and x['role']=='reviewer');assert a['verdict'].startswith('PASS '+candidate+' ');assert Path(a['review_evidence']).is_file();assert a['lifecycle']['activity']=='inactive';b=state(w);tb=state(tw);assert not b['status'] and not b['ignored'] and not tb['status'] and not tb['ignored'] and tb['head']==candidate;assert git(tw,'rev-parse',t['branch'])==candidate;git(w,'merge-base','--is-ancestor',t['review_base_sha'],candidate)
  a['integration_transaction']={'id':a['attempt_id'],'status':'merging','merge_before_sha':b['head'],'candidate_sha':candidate,'baseline':b,'generated_artifacts':[],'rollback':{'operation':'not-needed','target_sha':b['head']}};save();command(nn+'-integrate',w,['git','merge','--no-ff','--no-edit',candidate]);after=git(w,'rev-parse','HEAD');git(w,'merge-base','--is-ancestor',candidate,after);a['integration_transaction']['merge_after_sha']=after;a['integration_transaction']['status']='checking';save();data=command(nn+'-integration-verify',w,t['verify']);assert data['before']==data['after'] and not data['after']['status'] and not data['after']['ignored'];a['integration_checks']=[{'sha':after,'command':t['verify'],'evidence':str(D/f'logs/{nn}-integration-verify.json'),'status':'pass','typecheck':'N/A no configured checker'}]
  if nn=='07':command(nn+'-integration-cli-verify',w,['python3','-B','-m','unittest','tests.test_cli','-v'])
  a['integration_transaction']['status']='verified';s['integration']['sha']=after;status(nn,'done','Reviewed candidate '+candidate+'; integration Verify passed at '+after);print('DONE',nn,after)
 elif action=='cleanup':
  t=s['tickets'][nn];w=Path(t['worktree']);iw=Path(s['integration']['worktree']);assert t['status']=='done';assert not state(w)['status'] and not state(w)['ignored'];git(iw,'merge-base','--is-ancestor',t['branch'],s['integration']['ref']);reg=git(R,'worktree','list','--porcelain');assert 'worktree '+str(w)+'\n' in reg and 'branch refs/heads/'+t['branch'] in reg;assert all(x['lifecycle']['activity']=='inactive' for x in s['attempts'] if x['ticket']==nn and x['role']!='preparation');event('cleanup-intent',ticket=nn,worktree=str(w),branch=t['branch'],evidence='verified integration inclusion, clean worktree, exact registration, all owned agents inactive');p=raw(R,'git','worktree','remove',str(w));event('cleanup-worktree-result',ticket=nn,exit=p.returncode,output=p.stdout+p.stderr)
  if p.returncode==0:
   p=raw(iw,'git','branch','-d',t['branch']);event('cleanup-branch-result',ticket=nn,exit=p.returncode,output=p.stdout+p.stderr)
  print('CLEANUP',nn,p.returncode)
 elif action=='summary':print(json.dumps({'integration':s['integration'],'counters':s['counters'],'tickets':{k:{'status':v['status'],'counters':v['counters']} for k,v in s['tickets'].items()}},indent=2))
