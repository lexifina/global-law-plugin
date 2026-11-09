# Global law skills

Skills for Claude and other agents that answer legal questions from the **Global law** record: the
law of about 200 countries kept as a dated history. Every change is dated the day it took effect and
names the law that made it, so any provision can be read as it stood on any date, with a link to the
official text.

The skills use the hosted **Global law MCP server** at `https://mcp.lexifina.com/mcp`. It needs no
account, no key and no download.

| Skill | Use it for |
| --- | --- |
| [`global-law`](skills/global-law/SKILL.md) | What a law says, or said on a date, in any country, with the official text cited |
| [`law-change-trace`](skills/law-change-trace/SKILL.md) | How a provision or a body of law changed, and which law made each change |
| [`citation-check`](skills/citation-check/SKILL.md) | Checking the legislation cited in a brief, contract or memo against the record |

## Install

**Claude Code (plugin, with the MCP server included)**

```
/plugin marketplace add lexifina/global-law-skills
/plugin install global-law@global-law
```

**MCP server only**

```
claude mcp add --transport http global-law https://mcp.lexifina.com/mcp
```

Other clients: add a Streamable HTTP server with the URL `https://mcp.lexifina.com/mcp`.

**Skills only**: copy a folder from `skills/` into `~/.claude/skills/` (or your agent's skills
folder). The skills need the MCP server connected.

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
