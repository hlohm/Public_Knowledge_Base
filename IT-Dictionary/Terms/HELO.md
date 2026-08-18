---
type: "term"
branch: "Internet & Web"
aliases: ["EHLO", "HELO/EHLO", "Extended HELO"]
tags: ["web", "net", "email"]
status: "developed"
---

# HELO

> **Branch:** [[05 - Internet & Web|Internet & Web]]
> **Also known as:** EHLO, HELO/EHLO

The greeting that opens an [[SMTP]] session, in which the connecting client names itself. `EHLO` is the extended form: it asks the server to list the extensions it supports, and everything modern in SMTP hangs off that answer.

**Context.** The name a client gives is self-asserted and verified by nothing, so on its own it proves precisely as much as the `From:` header does — nothing. What receivers actually test is *well-formedness*, and it filters a surprising amount of abuse: the argument must be a fully qualified domain name or an address literal, it must not claim to be the receiving server's own name, it should resolve, and ideally it agrees with the client's [[FCrDNS]]. Botnet software routinely fails all four (`reject_invalid_helo_hostname` and friends in Postfix). Because this happens before any message body is transferred, it is among the cheapest rejections available.

`EHLO` matters for a second reason: it is SMTP's extension mechanism. `STARTTLS`, `AUTH`, `SIZE`, `PIPELINING`, `8BITMIME` and the rest are discovered from the EHLO response, which is why a session that falls back to plain `HELO` silently loses the ability to negotiate encryption or authentication. A server advertising nothing useful, or a client that never tries EHLO, is worth noticing during diagnosis.

## See also

- [[SMTP]]
- [[FCrDNS]]
- [[PTR Record]]
- [[STARTTLS]]
- [[MTA]]
- [[Email Ecosystem]]

## Further reading

- [RFC 5321 §4.1.1.1 — EHLO/HELO](https://datatracker.ietf.org/doc/html/rfc5321#section-4.1.1.1)
