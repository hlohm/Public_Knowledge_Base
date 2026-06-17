---
type: "term"
branch: "Security"
domain: "Threats & Attacks"
tags: ["threat"]
status: "developed"
---

# Buffer Overflow

> **Domain:** [[07 - Threats and Attacks|Threats & Attacks]]

Writing past allocated memory, corrupting adjacent data or control flow. The classic memory-corruption bug.

**Context.** The vulnerability that launched modern exploit mitigation: stack canaries, ASLR, DEP/NX, and CFG all exist to make overflows non-trivial to weaponize. Still very much alive in C/C++ and firmware, which is why memory-safe languages (Rust, Go) are now a security argument and agencies (CISA, NSA) actively push the migration.

## See also

- [[RCE]]
- [[Exploit]]

## Further reading

- [Wikipedia: Buffer overflow](https://en.wikipedia.org/wiki/Buffer_overflow)
