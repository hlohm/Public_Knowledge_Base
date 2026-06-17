---
type: "term"
branch: "Security"
domain: "Application Security"
aliases: ["Dynamic Application Security Testing"]
tags: ["appsec", "testing"]
status: "note"
---

# DAST

> **Domain:** [[08 - Application Security|Application Security]]
> **Also known as:** Dynamic Application Security Testing

**D**ynamic **A**pplication **S**ecurity **T**esting. Testing a running application from the outside.

**Context.** Tests the running app as an attacker sees it — no source needed, so it catches config and runtime issues SAST can't, but it only reaches what it can crawl and reach (authenticated, JS-heavy flows are its weak spot). OWASP ZAP is the open-source staple. Best used as one layer: DAST + SAST + SCA cover different blind spots.

## See also

- [[SAST]]
- [[IAST]]
