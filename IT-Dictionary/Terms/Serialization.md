---
type: "term"
branch: "Computing Foundations"
aliases: ["Marshalling"]
de: "Serialisierung"
tags: [foundations, fundamental]
status: "developed"
---

# Serialization

> **Branch:** [[01 - Computing Foundations|Computing Foundations]]
> **Also known as:** Marshalling
> **German:** Serialisierung

Converting an in-memory object or data structure into a flat byte stream (JSON, Protocol Buffers, etc.) that can be stored or sent, and back again (deserialization).

**Context.** Deserialization of untrusted input is a notorious security hole — it can instantiate arbitrary objects. The format you pick trades off human-readability (JSON) against size and speed (binary formats).

## See also

- [[JSON]]
- [[Protocol Buffers]]
- [[Endianness]]

## Further reading

- [Wikipedia: Serialization](https://en.wikipedia.org/wiki/Serialization)
