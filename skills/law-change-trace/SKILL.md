---
name: law-change-trace
description: >
  Use when the user asks how a provision or a body of law changed over time and why: "what changed
  in art. 1 GG since 1950", "which law amended this section", "what did the 2023 amendment do",
  "who wrote this sentence", "what changed in German federal law in 2020", "when did 'COVID' enter
  the Grundgesetz". Traces each change to the law that made it, from the Global law record through
  the Global law MCP server, with dates and official sources. Never reconstructs a history from memory.
license: CC0-1.0
metadata:
  author: Lexifina
  connector: https://global-law.lexifina.com/mcp
  version: "1.0.0"
---

# Law change trace

You explain how the law changed, change by change, from the Global law record: every change in it is
dated the day it took effect and names the law that made it. Requirements and citation rules are the
ones in the `global-law` skill: the Global law MCP server must be connected
(`https://global-law.lexifina.com/mcp`), cite the official text, pass on the record's limits, and never
answer from memory.

## One provision

1. Get its path with `find_provision` (with `jurisdiction`).
2. `provision_history` lists every law that changed it, oldest first, with in-force, enacted and
   published dates. Use it for "when" and "which law".
3. `compare_dates` with `date_a` and `date_b` gives a word-level diff and the laws in between. Use it
   for "what changed".
4. `who_wrote` (with `date`) shows which law wrote each word as it stood on that date.
5. `law_details` gives a change's full record (its dates, sources, scope, and what it did to every
   provision it touched). Give it the law's name as `provision_history` or `read_law` name it, or
   the commit those answers give; it does not take a provision path.

## A whole jurisdiction or a period

- `laws_between` with `start`, `end` and `jurisdiction`: every law that took effect in the period.
- `changes_between` with `date_a`, `date_b` and `jurisdiction`: every provision whose text differs.
- `search_changes` searches the change records themselves (for example "temporary" or "Bundesrat").
- `phrase_history` finds when words came into the law and when they left it, including text no
  longer in force.

## Writing it up

Give the changes in date order, each with the law that made it, its in-force date, and a sentence on
what it did, quoting the changed words where they matter. Cite each law's official source as the
answers give it. Keep in-force, enacted and published dates apart; say which one you use.
