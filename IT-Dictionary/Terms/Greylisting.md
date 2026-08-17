---
type: "term"
branch: "Security"
domain: "Network Security"
aliases: ["greylist", "temporary rejection"]
tags: ["security", "net", "email"]
status: "developed"
---

# Greylisting

> **Domain:** [[05 - Network Security|Network Security]]
> **Also known as:** greylist

An anti-spam technique that temporarily rejects the first delivery attempt from an unfamiliar sender triple (IP, envelope sender, recipient) with a `4xx` code, and accepts it when the sender retries after a delay.

**Context.** It exploits an asymmetry in effort rather than inspecting content: a legitimate [[MTA]] maintains a queue and will retry, because [[SMTP]] requires it, whereas simple spam-sending software historically fired once and moved on. The cost is latency — the first message from any new correspondent is delayed by minutes to an hour, which is genuinely awkward for password resets and one-time codes, so many operators now exempt those or have abandoned greylisting entirely as modern spam infrastructure retries properly. It remains a useful illustration of a broader defensive pattern: a **temporary** failure is a much safer default than a permanent one, because it costs a legitimate sender nothing but a delay while forcing an attacker to maintain state. The same logic makes `4xx` the right response when a policy service is unavailable, and makes rejecting in-transaction preferable to accepting and bouncing ([[Backscatter]]).

## See also

- [[SMTP]]
- [[MTA]]
- [[Backscatter]]
- [[Envelope Sender]]

## Further reading

- [Wikipedia: Greylisting (email)](https://en.wikipedia.org/wiki/Greylisting_(email))
