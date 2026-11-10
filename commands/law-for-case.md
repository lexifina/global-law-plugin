---
description: Which text of a provision applies to a case commenced on a date
argument-hint: <provision> <commenced YYYY-MM-DD>
disable-model-invocation: true
---

Use the `citation-check` skill and the Global law MCP server to answer for: $ARGUMENTS

1. `find_provision` for the provision's path (with `jurisdiction` when a country is named).
2. `applies_to_case` with the path and `commenced` set to the day the case was commenced.
3. Give the text that applies to the case, the law behind it, and each later change with whether it reaches
   the case, citing the official text and passing on every limit the answer states.

With a provision or a date missing, ask for it.
