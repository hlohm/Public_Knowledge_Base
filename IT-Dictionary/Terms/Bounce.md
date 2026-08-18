---
type: "term"
branch: "Internet & Web"
aliases: ["DSN", "Delivery Status Notification", "NDR"]
tags: ["web", "net", "email"]
status: "developed"
---

# Bounce

> **Branch:** [[05 - Internet & Web|Internet & Web]]
> **Also known as:** DSN, Delivery Status Notification, NDR

A message reporting that delivery failed, sent back to the envelope sender — permanent (hard, 5xx) or temporary (soft, 4xx).

**Context.** Hard bounces mean the address is wrong or gone and must be suppressed immediately and permanently; soft bounces mean full mailbox, throttling or a transient fault, and warrant retries before giving up. Two operational consequences follow. First, bounce rate is a reputation signal: a high hard-bounce rate reads as a purchased list and is punished quickly. Second, because the envelope sender is trivially forged, generating a bounce for a message you should have refused turns you into a source of [[Backscatter]] — which is why the rule is to reject unknown recipients *during* the SMTP transaction, while the sending server is still on the line to be told no.

## See also

- [[Backscatter]]
- [[SMTP]]
- [[MTA]]
- [[SRS]]
- [[Deliverability]]
- [[Email Ecosystem]]

## Often confused with

- [[Backscatter]] — a bounce is legitimate when the sender is real; backscatter is the same message sent to a forged address.

## Further reading

- [RFC 3464 — Delivery Status Notifications](https://datatracker.ietf.org/doc/html/rfc3464)
