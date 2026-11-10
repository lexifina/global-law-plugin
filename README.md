**The law itself: [lexifina/global-law](https://github.com/lexifina/global-law)** (the record this plugin reads; public domain, CC0) · **REST API: [lexifina.com/api/global-law](https://lexifina.com/api/global-law)**

<img src="assets/logo-400.png" alt="Global law" width="96">

# Global law plugin

The hosted **Global law** MCP server, packaged for Claude Code, Codex, Cursor, Gemini CLI and Grok Build, with skills that answer legal questions from the **Global law** record: the
law of about 200 countries kept as a dated history. Every change is dated the day it took effect and
names the law that made it, so any provision can be read as it stood on any date, with a link to the
official text.

The skills use the hosted **Global law MCP server** at `https://global-law.lexifina.com/mcp`. It needs no
account, no key and no download.

[![Install in Cursor](https://img.shields.io/badge/Install_in-Cursor-000000)](https://cursor.com/en/install-mcp?name=global-law&config=eyJ1cmwiOiJodHRwczovL2dsb2JhbC1sYXcubGV4aWZpbmEuY29tL21jcD9jbGllbnQ9Y3Vyc29yLWJ1dHRvbiJ9)
[![Install in VS Code](https://img.shields.io/badge/Install_in-VS_Code-007ACC)](https://vscode.dev/redirect/mcp/install?name=global-law&config=%7B%22type%22%3A%22http%22%2C%22url%22%3A%22https%3A%2F%2Fglobal-law.lexifina.com%2Fmcp%3Fclient%3Dvscode-button%22%7D)
[![Release](https://img.shields.io/github/v/release/lexifina/global-law-plugin)](https://github.com/lexifina/global-law-plugin/releases)

https://github.com/user-attachments/assets/00f76557-8b46-4765-9f30-c782ea297d1b

| Skill | Use it for |
| --- | --- |
| [`global-law`](skills/global-law/SKILL.md) | What a law says, or said on a date, in any country, with the official text cited |
| [`law-change-trace`](skills/law-change-trace/SKILL.md) | How a provision or a body of law changed, and which law made each change |
| [`citation-check`](skills/citation-check/SKILL.md) | Checking the legislation cited in a brief, contract or memo against the record |

## Install

**Claude Code** (plugin: the server and the skills)

```
/plugin marketplace add lexifina/global-law-plugin
/plugin install global-law@global-law
```

Server only: `claude mcp add --transport http global-law https://global-law.lexifina.com/mcp`

Commands: `/global-law:law-on-date`, `/global-law:law-changes`, `/global-law:check-citations`, `/global-law:law-for-case`.

**Codex** (plugin: the server and the skills)

```
codex plugin marketplace add lexifina/global-law-plugin
codex plugin add global-law@global-law
```

Server only: `codex mcp add global-law --url https://global-law.lexifina.com/mcp`

**Cursor**: use the button above, install **Global law** from the Cursor Marketplace, or add the server in Settings → MCP with the URL above
(`{"mcpServers": {"global-law": {"url": "https://global-law.lexifina.com/mcp"}}}`).

**VS Code**: use the button above, or run **MCP: Add Server** and give the URL.

**Gemini CLI**

```
gemini extensions install https://github.com/lexifina/global-law-plugin
```

**Grok Build**: install **global-law** from the plugin marketplace.

**Cline**: in the MCP Servers panel, add a remote server named `global-law` with the URL above (see [llms-install.md](llms-install.md)).

**Any other MCP client** (Claude.ai, ChatGPT, Zed, ...): add a remote MCP server with the URL above.

**Skills only**: copy a folder from `skills/` into `~/.claude/skills/` (or your agent's skills folder). The skills need
the MCP server connected.

The packaged addresses end in `?client=...` (for example `?client=plugin`). It only tells the server which
packaging a call came from, for usage counts; the server is the same with or without it.

## Examples

- "What did Article 1 of the German Basic Law say on 1 January 1950, and which law has changed it since?"
- "Which laws have changed 11 U.S.C. § 1182 since 2019, and what did each change do?"
- "Check the citations in this paragraph as of 1 June 2023: ..."

## Tests

The scripts and tests are on the [`tooling` branch](https://github.com/lexifina/global-law-plugin/tree/tooling), so
this branch holds only what an AI app installs. `tests/run_cases.py` there asks each question in `tests/cases.json`
through Claude Code with only this plugin, and fails if the expected skill or MCP tools were not used. See
[CONTRIBUTING.md](CONTRIBUTING.md).

## What it sends and what is kept

The plugin is text: skills, commands and the server's address. It runs nothing on your computer and reads none of
your files. When your AI app calls a tool, the request goes to `global-law.lexifina.com` with that tool's inputs (a
citation, a date, search words, or a passage whose citations you asked to have checked). The server answers and does
not store the inputs or the answer.

For each call the server keeps the time, the tool's name, whether it succeeded, how long it took, the kind of app that
made it and a scrambled fingerprint of your network address, used to count callers and apply rate limits. The address
itself is not kept. Rows are deleted after 400 days. The full text is in the
[privacy policy](https://lexifina.com/privacy-policy#global-law).

Support: [global-law@lexifina.com](mailto:global-law@lexifina.com), or
[open an issue](https://github.com/lexifina/global-law-plugin/issues).

## The record

- The MCP server's tools: [MCP.md](https://github.com/lexifina/global-law/blob/main/MCP.md).
- Every client, step by step: [MCP.md](https://github.com/lexifina/global-law/blob/main/MCP.md#install-on-each-client).

The record is a research aid, not legal advice. Read the official text before relying on any
provision.

## License

[CC0 1.0](LICENSE).
