---
description: Trace how a provision, or a country's law over a period, changed and which law made each change
argument-hint: <provision | country> [from YYYY-MM-DD] [to YYYY-MM-DD]
disable-model-invocation: true
---

Use the `law-change-trace` skill and the Global law MCP server to answer for: $ARGUMENTS

- A provision (a citation, a name with its country, or a path): `find_provision`, then `provision_history` for
  every law that changed it; with two dates, `compare_dates` for what changed between them.
- A country or jurisdiction with a period: `laws_between` for the laws that took effect, and `changes_between`
  for the provisions whose text differs.

Give the changes in date order, each with the law that made it, its in-force date and a sentence on what it
did, citing each law's official source. With no arguments, ask what to trace.
