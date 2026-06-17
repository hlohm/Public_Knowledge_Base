---
type: "term"
branch: "Security"
domain: "Application Security"
aliases: ["Output Encoding"]
tags: ["appsec"]
status: "note"
---

# Input Validation

> **Domain:** [[08 - Application Security|Application Security]]
> **Also known as:** Output Encoding

Scrub what comes in; **output encoding** escapes what goes out. The two halves of injection defense.

**Context.** Necessary but routinely over-trusted as an injection cure — it's the first layer, not the fix. Validate for *shape* (is this a plausible email, a positive integer?) with allowlists at the boundary, but stop injection at the *sink* with parameterized queries and context-aware output encoding. Defense that relies on blocklisting bad characters loses to encoding tricks.

## See also

- [[Injection Attacks]]
- [[XSS]]
