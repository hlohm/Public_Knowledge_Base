---
type: "term"
branch: "Internet & Web"
aliases: []
tags: ["web", "net", "email"]
status: "developed"
---

# Deliverability

> **Branch:** [[05 - Internet & Web|Internet & Web]]

Whether legitimate mail actually reaches the inbox rather than the junk folder or nowhere — a reputation question, distinct from whether it was technically delivered.

**Context.** This is the distinction that surprises people who have just finished configuring [[SPF]], [[DKIM]] and [[DMARC]]: authentication proves a message came from the domain it claims, and says nothing about whether that domain deserves trust. A perfectly authenticated message from a domain with poor history still lands in junk. Reputation is tracked per sending IP, per visible From: domain and per DKIM signing domain, so changing one does not shed the others. It is built slowly from complaint rates, spam-trap hits, engagement and consistent volume, and lost quickly by one campaign to a stale list. The practical levers are list hygiene, honest consent, prompt suppression of bounces and complaints, gradual warm-up of new addresses, and honouring 4xx deferrals rather than hammering through them.

## See also

- [[IP Reputation]]
- [[Feedback Loop]]
- [[Spam Trap]]
- [[Bounce]]
- [[DNSBL]]
- [[ESP]]
- [[Email Ecosystem]]

## Further reading

- [M3AAWG published documents](https://www.m3aawg.org/published-documents)
