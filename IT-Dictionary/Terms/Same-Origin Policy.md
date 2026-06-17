---
type: "term"
branch: "Security"
domain: "Application Security"
tags: ["appsec", "web"]
status: "developed"
---

# Same-Origin Policy

> **Domain:** [[08 - Application Security|Application Security]]

Browser rule that scripts from one origin can't read data from another. The foundation of web security.

**Context.** The invisible wall that makes the web survivable: without it, any tab could read your banking session in another. Almost everything else in browser security is an exception carved into it — CORS to relax it deliberately, cookies' SameSite to tighten it, CSP to constrain what loads within an origin. Understand SOP first; the rest of web security is commentary on it.

## See also

- [[CORS]]
- [[CSP]]
- [[XSS]]

## Further reading

- [MDN: Same-origin policy](https://developer.mozilla.org/en-US/docs/Web/Security/Same-origin_policy)
