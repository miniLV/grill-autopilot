#!/usr/bin/env python3
"""Fresh real Git/check facts; verdict/status/queue decisions are manual premises."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shlex
import subprocess
import sys
import tempfile


def command(cwd, *args, expected=0):
    print(f"{datetime.now(timezone.utc).isoformat()} $ (cwd={cwd}) {shlex.join(args)}", flush=True)
    result = subprocess.run(args, cwd=cwd, text=True, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, timeout=30)
    print(result.stdout.rstrip())
    print(f"exit={result.returncode}")
    assert result.returncode == expected
    return result.stdout.strip()


def sha(tree):
    return command(tree, "git", "rev-parse", "HEAD")


def state(tree):
    facts = {"sha": sha(tree),
             "ref": command(tree, "git", "symbolic-ref", "HEAD"),
             "status": command(tree, "git", "status", "--porcelain", "--untracked-files=all"),
             "ignored": command(tree, "git", "ls-files", "--others", "--ignored", "--exclude-standard"),
             "staged": command(tree, "git", "diff", "--cached", "--binary"),
             "unstaged": command(tree, "git", "diff", "--binary"),
             "files": {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                       for p in tree.iterdir() if p.name != ".git"}}
    print("state=" + json.dumps(facts, sort_keys=True))
    return facts


def commit(tree, filename, content, message):
    (tree / filename).write_text(content)
    command(tree, "git", "add", "--", filename)
    command(tree, "git", "commit", "-m", message)
    return sha(tree)


def fixture(root):
    original = root / "original"
    original.mkdir(parents=True)
    command(original, "git", "init", "-b", "base")
    command(original, "git", "config", "user.name", "Integration experiment")
    command(original, "git", "config", "user.email", "experiment@example.invalid")
    command(original, "git", "config", "commit.gpgSign", "false")
    command(original, "git", "config", "core.hooksPath", "/dev/null")
    base = commit(original, "shared.txt", "base\n", "fixture base")
    trees = {}
    for name in ("integration", "a", "b", "c"):
        tree = root / name
        command(original, "git", "worktree", "add", str(tree), "-b", name, base)
        trees[name] = tree
    return original, base, trees


def check(tree, expected=0, produce=""):
    before = state(tree)
    code = ("from pathlib import Path; " + produce +
            "assert Path('a.txt').read_text() == 'A accepted\\n'; "
            "assert not Path('b.txt').exists() or Path('b.txt').read_text() == 'B accepted\\n'; "
            "print('PASS: integrated content')")
    command(tree, sys.executable, "-c", code, expected=expected)
    after = state(tree)
    assert before["sha"] == after["sha"]
    print("real_check=" + json.dumps({"sha": before["sha"], "cwd": str(tree),
                                       "command": shlex.join([sys.executable, "-c", code]),
                                       "exit": expected, "content_state_after": after}, sort_keys=True))


def merge(tree, candidate):
    before = sha(tree)
    print("saved_merge_before_sha=" + before)
    command(tree, "git", "merge", "--no-ff", candidate, "-m", "recorded candidate integration")
    after = sha(tree)
    command(tree, "git", "merge-base", "--is-ancestor", candidate, after)
    return before, after


print("client_date=2026-10-14 Asia/Shanghai; timestamps below are actual UTC")
print("No host/model review dispatched. PASS, done, rejection, queue and failure verdicts are MANUAL protocol decisions.")
with tempfile.TemporaryDirectory(prefix="autopilot-integration-") as temporary:
    root = Path(temporary).resolve()
    for case in ("exact-rollback", "known-artifact", "unknown-user-file", "unknown-tracked-edit", "serialize-two-pass"):
        print("\nCASE " + case)
        repo, base, trees = fixture(root / case)
        integration, a, b, c = (trees[name] for name in ("integration", "a", "b", "c"))
        candidate_a = commit(a, "a.txt", "A accepted\n", "candidate A")
        candidate_b = commit(b, "b.txt", "B rejected\n", "candidate B")
        candidate_c = commit(c, "c.txt", "C accepted\n", "candidate C")
        print("MANUAL PREMISE: fixed base=" + base + "; PASS SHA/evidence qualified for the chosen candidates")
        before_a, after_a = merge(integration, candidate_a)
        assert before_a == base
        check(integration)
        accepted_state = state(integration)
        print("MANUAL DECISION: A done only now; A transaction complete")
        if case == "serialize-two-pass":
            print("MANUAL QUEUE: A and C PASS at same base; C waited for A merge/check/result")
            before_c, after_c = merge(integration, candidate_c)
            assert before_c == after_a and after_c != after_a
            check(integration)
            command(integration, "git", "merge-base", "--is-ancestor", candidate_a, after_c)
            assert (integration / "c.txt").read_text() == "C accepted\n"
            print("MANUAL DECISION: C done; second transaction used updated pre-merge SHA")
            continue
        before_b, after_b = merge(integration, candidate_b)
        assert before_b == after_a
        if case == "exact-rollback":
            # Prove rollback does not consult Git's mutable convenience ref.
            command(integration, "git", "update-ref", "ORIG_HEAD", base)
            assert command(integration, "git", "rev-parse", "ORIG_HEAD") != before_b
            check(integration, expected=1)
        else:
            producer = "Path('known-output.txt').write_text('owned generated output\\n'); "
            print("DECLARED BEFORE CHECK: known-output.txt absent; owned producer and literal content captured")
            assert not (integration / "known-output.txt").exists()
            if case == "unknown-user-file":
                producer += "Path('user-notes.txt').write_text('unknown user work\\n'); "
            if case == "unknown-tracked-edit":
                producer += "Path('shared.txt').write_text('unknown tracked user work\\n'); "
            check(integration, expected=1, produce=producer)
            # Target only the explicitly owned path after content/type verification.
            output = integration / "known-output.txt"
            assert output.is_file() and not output.is_symlink()
            assert output.read_text() == "owned generated output\n"
            print("MANUAL OWNERSHIP: no other writer stipulated; remove exact owned artifact after capture")
            output.unlink()
            preserved = state(integration)
            if case.startswith("unknown-"):
                print("MANUAL DECISION: unknown file/edit => failed; preserve merge/state; no reset/clean")
                assert preserved["sha"] == after_b and preserved["status"]
                assert state(integration) == preserved
                if case == "unknown-user-file":
                    assert (integration / "user-notes.txt").read_text() == "unknown user work\n"
                else:
                    assert (integration / "shared.txt").read_text() == "unknown tracked user work\n"
                continue
        assert state(integration)["status"] == ""
        print("MANUAL DECISION: red B check + safe clean ownership => rollback exact recorded target; B never done")
        command(integration, "git", "reset", "--hard", before_b)
        assert state(integration) == accepted_state
        command(integration, "git", "merge-base", "--is-ancestor", candidate_a, sha(integration))
        command(integration, "git", "merge-base", "--is-ancestor", candidate_b, sha(integration), expected=1)
        assert sha(b) == candidate_b and (b / "b.txt").read_text() == "B rejected\n"
        command(integration, "git", "cat-file", "-t", after_b)
        print("FACT: exact restored SHA/content preserve A; B candidate/failed merge object retained")

    print("\nCASE stale-pass-and-content")
    repo, base, trees = fixture(root / "stale")
    a, integration = trees["a"], trees["integration"]
    reviewed_a = commit(a, "a.txt", "A accepted\n", "reviewed A")
    command(a, "git", "diff", base + "..." + reviewed_a)
    before = state(integration)
    advanced_b = commit(a, "a.txt", "B unreviewed\n", "branch advances after PASS")
    assert advanced_b != reviewed_a
    print("MANUAL DECISION: reviewed SHA A != branch/worktree B => reject stale PASS; no merge")
    assert state(integration) == before
    command(a, "git", "diff", base + "..." + reviewed_a)
    (a / "a.txt").write_text("uncommitted candidate movement\n")
    assert sha(a) == advanced_b and state(a)["status"]
    print("MANUAL DECISION: unchanged HEAD with dirty candidate content still rejects PASS; preserve")
    assert state(integration) == before

    print("\nCASE worker-tip-success-new-candidate")
    repo, base, trees = fixture(root / "worker-tip-success")
    integration, a = trees["integration"], trees["a"]
    old_candidate = commit(a, "a.txt", "A accepted\n", "worker candidate before tip merge")
    tip = commit(integration, "c.txt", "integration update\n", "integration advances independently")
    command(a, "git", "merge", "--no-ff", tip, "-m", "worker merges fixed integration tip")
    new_candidate = sha(a)
    assert new_candidate != old_candidate
    command(a, "git", "merge-base", "--is-ancestor", tip, new_candidate)
    command(a, "git", "merge-base", "--is-ancestor", base, new_candidate)
    check(a)
    assert (a / "c.txt").read_text() == "integration update\n"
    command(a, "git", "diff", tip + "..." + new_candidate)
    assert command(a, "git", "diff", "--name-only", tip + "..." + new_candidate) == "a.txt"
    print("MANUAL DECISION: DONE new post-tip-merge SHA; review base fixed at merged tip; old PASS cannot cover new candidate")

    for case in ("integration-conflict", "worker-tip-conflict"):
        print("\nCASE " + case)
        repo, base, trees = fixture(root / case)
        integration, a = trees["integration"], trees["a"]
        tip = commit(integration, "shared.txt", "integration content\n", "integration advances")
        candidate = commit(a, "shared.txt", "worker content\n", "worker conflict candidate")
        target, other = (integration, candidate) if case == "integration-conflict" else (a, tip)
        baseline = state(target)
        command(target, "git", "merge", "--no-ff", other, "-m", "conflict intent", expected=1)
        conflict = state(target)
        command(target, "git", "rev-parse", "MERGE_HEAD")
        command(target, "git", "ls-files", "-u")
        print("conflict_content_before_abort=" + json.dumps((target / "shared.txt").read_text()))
        assert conflict["status"] and "<<<<<<<" in (target / "shared.txt").read_text()
        print("MANUAL SAFETY: clean baseline + no outside writer/unknown files => capture then abort")
        command(target, "git", "merge", "--abort")
        assert state(target) == baseline
        command(target, "git", "rev-parse", "--verify", "MERGE_HEAD", expected=128)
        print("FACT: diagnostics retained above; exact baseline restored; MANUAL FAIL/STUCK, no blind retry")
print("ALL REAL GIT/CHECK ASSERTIONS PASSED; protocol verdicts remain manual")
