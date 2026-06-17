---
type: "term"
branch: "Computing Foundations"
aliases: ["Epoch Time", "POSIX Time"]
tags: [foundations]
status: "developed"
---

# Unix Time

> **Branch:** [[01 - Computing Foundations|Computing Foundations]]
> **Also known as:** Epoch Time, POSIX Time

Time represented as the number of seconds elapsed since 00:00:00 UTC on 1 January 1970 (the 'epoch'), ignoring leap seconds.

**Context.** Simple and timezone-free, which is why it's the lingua franca for timestamps. A signed 32-bit count overflows on 19 January 2038 — the 'Year 2038 problem' — so 64-bit time is now standard.

## See also

- [[Epoch]]
- [[ISO 8601]]
- [[Integer Overflow]]

## Further reading

- [Wikipedia: Unix time](https://en.wikipedia.org/wiki/Unix_time)
