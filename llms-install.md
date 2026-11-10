# Installing the Global law MCP server

Global law is a hosted, read-only MCP server. There is nothing to download, build or configure, and it needs no
account, API key or environment variable.

- Transport: Streamable HTTP
- URL: `https://global-law.lexifina.com/mcp`

Add it as a remote server. In Cline's `cline_mcp_settings.json`:

```json
{
  "mcpServers": {
    "global-law": {
      "type": "streamableHttp",
      "url": "https://global-law.lexifina.com/mcp"
    }
  }
}
```

To check it works, call the `list_jurisdictions` tool with no arguments: it lists the countries the record holds.
Then try `read_law` with `{"path": "germany/bund/acts/grundgesetz/artikel/001.md", "date": "1950-01-01"}`.
