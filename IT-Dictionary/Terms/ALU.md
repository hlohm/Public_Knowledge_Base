---
type: "term"
branch: "Hardware & Architecture"
aliases: ["Arithmetic Logic Unit"]
tags: ["hw", "fundamental"]
status: "developed"
---

# ALU

> **Branch:** [[02 - Hardware & Architecture|Hardware & Architecture]]
> **Also known as:** Arithmetic Logic Unit

**A**rithmetic **L**ogic **U**nit. The combinational circuit that actually computes — integer add/subtract, AND/OR/XOR, shifts, comparisons — taking operands from registers and setting status flags (zero, carry, overflow).

**Context.** The ALU is where the abstraction tower touches ground: every `if` ultimately becomes an ALU comparison setting a flag that a branch instruction reads. Modern cores ship several ALUs and dispatch to them in parallel — superscalar execution is, concretely, 'more ALUs plus scheduling.'

## See also

- [[CPU]]
- [[Register]]
- [[Instruction Set]]
- [[Two's Complement]]

## Further reading

- [Wikipedia: Arithmetic logic unit](https://en.wikipedia.org/wiki/Arithmetic_logic_unit)
