---
type: "term"
branch: "Networking"
aliases: ["MX 0 .", "RFC 7505"]
tags: [net, email, security]
status: "developed"
---

# Null MX

> **Branch:** [[04 - Networking|Networking]]
> **Also known as:** MX 0 .

A single [[MX Record]] of the form `MX 0 .` — a root-label target — declaring that a domain accepts no mail at all, so senders fail immediately instead of retrying for days.

**Context.** Without it, a domain with no MX falls back to its [[A Record]], and mail to it is queued and retried against a web server for four or five days before bouncing. Null MX replaces that with an instant, unambiguous permanent failure, which is better for the sender (a fast, accurate bounce) and better for the receiver (no pointless connections).

Its real value is defensive, and it belongs in a set. Every domain and subdomain an organisation owns but does not send mail from — parked domains, defensive registrations, typo-squat protections, `www` and other subdomains — is otherwise a free identity for a spoofer. The standard hardening triple is a null MX, an SPF record of `v=spf1 -all`, and a DMARC record at `p=reject`, which together say: nothing sends as this name, nothing receives as this name, discard anything claiming otherwise. Cheap to publish and easy to forget, which is why unused subdomains are a favourite spoofing target and why [[DMARC]]'s `sp=` subdomain policy exists.

## See also

- [[MX Record]]
- [[SPF]]
- [[DMARC]]
- [[SMTP]]
- [[Bounce]]
- [[Email Ecosystem]]

## Further reading

- [RFC 7505 — A Null MX Resource Record](https://datatracker.ietf.org/doc/html/rfc7505)
