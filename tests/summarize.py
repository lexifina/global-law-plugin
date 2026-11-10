"""Summarise a `claude -p --output-format stream-json` transcript: MCP status, skills, tool calls, answer."""
import json
import sys


def parse(path):
    """The facts of one transcript: MCP servers, skills used, MCP tool calls, answer, cost, model invocations."""
    run = {'servers': None, 'skills': [], 'tools': [], 'calls': [], 'answer': '', 'cost_usd': None,
           'model_invocation_count': None}
    for line in open(path, encoding='utf-8'):
        try:
            e = json.loads(line)
        except ValueError:
            continue
        if not isinstance(e, dict):
            continue
        if e.get('type') == 'system' and e.get('subtype') == 'init':
            run['servers'] = [(s.get('name'), s.get('status')) for s in e.get('mcp_servers', [])]
        message = e.get('message')
        content = message.get('content') if isinstance(message, dict) else None
        for block in content if isinstance(content, list) else []:
            if block.get('type') == 'tool_use':
                name = block.get('name') or ''
                args = block.get('input') or {}
                if name == 'Skill':
                    run['skills'].append(str(args.get('skill') or args.get('command') or '').split(':')[-1])
                else:
                    tool = name.split('__')[-1]
                    run['tools'].append(tool)
                    run['calls'].append(tool + ' ' + json.dumps(args, ensure_ascii=False)[:110])
        if e.get('type') == 'result':
            run['answer'] = e.get('result') or ''
            run['cost_usd'] = e.get('total_cost_usd')
            run['model_invocation_count'] = e.get('num_turns')
    return run


def summary(run):
    lines = [f"MCP servers: {run['servers']}", f"Skills used: {run['skills']}", 'Tool calls:']
    lines += ['   ' + call for call in run['calls']]
    cost = run['cost_usd']
    lines.append(f"Cost: {'$%.4f' % cost if cost is not None else 'unknown'}"
                 f"   Model invocations: {run['model_invocation_count']}")
    lines += ['--- answer ---', run['answer']]
    return '\n'.join(lines)


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    print(summary(parse(sys.argv[1])))
