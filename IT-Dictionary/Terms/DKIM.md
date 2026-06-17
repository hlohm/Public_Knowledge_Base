---
type: "term"
branch: "Security"
domain: "Network Security"
aliases: ["DomainKeys Identified Mail"]
tags: ["security", "network", "email", "crypto"]
status: "developed"
---

# DKIM

> **Domain:** [[05 - Network Security|Network Security]]
> **Also known as:** DomainKeys Identified Mail

**D**omain**K**eys **I**dentified **M**ail. The sending server signs outgoing messages with a private key; the public key is published in DNS, so receivers can verify the mail wasn't altered and really came from the domain.

**Context.** DKIM survives forwarding (which breaks [[SPF]], since the forwarder's IP isn't in the record) because the signature travels with the message. The selector in the DNS record name (`selector._domainkey.example.com`) allows key rotation and multiple senders. A valid DKIM signature says the *signing domain* vouches for the mail — it says nothing about whether that domain is trustworthy.

## See also

- [[SPF]]
- [[DMARC]]
- [[SMTP]]
- [[Digital Signature]]
- [[DNS]]

## Further reading

- [RFC 6376 — DomainKeys Identified Mail](https://datatracker.ietf.org/doc/html/rfc6376)
- [Wikipedia: DomainKeys Identified Mail](https://en.wikipedia.org/wiki/DomainKeys_Identified_Mail)
