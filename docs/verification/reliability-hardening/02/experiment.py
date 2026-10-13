#!/usr/bin/env python3
"""Real two-worktree input visibility experiment, not a scheduler/runtime test."""
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
    print("stdout_json=" + json.dumps(result.stdout) if "\0" in result.stdout else result.stdout.rstrip())
    print(f"exit={result.returncode}")
    assert result.returncode == expected, (args, result.returncode, expected)
    return result.stdout.strip()


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def original_state(repo, owned):
    untracked = command(repo, "git", "ls-files", "--others", "--exclude-standard", "-z")
    state = {
        "head": command(repo, "git", "symbolic-ref", "HEAD"),
        "base_sha": command(repo, "git", "rev-parse", "base"),
        "tracked_diff": command(repo, "git", "diff", "--binary"),
        "staged_diff": command(repo, "git", "diff", "--cached", "--binary"),
        "non_run_untracked": {
            name: digest(repo / name)
            for name in untracked.split("\0") if name and name not in owned
        },
        "payload": digest(repo / "payload.txt"),
    }
    print("original_state=" + json.dumps(state, sort_keys=True))
    return state


spec_text = "# Demo spec\n\nExport the literal value 42.\n"
task_text = "# 01: Export value\n\nFiles: payload.txt\nExample: export() -> 42\nVerify: python3 -m unittest\n"
reader = """import hashlib,json,pathlib,sys
paths=[pathlib.Path(p) for p in sys.argv[1:]]
assert all(p.is_absolute() and p == p.resolve() for p in paths)
print(json.dumps([{\"path\":str(p),\"sha256\":hashlib.sha256(p.read_bytes()).hexdigest(),\"text\":p.read_text()} for p in paths],sort_keys=True))
"""

with tempfile.TemporaryDirectory(prefix="autopilot-inputs-") as temporary:
    root = pathlib.Path(temporary).resolve()
    repo = root / "original"
    repo.mkdir()
    command(repo, "git", "--version")
    command(repo, "git", "init", "-b", "base")
    command(repo, "git", "config", "user.name", "Input experiment")
    command(repo, "git", "config", "user.email", "experiment@example.invalid")
    command(repo, "git", "config", "commit.gpgSign", "false")
    command(repo, "git", "config", "core.hooksPath", "/dev/null")
    (repo / "payload.txt").write_text("source content\n")
    command(repo, "git", "add", "payload.txt")
    command(repo, "git", "commit", "-m", "fixture base")
    base = command(repo, "git", "rev-parse", "base")
    (repo / "user-notes.bin").write_bytes(b"user content\x00\xff\n")
    before = original_state(repo, set())
    assert before["non_run_untracked"] == {"user-notes.bin": digest(repo / "user-notes.bin")}

    tracker = repo / ".scratch/demo"
    run = tracker / "runs/demo-inputs-01"
    snapshots = run / "snapshots"
    (snapshots / "tickets").mkdir(parents=True)
    spec = snapshots / "spec.md"
    ticket = snapshots / "tickets/01.md"
    source_spec = tracker / "spec.md"
    source_ticket = tracker / "issues/01-export.md"
    source_ticket.parent.mkdir()
    source_spec.write_text(spec_text)
    source_ticket.write_text(task_text + "\nStatus: ready-for-agent\n\n## Comments\n- created\n")
    # Literal frozen task body, independently specified above: no Status/Comments.
    spec.write_text(spec_text)
    ticket.write_text(task_text)
    spec.chmod(0o444)
    ticket.chmod(0o444)
    saved_hashes = [digest(spec), digest(ticket)]
    assert all(path.stat().st_mode & 0o222 == 0 for path in (spec, ticket))
    record = run / "run.md"
    record.write_text("# Protocol rehearsal\nPhase: inputs-ready\nResult: not-final\n")
    owned = {str(path.relative_to(repo)) for path in (source_spec, source_ticket, spec, ticket, record)}
    print("owned_tracker_files=" + json.dumps(sorted(owned)))

    worktrees = [root / "worker", root / "reviewer"]
    for index, worktree in enumerate(worktrees, start=1):
        command(repo, "git", "worktree", "add", str(worktree), "-b", f"autopilot/demo/tickets/{index:02}", base)
        print("RED: checkout-relative tracker input is absent")
        command(worktree, "cat", ".scratch/demo/spec.md", expected=1)
        command(worktree, "cat", ".scratch/demo/issues/01-export.md", expected=1)

    outputs = []
    for worktree in worktrees:
        print("GREEN: canonical absolute snapshots are readable")
        output = command(worktree, sys.executable, "-c", reader, str(spec), str(ticket))
        values = json.loads(output)
        assert [entry["text"] for entry in values] == [spec_text, task_text]
        assert [entry["sha256"] for entry in values] == saved_hashes
        outputs.append(values)
    assert outputs[0] == outputs[1]
    print("PASS: both real worktrees read identical canonical spec/task bytes and hashes")

    # Planner rehearsal: mutable updates do not rewrite distributed inputs.
    source_ticket.write_text(task_text + "\nStatus: blocked\n\n## Comments\n- scope expansion requires another run\n")
    record.write_text(record.read_text() + "Event: scope expansion; ticket blocked; frozen task retained\nAssumption: new scope excluded\n")
    assert [digest(spec), digest(ticket)] == saved_hashes
    assert spec.read_text() == spec_text and ticket.read_text() == task_text
    print("PASS: planner status/event rehearsal preserves frozen spec/task")

    after = original_state(repo, owned)
    assert after == before
    for worktree in worktrees:
        assert command(worktree, "git", "status", "--porcelain") == ""
    command(repo, "git", "worktree", "list", "--porcelain")
    print("PASS: original ref, base SHA, tracked/staged diff and unrelated untracked bytes unchanged")

print("PASS: real Git input experiment and explicitly identified planner rehearsal")
