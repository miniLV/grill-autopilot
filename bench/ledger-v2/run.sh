#!/usr/bin/env bash
# Run the ledger-v2 benchmark on Codex: arm A (to-tickets + implement-spec) then arm B (grill-autopilot).
# Usage: bash bench/ledger-v2/run.sh
# Env: CODEX_HOME (default ~/.codex), BENCH_ROOT (default $HOME/autopilot-bench-ledger-v2, must not exist), ARMS ("a b"),
#      MODEL (gpt-6.1-sol), EFFORT (high), SANDBOX (workspace-write).
set -euo pipefail

here="$(cd "$(dirname "$0")" && pwd)"
repo="$(cd "$here/../.." && pwd)"
bench="${BENCH_ROOT:-$HOME/autopilot-bench-ledger-v2}"
arms="${ARMS:-a b}"
model="${MODEL:-gpt-6.1-sol}"
effort="${EFFORT:-high}"
sandbox="${SANDBOX:-workspace-write}"
skill_md="$repo/skills/grill-autopilot/SKILL.md"

command -v codex >/dev/null || { echo "codex CLI not found" >&2; exit 1; }
codex_home="${CODEX_HOME:-$HOME/.codex}"
for s in grilling to-spec to-tickets tdd code-review setup-matt-pocock-skills implement-spec; do
  [ -f "$codex_home/skills/$s/SKILL.md" ] || { echo "missing companion skill: $codex_home/skills/$s" >&2; exit 1; }
done
if [ -e "$bench" ]; then
  echo "BENCH_ROOT already exists: $bench (choose a new path; nothing was changed)" >&2
  exit 1
fi

# 1. Seed repository and one clean clone per arm.
mkdir -p "$bench"
cp -R "$here/seed" "$bench/seed"
git -C "$bench/seed" init -q -b main
git -C "$bench/seed" add .
git -C "$bench/seed" -c user.name=Bench -c user.email=bench@example.invalid commit -qm "Seed ledger benchmark"
(cd "$bench/seed" && python3 -B -m unittest discover -s tests >/dev/null 2>&1) || { echo "seed baseline failed" >&2; exit 1; }
for name in arm-a-implement-spec arm-b-grill-autopilot; do
  git clone -q "$bench/seed" "$bench/$name"
  git -C "$bench/$name" remote remove origin
  git -C "$bench/$name" config user.name Bench
  git -C "$bench/$name" config user.email bench@example.invalid
done

# 2. Render prompts with this machine's absolute paths.
for f in "$here"/prompts/*.md; do
  sed -e "s|{{BENCH}}|$bench|g" -e "s|{{SKILL_MD}}|$skill_md|g" "$f" > "$bench/$(basename "$f")"
done
git -C "$repo" rev-parse HEAD > "$bench/skill-commit.txt"
date -u +%Y-%m-%dT%H:%M:%SZ > "$bench/started_at.txt"

# 3. Run each arm in its own fresh Codex session.
run_arm() {
  local key="$1" name="$2"
  echo "== arm $key: $name (started $(date -u +%H:%M:%SZ))"
  date -u +%Y-%m-%dT%H:%M:%SZ > "$bench/arm-$key-start.txt"
  set +e
  codex exec -m "$model" -c model_reasoning_effort="$effort" -s "$sandbox" \
    --add-dir "$bench" -C "$bench/$name" --json -o "$bench/arm-$key-last.md" \
    "$(cat "$bench/$name.md")" > "$bench/arm-$key-events.jsonl" 2> "$bench/arm-$key-stderr.log"
  echo $? > "$bench/arm-$key-exit.txt"
  set -e
  date -u +%Y-%m-%dT%H:%M:%SZ > "$bench/arm-$key-end.txt"
  echo "== arm $key finished, exit $(cat "$bench/arm-$key-exit.txt")"
}
for key in $arms; do
  case "$key" in
    a) run_arm a arm-a-implement-spec ;;
    b) run_arm b arm-b-grill-autopilot ;;
    *) echo "unknown arm: $key" >&2; exit 1 ;;
  esac
done

# 4. Collect token usage, git history and briefs into the repo.
out="$repo/docs/verification/codex-bench-ledger-v2/$(hostname -s)-$(date -u +%Y%m%dT%H%M%SZ)"
python3 "$here/collect.py" "$bench" "$out" "$repo/tools/context-report.py"
echo
echo "Results: $out"
echo "Next: git -C \"$repo\" add \"$out\" && git -C \"$repo\" commit -m \"bench: ledger-v2 codex results\" && git -C \"$repo\" push"
