---
type: "term"
branch: "Internet & Web"
aliases: ["Received", "Received:", "Trace header"]
tags: ["web", "net", "email"]
status: "developed"
---

# Received Header

> **Branch:** [[05 - Internet & Web|Internet & Web]]
> **Also known as:** Received, Trace header

A trace line that each server prepends to a message as it handles it, recording who it came from, who took it, over what protocol, and when — so the accumulated stack describes the path the message travelled.

**Context.** Because each hop *prepends*, the headers read newest-first: the top line is the last server to touch the message and the bottom line claims to be the first. That inversion catches people out on first reading. Together with [[Message-ID]] this is the primary forensic artefact in email — reconstructing a path, finding where a message was injected, or checking whether a claimed origin is plausible all start here.

The rule that makes it usable is a trust rule, and it is the same one that governs `Authentication-Results`: **only the lines added by systems you control are evidence.** A sender can write any number of convincing `Received:` headers into a message before sending it, manufacturing a plausible history that is entirely fictional. So you read from the top down, and the moment you pass the last server inside your own boundary, everything below is an unverified assertion by the message itself. Analysts who read from the bottom up — the chronological direction, which feels natural — start their reasoning in exactly the part an attacker controls.

## See also

- [[Message-ID]]
- [[SMTP]]
- [[MTA]]
- [[DMARC]]
- [[Phishing]]
- [[Email Ecosystem]]

## Further reading

- [RFC 5321 §4.4 — Trace Information](https://datatracker.ietf.org/doc/html/rfc5321#section-4.4)
