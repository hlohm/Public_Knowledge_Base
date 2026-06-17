---
type: "term"
branch: "Security"
domain: "Network Security"
aliases: ["Sender Rewriting Scheme"]
tags: ["network", "email"]
status: "developed"
---

# SRS

> **Domain:** [[05 - Network Security|Network Security]]
> **Also known as:** Sender Rewriting Scheme

A scheme for rewriting the envelope sender when *forwarding* mail, so the forwarded message still passes [[SPF]] at the final destination.

**Context.** Forwarding re-emits a message from a new IP that isn't in the original sender's SPF, so SPF breaks at the next hop. SRS fixes it by rewriting the envelope `MAIL FROM` to the forwarder's own domain (an encoded, reversible address) — so SPF checks against the forwarder, and bounces still route back correctly. It's the piece a receive-and-forward relay needs to stay deliverable; DKIM, by contrast, usually survives forwarding untouched as long as the body/headers aren't modified, so [[DMARC]] can still pass via DKIM alignment.

## See also

- [[SPF]]
- [[DKIM]]
- [[DMARC]]
- [[Envelope Sender]]
- [[SMTP]]

## Further reading

- [Wikipedia: Sender Rewriting Scheme](https://en.wikipedia.org/wiki/Sender_Rewriting_Scheme)
