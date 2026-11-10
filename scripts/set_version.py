"""Set the plugin's version in every file that states it, or check that they agree.

    python scripts/set_version.py 1.2.3     write 1.2.3 everywhere
    python scripts/set_version.py --check   exit 1 unless every file states the same version
"""
import json
import os
import pathlib
import re
import sys

# The plugin is a checkout of the main branch: PLUGIN_ROOT, or the folder the script is run from.
ROOT = pathlib.Path(os.environ.get('PLUGIN_ROOT') or pathlib.Path.cwd()).resolve()
if not (ROOT / '.claude-plugin' / 'plugin.json').is_file():
    sys.exit('run this from a checkout of the main branch, or set PLUGIN_ROOT to one')
JSON_FILES = ['.claude-plugin/plugin.json', '.cursor-plugin/plugin.json', '.codex-plugin/plugin.json',
              '.grok-plugin/plugin.json', 'gemini-extension.json', 'openai/plugin.json']
MARKETPLACE = '.claude-plugin/marketplace.json'
SKILLS = sorted(str(p.relative_to(ROOT)).replace('\\', '/') for p in (ROOT / 'skills').glob('*/SKILL.md'))
SKILL_VERSION = re.compile(r'^(  version: ")([^"]+)(")$', re.M)


def read(path):
    return (ROOT / path).read_text(encoding='utf-8').replace('\r\n', '\n')


def versions():
    found = {path: json.loads(read(path))['version'] for path in JSON_FILES}
    market = json.loads(read(MARKETPLACE))
    found[MARKETPLACE + ' (plugin)'] = market['plugins'][0]['version']
    found[MARKETPLACE + ' (metadata)'] = market['metadata']['version']
    for path in SKILLS:
        match = SKILL_VERSION.search(read(path))
        found[path] = match.group(2) if match else None
    return found


def write(new):
    for path in JSON_FILES + [MARKETPLACE]:
        text = read(path)
        old_values = set(re.findall(r'"version": "([^"]+)"', text))
        for old in old_values:
            text = text.replace(f'"version": "{old}"', f'"version": "{new}"')
        (ROOT / path).write_text(text, encoding='utf-8', newline='\n')
    for path in SKILLS:
        (ROOT / path).write_text(SKILL_VERSION.sub(rf'\g<1>{new}\g<3>', read(path)), encoding='utf-8', newline='\n')


def main(argv):
    if argv == ['--check']:
        found = versions()
        if len(set(found.values())) != 1:
            for path, version in found.items():
                print(f'{version}  {path}')
            print('versions differ: run python scripts/set_version.py <version>')
            return 1
        print(f'every file states {next(iter(found.values()))}')
        return 0
    if len(argv) != 1 or not re.fullmatch(r'\d+\.\d+\.\d+', argv[0]):
        print(__doc__)
        return 2
    write(argv[0])
    return main(['--check'])


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
