# Contributing

This repository holds the packaging and the skills. The law itself is in
[lexifina/global-law](https://github.com/lexifina/global-law); report a wrong or missing text there.

## Tooling

The scripts and tests are on the `tooling` branch, because `main` holds only what an AI app installs (Markdown,
JSON, YAML and images). Check it out beside this branch and run the scripts from here:

```sh
git worktree add ../global-law-plugin-tooling tooling
```

## Changing a skill

1. Edit the `SKILL.md` under `skills/`. Each skill must work on its own, so keep its rules in the file.
2. Rebuild the Gemini CLI context file: `python ../global-law-plugin-tooling/scripts/build_gemini_md.py`. Do not edit `GEMINI.md` by hand.
3. Check the plugin: `claude plugin validate .`
4. Run the tests: `python ../global-law-plugin-tooling/tests/run_cases.py` (each case is one paid Claude Code run
   against the hosted server). Add a case to `tests/cases.json` on the `tooling` branch for a new behaviour.

Name only tools the server has. `tools/list` on `https://global-law.lexifina.com/mcp` gives the current set.

## Releasing

Every push to `main` is picked up by the Claude directory as a new version, so raise the version with each change:
`python ../global-law-plugin-tooling/scripts/set_version.py X.Y.Z` writes it to every manifest and skill
(`--check` confirms they agree). Add the release to `CHANGELOG.md`, tag `vX.Y.Z` and publish a GitHub release.

## The OpenAI package

`python ../global-law-plugin-tooling/scripts/build_openai_zip.py --check-server` checks `openai/plugin.json` and `openai/mcp.json` against
OpenAI's limits and the live server's tools, then writes `dist/global-law-openai-<version>.zip` for upload at
platform.openai.com/plugins.

## License

Contributions are released under [CC0 1.0](LICENSE).
