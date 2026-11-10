---
description: Check the legal citations in a text or file against the law in force on a date
argument-hint: <text or file path> [date YYYY-MM-DD]
disable-model-invocation: true
---

Use the `citation-check` skill and the Global law MCP server to check the citations in: $ARGUMENTS

If the argument is a file path, read the file first. Use the date given; with none, use the date of the
document if it states one, otherwise today, and say which you used.

1. `resolve_citations` with the text and the date.
2. For a citation it does not list, `find_provision` with the country's `jurisdiction`.
3. `read_law` for each citation the text relies on, to quote what it said on that date.

Report one row per citation: as written, what it resolved to, in force on the date or not, the law that last
changed it, any change since, and the official link. Then list what the record could not resolve. With no
arguments, ask for the text.
