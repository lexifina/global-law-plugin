"""Summarise a `claude -p --output-format stream-json` transcript: MCP status, skills, tool calls, answer."""
import json
import sys
sys.stdout.reconfigure(encoding="utf-8")

tools, skills, result, servers = [], [], '', None
for line in open(sys.argv[1], encoding='utf-8'):
    try:
        e = json.loads(line)
    except ValueError:
        continue
    if e.get('type') == 'system' and e.get('subtype') == 'init':
        servers = [(s.get('name'), s.get('status')) for s in e.get('mcp_servers', [])]
    content = (e.get('message') or {}).get('content')
    for block in content if isinstance(content, list) else []:
        if block.get('type') == 'tool_use':
            name = block.get('name') or ''
            args = block.get('input') or {}
            if name == 'Skill':
                skills.append(args.get('skill') or args.get('command'))
            else:
                tools.append(name.split('__')[-1] + ' ' + json.dumps(args, ensure_ascii=False)[:110])
    if e.get('type') == 'result':
        result = e.get('result') or ''
        cost = e.get('total_cost_usd')
        turns = e.get('num_turns')
print('MCP servers:', servers)
print('Skills used:', skills)
print('Tool calls:')
for t in tools:
    print('  ', t)
print('--- answer ---')
print(result)
