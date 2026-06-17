---
type: "term"
branch: "Security"
domain: "Application Security"
tags: ["appsec"]
status: "note"
---

# STRIDE

> **Domain:** [[08 - Application Security|Application Security]]

Microsoft threat-modeling mnemonic: **S**poofing, **T**ampering, **R**epudiation, **I**nformation disclosure, **D**enial of service, **E**levation of privilege.

**Context.** The most approachable way to start threat modeling: walk a data-flow diagram and ask each STRIDE question at each element and boundary. It maps cleanly to defenses — Spoofing→authentication, Tampering→integrity, Repudiation→logging, and so on — which makes it a teaching tool as much as an analysis one. Good for breadth; pair with attack trees for depth on a specific concern.

## See also

- [[Threat Modeling]]
