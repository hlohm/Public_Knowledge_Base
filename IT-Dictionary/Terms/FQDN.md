---
type: "term"
branch: "Networking"
aliases: ["Fully Qualified Domain Name"]
tags: [net, fundamental]
status: "developed"
---

# FQDN

> **Branch:** [[04 - Networking|Networking]]
> **Also known as:** Fully Qualified Domain Name

A **f**ully **q**ualified **d**omain **n**ame: a name complete to the root, unambiguous on its own — conventionally written with a trailing dot, `host.example.com.`

**Context.** Qualified means no [[Search Domain|search suffix]] is appended — the resolver queries it verbatim. That makes the FQDN the diagnostic tool of choice for split-horizon and bare-name trouble: it sidesteps both `/etc/hosts` single-label synthetic matches and search-list ambiguity, going straight to the authority for that exact name. The trailing dot (the root label) is usually implied in everyday use but is what makes 'fully qualified' literally true.

## See also

- [[Search Domain]]
- [[DNS Zone]]
- [[Stub Resolver]]

## Further reading

- [Wikipedia: Fully qualified domain name](https://en.wikipedia.org/wiki/Fully_qualified_domain_name)
