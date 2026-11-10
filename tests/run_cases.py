"""Ask every question in cases.json through Claude Code with only this plugin, and fail if a case did not use
the skill and MCP tools it should.

    python tests/run_cases.py                 every case
    python tests/run_cases.py change-trace    the named cases
    python tests/run_cases.py --out DIR       keep transcripts and summaries in DIR (default tests/results)

A case passes when the Global law server connected, one of its `skills` was used, every tool in `tools` and at
least one in `any_tools` was called, and there is an answer. Exit code 1 if any case fails. Needs the `claude`
command and network access to the hosted server; each case is one paid model run.
"""
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
PLUGIN = pathlib.Path(os.environ.get('PLUGIN_ROOT') or pathlib.Path.cwd()).resolve()
if not (PLUGIN / '.claude-plugin' / 'plugin.json').is_file():
    sys.exit('run this from a checkout of the main branch, or set PLUGIN_ROOT to one')
sys.path.insert(0, str(HERE))
from summarize import parse, summary  # noqa: E402

SERVER = 'global-law'


def run_case(case, out):
    claude = shutil.which('claude')
    if not claude:
        raise SystemExit('the `claude` command is not on PATH')
    transcript = out / f"{case['name']}.jsonl"
    with tempfile.TemporaryDirectory() as work, open(transcript, 'wb') as stdout, \
            open(out / f"{case['name']}.err", 'wb') as stderr:
        subprocess.run(
            [claude, '-p', case['question'], '--plugin-dir', str(PLUGIN), '--output-format', 'stream-json',
             '--verbose',
             '--allowedTools', 'Skill', f'mcp__plugin_{SERVER}_{SERVER}', f'mcp__plugin_{SERVER}_{SERVER}__*',
             '--disallowedTools', 'Bash', 'Write', 'Edit', 'WebSearch', 'WebFetch', 'Task'],
            cwd=work, stdin=subprocess.DEVNULL, stdout=stdout, stderr=stderr, check=False)
    run = parse(transcript)
    (out / f"{case['name']}.summary.txt").write_text(summary(run), encoding='utf-8')
    return run


def failures(case, run):
    found = []
    servers = run['servers'] or []
    if not any(SERVER in str(name) and status == 'connected' for name, status in servers):
        found.append(f'Global law server not connected: {servers}')
    if not set(case.get('skills', [])) & set(run['skills']):
        found.append(f"skill: wanted one of {case.get('skills')}, used {run['skills']}")
    missing = [tool for tool in case.get('tools', []) if tool not in run['tools']]
    if missing:
        found.append(f"tools not called: {missing} (called {sorted(set(run['tools']))})")
    if case.get('any_tools') and not set(case['any_tools']) & set(run['tools']):
        found.append(f"none of {case['any_tools']} called (called {sorted(set(run['tools']))})")
    if not run['answer'].strip():
        found.append('no answer')
    return found


def main(argv):
    out = HERE / 'results'
    if '--out' in argv:
        at = argv.index('--out')
        out = pathlib.Path(argv[at + 1])
        argv = argv[:at] + argv[at + 2:]
    out.mkdir(parents=True, exist_ok=True)
    cases = json.loads((HERE / 'cases.json').read_text(encoding='utf-8'))
    unknown = set(argv) - {case['name'] for case in cases}
    if unknown:
        raise SystemExit(f'no such case: {sorted(unknown)}')
    failed = 0
    for case in cases:
        if argv and case['name'] not in argv:
            continue
        run = run_case(case, out)
        found = failures(case, run)
        failed += bool(found)
        cost = f"${run['cost_usd']:.2f}" if run['cost_usd'] is not None else 'cost unknown'
        print(f"{'FAIL' if found else 'PASS'}  {case['name']}  ({cost})", flush=True)
        for line in found:
            print(f'      {line}')
    print(f"{failed} failed" if failed else 'all passed')
    return 1 if failed else 0


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.exit(main(sys.argv[1:]))
