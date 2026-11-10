# Changelog

## 1.2.1 (2026-11-10)

- README: what the plugin sends and what the server keeps, with the privacy policy's Global law section and a
  support address.

## 1.2.0 (2026-11-10)

- Codex: `.codex-plugin/plugin.json` and a Codex marketplace file (`.agents/plugins/marketplace.json`).
- Grok Build: `.grok-plugin/plugin.json`.
- Cursor: the manifest names its skills, commands and server file, and has a display name.
- Commands: `law-on-date`, `law-changes`, `check-citations`, `law-for-case`.
- README: install buttons for Cursor and VS Code, and a 30-second film of an answer.
- The packaged server addresses carry `?client=...`, so usage can be counted by packaging.

## 1.1.0 (2026-11-10)

- Skills now use three more server tools: `list_provisions` (browse an act or a code), `what_else_changes`
  (what cites a provision or uses its definitions) and `world_on_date` (the last change in force in each
  jurisdiction on a date).
- `law-change-trace` and `citation-check` state their own rules, so each works when installed on its own.
- When the server's tools are missing, the skills first ask for the plugin to be enabled or reinstalled, and
  give the `claude mcp add` command only for a skill copied without the plugin.
- `GEMINI.md` is built from all three skills (`scripts/build_gemini_md.py`), so the Gemini CLI extension has
  the change-trace and citation-check guidance too.
- Tests: `tests/run_cases.py` runs the questions in `tests/cases.json` and fails when the expected skill or
  tools were not used.

## 1.0.0 (2026-11-10)

- First release: the `global-law`, `law-change-trace` and `citation-check` skills with the hosted Global law
  MCP server, packaged for Claude Code, Cursor, Gemini CLI and Cline.
