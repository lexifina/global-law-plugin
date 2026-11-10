"""Build GEMINI.md (the Gemini CLI context file) from the three skills, so it cannot drift from them.

    python scripts/build_gemini_md.py           write GEMINI.md
    python scripts/build_gemini_md.py --check   exit 1 if GEMINI.md is out of date

GEMINI.md is the global-law skill's body, then the other two skills' bodies one heading level down, without
their "Rules" section (the global-law body already states those rules).
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
MAIN = 'global-law'
OTHERS = ['law-change-trace', 'citation-check']
NOTE = '<!-- Generated from skills/ by scripts/build_gemini_md.py. Edit the skills, then run it. -->\n\n'


def body(skill):
    text = (ROOT / 'skills' / skill / 'SKILL.md').read_text(encoding='utf-8').replace('\r\n', '\n')
    match = re.match(r'---\n.*?\n---\n', text, re.S)
    if not match:
        raise SystemExit(f'skills/{skill}/SKILL.md has no frontmatter')
    return text[match.end():].strip() + '\n'


def without_section(text, heading):
    return re.sub(rf'^## {re.escape(heading)}\n.*?(?=^## |\Z)', '', text, flags=re.S | re.M)


def demoted(text):
    return re.sub(r'^(#+) ', r'#\1 ', text, flags=re.M)


def build():
    parts = [NOTE + body(MAIN)]
    for skill in OTHERS:
        parts.append(demoted(without_section(body(skill), 'Rules')).strip() + '\n')
    return '\n'.join(parts)


def main():
    target = ROOT / 'GEMINI.md'
    wanted = build()
    if '--check' in sys.argv[1:]:
        current = target.read_text(encoding='utf-8').replace('\r\n', '\n') if target.exists() else ''
        if current != wanted:
            print('GEMINI.md is out of date: run python scripts/build_gemini_md.py')
            return 1
        print('GEMINI.md is up to date')
        return 0
    target.write_text(wanted, encoding='utf-8', newline='\n')
    print('wrote GEMINI.md')
    return 0


if __name__ == '__main__':
    sys.exit(main())
