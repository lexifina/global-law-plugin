# Contributing

This repository holds the packaging and the skills. The law itself is in
[lexifina/global-law](https://github.com/lexifina/global-law); report a wrong or missing text there.

## Changing a skill

1. Edit the `SKILL.md` under `skills/`. Each skill must work on its own, so keep its rules in the file.
2. Rebuild the Gemini CLI context file: `python scripts/build_gemini_md.py`. Do not edit `GEMINI.md` by hand.
3. Check the plugin: `claude plugin validate .`
4. Run the tests: `python tests/run_cases.py` (each case is one paid Claude Code run against the hosted
   server). Add a case to `tests/cases.json` for a new behaviour.

Name only tools the server has. `tools/list` on `https://global-law.lexifina.com/mcp` gives the current set.

## Releasing

The version is written in `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` (twice),
`.cursor-plugin/plugin.json`, `gemini-extension.json` and each `SKILL.md`. Change all of them together, add
the release to `CHANGELOG.md`, tag `vX.Y.Z` and publish a GitHub release.

## License

Contributions are released under [CC0 1.0](LICENSE).
