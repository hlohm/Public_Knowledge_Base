---
type: "term"
branch: "Internet & Web"
aliases: ["HTTP Cookie"]
tags: [web, fundamental]
status: "developed"
---

# Cookie

> **Branch:** [[05 - Internet & Web|Internet & Web]]
> **Also known as:** HTTP Cookie

A small key–value string a server sets in the browser with a `Set-Cookie` response header; the browser then echoes it back in a `Cookie` header on every later request whose scope matches. It is the original way to bolt state — a login, a preference — onto stateless [[HTTP]].

**Context — the parameters that matter.** A cookie is mostly defined by its attributes, which do three jobs. *Scope:* `Domain` (omit it and the cookie is host-only; set it and the cookie reaches all subdomains) and `Path` decide where it's sent. *Lifetime:* with no `Expires`/`Max-Age` it's a *session cookie* (gone when the browser closes); with one it's *persistent* and written to disk. *Security:* `Secure` (HTTPS only), `HttpOnly` (invisible to JavaScript, so [[XSS]] can't read it), and `SameSite` — `Strict`, `Lax` (the modern default, sent only on top-level navigation), or `None` (cross-site, valid only together with `Secure`). The `__Host-` and `__Secure-` name *prefixes* bake guarantees into the name itself: a `__Host-` cookie is refused unless it is `Secure`, host-only (no `Domain`), and `Path=/`, the strongest anti-tampering scoping available. `Partitioned` (CHIPS) gives a third-party cookie a separate jar per top-level site so it can't track across sites.

**Context — how they're used in practice.** The dominant use is carrying a *session identifier*: the cookie holds an opaque ID and the real state lives server-side (see [[Session]]). A hardened session cookie therefore reads `Set-Cookie: __Host-id=…; Secure; HttpOnly; SameSite=Lax; Path=/`. Two structural caveats. First, a cookie is a [[Bearer Token]] — whoever copies it *is* you until it expires; `HttpOnly`/`Secure` stop script theft and sniffing but not local malware reading the browser's cookie store, which is the gap [[DBSC]] closes by binding the session to a device key. Second, cookies are weakly bound to scheme/port, capped near 4 KB, and sent on *every* matching request, so keep them tiny and never store anything you wouldn't put on a postcard. Client-only data belongs in [[Web Storage]] or [[IndexedDB]] instead; third-party cookies are being phased out for tracking reasons.

## See also

- [[Session]]
- [[HTTP]]
- [[CSRF]]
- [[Same-Origin Policy]]
- [[Bearer Token]]
- [[Web Storage]]

## Often confused with

- [[Web Storage]] — a cookie is sent to the server on every matching request; localStorage/sessionStorage stay in the browser and are never auto-transmitted.
- [[Session]] — the session is the server-side state; the cookie is just the client-side carrier of its ID.

## Further reading

- [MDN: Using HTTP cookies](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Cookies)
- [RFC 6265: HTTP State Management Mechanism](https://datatracker.ietf.org/doc/html/rfc6265)
