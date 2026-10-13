#!/usr/bin/env python3
"""Real Git fixtures and a preflight protocol rehearsal; no agent/scheduler mock."""
import hashlib
import json
import pathlib
import shlex
import subprocess
import tempfile


def command(repo, *args, expected=0):
    argv = ["git", "-C", str(repo), *args]
    print("$ " + shlex.join(argv), flush=True)
    result = subprocess.run(argv, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print(result.stdout.rstrip())
    print(f"exit={result.returncode}")
    assert result.returncode == expected, (argv, result.returncode, expected)
    return result.stdout.strip()


def fixture(root, name):
    directory = root / name
    repo = directory / "repo"
    repo.mkdir(parents=True)
    command(repo, "init", "-b", "base")
    command(repo, "config", "user.name", "Branch experiment")
    command(repo, "config", "user.email", "experiment@example.invalid")
    command(repo, "config", "commit.gpgSign", "false")
    command(repo, "config", "core.hooksPath", "/dev/null")
    (repo / "payload.txt").write_text("base content\n")
    command(repo, "add", "payload.txt")
    command(repo, "commit", "-m", "fixture base")
    base = command(repo, "rev-parse", "--verify", "base^{commit}")
    return directory, repo, base


def snapshot(directory, repo):
    state = {
        "base": command(repo, "rev-parse", "--verify", "base^{commit}"),
        "head": command(repo, "symbolic-ref", "HEAD"),
        "refs": command(repo, "for-each-ref", "--format=%(refname) %(objectname)", "refs/heads/"),
        "worktrees": command(repo, "worktree", "list", "--porcelain"),
        "files": {
            str(path.relative_to(directory)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted(directory.rglob("*"))
            if path.is_file() and ".git" not in path.relative_to(directory).parts
        },
    }
    print("snapshot=" + json.dumps(state, sort_keys=True))
    return state


def unchanged(directory, repo, before):
    assert snapshot(directory, repo) == before
    print("PASS: rejection left base, HEAD, refs, worktrees and file bytes unchanged")


with tempfile.TemporaryDirectory(prefix="autopilot-branches-") as temporary:
    root = pathlib.Path(temporary)
    command(root, "--version")

    print("\nRED: old default integration ref blocks its ticket child")
    directory, repo, base = fixture(root, "red")
    command(repo, "worktree", "add", str(directory / "demo-integration"), "-b", "autopilot/demo", base)
    before = snapshot(directory, repo)
    command(repo, "worktree", "add", str(directory / "demo-01"), "-b", "autopilot/demo/01", base, expected=255)
    unchanged(directory, repo, before)

    print("\nGREEN: demo integration and both tickets coexist")
    directory, repo, base = fixture(root, "green")
    for ref in ("autopilot/demo/integration", "autopilot/demo/tickets/01", "autopilot/demo/tickets/02"):
        command(repo, "check-ref-format", "--branch", ref)
    assert command(repo, "for-each-ref", "--format=%(refname:short)", "refs/heads/") == "base"
    command(repo, "worktree", "list", "--porcelain")
    for suffix, ref in (("integration", "autopilot/demo/integration"), ("01", "autopilot/demo/tickets/01"), ("02", "autopilot/demo/tickets/02")):
        path = directory / f"demo-{suffix}"
        assert not path.exists()
        command(repo, "worktree", "add", str(path), "-b", ref, base)
        assert (path / "payload.txt").read_text() == "base content\n"
    assert command(repo, "for-each-ref", "--format=%(refname:short)", "refs/heads/").splitlines() == [
        "autopilot/demo/integration", "autopilot/demo/tickets/01", "autopilot/demo/tickets/02", "base"
    ]
    assert command(repo, "rev-parse", "base") == base
    assert command(repo, "symbolic-ref", "HEAD") == "refs/heads/base"
    assert (repo / "payload.txt").read_text() == "base content\n"
    print("PASS: three default refs created; base SHA, checkout ref and content unchanged")
    for number in ("01", "02"):
        ref = f"autopilot/demo/tickets/{number}"
        command(repo, "merge-base", "--is-ancestor", ref, "autopilot/demo/integration")
        command(repo, "worktree", "remove", str(directory / f"demo-{number}"))
        command(repo, "branch", "-d", ref)
    assert command(repo, "rev-parse", "base") == base
    assert command(repo, "rev-parse", "autopilot/demo/integration") == base
    print("PASS: cleanup commands delete the named ticket refs and preserve integration/base")

    print("\nREJECT: old ref and dirty worktree retained")
    directory, repo, base = fixture(root, "old-ref")
    existing = directory / "demo-integration"
    command(repo, "worktree", "add", str(existing), "-b", "autopilot/demo", base)
    (existing / "payload.txt").write_text("unfinished tracked edit\n")
    (existing / "notes.txt").write_text("unfinished untracked work\n")
    command(repo, "pack-refs", "--all")
    before = snapshot(directory, repo)
    refs = command(repo, "for-each-ref", "--format=%(refname:short)", "refs/heads/").splitlines()
    assert "autopilot/demo" in refs
    print("Protocol decision: CONFLICT autopilot/demo is an ancestor of all planned refs; stop before creation")
    unchanged(directory, repo, before)

    for name, args, expected in (
        ("missing-base", ("rev-parse", "--verify", "--end-of-options", "missing^{commit}"), 128),
        ("invalid-slug", ("check-ref-format", "--branch", "autopilot/bad:slug/integration"), 128),
    ):
        print(f"\nREJECT: {name}")
        directory, repo, base = fixture(root, name)
        before = snapshot(directory, repo)
        command(repo, *args, expected=expected)
        print("Protocol decision: validation failed; stop before any branch/worktree creation")
        unchanged(directory, repo, before)

    for name, ref in (
        ("existing-ticket", "autopilot/demo/tickets/01"),
        ("descendant-ref", "autopilot/demo/integration/leftover"),
        ("same-slug-residue", "autopilot/demo/tickets/99"),
    ):
        print(f"\nREJECT: {name}")
        directory, repo, base = fixture(root, name)
        command(repo, "branch", ref, base)
        before = snapshot(directory, repo)
        assert ref in command(repo, "for-each-ref", "--format=%(refname:short)", "refs/heads/").splitlines()
        print(f"Protocol decision: CONFLICT {ref} is an exact/prefix conflict or residual same-slug ref; stop before creation")
        unchanged(directory, repo, before)

    print("\nREJECT: occupied unregistered target path")
    directory, repo, base = fixture(root, "occupied-path")
    existing = directory / "demo-01"
    existing.mkdir()
    (existing / "notes.txt").write_text("unowned content\n")
    before = snapshot(directory, repo)
    command(repo, "worktree", "list", "--porcelain")
    assert existing.exists()
    print("Protocol decision: CONFLICT target path exists; stop before creating integration or tickets")
    unchanged(directory, repo, before)

print("\nPASS: all real Git experiments and read-only rejection rehearsals")
