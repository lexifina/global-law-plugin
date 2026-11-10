"""Check the OpenAI (ChatGPT and Codex directory) package and build its upload ZIP.

    python scripts/build_openai_zip.py                 check, then write dist/global-law-openai-<version>.zip
    python scripts/build_openai_zip.py --check-server  also ask the live server for its tools and check them

The ZIP holds openai/plugin.json and openai/mcp.json at its root (the portable Agent Plugins layout OpenAI's
portal takes), with skills/, README.md, LICENSE and the icon. The other clients' manifests are left out.
Limits follow OpenAI's plugin submission reference as of November 2026.
"""
import json
import pathlib
import re
import struct
import sys
import urllib.request
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
SOURCE = ROOT / 'openai'
ICON = ROOT / '.claude-plugin' / 'icon.png'
# The category titles the portal accepts (read from platform.openai.com/plugins, November 2026).
CATEGORIES = {'Business', 'Collaboration', 'Design', 'Developer Tools', 'Education', 'Entertainment', 'Finance',
              'Food', 'Lifestyle', 'News', 'Productivity', 'Shopping', 'Travel'}
PRICING = re.compile(r'(free|pricing|price|subscription|discount|trial)', re.I)
problems = []


def check(condition, message):
    if not condition:
        problems.append(message)


def png_size(path):
    head = path.read_bytes()[:24]
    check(head[:8] == b'\x89PNG\r\n\x1a\n', f'{path.name} is not a PNG')
    return struct.unpack('>II', head[16:24])


def contrast(foreground, background):
    def luminance(colour):
        channels = [int(colour[i:i + 2], 16) / 255 for i in (1, 3, 5)]
        r, g, b = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
        return 0.2126 * r + 0.7152 * g + 0.0722 * b
    lighter, darker = sorted((luminance(foreground), luminance(background)), reverse=True)
    return (lighter + 0.05) / (darker + 0.05)


def live_tools(url):
    body = json.dumps({'jsonrpc': '2.0', 'id': 1, 'method': 'tools/list'}).encode()
    request = urllib.request.Request(url, data=body, method='POST', headers={
        'Content-Type': 'application/json', 'Accept': 'application/json, text/event-stream',
        'User-Agent': 'global-law-plugin-check/1.0'})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read())['result']['tools']


def check_package(manifest, servers, check_server):
    name = manifest.get('name', '')
    check(re.fullmatch(r'[a-z0-9]+(-[a-z0-9]+)*', name) and len(name) <= 64, 'name: lowercase, hyphens, up to 64')
    check(re.fullmatch(r'\d+\.\d+\.\d+', manifest.get('version', '')), 'version: a semantic version')
    claude = json.loads((ROOT / '.claude-plugin' / 'plugin.json').read_text(encoding='utf-8'))
    check(manifest.get('version') == claude.get('version'), 'openai/plugin.json: same version as .claude-plugin/plugin.json')
    check(len(manifest.get('description', '')) <= 4000, 'description: up to 4000 characters')
    openai = manifest.get('extensions', {}).get('com.openai', {})
    interface = openai.get('interface', {})
    for field, limit in (('displayName', 30), ('shortDescription', 30), ('longDescription', 4000), ('developerName', 80)):
        check(interface.get(field) and len(interface[field]) <= limit, f'interface.{field}: required, up to {limit}')
    check(interface.get('category') in CATEGORIES, 'interface.category: one of the categories the portal accepts')
    check(not PRICING.search(manifest.get('description', '')), 'description: no pricing words (the portal rejects them)')
    check(not PRICING.search(interface.get('longDescription', '')), 'interface.longDescription: no pricing words (the portal rejects them)')
    capabilities = interface.get('capabilities', [])
    check(0 < len(capabilities) <= 20 and all(len(item) <= 120 for item in capabilities),
          'interface.capabilities: 1 to 20, each up to 120 characters')
    for field in ('websiteURL', 'supportURL', 'privacyPolicyURL', 'termsOfServiceURL'):
        value = interface.get(field, '')
        check(value.startswith('https://') and len(value) <= 1024, f'interface.{field}: an HTTPS URL')
    prompts = interface.get('defaultPrompt', [])
    check(len(prompts) <= 3 and len(set(prompts)) == len(prompts) and all(len(p) <= 128 and '@' not in p for p in prompts),
          'interface.defaultPrompt: up to 3 unique prompts, 128 characters each, no @')
    colour = interface.get('brandColor')
    if colour:
        check(re.fullmatch(r'#[0-9A-Fa-f]{6}', colour) and contrast(colour, '#FFFFFF') >= 2, 'interface.brandColor: #RRGGBB, 2:1 on white')
    width, height = png_size(ICON)
    check(width == height and 48 <= width <= 4096 and ICON.stat().st_size <= 5 * 1024 * 1024, 'icon: square, 48 to 4096 px, up to 5 MiB')
    for field in ('logo', 'composerIcon'):
        check(interface.get(field) in ('./assets/logo.png', './assets/icon.png'), f'interface.{field}: ./assets/logo.png or ./assets/icon.png')
    skills = sorted((ROOT / 'skills').glob('*/SKILL.md'))
    check(skills, 'at least one skill')
    for skill in skills:
        text = skill.read_text(encoding='utf-8')
        skill_name = re.search(r'^name: (\S+)$', text, re.M)
        check(skill_name and len(f'{name}:{skill_name.group(1)}') <= 64, f'{skill.parent.name}: plugin:skill name up to 64')
        description = re.search(r'^description: >\n((?:  .*\n)+)', text, re.M)
        check(description and len(' '.join(description.group(1).split())) <= 1024, f'{skill.parent.name}: description up to 1024')
    review = openai.get('review', {})
    tests = review.get('test_cases', {})
    positive, negative = tests.get('positive', []), tests.get('negative', [])
    check(len(positive) == 5, 'review.test_cases.positive: exactly five')
    check(len(negative) == 3, 'review.test_cases.negative: exactly three')
    for case in positive:
        check(all(case.get(f) for f in ('description', 'prompt', 'tools_triggered', 'expected_behavior')),
              f"positive case {case.get('description')!r}: all four fields")
    for case in negative:
        check(case.get('description') and case.get('prompt'), 'each negative case: description and prompt')
    check(not {'test_credentials', 'reviewer_instructions'} & set(review), 'reviewer credentials never go in the package')
    check('hooks' not in openai and 'apps' not in openai, 'no hooks or app references in a submitted package')
    check(len(servers) == 1, 'mcp.json: exactly one server')
    for server in servers.values():
        check(server.get('type') == 'streamable-http' and server.get('url', '').startswith('https://'), 'mcp.json: streamable-http over HTTPS')
        check(not server.get('headers'), 'mcp.json: no headers')
        check(server.get('extensions', {}).get('com.openai', {}).get('auth', {}).get('type') == 'none', 'mcp.json: auth none')
        if check_server:
            tools = live_tools(server['url'])
            names = {tool['name'] for tool in tools}
            for case in positive:
                wanted = {item.strip() for item in case.get('tools_triggered', '').split(',')}
                check(wanted <= names, f"positive case {case.get('description')!r} names tools the server lacks: {sorted(wanted - names)}")
            for tool in tools:
                hints = tool.get('annotations') or {}
                missing = [h for h in ('readOnlyHint', 'destructiveHint', 'openWorldHint') if not isinstance(hints.get(h), bool)]
                check(not missing, f"{tool['name']}: no explicit {', '.join(missing)}")
                check(tool.get('description'), f"{tool['name']}: no description")


def main(argv):
    manifest = json.loads((SOURCE / 'plugin.json').read_text(encoding='utf-8'))
    servers = json.loads((SOURCE / 'mcp.json').read_text(encoding='utf-8')).get('mcpServers', {})
    check_package(manifest, servers, '--check-server' in argv)
    if problems:
        print('\n'.join(problems))
        return 1
    dist = ROOT / 'dist'
    dist.mkdir(exist_ok=True)
    target = dist / f"global-law-openai-{manifest['version']}.zip"
    with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED) as archive:
        archive.write(SOURCE / 'plugin.json', 'plugin.json')
        archive.write(SOURCE / 'mcp.json', 'mcp.json')
        archive.write(ROOT / 'README.md', 'README.md')
        archive.write(ROOT / 'LICENSE', 'LICENSE')
        archive.write(ICON, 'assets/icon.png')
        archive.write(ICON, 'assets/logo.png')
        for skill in sorted((ROOT / 'skills').glob('*/SKILL.md')):
            archive.write(skill, f'skills/{skill.parent.name}/SKILL.md')
    print(f'wrote {target.relative_to(ROOT)} ({target.stat().st_size // 1024} KiB)')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
