---
type: "term"
branch: "Internet & Web"
aliases: ["Web Session", "HTTP Session"]
tags: [web, fundamental]
status: "developed"
---

# Session

> **Branch:** [[05 - Internet & Web|Internet & Web]]
> **Also known as:** Web Session, HTTP Session

The server-side notion of a *continuing relationship* with one client across many stateless [[HTTP]] requests: the server holds the state (who you are, what's in your cart) under an opaque **session ID**, and the browser carries that ID back on each request — almost always inside a [[Cookie]].

**Context.** Sessions are how login survives statelessness: authenticate once, receive a session ID, present it thereafter instead of re-sending credentials. That ID is a [[Bearer Token]] — possession is authority — which makes its handling the crux of web-auth security. The failure modes are worth knowing by name: [[Session Hijacking]] (stealing the ID, e.g. via [[XSS]] or a lifted cookie store), countered by `HttpOnly`/`Secure` cookies, short idle timeouts, and TLS everywhere; and [[Session Fixation]] (planting a known ID before login), countered by regenerating the ID at every privilege change. The classic design split is *server-side sessions* (ID in the cookie, state in a server store like Redis) versus *stateless* schemes that push the state to the client inside a signed [[JWT]] — trading server memory and easy revocation against statelessness and harder revocation.

## See also

- [[Cookie]]
- [[HTTP]]
- [[Bearer Token]]
- [[JWT]]
- [[Authentication]]

## Often confused with

- [[Cookie]] — the session is the server-side state and its lifecycle; the cookie is merely the transport for the session ID.
- [[JWT]] — a server-side session keeps state on the server and hands out an opaque ID; a JWT carries the state itself, signed, on the client.

## Further reading

- [Wikipedia: Session (computer science)](https://en.wikipedia.org/wiki/Session_(computer_science))
