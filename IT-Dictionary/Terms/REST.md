---
type: "term"
branch: "Internet & Web"
aliases: ["Representational State Transfer"]
tags: [web, fundamental]
status: "developed"
---

# REST

> **Branch:** [[05 - Internet & Web|Internet & Web]]
> **Also known as:** Representational State Transfer

An architectural style (Fielding) for web APIs: resources identified by URLs, manipulated with standard HTTP methods, stateless interactions.

**Context.** Most 'REST APIs' are really JSON-over-HTTP that ignore REST's stricter constraints (HATEOAS). Its strength is leaning on HTTP's existing semantics — caching, idempotency, status codes — instead of reinventing them.

## See also

- [[HTTP]]
- [[GraphQL]]
- [[JSON]]
- [[Idempotent]]

## Often confused with

- [[GraphQL]] — REST = many endpoints, fixed shapes; GraphQL = one endpoint, client picks the shape.

## Further reading

- [Wikipedia: REST](https://en.wikipedia.org/wiki/REST)
