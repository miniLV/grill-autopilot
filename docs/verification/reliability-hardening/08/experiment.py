#!/usr/bin/env python3
"""Real Git/check facts plus explicitly manual resume decisions; no scheduler."""
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


def retained(repo, integration, ticket):
    return {
        "refs": command(repo, "git", "for-each-ref", "--format=%(refname) %(objectname)"),
        "registrations": command(repo, "git", "worktree", "list", "--porcelain"),
        "integration_status": command(integration, "git", "status", "--porcelain", "--untracked-files=all"),
        "ticket_status": command(ticket, "git", "status", "--porcelain", "--untracked-files=all"),
        "files": {str(p): hashlib.sha256(p.read_bytes()).hexdigest()
                  for tree in (integration, ticket) for p in tree.iterdir() if p.name != ".git"},
    }


def verify(integration, log):
    before = command(integration, "git", "rev-parse", "HEAD")
    assert command(integration, "git", "status", "--porcelain", "--untracked-files=all") == ""
    code = "from pathlib import Path; assert Path('payload.txt').read_text() == 'candidate content\\n'; print('PASS: candidate content')"
    started = datetime.now(timezone.utc).isoformat()
    output = command(integration, sys.executable, "-c", code)
    after = command(integration, "git", "rev-parse", "HEAD")
    assert command(integration, "git", "status", "--porcelain", "--untracked-files=all") == ""
    assert before == after
    evidence = {"sha": before, "sha_after": after, "command": shlex.join([sys.executable, "-c", code]),
                "cwd": str(integration), "started_at": started,
                "ended_at": datetime.now(timezone.utc).isoformat(), "exit": 0,
                "output": output, "clean_before_after": True, "log": str(log)}
    log.write_text(json.dumps(evidence, sort_keys=True) + "\n")
    print("captured_check_log=" + log.read_text().strip())
    return evidence


print("client_date=2026-10-14 Asia/Shanghai (supplied context; not log timestamp)")
print("actual_started_at_utc=" + datetime.now(timezone.utc).isoformat())
print("No host dispatched. Identity, fingerprint, review PASS and resume decisions are manual protocol premises.")
with tempfile.TemporaryDirectory(prefix="autopilot-resume-") as temporary:
    for case in ("matching-evidence", "missing-evidence", "older-check-sha", "inconsistent-branch-sha"):
        print("\nCASE " + case)
        root = Path(temporary).resolve() / case
        repo = root / "original"
        repo.mkdir(parents=True)
        command(repo, "git", "init", "-b", "base")
        command(repo, "git", "config", "user.name", "Resume experiment")
        command(repo, "git", "config", "user.email", "experiment@example.invalid")
        command(repo, "git", "config", "commit.gpgSign", "false")
        command(repo, "git", "config", "core.hooksPath", "/dev/null")
        (repo / "payload.txt").write_text("base content\n")
        command(repo, "git", "add", "payload.txt")
        command(repo, "git", "commit", "-m", "resume fixture base")
        base = command(repo, "git", "rev-parse", "HEAD")
        integration, ticket = root / "integration", root / "ticket"
        iref, tref = "autopilot/demo/integration", "autopilot/demo/tickets/01"
        command(repo, "git", "worktree", "add", str(integration), "-b", iref, base)
        command(repo, "git", "worktree", "add", str(ticket), "-b", tref, base)
        (ticket / "payload.txt").write_text("candidate content\n")
        command(ticket, "git", "add", "payload.txt")
        command(ticket, "git", "commit", "-m", "candidate")
        candidate = command(ticket, "git", "rev-parse", "HEAD")
        command(integration, "git", "merge", "--no-ff", tref, "-m", "recorded integration intent")
        merged = command(integration, "git", "rev-parse", "HEAD")
        log = root / "integration-check.json"
        checks = [] if case == "missing-evidence" else [verify(integration, log)]
        # Minimal scenario projection, not a replacement for the product record schema.
        record = {"run_id": "fixture-08-" + case, "status": "in-review", "candidate_sha": candidate,
                  "reviewed_sha": candidate, "verdict": "PASS (manual premise)",
                  "merge_before_sha": base, "merge_after_sha": merged, "integration_checks": checks}
        if case == "older-check-sha":
            (integration / "later.txt").write_text("documented later integration commit\n")
            command(integration, "git", "add", "later.txt")
            command(integration, "git", "commit", "-m", "attributed later transaction")
        if case == "inconsistent-branch-sha":
            (ticket / "payload.txt").write_text("unexpected committed content\n")
            command(ticket, "git", "add", "payload.txt")
            command(ticket, "git", "commit", "-m", "unattributed branch advance")
            (ticket / "payload.txt").write_text("unfinished tracked evidence\n")
            (ticket / "notes.txt").write_text("unfinished untracked evidence\n")
        record_path = root / "pending-record.json"
        record_path.write_text(json.dumps(record, sort_keys=True) + "\n")
        print("pending_record=" + record_path.read_text().strip())
        current = command(integration, "git", "rev-parse", "HEAD")
        command(repo, "git", "merge-base", "--is-ancestor", candidate, current)
        command(repo, "git", "merge-base", "--is-ancestor", candidate, merged)
        branch_tip = command(ticket, "git", "rev-parse", "HEAD")
        before = retained(repo, integration, ticket)
        if case == "matching-evidence":
            assert branch_tip == candidate and checks[0]["sha"] == current
            assert json.loads(log.read_text()) == checks[0]
            print("MANUAL DECISION: matching current SHA/check/log => supplement done; no merge/dispatch")
        elif case in ("missing-evidence", "older-check-sha"):
            assert branch_tip == candidate
            assert not checks or checks[0]["sha"] != current
            print("MANUAL DECISION: no current-SHA evidence => bounded reverify; no merge/dispatch")
            fresh = verify(integration, root / "reverification.json")
            assert fresh["sha"] == current
            print("MANUAL DECISION: fresh unchanged current SHA/check/log => supplement done")
        else:
            assert branch_tip != candidate
            command(repo, "git", "merge-base", "--is-ancestor", branch_tip, current, expected=1)
            print("MANUAL DECISION: unexplainable branch SHA => failed brief, preserve dirt/refs; no reset/clean/reverify/dispatch")
        assert retained(repo, integration, ticket) == before
        assert command(repo, "git", "rev-parse", "base") == base
        assert json.loads(record_path.read_text())["status"] == "in-review"
        print("PASS: real Git facts/checks and preserved pending record; status/brief decision remains a manual rehearsal")
print("actual_finished_at_utc=" + datetime.now(timezone.utc).isoformat())
print("PASS: four fresh real Git fixtures; no production resume engine or runtime compliance claim")
