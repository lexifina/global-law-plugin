---
name: citation-check
description: >
  Use when the user gives a text that cites legislation (a brief, contract, memo, judgment, email
  or article) and wants the citations checked: do they exist, what do they say, were they in force
  on the relevant date, have they changed since, does a court's reading still hold, which version
  applies to a case filed on a date. Resolves each citation against the Global law record through the
  Global law MCP server and reports per citation, with official sources. Never confirms a citation
  from memory.
license: CC0-1.0
metadata:
  author: Lexifina
  connector: https://global-law.lexifina.com/mcp
  version: "1.0.0"
---

# Citation check

You check the legal citations in a text against the Global law record. Requirements and citation
rules are the ones in the `global-law` skill: the Global law MCP server must be connected
(`https://global-law.lexifina.com/mcp`), cite the official text, pass on the record's limits, and never
confirm or correct a citation from memory.

## Steps

1. **Pick the date that matters**: the date of the document, the contract, the events, or the
   filing. Ask if it is unclear; otherwise use today and say so.
2. **Resolve every citation at once**: `resolve_citations` with the text (up to 50,000 characters)
   and `date`. It returns each citation's provision, whether it was in force on that date, the law
   that last changed it, and the next change. It knows each country's own citation forms (`Art. 1
   Abs. 3 GG`, `art. 1357 Codul civil`, `11 U.S.C. 1182`); a citation it does not list, often one
   written in English ("Article 1(3) of the German Basic Law"), still needs checking: find it with
   `find_provision` and the country's `jurisdiction`, and say which citations you resolved that way.
3. **Read what matters**: for a citation the user relies on, `read_law` with its path and the date,
   to quote what it actually said.
4. **Court decisions**: when the text relies on how a court applied a provision, `check_precedent`
   with the path and the day of the decision (`decided`) tells you whether that text is still the
   law in force, and which laws changed it since.
5. **A case filed on a date**: `applies_to_case` with the path and `commenced` gives the text that
   applies to that case and the later changes that do or do not reach it.

## Report

One row per citation: the citation as written, what it resolved to, in force on the date or not,
the law that last changed it (with in-force date), any change since, and the official link. Then
list citations the record could not resolve, and say that "not resolved" means not in the record,
not necessarily wrong. Quote the text where a citation's wording carries the argument.
