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

**Context.** Forwarding re-emits a message from a new IP that isn't in the original sender's SPF, so SPF breaks at the next hop. SRS fixes it by rewriting the envelope `MAIL FROM` to the forwarder's own domain (an encoded, reversible address of the shape `SRS0=HHH=TT=origdomain=user@forwarder.example`, carrying a timestamp and an HMAC so the forwarder can reverse it for bounces and nobody else can forge it) — so SPF checks against the forwarder, and bounces still route back correctly. It's the piece a receive-and-forward relay needs to stay deliverable; DKIM, by contrast, usually survives forwarding untouched as long as the body/headers aren't modified, so [[DMARC]] can still pass via DKIM alignment.

Two things worth internalising. SRS is the **supporting** fix, not the load-bearing one: DMARC passes if *either* SPF or DKIM is aligned, and since SRS deliberately moves the SPF identity to the forwarder, it is the DKIM signature that actually carries mail across the hop. Forget DKIM and forwarding fails for everyone; forget SRS and mostly your bounce path looks wrong. And on a **multi-node** forwarder the HMAC secret must be byte-identical across all nodes — generate once and distribute, never per node, or node A cannot reverse a bounce for a message node B rewrote.

## See also

- [[SPF]]
- [[DKIM]]
- [[DMARC]]
- [[Envelope Sender]]
- [[SMTP]]
- [[MTA]]
- [[HMAC]]
- [[Backscatter]]

## Further reading

- [Wikipedia: Sender Rewriting Scheme](https://en.wikipedia.org/wiki/Sender_Rewriting_Scheme)
