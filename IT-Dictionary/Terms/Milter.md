---
type: "term"
branch: "Internet & Web"
aliases: ["mail filter", "Sendmail Mail Filter API", "smtpd_milters"]
tags: ["web", "net", "email"]
status: "developed"
---

# Milter

> **Branch:** [[05 - Internet & Web|Internet & Web]]
> **Also known as:** mail filter, Sendmail Mail Filter API

A protocol (originating with Sendmail, adopted by Postfix) that lets an external process inspect and modify a message *while the SMTP transaction is still open* — at connect, HELO, MAIL FROM, RCPT TO, header and body stages — and return accept, reject, quarantine or "add this header".

**Context.** Milters are how signing and policy bolt onto an [[MTA]] without patching it: OpenDKIM signs outbound and verifies inbound, OpenDMARC applies policy, rspamd and SpamAssassin score. The decisive advantage over a post-queue content filter is that a milter can **reject during the SMTP dialogue**, so the sending server is told "no" and owns the problem — no bounce message needs to be generated, which is how you avoid [[Backscatter]]. The operational trap is availability: `milter_default_action` decides what happens when the milter socket is down, and the choice is between accepting unsigned/unchecked mail (`accept`) and refusing all mail because a helper crashed (`tempfail`). Getting this backwards turns a minor daemon failure into a full mail outage.

## See also

- [[MTA]]
- [[DKIM]]
- [[DMARC]]
- [[Backscatter]]
- [[API]]

## Further reading

- [Postfix Milter support](https://www.postfix.org/MILTER_README.html)
- [Wikipedia: Milter](https://en.wikipedia.org/wiki/Milter)
