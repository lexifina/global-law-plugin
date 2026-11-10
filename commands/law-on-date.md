---
description: Read a provision as it stood on a date, with the law behind it
argument-hint: <provision> [date YYYY-MM-DD]
disable-model-invocation: true
---

Use the `global-law` skill and the Global law MCP server to answer for: $ARGUMENTS

Read the first part as the provision (a citation such as "11 U.S.C. 1182" or "Art. 16a GG", a name with its
country, or a path) and the date as the day to read it on; with no date, read it as in force today and say so.

1. `find_provision` for the path (with `jurisdiction` when a country is named).
2. `read_law` with the path and the date.
3. Give the text for that date, the law that last changed it with its in-force date, the next change if there
   is one, the official text link and the pincite, and every limit the answer states.

With no arguments, ask which provision and which date.
