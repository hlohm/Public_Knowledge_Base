---
type: "term"
branch: "Networking"
aliases: ["Authoritative Name Server"]
tags: [net]
status: "developed"
---

# Authoritative DNS Server

> **Branch:** [[04 - Networking|Networking]]
> **Also known as:** Authoritative Name Server

A nameserver that holds the actual records for a zone and answers for it as the source of truth, rather than by asking anyone else.

**Context.** The other half of the split that confuses people: an authoritative server *owns* answers for its zones; a [[Recursive Resolver]] *finds* answers by walking from the root down to whichever authoritative server is responsible. The `aa` (authoritative answer) flag in a response tells you which you got. Your public zone lives on authoritative servers (a DNS host like deSEC or a registrar's nameservers); your laptop never talks to them directly — a resolver does that on its behalf.

## See also

- [[Recursive Resolver]]
- [[DNS Zone]]
- [[NS Record]]
- [[DNS]]

## Often confused with

- [[Recursive Resolver]] — Authoritative = owns the zone's records; recursive = fetches them for a client by querying authoritatives.

## Further reading

- [RFC 1034 — Domain Concepts and Facilities](https://datatracker.ietf.org/doc/html/rfc1034)
