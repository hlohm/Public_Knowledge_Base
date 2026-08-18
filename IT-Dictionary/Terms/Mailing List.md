---
type: "term"
branch: "Internet & Web"
aliases: ["Discussion list", "List server"]
de: "Verteiler"
tags: ["web", "net", "email"]
status: "developed"
---

# Mailing List

> **Branch:** [[05 - Internet & Web|Internet & Web]]
> **Also known as:** Discussion list, List server
> **German:** Verteiler

A service that receives one message and re-sends it to many subscribers, usually modifying it on the way — subject tags, footers, or rewritten headers.

**Context.** Every modification invalidates the original [[DKIM]] signature, and since the [[SPF]] check now sees the list server's address rather than the author's, a message from a domain publishing `p=reject` fails [[DMARC]] outright. That collision was not hypothetical: when a large consumer provider moved to `p=reject` in 2014, mailing lists across the internet began rejecting their own members' posts. The immediate workaround was to rewrite `From:` to the list address, losing the real author; the considered answer was [[ARC]], which lets the list seal what it saw before it made changes. Lists are the standard example of a domain-level policy having consequences far outside the domain that set it.

## See also

- [[ARC]]
- [[DMARC]]
- [[DKIM]]
- [[SPF]]
- [[Sieve]]
- [[Email Ecosystem]]

## Further reading

- [Wikipedia: Electronic mailing list](https://en.wikipedia.org/wiki/Electronic_mailing_list)
