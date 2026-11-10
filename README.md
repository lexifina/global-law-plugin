# Global law plugin: tooling

Scripts and tests for [the Global law plugin](https://github.com/lexifina/global-law-plugin). They live on this
branch because the plugin's `main` branch holds only what an AI app installs: Markdown, JSON, YAML and images.

Check this branch out next to a checkout of `main`, then run the scripts from the `main` checkout (or set
`PLUGIN_ROOT` to it):

```sh
git worktree add ../global-law-plugin-tooling tooling
python ../global-law-plugin-tooling/scripts/set_version.py --check
```

| Script | What it does |
|---|---|
| `scripts/set_version.py X.Y.Z` | Writes the version to every manifest and skill; `--check` confirms they agree |
| `scripts/build_gemini_md.py` | Rebuilds `GEMINI.md` from the three skills; `--check` confirms it is current |
| `scripts/build_openai_zip.py` | Checks `openai/plugin.json` and `openai/mcp.json`, then writes the OpenAI upload ZIP to `dist/`; `--check-server` also checks the live server's tools |
| `tests/run_cases.py` | Asks each question in `tests/cases.json` through Claude Code with only the plugin, and fails if the expected skill or MCP tools were not used. Each case is one paid Claude Code run |

Released under [CC0 1.0](LICENSE).
