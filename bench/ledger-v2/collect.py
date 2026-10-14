#!/usr/bin/env python3
"""Collect ledger-v2 benchmark results without copying raw transcripts.

Usage: collect.py <bench-root> <output-dir> <context-report.py>

Writes per arm: token usage by model (from ~/.codex/sessions rollouts whose cwd is
inside that arm or its worktrees), the final message, a git bundle of every ref,
the git graph, the tracker files under .scratch/, and context reports.
"""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ARMS = {"a": "arm-a-implement-spec", "b": "arm-b-grill-autopilot"}
FIELDS = ["input_tokens", "cached_input_tokens", "output_tokens", "reasoning_output_tokens"]


def read_text(path):
    return path.read_text().strip() if path.exists() else None


def arm_for(cwds):
    for key, name in ARMS.items():
        if any(name in c for c in cwds):
            return key
    return None


def scan_rollout(path, bench):
    """Return (arm, summary) for a rollout inside the bench, else (None, None)."""
    cwds, models, usage = set(), {}, {}
    model = "unknown"
    first = last = None
    meta = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            ts = rec.get("timestamp")
            first, last = first or ts, ts or last
            kind, p = rec.get("type"), rec.get("payload") or {}
            if kind == "session_meta":
                cwds.add(p.get("cwd", ""))
                meta = {"id": p.get("id"), "source": p.get("source"), "thread_source": p.get("thread_source")}
            elif kind == "turn_context":
                cwds.add(p.get("cwd", ""))
                model = p.get("model") or model
                models[model] = p.get("effort")
            elif kind == "token_usage_record":
                u = p.get("usage") or {}
                bucket = usage.setdefault(model, dict.fromkeys(FIELDS, 0))
                for k in FIELDS:
                    bucket[k] += u.get(k, 0)
    if not any(c.startswith(str(bench)) for c in cwds):
        return None, None
    return arm_for(cwds), {"file": path.name, "cwds": sorted(cwds), "models": models,
                           "usage": usage, "first": first, "last": last, **meta}


def collect_sessions(bench, since):
    found = {k: [] for k in ARMS}
    root = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")) / "sessions"
    for path in sorted(root.rglob("rollout-*.jsonl")):
        if path.stat().st_mtime < since:
            continue
        arm, summary = scan_rollout(path, bench)
        if arm:
            summary["path"] = str(path)
            found[arm].append(summary)
    return found


def totals(sessions):
    out = {}
    for s in sessions:
        for model, u in s["usage"].items():
            bucket = out.setdefault(model, dict.fromkeys(FIELDS, 0))
            for k in FIELDS:
                bucket[k] += u[k]
    return out


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True).stdout


def main():
    bench, out, context_report = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    out.mkdir(parents=True)
    started = (bench / "started_at.txt").stat().st_mtime - 60
    sessions = collect_sessions(bench, started)
    summary = {"skill_commit": read_text(bench / "skill-commit.txt"), "arms": {}}
    for key, name in ARMS.items():
        arm_dir, arm_out = bench / name, out / name
        if not (bench / f"arm-{key}-start.txt").exists():
            continue
        arm_out.mkdir()
        for suffix in ["last.md", "stderr.log"]:
            src = bench / f"arm-{key}-{suffix}"
            if src.exists():
                shutil.copy(src, arm_out / suffix)
        git(arm_dir, "bundle", "create", str(arm_out / "repo.bundle"), "--all")
        (arm_out / "git-graph.txt").write_text(git(arm_dir, "log", "--all", "--oneline", "--graph"))
        if (arm_dir / ".scratch").exists():
            shutil.copytree(arm_dir / ".scratch", arm_out / "scratch")
        main_sessions = [s for s in sessions[key] if s.get("cwds") == [str(arm_dir)]]
        for i, s in enumerate(main_sessions):
            report = subprocess.run([sys.executable, str(context_report), s["path"]], capture_output=True, text=True)
            (arm_out / f"context-report-{i}.txt").write_text(report.stdout + report.stderr)
        for s in sessions[key]:
            s.pop("path", None)
        summary["arms"][name] = {
            "start": read_text(bench / f"arm-{key}-start.txt"),
            "end": read_text(bench / f"arm-{key}-end.txt"),
            "exit": read_text(bench / f"arm-{key}-exit.txt"),
            "sessions": len(sessions[key]),
            "tokens_by_model": totals(sessions[key]),
            "session_details": sessions[key],
        }
    (out / "summary.json").write_text(json.dumps(summary, indent=2))
    for name, arm in summary["arms"].items():
        print(f"{name}: exit {arm['exit']}, {arm['sessions']} sessions, {arm['start']} -> {arm['end']}")
        for model, u in arm["tokens_by_model"].items():
            print(f"  {model}: " + ", ".join(f"{k}={v:,}" for k, v in u.items()))


if __name__ == "__main__":
    main()
