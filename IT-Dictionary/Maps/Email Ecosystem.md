---
type: "map"
tags: [map, email, net, web, security]
aliases: ["Email Map", "Mail Ecosystem", "How Email Works"]
status: "developed"
---

# Email Ecosystem

> **Topical map** — a cross-branch tour of how email actually works, from the basics to the current state of the art. Sits across [[05 - Internet & Web|Internet & Web]], [[04 - Networking|Networking]] and [[16 - Security|Security]].

![[email-ecosystem-map.svg]]

> [!tip] Interactive version
> `assets/email-ecosystem-map.html` — the same map with **five detail views** and a click-through panel on every component. Open it in a browser; the static SVG above is a snapshot of the first view only.

## Why email is worth a map

Almost every property people expect from email — that the sender is who they claim, that the hop was encrypted, that the message is not spam — is a **layer added later**. SMTP was specified in 1982 for a small network of hosts that trusted each other. It verifies nothing, and it was never revised to; instead, each missing property got its own patch, published in DNS and evaluated independently by whoever receives the message.

That history is the reason email looks baroque, and it is also the key to learning it quickly. **Every mechanism is a patch over one specific hole.** Learn which hole, and the design stops being arbitrary.

The second organising idea is that there is no central authority. Nobody can mandate a change. What actually happens is that the largest mailbox providers decide what they will accept, and everyone else follows — which is why the most consequential development of recent years is not an RFC but a set of enforced bulk-sender requirements.

## The five views

| View | Question it answers |
|---|---|
| **1 · Path** | Who are the participants, and what happens to a message between the author's keyboard and the reader's screen? |
| **2 · Stack & ports** | What speaks to what, on which port, and where does TLS sit? |
| **3 · Identity** | How does a receiver decide whether the sender is who they claim? |
| **4 · Security & delivery** | Was the hop private — and, separately, will the message reach the inbox? |
| **5 · Common setups** | How are the same components assembled for a person, a business, and a provider? |

Start with **Path**. Everything else is a detail lens on one of its stages.

## The five things that actually explain email

**1 · There are two identities in every message, and they need not match.** The *envelope* (`MAIL FROM`, `RCPT TO`) is the SMTP conversation the servers act on; the *headers* (`From:`, `To:`) are text inside the message that the human sees. Routing never looks at the headers. Most email confusion — and most of [[SPF]], [[DKIM]] and [[DMARC]] — dissolves once this split is clear.

**2 · Submission and relay are different jobs.** Accepting new mail from your own authenticated user (port 587, [[MSA]]) and accepting mail from a stranger for a domain you host (port 25, [[MTA]]) are separate trust models. Confusing them produces an [[Open Relay]]. The port is the most reliable clue to which one you are looking at.

**3 · Anonymous inbound is a feature, not a hole.** An [[MX Record|MX]] host must accept connections from the whole internet or nobody can send you mail. The security boundary is the *recipient* address, not the sender's identity — which is why "reject unauthorised destinations" is the single most important line in an MTA config.

**4 · Forwarding is the instructive edge case.** It breaks [[SPF]] (the forwarder's IP was never authorised), survives in [[DKIM]] (the signature travels with the message), needs [[SRS]] to repair the bounce path, and motivated ARC for intermediaries that must modify content. If you understand forwarding, you understand the authentication layer.

**5 · Authentication is not deliverability.** Passing SPF, DKIM and DMARC proves a message came from the domain it claims. It says nothing about whether that domain deserves trust, and a perfectly authenticated message from a domain with poor history still lands in junk. Reputation — see [[IP Reputation]] — decides the inbox.

## A study path

1. **The shape of it** — [[SMTP]], then the three roles in order: [[MSA]] → [[MTA]] → [[MDA]], and [[MX Record]] for how routing is discovered.
2. **The split** — envelope versus header. Read view 3 of the map before touching any DNS record.
3. **The three patches** — [[SPF]], then [[DKIM]], then [[DMARC]] as the thing that ties them to the visible sender.
4. **The complications** — [[SRS]], forwarding, mailing lists, and why [[Open Relay]] and [[Backscatter]] are the two ways to accidentally become a spam source.
5. **Transport security** — [[TLS]] and STARTTLS's opportunism, then [[MTA-STS]] and [[DANE]] as two answers to the same problem with different trust roots ([[DNSSEC]] versus the web PKI).
6. **Operations** — [[Greylisting]], [[IP Reputation]], [[Null Client]], [[Milter]], and the deliverability material in view 4.

For the hands-on counterpart, see the Field Manual's `postfix` and `dns` cheat sheets.

## Terms in this map

Every component on the map has a dictionary entry. Grouped by the view it belongs to:

**Participants and the path** — [[MUA]] · [[MSA]] · [[MTA]] · [[MDA]] · [[SMTP]] · [[MX Record]] · [[Smarthost]] · [[Null Client]] · [[Mailing List]] · [[ESP]] · [[Milter]]

**Message internals** — [[Envelope Sender]] · [[Received Header]] · [[Message-ID]] · [[HELO]] · [[MIME]]

**Stack, ports and formats** — [[IMAP]] · [[POP3]] · [[JMAP]] · [[LMTP]] · [[Sieve]] · [[Maildir]] · [[SASL]] · [[TCP]] · [[HTTPS]]

**Identity** — [[SPF]] · [[DKIM]] · [[DMARC]] · [[ARC]] · [[SRS]] · [[BIMI]] · [[DNS]] · [[TXT Record]] · [[PTR Record]] · [[FCrDNS]] · [[Null MX]]

**Transport security** — [[TLS]] · [[STARTTLS]] · [[MTA-STS]] · [[DANE]] · [[TLS-RPT]] · [[DNSSEC]] · [[S-MIME|S/MIME]] · [[OpenPGP]]

**Deliverability and abuse** — [[IP Reputation]] · [[DNSBL]] · [[Greylisting]] · [[Spam Trap]] · [[Feedback Loop]] · [[Bounce]] · [[Backscatter]] · [[Open Relay]] · [[Deliverability]] · [[Phishing]] · [[MFA]]

## Further reading

- [RFC 5321 — SMTP](https://datatracker.ietf.org/doc/html/rfc5321) and [RFC 5322 — Internet Message Format](https://datatracker.ietf.org/doc/html/rfc5322) — the two halves: the conversation and the message.
- [RFC 6409 — Message Submission](https://datatracker.ietf.org/doc/html/rfc6409) — why 587 exists.
- [RFC 7208 (SPF)](https://datatracker.ietf.org/doc/html/rfc7208) · [RFC 6376 (DKIM)](https://datatracker.ietf.org/doc/html/rfc6376) · [RFC 7489 (DMARC)](https://datatracker.ietf.org/doc/html/rfc7489) · [RFC 8617 (ARC)](https://datatracker.ietf.org/doc/html/rfc8617)
- [RFC 8461 (MTA-STS)](https://datatracker.ietf.org/doc/html/rfc8461) · [RFC 7672 (DANE for SMTP)](https://datatracker.ietf.org/doc/html/rfc7672) · [RFC 8314 (implicit TLS)](https://datatracker.ietf.org/doc/html/rfc8314)
- [M3AAWG best practices](https://www.m3aawg.org/published-documents) — where operational consensus is actually written down.

---
← Back to [[_Home]]
