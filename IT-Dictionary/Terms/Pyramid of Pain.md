---
type: "term"
branch: "Security"
domain: "SecOps, Detection & Response"
tags: ["secops", "model"]
status: "developed"
---

# Pyramid of Pain

> **Domain:** [[11 - SecOps Detection and Response|SecOps, Detection & Response]]

David Bianco's model: the higher up the indicator type, the more painful for the attacker to change. Hashes (easy) → TTPs (hard).

**Context.** The strategy argument in one diagram: blocking hashes and IPs annoys an attacker for minutes (they rotate them trivially), while detecting their TTPs forces them to relearn how they operate. It's the case for investing detection effort *up* the pyramid — behavioral, ATT&CK-mapped detections over IOC feeds — even though the IOCs are easier to obtain.

## See also

- [[IOC]]
- [[IOA]]
- [[TTPs]]

## Further reading

- [Detect-Respond: The Pyramid of Pain](https://detect-respond.blogspot.com/2013/03/the-pyramid-of-pain.html)
