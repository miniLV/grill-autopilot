"""Read-only CLI syntax capture, not a model dispatch or lifecycle test."""
from datetime import datetime, timezone
from pathlib import Path
import subprocess

COMMANDS = [
    ['codex', '--version'], ['codex', 'exec', '--help'],
    ['codex', 'exec', 'resume', '--help'], ['claude', '--version'],
    ['claude', '--help'], ['claude', 'agents', '--help'],
    ['claude', 'logs', '--help'], ['claude', 'stop', '--help'],
    ['claude', 'rm', '--help'],
]
print('Read-only CLI syntax evidence; no model dispatch, process stop or session deletion performed.')
print('Output normalization: trailing whitespace removed; remaining help text preserved.')
print('Client date for retained capture: 2026-10-14 Asia/Shanghai; actual command times follow in UTC.')
for command in COMMANDS:
    print(f'\nUTC: {datetime.now(timezone.utc).isoformat()}\nCwd: {Path.cwd()}\nCommand: {" ".join(command)}', flush=True)
    result = subprocess.run(command, capture_output=True, text=True, timeout=30)
    output = '\n'.join(line.rstrip() for line in (result.stdout + result.stderr).splitlines())
    print(f'Exit: {result.returncode}\n{output}', flush=True)
    if result.returncode:
        raise SystemExit(result.returncode)
