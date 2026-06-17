---
type: "term"
branch: "Computing Foundations"
tags: [foundations]
status: "developed"
---

# Code Point

> **Branch:** [[01 - Computing Foundations|Computing Foundations]]

A single number in a character set, e.g. U+0041 for 'A'. A code point is not the same as a byte, nor always a single visible glyph.

**Context.** A user-perceived character ('grapheme', like an emoji with a skin-tone modifier) can be several code points; one code point can be several bytes. Three different counts — bytes, code points, graphemes — that string-length bugs constantly confuse.

## See also

- [[Unicode]]
- [[UTF-8]]

## Further reading

- [Wikipedia: Code point](https://en.wikipedia.org/wiki/Code_point)
