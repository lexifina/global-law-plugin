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

Every push to `main` is picked up by the Claude directory as a new version, so raise the version with each change:
`python scripts/set_version.py X.Y.Z` writes it to every manifest and skill (`--check` confirms they agree). Add the
release to `CHANGELOG.md`, tag `vX.Y.Z` and publish a GitHub release.

## The OpenAI package

`python scripts/build_openai_zip.py --check-server` checks `openai/plugin.json` and `openai/mcp.json` against
OpenAI's limits and the live server's tools, then writes `dist/global-law-openai-<version>.zip` for upload at
platform.openai.com/plugins.

## License

Contributions are released under [CC0 1.0](LICENSE).
