---
type: "term"
branch: "Security"
domain: "Core Principles & Models"
aliases: ["TCB"]
tags: ["principle"]
status: "developed"
---

# Trusted Computing Base

> **Domain:** [[01 - Core Principles|Core Principles & Models]]
> **Also known as:** TCB

The set of components — hardware, firmware, kernel, and software — that *must* be trusted for a system's security to hold. A flaw anywhere inside the TCB can defeat every control built on top of it; everything outside it can fail without breaking the security guarantee.

**Context.** Security design is largely the art of keeping the TCB *small* and *named*, because you can only audit and harden what you've enumerated. The classic exercise is honest boundary-drawing: on a hosted VM the hypervisor operator is inside your TCB whether you like it or not — full-disk encryption protects a stolen drive, not against the host. Modern additions to the list: a [[Reference Monitor]] is the idealized minimal TCB (every access mediated, tamper-proof, verifiable); [[Measured Boot]] and a [[TPM]] try to extend trust up from hardware; and delegating work to a vendor-hosted [[AI Agent]] pulls that vendor's infrastructure into your TCB — worth writing down before, not after, a compliance review. When someone claims a security property, the sharp question is "what's in the TCB that this rests on?"

## See also

- [[Reference Monitor]]
- [[Attack Surface]]
- [[Measured Boot]]
- [[Hypervisor]]
- [[Zero Trust]]

## Often confused with

- [[Attack Surface]] — the attack surface is where an adversary can *poke*; the TCB is what must stay sound for defenses to hold. Shrinking either helps, but they're different lists.

## Further reading

- [Wikipedia: Trusted computing base](https://en.wikipedia.org/wiki/Trusted_computing_base)
