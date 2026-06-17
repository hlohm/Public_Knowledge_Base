---
type: "term"
branch: "Security"
domain: "Application Security"
aliases: ["Secure SDLC", "\"SSDLC\""]
tags: ["appsec"]
status: "note"
---

# SDLC

> **Domain:** [[08 - Application Security|Application Security]]
> **Also known as:** Secure SDLC, "SSDLC"

**S**oftware **D**evelopment **L**ife **C**ycle. The phases of building software. **Secure SDLC** weaves security into each phase.

**Context.** The point of "secure SDLC" is that security bolted on at the end is the most expensive place to find a flaw — design review catches what no scanner will, and a bug fixed in code review costs a fraction of one fixed in production. In practice it's threat modeling at design, SAST/SCA in CI, DAST in staging, and a pentest before big releases — woven in, not gated at the end.

## See also

- [[Shift Left]]
- [[Threat Modeling]]
