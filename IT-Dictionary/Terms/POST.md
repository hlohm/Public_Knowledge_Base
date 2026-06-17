---
type: "term"
branch: "Internet & Web"
tags: [web]
status: "developed"
---

# POST

> **Branch:** [[05 - Internet & Web|Internet & Web]]

The HTTP method for submitting data to be processed, typically creating a resource or triggering a state change. Not safe, not idempotent.

**Context.** Because it isn't idempotent, a retried POST can double-submit — hence the 'press refresh to resubmit?' prompt, and why idempotency keys exist for payments.

## See also

- [[GET]]
- [[PUT]]
- [[HTTP]]
- [[Idempotency Key]]

## Further reading

- [Wikipedia: HTTP](https://en.wikipedia.org/wiki/HTTP)
