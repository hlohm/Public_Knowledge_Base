---
type: "term"
branch: "Security"
domain: "Application Security"
tags: ["appsec"]
status: "note"
---

# Shift Left

> **Domain:** [[08 - Application Security|Application Security]]

Move security activities earlier in the SDLC (design, code) where fixes are cheaper.

**Context.** Sound economics — a flaw caught at design costs orders of magnitude less than one in production — but it curdles into "dump every scanner into the pipeline and block the build" if done thoughtlessly. Done well it's developer-owned, low-friction guardrails (IDE hints, fast PR checks, pre-commit secret scanning) that catch issues without becoming the thing engineers route around.

## See also

- [[SDLC]]
- [[SAST]]
- [[Threat Modeling]]
