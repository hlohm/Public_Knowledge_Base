---
type: "term"
branch: "Security"
domain: "Application Security"
aliases: ["Content Security Policy"]
tags: ["appsec", "web"]
status: "developed"
---

# CSP

> **Domain:** [[08 - Application Security|Application Security]]
> **Also known as:** Content Security Policy

**C**ontent **S**ecurity **P**olicy. HTTP header restricting what content a browser will load. Major XSS defense.

**Context.** The browser-side backstop for XSS: declare which origins may serve scripts/styles and inline script stops executing. The honest part is that a strict CSP on an existing app is real work — inventory every source, replace inline handlers, often adopt nonces/hashes — so teams start in report-only mode and tighten. `unsafe-inline` defeats the whole point; if it's there, the CSP is theater.

## See also

- [[XSS]]
- [[Same-Origin Policy]]

## Further reading

- [MDN: Content Security Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP)
