# Global law plugin

The hosted **Global law** MCP server, packaged for Claude Code, Cursor, Gemini CLI and Grok Build, with skills that answer legal questions from the **Global law** record: the
law of about 200 countries kept as a dated history. Every change is dated the day it took effect and
names the law that made it, so any provision can be read as it stood on any date, with a link to the
official text.

The skills use the hosted **Global law MCP server** at `https://global-law.lexifina.com/mcp`. It needs no
account, no key and no download.

| Skill | Use it for |
| --- | --- |
| [`global-law`](skills/global-law/SKILL.md) | What a law says, or said on a date, in any country, with the official text cited |
| [`law-change-trace`](skills/law-change-trace/SKILL.md) | How a provision or a body of law changed, and which law made each change |
| [`citation-check`](skills/citation-check/SKILL.md) | Checking the legislation cited in a brief, contract or memo against the record |

## Install

The server is `https://global-law.lexifina.com/mcp` (Streamable HTTP). It needs no account, no key and no download.

**Claude Code** (plugin: the server and the skills)

```
/plugin marketplace add lexifina/global-law-plugin
/plugin install global-law@global-law
```

Server only: `claude mcp add --transport http global-law https://global-law.lexifina.com/mcp`

**Cursor**: install **Global law** from the Cursor Marketplace, or add the server in Settings → MCP with the URL above
(`mcp.json` in this repo: `{"mcpServers": {"global-law": {"url": "https://global-law.lexifina.com/mcp"}}}`).

**Gemini CLI**

```
gemini extensions install https://github.com/lexifina/global-law-plugin
```

**Grok Build**: install **global-law** from the plugin marketplace.

**Cline**: in the MCP Servers panel, add a remote server named `global-law` with the URL above (see [llms-install.md](llms-install.md)).

**Any other MCP client** (Claude.ai, ChatGPT, VS Code, Zed, ...): add a remote MCP server with the URL above.

**Skills only**: copy a folder from `skills/` into `~/.claude/skills/` (or your agent's skills folder). The skills need
the MCP server connected.

## Examples

- "What did Article 1 of the German Basic Law say on 1 January 1950, and which law has changed it since?"
- "Which laws have changed 11 U.S.C. § 1182 since 2019, and what did each change do?"
- "Check the citations in this paragraph as of 1 June 2023: ..."

## The record

- Data: [github.com/lexifina/global-law](https://github.com/lexifina/global-law) (public domain,
  CC0), with the MCP server's tools described in [MCP.md](https://github.com/lexifina/global-law/blob/main/MCP.md).
- REST API: [lexifina.com/api/global-law](https://lexifina.com/api/global-law).

The record is a research aid, not legal advice. Read the official text before relying on any
provision.

## License

[CC0 1.0](LICENSE).
