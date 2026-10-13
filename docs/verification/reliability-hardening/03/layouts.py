#!/usr/bin/env python3
"""Build four synthetic installation layouts and print facts for manual review.

This does not resolve/select companions, read product docs, or test a scheduler.
"""
import hashlib
import json
import pathlib
import shlex
import subprocess
import tempfile


skills = ("grilling", "to-spec", "to-tickets", "tdd", "code-review", "setup-matt-pocock-skills")
helpers = ("tdd/tests.md", "tdd/mocking.md", "setup-matt-pocock-skills/issue-tracker-local.md", "setup-matt-pocock-skills/triage-labels.md")


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    print(f"WRITE {path}: {text!r}")


def installed(root, names=skills, missing=()):
    for name in names:
        write(root / name / "SKILL.md", f"# Synthetic {name}\nLayout-only payload; semantic eligibility is stipulated for this rehearsal.\n")
    for name in helpers:
        if name not in missing and name.split("/")[0] in names:
            write(root / name, f"# Synthetic helper {name}\n")


def inventory(root):
    facts = {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
             for p in sorted(root.rglob("*.md"))}
    print("INVENTORY " + str(root) + " " + json.dumps(facts, sort_keys=True))


def command(cwd, *args):
    print(f"$ (cwd={cwd}) " + shlex.join(args), flush=True)
    result = subprocess.run(args, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print(result.stdout.rstrip())
    print(f"exit={result.returncode}")
    result.check_returncode()
    return result.stdout.strip()


with tempfile.TemporaryDirectory(prefix="autopilot-companions-") as temporary:
    root = pathlib.Path(temporary).resolve()
    print("CASE 1: six entries split across two incomplete project roots")
    first, second = root / "split/project/plugin-a/skills", root / "split/project/plugin-b/skills"
    installed(first, skills[:3])
    installed(second, skills[3:])
    inventory(first)
    inventory(second)

    print("\nCASE 2: plugin set missing local-tracker helper")
    missing = root / "missing/project/plugin/skills"
    installed(missing, missing=("setup-matt-pocock-skills/issue-tracker-local.md",))
    inventory(missing)

    print("\nCASE 3: two complete same-priority project plugin sets with different content")
    first, second = root / "ambiguous/project/plugin-a/skills", root / "ambiguous/project/plugin-b/skills"
    installed(first)
    installed(second)
    write(second / "grilling/SKILL.md", "# Synthetic grilling\nDifferent layout-only payload; eligibility remains stipulated.\n")
    inventory(first)
    inventory(second)

    print("\nCASE 4: selected set's helper content drifts while source commit stays fixed")
    selected = root / "drift/user/plugin/skills"
    installed(selected)
    command(selected, "git", "init", "-b", "source")
    command(selected, "git", "config", "user.name", "Layout rehearsal")
    command(selected, "git", "config", "user.email", "experiment@example.invalid")
    command(selected, "git", "config", "commit.gpgSign", "false")
    command(selected, "git", "config", "core.hooksPath", "/dev/null")
    command(selected, "git", "add", ".")
    command(selected, "git", "commit", "-m", "synthetic companion source")
    frozen = root / "drift/run/snapshots"
    write(frozen / "spec.md", "# Frozen spec\n")
    write(frozen / "ticket.md", "# Frozen task\n")
    print("BEFORE source commit and content:")
    command(selected, "git", "rev-parse", "HEAD")
    inventory(selected)
    inventory(frozen)
    write(selected / "tdd/tests.md", "# Synthetic helper tdd/tests.md\nChanged before resume.\n")
    print("AFTER source commit and content (intentionally preserved):")
    command(selected, "git", "rev-parse", "HEAD")
    command(selected, "git", "status", "--short")
    inventory(selected)
    inventory(frozen)

print("Fixture construction/inspection complete (exit 0). Decisions require manual protocol review; no automatic resolver verdict.")
