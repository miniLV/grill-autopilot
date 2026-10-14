"""Run the real benchmark launcher with deterministic sandboxed Git probes.

No models are called. The Codex stub preserves the launcher's writable roots
and replays their observed .git protection using the installed macOS sandbox.
Actual codex-exec control/treatment evidence is recorded separately.
"""
from pathlib import Path
import argparse
import json
import os
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
parser = argparse.ArgumentParser()
parser.add_argument('--runner', type=Path, default=ROOT / 'bench/ledger-v2/run.sh')
args = parser.parse_args()
real_codex = shutil.which('codex')
assert real_codex, 'Codex CLI is required'

STUB = r'''#!/usr/bin/env python3
import json, os, subprocess, sys
from pathlib import Path
a=sys.argv[1:]
assert a[0]=='exec', a
cwd=Path(a[a.index('-C')+1]); out=Path(a[a.index('-o')+1])
roots=[a[i+1] for i,x in enumerate(a) if x=='--add-dir']
assert a[a.index('-s')+1]=='workspace-write'
fs={str(cwd):{'.agents':'read','.codex':'read','.aws':'read'}}
if str(cwd/'.git') not in roots:
    fs[str(cwd)]['.git']='read'
config='permissions={probe={extends=":workspace",workspace_roots={'
config+=','.join(json.dumps(str(p))+'=true' for p in [str(cwd),*roots])
config+='},filesystem={'
config+=','.join(json.dumps(k)+'={'+','.join(json.dumps(p)+'='+json.dumps(v) for p,v in values.items())+'}' for k,values in fs.items())
config+='}}}'
code="""from pathlib import Path
import subprocess, sys
repo=Path.cwd();root=repo.parent/(repo.name+'.probe-worktrees')
def git(p,*a): subprocess.run(['git','-C',str(p),*a],check=True)
integration=root/'integration';ticket=root/'ticket'
git(repo,'worktree','add',str(integration),'-b','probe/integration','main')
git(repo,'worktree','add',str(ticket),'-b','probe/ticket','probe/integration')
(ticket/'verified.txt').write_text('verified\\n')
git(ticket,'add','verified.txt');git(ticket,'commit','-m','Verify shared Git metadata')
git(integration,'merge','--no-ff','probe/ticket','-m','Integrate probe')
assert (integration/'verified.txt').exists()
assert not subprocess.check_output(['git','-C',str(integration),'status','--porcelain'])
print('PASSED: worktrees, commit, merge, clean integration')
"""
r=subprocess.run([os.environ['PROBE_CODEX'],'sandbox','-c',config,'-P','probe','-C',str(cwd),'--','python3','-c',code],text=True,capture_output=True)
out.write_text(r.stdout+r.stderr)
(cwd.parent/(cwd.name+'-argv.json')).write_text(json.dumps(a,indent=2))
print(json.dumps({'type':'probe.result','exit':r.returncode,'output':r.stdout+r.stderr}))
sys.exit(r.returncode)
'''

with tempfile.TemporaryDirectory(prefix='ledger-git-access-') as temporary:
    root=Path(temporary);repo=root/'repo';repo.mkdir()
    shutil.copytree(ROOT/'bench/ledger-v2',repo/'bench/ledger-v2')
    shutil.copy2(args.runner,repo/'bench/ledger-v2/run.sh')
    (repo/'tools').mkdir()
    shutil.copy2(ROOT/'tools/context-report.py',repo/'tools/context-report.py')
    for command in [['init','-q','-b','main'],['config','user.name','Probe'],['config','user.email','probe@example.invalid'],['add','.'],['commit','-qm','Launcher fixture']]:
        subprocess.run(['git','-C',str(repo),*command],check=True,capture_output=True)
    binaries=root/'bin';binaries.mkdir()
    stub=binaries/'codex';stub.write_text(STUB);stub.chmod(0o755)
    environment=dict(os.environ)
    for key in ['BENCH_ROOT','ARMS','MODEL','EFFORT','SANDBOX']:
        environment.pop(key,None)
    environment.update(PATH=str(binaries)+os.pathsep+os.environ['PATH'],BENCH_ROOT=str(root/'bench'),PROBE_CODEX=real_codex)
    result=subprocess.run(['bash','bench/ledger-v2/run.sh'],cwd=repo,env=environment,text=True,capture_output=True)
    assert result.returncode==0,result.stdout+result.stderr
    for key,name in [('a','arm-a-implement-spec'),('b','arm-b-grill-autopilot')]:
        exit_code=(root/'bench'/f'arm-{key}-exit.txt').read_text().strip()
        report=(root/'bench'/f'arm-{key}-last.md').read_text()
        print(f'arm {key}: exit={exit_code}\n{report}')
        assert exit_code=='0',f'{name}: shared Git metadata remains unwritable'
        bundle=next((repo/'docs/verification/codex-bench-ledger-v2').glob(f'*/{name}/repo.bundle'))
        heads=subprocess.check_output(['git','bundle','list-heads',str(bundle)],text=True)
        assert 'refs/heads/probe/integration' in heads and 'refs/heads/probe/ticket' in heads,heads
    print('PASS: both launcher arms commit/merge inside the sandbox; bundles contain implementation refs.')
