#!/usr/bin/env python3
"""Actual Git retention/cleanup evidence; activity/ownership decisions are rehearsed."""
from datetime import datetime, timezone
import hashlib
import json
import pathlib
import shlex
import subprocess
import sys
import tempfile


def command(cwd, *args, expected=0):
    print(datetime.now(timezone.utc).isoformat() + f" $ (cwd={cwd}) " + shlex.join(args), flush=True)
    result = subprocess.run(args, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print(result.stdout.rstrip())
    print(f"exit={result.returncode}")
    assert result.returncode != 0 if expected == "nonzero" else result.returncode == expected
    return result.stdout.strip()


def retained_state(worktree, branch):
    state = {
        "branch_sha": command(worktree, "git", "rev-parse", branch),
        "status": command(worktree, "git", "status", "--porcelain", "--untracked-files=all"),
        "files": {name: hashlib.sha256((worktree / name).read_bytes()).hexdigest()
                  for name in ("payload.txt", "notes.txt")},
    }
    print("retained_state=" + json.dumps(state, sort_keys=True))
    return state


print("client_date=2026-10-14 Asia/Shanghai (supplied context; not a log timestamp)")
print("actual_started_at_utc=" + datetime.now(timezone.utc).isoformat())
with tempfile.TemporaryDirectory(prefix="autopilot-retain-") as temporary:
    root = pathlib.Path(temporary).resolve()
    repo = root / "original"
    repo.mkdir()
    command(repo, "git", "init", "-b", "base")
    command(repo, "git", "config", "user.name", "Retention experiment")
    command(repo, "git", "config", "user.email", "experiment@example.invalid")
    command(repo, "git", "config", "commit.gpgSign", "false")
    command(repo, "git", "config", "core.hooksPath", "/dev/null")
    (repo / "payload.txt").write_text("base content\n")
    command(repo, "git", "add", "payload.txt")
    command(repo, "git", "commit", "-m", "retention fixture base")
    base = command(repo, "git", "rev-parse", "base")
    integration = root / "integration"
    command(repo, "git", "worktree", "add", str(integration), "-b", "autopilot/demo/integration", base)

    print("\nBLOCKED: preserve tracked and untracked dirty work, not just the branch")
    blocked, branch = root / "blocked-01", "autopilot/demo/tickets/01"
    command(repo, "git", "worktree", "add", str(blocked), "-b", branch, base)
    (blocked / "payload.txt").write_text("unfinished tracked change\n")
    (blocked / "notes.txt").write_text("unfinished untracked notes\n")
    before = retained_state(blocked, branch)
    assert command(repo, "git", "show", branch + ":payload.txt") == "base content"
    command(repo, "git", "cat-file", "-e", branch + ":notes.txt", expected="nonzero")
    print("FACT: branch objects have old tracked content and no notes; dirty files live only in worktree")
    print("RED: original blocked-removal instruction cannot remove this dirty tree without force")
    command(repo, "git", "worktree", "remove", str(blocked), expected="nonzero")
    assert retained_state(blocked, branch) == before
    print("PLANNER REHEARSAL: blocked retains canonical worktree/branch, dirty inventory and evidence; no agent was launched")

    print("\nSUCCESS: actual clean merged ticket cleanup keeps integration")
    success, success_branch = root / "success-02", "autopilot/demo/tickets/02"
    command(repo, "git", "worktree", "add", str(success), "-b", success_branch, base)
    (success / "payload.txt").write_text("integrated content\n")
    command(success, "git", "add", "payload.txt")
    command(success, "git", "commit", "-m", "fixture ticket candidate")
    command(integration, "git", "merge", "--no-ff", success_branch, "-m", "fixture integration")
    command(integration, sys.executable, "-c", "from pathlib import Path; assert Path('payload.txt').read_text() == 'integrated content\\n'")
    verified_sha = command(integration, "git", "rev-parse", "HEAD")
    command(repo, "git", "merge-base", "--is-ancestor", success_branch, "autopilot/demo/integration")
    assert command(success, "git", "status", "--porcelain", "--untracked-files=all") == ""
    print("PLANNER REHEARSAL: done is recorded from merge/check evidence; run ownership and inactivity are stipulated, not host observations")
    command(repo, "git", "worktree", "remove", str(success))
    command(integration, "git", "branch", "-d", success_branch)
    assert not success.exists() and integration.exists()
    command(repo, "git", "show-ref", "--verify", "refs/heads/" + success_branch, expected="nonzero")
    assert command(integration, "git", "rev-parse", "HEAD") == verified_sha
    print("PASS: clean merged ticket path/ref removed; verified integration path/SHA retained")

    for name, ref, reason in (("active-03", "autopilot/demo/tickets/03", "active agent flag"),
                              ("unowned-04", "autopilot/demo/tickets/04", "ownership not established")):
        print("\nSKIP rehearsal: " + reason)
        path = root / name
        command(repo, "git", "worktree", "add", str(path), "-b", ref, verified_sha)
        command(repo, "git", "merge-base", "--is-ancestor", ref, "autopilot/demo/integration")
        assert command(path, "git", "status", "--porcelain", "--untracked-files=all") == ""
        before_sha = command(repo, "git", "rev-parse", ref)
        print("PLANNER REHEARSAL: skip deletion for " + reason + "; no cleanup command issued")
        assert path.exists() and command(repo, "git", "rev-parse", ref) == before_sha

    print("\nCLEANUP WARNING: locked clean/merged fixture refuses non-force removal")
    locked, locked_ref = root / "locked-05", "autopilot/demo/tickets/05"
    command(repo, "git", "worktree", "add", str(locked), "-b", locked_ref, verified_sha)
    command(repo, "git", "merge-base", "--is-ancestor", locked_ref, "autopilot/demo/integration")
    assert command(locked, "git", "status", "--porcelain", "--untracked-files=all") == ""
    locked_content = hashlib.sha256((locked / "payload.txt").read_bytes()).hexdigest()
    command(repo, "git", "worktree", "lock", str(locked), "--reason", "fixture cleanup failure")
    command(repo, "git", "worktree", "remove", str(locked), expected="nonzero")
    print("PLANNER REHEARSAL: cleanup warning; prior verified result remains done; do not force, unlock or delete branch")
    assert locked.exists() and command(repo, "git", "rev-parse", locked_ref) == verified_sha
    assert hashlib.sha256((locked / "payload.txt").read_bytes()).hexdigest() == locked_content
    assert command(integration, "git", "rev-parse", "HEAD") == verified_sha
    assert retained_state(blocked, branch) == before
    assert command(repo, "git", "rev-parse", "base") == base
    command(repo, "git", "worktree", "list", "--porcelain")

print("actual_finished_at_utc=" + datetime.now(timezone.utc).isoformat())
print("PASS: actual Git preservation/cleanup checks; ownership/activity/warning verdicts are labeled protocol rehearsals")
