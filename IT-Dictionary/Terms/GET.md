---
type: "term"
branch: "Internet & Web"
tags: [web]
status: "developed"
---

# GET

> **Branch:** [[05 - Internet & Web|Internet & Web]]

The HTTP method for retrieving a resource. Defined to be safe (no side effects) and idempotent, and is cacheable.

**Context.** Never use GET for actions that change state — caches, prefetchers, and crawlers will replay it, and parameters land in logs and history.

## See also

- [[POST]]
- [[HTTP]]
- [[Idempotent]]
- [[Safe (HTTP)]]

## Often confused with

- [[POST]] — GET retrieves (safe, cacheable); POST submits/changes state (not safe, not cacheable by default).

## Further reading

- [Wikipedia: HTTP](https://en.wikipedia.org/wiki/HTTP)
