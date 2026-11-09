#!/bin/bash
# Run one question through Claude Code with only this plugin (skills + the hosted Global law MCP) and record which
# skill fired, which MCP tools it called, and the answer.   tests/run_skill_test.sh <name> "<question>" <out dir>
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
PLUGIN="$(cd "$HERE/.." && pwd)"
name="$1"; question="$2"
mkdir -p "$3"; out="$(cd "$3" && pwd)"
PY=$(command -v python || command -v python3)
work=$(mktemp -d)
cd "$work"
claude -p "$question" --plugin-dir "$PLUGIN" --output-format stream-json --verbose \
  --allowedTools "Skill" "mcp__plugin_global-law_global-law" "mcp__plugin_global-law_global-law__*" \
  --disallowedTools "Bash" "Write" "Edit" "WebSearch" "WebFetch" "Task" \
  > "$out/$name.jsonl" 2> "$out/$name.err"
"$PY" "$HERE/summarize.py" "$out/$name.jsonl" > "$out/$name.summary.txt"
cd / && rm -rf "$work"
