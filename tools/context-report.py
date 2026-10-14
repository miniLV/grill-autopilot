#!/usr/bin/env python3
"""Report how a session's main-window context grows, turn by turn.

Usage:
  python3 context-report.py <claude-session.jsonl | codex-rollout.jsonl>

Claude Code transcripts: ~/.claude/projects/<project>/<session-id>.jsonl
  (subagent transcripts in <session-id>/subagents/ are summarised separately)
Codex rollouts: ~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl
"""
import json
import sys
from pathlib import Path

BARS = " ▁▂▃▄▅▆▇█"


def read_jsonl(path):
    with open(path, encoding="utf-8") as f:
        for line in f:
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue


def claude_turns(path):
    """Context size per API call: input + cache writes + cache reads."""
    seen, turns, cached = set(), [], 0
    for rec in read_jsonl(path):
        if rec.get("type") != "assistant" or rec.get("isSidechain"):
            continue
        msg = rec.get("message", {})
        usage, key = msg.get("usage"), msg.get("id") or rec.get("requestId")
        if not usage or key in seen:
            continue
        seen.add(key)
        read = usage.get("cache_read_input_tokens", 0)
        turns.append(usage.get("input_tokens", 0) + usage.get("cache_creation_input_tokens", 0) + read)
        cached += read
    return turns, cached


def codex_turns(path):
    turns, cached, window = [], 0, None
    for rec in read_jsonl(path):
        payload = rec.get("payload") or {}
        if payload.get("type") != "token_count" or not payload.get("info"):
            continue
        last = payload["info"].get("last_token_usage") or {}
        if last.get("input_tokens"):
            turns.append(last["input_tokens"])
            cached += last.get("cached_input_tokens", 0)
        window = payload["info"].get("model_context_window", window)
    return turns, cached, window


def sparkline(values, width=48):
    if not values:
        return ""
    step = max(1, len(values) // width)
    sampled = [max(values[i:i + step]) for i in range(0, len(values), step)]
    top = max(sampled) or 1
    return "".join(BARS[round(v / top * (len(BARS) - 1))] for v in sampled)


def k(n):
    return f"{n / 1000:,.1f}K"


def report(label, turns, cached, window=None):
    if not turns:
        print(f"{label}: no token usage found")
        return
    total = sum(turns)
    print(f"{label}")
    print(f"  turns            {len(turns)}")
    print(f"  context start    {k(turns[0])}")
    print(f"  context peak     {k(max(turns))}" + (f"  ({max(turns) / window:.0%} of {k(window)})" if window else ""))
    print(f"  context final    {k(turns[-1])}")
    print(f"  input sent total {k(total)}  (cache reads {cached / total:.0%})")
    print(f"  growth           {sparkline(turns)}")


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    path = Path(sys.argv[1]).expanduser()
    if "rollout-" in path.name:
        turns, cached, window = codex_turns(path)
        report(f"Codex session {path.name}", turns, cached, window)
        return
    turns, cached = claude_turns(path)
    report(f"Main window  {path.name}", turns, cached)
    sub_dir = path.with_suffix("") / "subagents"
    subs = sorted(sub_dir.glob("*.jsonl")) if sub_dir.is_dir() else []
    if subs:
        print(f"\nSubagents ({len(subs)}), context that stayed out of the main window:")
        for sub in subs:
            sub_turns = [t for t in _all_turns(sub)]
            if sub_turns:
                print(f"  {sub.stem:<28} turns {len(sub_turns):>4}  peak {k(max(sub_turns)):>9}  sent {k(sum(sub_turns)):>10}")


def _all_turns(path):
    """Subagent transcripts mark every record as a sidechain, so read them all."""
    seen = set()
    for rec in read_jsonl(path):
        msg = rec.get("message", {}) if rec.get("type") == "assistant" else {}
        usage, key = msg.get("usage"), msg.get("id") or rec.get("requestId")
        if usage and key not in seen:
            seen.add(key)
            yield usage.get("input_tokens", 0) + usage.get("cache_creation_input_tokens", 0) + usage.get("cache_read_input_tokens", 0)


if __name__ == "__main__":
    main()
