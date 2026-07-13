---
type: "term"
branch: "Security"
domain: "Network Security"
aliases: ["Single-Use Reply Block"]
tags: ["anonymity", "cryptography"]
status: "note"
---

# SURB

> **Domain:** [[05 - Network Security|Network Security]]
> **Also known as:** Single-Use Reply Block

**S**ingle-**U**se **R**eply **B**lock. A pre-built, cryptographically sealed set of routing instructions that lets someone reply to an anonymous sender without ever learning who or where they are. The sender constructs the return path in advance, hands it over as an opaque token, and the recipient spends it once to send a reply back through the [[Mixnet]].

**Context.** It solves the hard half of anonymous messaging: hiding the *sender* is one thing; letting them *receive* a reply without exposing a return address is another. Because each block is single-use and, on the wire, indistinguishable from a normal forward message, replies don't form a separate, attackable class of traffic. Introduced with the [[Sphinx Packet Format]] and used by Loopix/Nym.

## See also

- [[Sphinx Packet Format]]
- [[Mixnet]]
