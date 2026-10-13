#!/usr/bin/env python3
"""Real Git/command preparation evidence plus explicitly scripted planner records."""
import hashlib
import json
import pathlib
import shlex
import subprocess
import sys
import tempfile


def command(cwd, *args, expected=0):
    print(f"$ (cwd={cwd}) " + shlex.join(args), flush=True)
    result = subprocess.run(args, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print(result.stdout.rstrip())
    print(f"exit={result.returncode}")
    assert result.returncode == expected, (args, result.returncode, expected)
    return result.returncode


def source_state(worktree):
    state = {name: hashlib.sha256((worktree / name).read_bytes()).hexdigest()
             for name in ("business.py", "check_baseline.py", "initialize.py", "dependencies.lock", ".gitignore")}
    print("tracked_content=" + json.dumps(state, sort_keys=True))
    return state


with tempfile.TemporaryDirectory(prefix="autopilot-bootstrap-") as temporary:
    root = pathlib.Path(temporary).resolve()
    repo = root / "original"
    repo.mkdir()
    command(repo, "git", "init", "-b", "base")
    command(repo, "git", "config", "user.name", "Bootstrap experiment")
    command(repo, "git", "config", "user.email", "experiment@example.invalid")
    command(repo, "git", "config", "commit.gpgSign", "false")
    command(repo, "git", "config", "core.hooksPath", "/dev/null")
    (repo / ".gitignore").write_text(".deps/\n__pycache__/\n")
    (repo / "dependencies.lock").write_text("fixture_dep=1\n")
    (repo / "initialize.py").write_text("""from pathlib import Path
if Path('dependencies.lock').read_text() != 'fixture_dep=1\\n':
    raise SystemExit('unexpected fixture lock version')
Path('.deps').mkdir(exist_ok=True)
Path('.deps/fixture_dep.py').write_text('VALUE = 42\\n')
print('prepared existing fixture lock dependency')
""")
    (repo / "business.py").write_text("from fixture_dep import VALUE\n\ndef export():\n    return VALUE\n")
    (repo / "check_baseline.py").write_text("""import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path('.deps').resolve()))
from business import export
class Baseline(unittest.TestCase):
    def test_export_literal(self):
        self.assertEqual(export(), 42)
unittest.main()
""")
    command(repo, "git", "add", ".")
    command(repo, "git", "commit", "-m", "bootstrap fixture base")
    command(repo, "git", "rev-parse", "base")
    original = source_state(repo)
    command(repo, sys.executable, "initialize.py")
    command(repo, sys.executable, "check_baseline.py")
    command(repo, "git", "check-ignore", ".deps/fixture_dep.py")
    print("FACT: original ignored dependency exists=" + str((repo / ".deps/fixture_dep.py").exists()))

    print("\nINTEGRATION and TICKET: missing ignored dependency, then initialization and green baseline")
    for name, branch in (("integration", "autopilot/demo/integration"), ("ticket-01", "autopilot/demo/tickets/01")):
        worktree = root / name
        command(repo, "git", "worktree", "add", str(worktree), "-b", branch, "base")
        print("FACT: new worktree dependency exists=" + str((worktree / ".deps/fixture_dep.py").exists()))
        assert not (worktree / ".deps/fixture_dep.py").exists()
        before = source_state(worktree)
        command(worktree, sys.executable, "check_baseline.py", expected=1)
        command(worktree, sys.executable, "initialize.py")
        command(worktree, sys.executable, "check_baseline.py")
        assert source_state(worktree) == before
        command(worktree, "git", "status", "--porcelain")
        print('PLANNER REHEARSAL: {"preparation":"ready","implementation_attempts":0,"reason":"gate completed; no worker was dispatched"}')

    print("\nINIT EXIT 7: stop before baseline/implementation; no business repair")
    worktree = root / "ticket-init-7"
    command(repo, "git", "worktree", "add", str(worktree), "-b", "autopilot/demo/tickets/02", "base")
    before = source_state(worktree)
    command(worktree, sys.executable, "-c", "import sys; print('fixture initialization failure'); sys.exit(7)", expected=7)
    print('PLANNER REHEARSAL: {"preparation":"environment-error","operation":"initialization","exit":7,"implementation_attempts":0,"handoff":"command evidence retained; no worker or baseline call"}')
    assert source_state(worktree) == before
    command(worktree, "git", "status", "--porcelain")

    print("\nBASELINE RED: seed a pre-existing defect before the preparation experiment")
    worktree = root / "ticket-baseline-red"
    command(repo, "git", "worktree", "add", str(worktree), "-b", "autopilot/demo/tickets/03", "base")
    (worktree / "business.py").write_text("from fixture_dep import VALUE\n\ndef export():\n    return VALUE - 1\n")
    command(worktree, "git", "add", "business.py")
    command(worktree, "git", "commit", "-m", "seed pre-existing red baseline")
    before = source_state(worktree)
    command(worktree, sys.executable, "initialize.py")
    command(worktree, sys.executable, "check_baseline.py", expected=1)
    print('PLANNER REHEARSAL: {"preparation":"environment-error","operation":"baseline","exit":1,"implementation_attempts":0,"handoff":"pre-existing baseline defect preserved; business repair not attempted"}')
    assert source_state(worktree) == before
    command(worktree, "git", "status", "--porcelain")
    print("PASS: initialization and baseline failures preserve all tracked fixture bytes")

    print('CHECK CHOICE REHEARSAL: {"typecheck":"N/A","reason":"standard-library Python fixture with an artificial local module; no configured static-type checker/contract","behavior_tests":"check_baseline.py executed, not waived"}')
    print('CHECK CHOICE REHEARSAL: {"initialization":"None only for an already runnable environment","effect":"skip initialization process, still require applicable baseline behavior checks"}')
    assert source_state(repo) == original
    command(repo, "git", "symbolic-ref", "HEAD")
    command(repo, "git", "rev-parse", "base")
    command(repo, "git", "status", "--porcelain")

print("PASS: real Git/command experiment; preparation/counter/check-choice records are planner rehearsals, not runtime automation")
